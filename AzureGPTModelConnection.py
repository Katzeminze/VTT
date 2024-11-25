import os
import requests
import base64
import time

class ChatBot:
    def init(self, max_tokens=800):
        self.session = requests.Session()
        # Configuration
        self.API_KEY = r"YOUR_API"
        # self.IMAGE_PATH = "YOUR_IMAGE_PATH"
        # self.encoded_image = base64.b64encode(open(self.IMAGE_PATH, 'rb').read()).decode('ascii')
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
            }
        self.max_tokens = max_tokens
    
    def send_request_and_get_response(self, message):
        # Payload for the request
        payload = {
            "messages": [
                {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": message
                    }
                ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": self.max_tokens 
        }

        ENDPOINT = "https://2024090111eny.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

        # Send request
        try:
            response = self.session.post(ENDPOINT, headers=self.headers, json=payload)
            response.raise_for_status() # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            if response.status_code == 429:
                print(f'Failed to make the request. Error: {e}. Retry after {int(response.headers["Retry-After"])}')
                # time.sleep(int(response.headers["Retry-After"]))
                return int(response.headers["Retry-After"])
            # temp
            self.close_session()  
            raise SystemExit(f"Failed to make the request. Error: {e}")
            # return None
        return response
    
    def close_session(self):
        self.session.close()

# chat = ChatBot()
# response = chat.send_request_and_get_rwsponse("How to say I was born in Kazakhstan in Kazakh language?")
# # Handle the response as needed (e.g., print or process)
# print(response.json())
