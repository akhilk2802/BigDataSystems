import openai
import openai.error
from project_logging import logging_module


class OpenAIClient:
    def __init__(self, api_key: str):
        """
        Initializes the OpenAIClient with all system prompts and the provided API key.
        """
        openai.api_key = api_key

        # System content strings
        self.system_prompts = {
            "val": """Every prompt will begin with the text "Question:" followed by the question 
                      enclosed in triple backticks. The text "Output Format:" explains how the Question 
                      must be answered. You are an AI that reads the Question enclosed in triple backticks 
                      and provides the answer in the mentioned Output Format.""",
            "ann": """Every prompt will begin with the text "Question:" followed by the question 
                      enclosed in triple backticks. The "Annotator Steps:" mentions the steps that you should take 
                      for answering the question. The text "Output Format:" explains how the Question 
                      output must be formatted. You are an AI that reads the Question enclosed in triple backticks 
                      and follows the Annotator Steps and provides the answer in the mentioned Output Format.""",
            "audio": """Every prompt will begin with the text "Question:" followed by the question 
                        enclosed in triple backticks. The question will mention that there is an .mp3 file attached; 
                        however, the .mp3 file has already been transcribed and the transcribed text is attached 
                        after the text: "Transcription:". The text "Output Format:" explains how the Question must be answered. 
                        You are an AI that reads the Question enclosed in triple backticks and the Transcript 
                        and provides the answer in the mentioned Output Format.""",
        }

        self.output_format = "Provide a clear and conclusive answer to the Question being asked. Do not provide any reasoning or references for your answer."
        self.assistant_instruction = "You are an assistant that answers any questions relevant to the file that is uploaded in the thread."

    def _log_and_return_error(self, error, custom_message=""):
        """
        Logs the error and returns a formatted error message.
        """
        logging_module.log_error(f"{custom_message} {error}")
        return f"Error: {error}"

    def format_content(self, format_type: int, question: str, transcription: str = None, annotator_steps: str = None) -> str:
        """
        Formats the content based on the format type.
        """
        if format_type == 0:
            return f"Question: ```{question}```\nOutput Format: {self.output_format}\n"
        elif format_type == 1:
            return f"Question: ```{question}```\nTranscription: {transcription}\nOutput Format: {self.output_format}\n"
        elif format_type == 2:
            return f"Question: ```{question}```\nTranscription: {transcription}\nAnnotator Steps: {annotator_steps}\nOutput Format: {self.output_format}\n"
        else:
            return f"Question: ```{question}```\nAnnotator Steps: {annotator_steps}\nOutput Format: {self.output_format}\n"

    def _make_openai_request(self, system_content, user_content, model, imageurl=None):
        """
        Sends a request to the OpenAI API and returns the response.
        """
        try:
            logging_module.log_success(f"System Content: {system_content}")
            logging_module.log_success(f"User Content: {user_content}")

            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ]

            if imageurl:
                messages[1]["content"] = [
                    {"type": "text", "text": user_content},
                    {"type": "image_url", "image_url": {"url": imageurl, "detail": "low"}},
                ]

            response = openai.ChatCompletion.create(model=model.lower(), messages=messages)
            logging_module.log_success(f"Response: {response.choices[0].message.content}")
            return response.choices[0].message.content
        except openai.error.OpenAIError as e:
            return self._log_and_return_error(e, "OpenAI API Error:")
        except Exception as e:
            return self._log_and_return_error(e, "Unexpected Error:")

    def validation_prompt(self, system_content: str, user_content: str, model: str, imageurl: str = None) -> str:
        """
        Wrapper for sending a validation prompt.
        """
        return self._make_openai_request(system_content, user_content, model, imageurl)

    def _upload_and_process_file(self, file_path, assistant_id, system_content, validation_content):
        """
        Uploads the file to OpenAI and processes the thread.
        """
        try:
            logging_module.log_success(f"Uploading file: {file_path}")
            query_file = openai.File.create(file=open(file_path, "rb"), purpose="assistants")

            logging_module.log_success(f"File uploaded with ID: {query_file.id}")
            thread = openai.Thread.create()

            openai.ThreadMessage.create(
                thread.id,
                role="user",
                content=validation_content,
                attachments=[{"file_id": query_file.id, "tools": [{"type": "file_search"}]}],
            )

            logging_module.log_success(f"Message created in thread: {thread.id}")
            run = openai.ThreadRun.create_and_poll(thread_id=thread.id, assistant_id=assistant_id)

            if run.status == "completed":
                messages = openai.ThreadMessage.list(thread_id=thread.id)
                response_content = messages.data[0].content[0].text.value
                logging_module.log_success(f"Response: {response_content}")
                return response_content
            else:
                logging_module.log_error(f"Thread run failed with status: {run.status}")
                return f"Thread run status: {run.status}"
        except openai.error.OpenAIError as e:
            return self._log_and_return_error(e, "Error during file upload and processing:")
        except Exception as e:
            return self._log_and_return_error(e, "Unexpected Error during file processing:")

    def file_validation_prompt(self, file_path: str, system_content: str, validation_content: str, model: str) -> str:
        """
        Sends a validation prompt with a file to the OpenAI API.
        """
        try:
            assistant = openai.Assistant.create(
                instructions=self.assistant_instruction + system_content,
                model=model.lower(),
                tools=[{"type": "file_search"}],
            )
            logging_module.log_success(f"Assistant created with ID: {assistant.id}")

            response = self._upload_and_process_file(file_path, assistant.id, system_content, validation_content)
            self._cleanup_resources(assistant.id, None, None)  # Cleanup assistant only
            return response
        except Exception as e:
            return self._log_and_return_error(e, "Error in file validation:")

    def _cleanup_resources(self, assistant_id: str, file_id: str = None, thread_id: str = None) -> None:
        """
        Cleans up the resources after validation.
        """
        try:
            if assistant_id:
                openai.Assistant.delete(assistant_id)
                logging_module.log_success(f"Assistant {assistant_id} deleted.")

            if file_id:
                openai.File.delete(file_id)
                logging_module.log_success(f"File {file_id} deleted.")

            if thread_id:
                openai.Thread.delete(thread_id)
                logging_module.log_success(f"Thread {thread_id} deleted.")
        except Exception as e:
            logging_module.log_error(f"Cleanup Error: {e}")