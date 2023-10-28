from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from .utils.apigraph import ApiGraph


apigraph = ApiGraph()


class setupView(generics.GenericAPIView):
    serializer_class = None
    http_method_names = ['get']

    # https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/
    def get(self, _):
        response = apigraph.setup()
        return Response(data=response, status=status.HTTP_200_OK)


class WebhookView(generics.GenericAPIView):
    serializer_class = None
    http_method_names = ['get', 'post']

    # https://developers.facebook.com/docs/messenger-platform/webhooks
    def get(self, request):
        query_params = request.GET
        hub_mode = query_params.get('hub.mode')
        hub_challenge = query_params.get('hub.challenge')
        hub_verify_token = query_params.get('hub.verify_token')

        if hub_mode == 'subscribe' and hub_verify_token == settings.META_VERIFY:
            return Response(data=int(hub_challenge), status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        data = request.data
        for entry in data['entry']:
            messaging = entry['messaging']
            for message in messaging:
                sender_id = message['sender']['id']
                apigraph.send_message(
                    sender_id,
                    'Respuesta de TECSUP'
                )
        return Response(status=status.HTTP_200_OK)
