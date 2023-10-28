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
                },
                'greeting': [
                    {
                        'locale': 'default',
                        'text': 'Hola {{user_full_name}}'
                    }
                ]
            }
        )
        return response.json()

    def send_message(self, recipient_id, body):
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
                'message': body
            }
        )
        print(response.json())

    def quick_reply_message(self, recipient_id, message, options):
        return self.send_message(
            recipient_id,
            {
                'text': message,
                "quick_replies": options
            }
        )

    def welcome_message(self, recipient_id):
        return self.quick_reply_message(
            recipient_id,
            'Hola, ¿Qué deseas hacer?',
            [
                {
                    'content_type': 'text',
                    'title': 'Buscar Musica',
                    'payload': 'SEARCH_MUSIC',
                    'image_url': 'https://cdn-icons-png.flaticon.com/512/3313/3313676.png'
                },
                {
                    'content_type': 'text',
                    'title': 'Conversar',
                    'payload': 'TALK_MESSAGE',
                    'image_url': 'https://cdn.icon-icons.com/icons2/2645/PNG/512/chat_text_icon_160277.png'
                }
            ]
        )
