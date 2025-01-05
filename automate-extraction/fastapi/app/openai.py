import openai
# from openai import InvalidRequestError, AuthenticationError

class OpenAIClient:
    def __init__(self, api_key: str, default_model: str = "gpt-4"):
        """
        Initialize the OpenAI Client with the API key and default model.
        """
        self.api_key = api_key
        openai.api_key = self.api_key
        self.default_model = default_model
        self.supported_models = ["gpt-4", "gpt-4o", "gpt-3.5-turbo"]

        if self.default_model not in self.supported_models:
            raise ValueError(f"Default model '{self.default_model}' is not supported. Choose from: {self.supported_models}")

    def list_supported_models(self):
        """
        List all supported models.
        """
        return self.supported_models

    def set_default_model(self, model: str):
        """
        Set the default model.
        """
        if model not in self.supported_models:
            raise ValueError(f"Model '{model}' is not supported. Choose from: {self.supported_models}")
        self.default_model = model

    def send_prompt(self, question: str, context: str, model: str = None, max_tokens: int = 150):
        """
        Sends a single question and context to the OpenAI API and returns the response.

        :param question: The user's question.
        :param context: The context for the question (e.g., extracted text from a PDF).
        :param model: The model to use. Defaults to the default model.
        :param max_tokens: Maximum number of tokens for the response.
        :return: The response from OpenAI.
        """
        if not model:
            model = self.default_model

        if model not in self.supported_models:
            raise ValueError(f"Model '{model}' is not supported. Choose from: {self.supported_models}")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Question: {question}\nContext: {context}"}
        ]

        try:
            response = openai.chat.completions.create(
                model=model.lower(),
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except openai.BadRequestError as e:
            print(f"Error: {e}")
            return f"Error-BDIA: {e}"
        except openai.APIError as e:
            print(f"Error: {e}")
            return f"Error-BDIA: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return f"Error-BDIA: {e}"