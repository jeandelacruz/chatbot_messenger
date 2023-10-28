from django.conf import settings
from requests import post


class ApiGraph:
    def __init__(self):
        self.meta_token = settings.META_TOKEN
        self.url = 'https://graph.facebook.com'
        self.headers = {
            'Content-Type': 'application/json'
        }

    def setup(self):
        response = post(
            f'{self.url}/v18.0/me/messenger_profile',
            params={
                'access_token': self.meta_token
            },
            headers=self.headers,
            json={
                'get_started': {
                    'payload': 'GET_STARTED_PAYLOAD'
                }
            }
        )
        return response.json()

    def send_message(self, recipient_id, message):
        # https://developers.facebook.com/docs/messenger-platform/reference/send-api/
        # https://developers.facebook.com/docs/messenger-platform/send-messages/
        response = post(
            f'{self.url}/v18.0/me/messages',
            params={
                'access_token': self.meta_token
            },
            headers=self.headers,
            json={
                'recipient': {
                    'id': recipient_id
                },
                'messaging_type': 'RESPONSE',
                'message': {
                    'text': message
                }
            }
        )
        print(response.json())