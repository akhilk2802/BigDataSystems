import os
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
load_dotenv()



def extract_text_unstructured():
    local_file_input_dir = "../downloaded_pdfs"
    local_file_output_dir = "../extracted_texts/unstructured"

    log_info("Extracting text from PDFs using Unstructured")
    log_info(f"Input directory: {local_file_input_dir}")
    log_info(f"Output directory: {local_file_output_dir}")

    try:
        # Check if the input directory exists
        if not os.path.exists(local_file_input_dir):
            log_error(f"Input directory {local_file_input_dir} does not exist.")
            raise FileNotFoundError(f"Input directory {local_file_input_dir} does not exist.")
        
        # Check if output directory exists; if not, create it
        os.makedirs(local_file_output_dir, exist_ok=True)

        # Validate API configuration
        # if not UNSTRUCTURED_CONFIG.get('api_url') or not UNSTRUCTURED_CONFIG.get('api_key'):
        #     log_error("API configuration for Unstructured is incomplete.")
        #     raise ValueError("API configuration for Unstructured is incomplete. Check 'api_url' and 'api_key'.")

        log_info(f"API URL: {UNSTRUCTURED_CONFIG['api_url']}")
        log_info(f"API Key: {UNSTRUCTURED_CONFIG['api_key']}")

        try:
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
                ),
                chunker_config=ChunkerConfig(
                    chunking_strategy="basic",
                    chunk_max_characters=1000,
                    chunk_overlap=20
                ),
                # Embedding step is skipped
                uploader_config=LocalUploaderConfig(output_dir=local_file_output_dir)
            ).run()

            log_info("Text extraction completed successfully using Unstructured.")

        except Exception as extraction_error:
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