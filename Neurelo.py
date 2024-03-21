import requests
import requests
import uuid
from datetime import datetime
import json

class Neurelo:
	_instance = None  # Class attribute that holds the singleton instance
	
	@classmethod
	def get_instance(cls):
		if cls._instance is None:
			cls._instance = cls.__new__(cls)  # Create a new instance if it doesn't exist
            # Initialize the instance
			cls._instance.base_url = 'https://us-east-2.aws.neurelo.com'
			cls._instance.headers = {
                "X-API-KEY": "neurelo_9wKFBp874Z5xFw6ZCfvhXa78oWeFPl4TMJmGRq9OIUeLqcYrmCxmVABYk7A9CbUxWJJrb5OLWrqEKiXlLSQXf164DC2vJAmAbEO15aZAj1HEbb7p9mM9ZtGo9EQDx3yDZkbNDm9bXjpGvqxdHNmVp7t+T2K+xLmsqICaoxugukwX+aTjH3GzmT2AiYhh7L+q_sz8LfjkA15Qc6uRQrry+1JwNsXi567XBHch+LiVQmRI=",
                "Content-Type": "application/json"
            }
		return cls._instance
	
	def pop_item_from_queue(self, proc):
		me = proc.me.to_dict()['name']
		response = requests.delete(f"{self.base_url}/custom/queue_pop?dst={me}", headers=self.headers)
		if response.status_code == 200:
			return response.json()
		else:
			response.raise_for_status()

	def push_item_to_queue(self, proc, msg):
		message = {
            "element_identifier": str(uuid.uuid4()),
            "time_inserted": datetime.now().isoformat(sep='T')+'Z',
            "dst": proc.me.to_dict()['name'],
            "payload": json.dumps(msg.to_dict())
        }
		response = requests.post(f"{self.base_url}/rest/queue_item/__one", json=message, headers=self.headers)
		if response.status_code not in [200, 201]:
			print(response.json())
	
	def delete_items_in_queue(self):
		response = requests.delete(f"{self.base_url}/custom/queue_pop_all", headers=self.headers)
		return response

