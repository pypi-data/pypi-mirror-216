import requests

class Toodetest:
    def __init__(self, project_1_url):
        self.project_1_url = project_1_url

    def track_user_message(self, message):
        self._send_chat_data(message, sender='user')

    def track_ai_response(self, message):
        self._send_chat_data(message, sender='ai')

    def _send_chat_data(self, message, sender):
        data = {
            'message': message,
            'sender': sender
        }

        try:
            response = requests.post(f"{self.project_1_url}/chatdata", json=data)
            if response.ok:
                print("Data sent successfully to Project 1")
            else:
                print("Failed to send data to Project 1")
        except requests.exceptions.RequestException as e:
            print("Error while sending data:", e)

print("toodetest imported correctly")
