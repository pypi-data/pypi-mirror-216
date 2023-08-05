# Agent
import requests
import json

class Agent:
    def __init__(self, api_key, agent_id):
        self.api_key = api_key
        self.agent_id = agent_id

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_agent_id(self, agent_id):
        self.agent_id = agent_id

    def completion(self, prompt, stream=False):
        # Headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        # Endpoint
        url = 'https://playground.judini.ai/api/v1/agent/'+ self.agent_id
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.post(url, json=data, headers=headers)
        tokens = ''
        report = []
        if(stream == False):
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    raw_data = chunk.decode('utf-8').replace("data: ", '')
                    if "[DONE]" in raw_data or raw_data != "":
                        try:
                            json_object = json.loads(raw_data.strip())
                            result = json_object['data']
                            result = result.replace("\n", "")        
                            tokens += result
                        except json.JSONDecodeError as e:
                            print('error', e)
            return tokens
        else:
            return response