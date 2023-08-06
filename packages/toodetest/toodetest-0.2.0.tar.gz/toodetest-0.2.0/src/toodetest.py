import requests

class Toodetest:
    def __init__(self, project_1_url):
        self.project_1_url = project_1_url

    def track(self, message, url, ip_address=None):
        data = {
            'message': message,
            'url': url,
            'ip_address': ip_address
        }

        try:
            response = requests.post(f"{self.project_1_url}/chatdata", json=data)
            if response.ok:
                print("Data sent successfully to Project 1")
            else:
                print("Failed to send data to Project 1")
        except requests.exceptions.RequestException as e:
            print("Error while sending data:", e)
