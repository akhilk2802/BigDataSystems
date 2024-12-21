from components.data_read import insert_model_response
from components.data_s3 import RETRIEVAL_EXT, CI_EXT, IMG_EXT, MP3_EXT, ERR_EXT


def ask_gpt(
    openai_client,
    system_content: str,
    question_selected: str,
    format_type: int,
    model: str,
    loaded_file: dict = None,
    annotated_steps: str = None,
):
    """
    Sends a prompt to the GPT model using the specified parameters and returns the model's response.

    Args:
        openai_client (OpenAIClient): The client instance used to interact with the OpenAI API.
        system_content (str): The system message that sets the context for the model.
        question_selected (str): The question that requires a response from the model.
        format_type (int): The format type used to determine how the content is structured.
        model (str): The model to be used for generating the response (e.g., "gpt-4").
        loaded_file (dict, optional): The file details dictionary containing 'path', 'extension', and optionally 'url'.
        annotated_steps (str, optional): Annotator steps included when `format_type` is 3.

    Returns:
        str: The response generated by the model or an error message if the file extension is not supported.
    """

    # Format the content based on format type
    validation_content = format_validation_content(openai_client, format_type, question_selected, annotated_steps, loaded_file)

    if loaded_file:
        # Handle file-specific validation
        ai_response = handle_file_based_prompt(
            openai_client, loaded_file, system_content, validation_content, model
        )
    else:
        # Simple validation if no file is attached
        ai_response = openai_client.validation_prompt(system_content, validation_content, model)

    return ai_response


def format_validation_content(openai_client, format_type, question, annotated_steps=None, loaded_file=None):
    """
    Formats validation content based on the format type and additional data.

    Args:
        openai_client (OpenAIClient): The client instance used to format the content.
        format_type (int): Determines the content format.
        question (str): The main question text.
        annotated_steps (str, optional): Annotator steps if required.
        loaded_file (dict, optional): File data if available.

    Returns:
        str: Formatted content for validation.
    """
    if format_type == 0:
        return openai_client.format_content(format_type, question)
    elif format_type == 3:
        return openai_client.format_content(format_type, question, None, annotated_steps)
    elif loaded_file and "path" in loaded_file:
        transcription = openai_client.stt_validation_prompt(loaded_file["path"])
        return openai_client.format_content(format_type, question, transcription, annotated_steps)


def handle_file_based_prompt(openai_client, loaded_file, system_content, validation_content, model):
    """
    Handles file-based prompts and returns the model's response.

    Args:
        openai_client (OpenAIClient): The client instance.
        loaded_file (dict): File details (path, extension, etc.).
        system_content (str): The system instructions for the model.
        validation_content (str): The validation question/content.
        model (str): The model to use for the prompt.

    Returns:
        str: The model's response or an error message.
    """
    file_extension = loaded_file.get("extension")

    if file_extension in RETRIEVAL_EXT:
        return openai_client.file_validation_prompt(
            loaded_file["path"], system_content, validation_content, model
        )
    elif file_extension in CI_EXT:
        return openai_client.ci_file_validation_prompt(
            loaded_file["path"], system_content, validation_content, model
        )
    elif file_extension in IMG_EXT:
        return openai_client.validation_prompt(
            system_content, validation_content, model, loaded_file.get("url")
        )
    elif file_extension in ERR_EXT:
        return "The LLM model currently does not support these file extensions."
    else:
        transcription = openai_client.stt_validation_prompt(loaded_file["path"])
        return openai_client.validation_prompt(system_content, validation_content, model)


def answer_validation_check(final_answer: str, validation_answer: str) -> bool:
    """
    Validates if the final answer matches the validation answer.

    Args:
        final_answer (str): The user-provided answer.
        validation_answer (str): The reference answer.

    Returns:
        bool: True if validation fails, False if successful.
    """
    final_answer = final_answer.strip().lower()
    validation_answer = validation_answer.strip().lower().replace('`', '')

    if final_answer.isdigit():
        return final_answer not in validation_answer.split()
    return final_answer not in validation_answer