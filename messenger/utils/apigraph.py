from django.conf import settings
from requests import post
from random import choice
from .spotify import SpotifyClient


class ApiGraph:
    def __init__(self):
        self.meta_token = settings.META_TOKEN
        self.url = 'https://graph.facebook.com'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.spotify = SpotifyClient()

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

    def __options(self):
        return [
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

    def welcome_message(self, recipient_id):
        return self.quick_reply_message(
            recipient_id,
            'Hola, ¿Qué deseas hacer?',
            self.__options()
        )

    def retry_options(self, recipient_id):
        return self.quick_reply_message(
            recipient_id,
            'Ahora, que deseas hacer?',
            self.__options()
        )

    def talk_chat_message(self, recipient_id):
        messages = [
            'Estas bien ?',
            'Ella no te ama',
            'Funciona'
        ]
        return self.send_message(
            recipient_id,
            {
                'text': choice(messages)
            }
        )

    def search_music_message(self, recipient_id):
        return self.send_message(
            recipient_id,
            {
                'text': 'Escriba el nombre de la canción o del artista a buscar:'
            }
        )

    def spotify_search_track(self, recipient_id, track):
        results = self.spotify.search_by_track(track)
        tracks = results['tracks']['items']
        elements = [
            self.__template_track(track)
            for track in tracks
        ]
        return self.send_message(
            recipient_id,
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': elements
                    }
                }
            }
        )

    def __template_track(self, track):
        name = track['name']
        artist = track['artists'][0]['name']
        album_image = track['album']['images'][0]['url']
        album = track['album']['name']
        url = track['external_urls']['spotify']

        return {
            "title": f'{artist} - {name}',
            "image_url": album_image,
            "subtitle": album,
            "default_action": {
                "type": "web_url",
                "url": url,
                "webview_height_ratio": "tall"
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": url,
                    "title": "Play Spotify"
                }
            ]
        }
