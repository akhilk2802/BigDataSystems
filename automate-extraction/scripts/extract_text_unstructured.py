import os
from multiprocessing import set_start_method, Process
from unstructured_ingest.v2.pipeline.pipeline import Pipeline
from unstructured_ingest.v2.interfaces import ProcessorConfig
from unstructured_ingest.v2.processes.partitioner import PartitionerConfig
from unstructured_ingest.v2.processes.connectors.local import (LocalIndexerConfig, LocalDownloaderConfig, LocalConnectionConfig, LocalUploaderConfig)
from unstructured_ingest.v2.processes.connectors.local import LocalUploaderConfig
from unstructured_ingest.v2.processes.chunker import ChunkerConfig
from unstructured_ingest.v2.processes.embedder import EmbedderConfig
from dotenv import load_dotenv
from utils.logging_module import log_error, log_info
from utils.config import UNSTRUCTURED_CONFIG
import traceback
load_dotenv()

set_start_method("spawn", force=True)

def extract_text_unstructured():
    local_file_input_dir = "../downloaded_pdfs"
    local_file_output_dir = "../extracted_texts/unstructured"

    log_info("Extracting text from PDFs using Unstructured")
    log_info(f"Input Directory Exists: {os.path.exists(local_file_input_dir)}")
    log_info(f"Input directory: {local_file_input_dir}")
    log_info(f"Output Directory Exists: {os.path.exists(local_file_output_dir)}")
    log_info(f"Output directory: {local_file_output_dir}")

    try:
        # Check if the input directory exists
        if not os.path.exists(local_file_input_dir):
            log_error(f"Input directory {local_file_input_dir} does not exist.")
            raise FileNotFoundError(f"Input directory {local_file_input_dir} does not exist.")
        
        # Check if output directory exists; if not, create it
        os.makedirs(local_file_output_dir, exist_ok=True)

        log_info(f"API URL: {UNSTRUCTURED_CONFIG['api_url']}")
        log_info(f"API Key: {UNSTRUCTURED_CONFIG['api_key']}")

        try:
            log_info("Starting pipeline execution...")
            Pipeline.from_configs(
                context=ProcessorConfig(),
                indexer_config=LocalIndexerConfig(input_path=local_file_input_dir),
                downloader_config=LocalDownloaderConfig(),
                source_connection_config=LocalConnectionConfig(),
                partitioner_config=PartitionerConfig(
                    partition_by_api=True,
                    api_key=UNSTRUCTURED_CONFIG['api_key'],
                    partition_endpoint=UNSTRUCTURED_CONFIG['api_url'],
                    strategy="hi_res",
                    additional_partition_args={
                        "split_pdf_page": True,
                        "split_pdf_allow_failed": True,
                        "split_pdf_concurrency_level": 15,
                        "infer_table_structure": True,
                        "extract_images_in_pdf": True,
                        "extract_image_block_types": ["Image"]
                    }
                ),
                # chunker_config=ChunkerConfig(
                #     chunking_strategy="basic",
                #     chunk_max_characters=1000,
                #     chunk_overlap=20
                # ),
                # Embedding step is skipped
                uploader_config=LocalUploaderConfig(output_dir=local_file_output_dir)
            ).run()

            log_info("Text extraction completed successfully using Unstructured.")
        except KeyError as key_error:
            log_error(f"Invalid configuration: {key_error}")
        except Exception as extraction_error:
            log_error(traceback.format_exc())
            log_error(f"Failed during pipeline execution: {extraction_error}")
            raise RuntimeError(f"Pipeline execution error: {extraction_error}")

    except FileNotFoundError as fnf_error:
        log_error(f"File not found: {fnf_error}")
        raise

    except ValueError as val_error:
        log_error(f"Invalid configuration: {val_error}")
        raise

    except Exception as e:
        log_error(f"Unexpected error during text extraction: {e}")
        raise RuntimeError(f"Unexpected error during text extraction: {e}")