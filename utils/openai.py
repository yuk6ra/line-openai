import os
import openai
import dotenv

dotenv.load_dotenv()

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPEN_AI_KEY")

class OpenAI():

    def get_openai_response(self, content):
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": content}]
        )

        openai_content = response['choices'][0]["message"]["content"]

        return openai_content
