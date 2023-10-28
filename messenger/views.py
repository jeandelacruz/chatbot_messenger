from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from .utils.apigraph import ApiGraph


apigraph = ApiGraph()


class SetupView(generics.GenericAPIView):
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
                postback = message.get('postback')
                msg = message.get('message')
                if postback:
                    self.post_back_event(sender_id, postback)
                else:
                    self.message_event(sender_id, msg)
        return Response(status=status.HTTP_200_OK)

    def post_back_event(self, sender_id, postback):
        payload = postback.get('payload')

        if payload == 'GET_STARTED_PAYLOAD':
            return apigraph.welcome_message(sender_id)

    def message_event(self, sender_id, message):
        quick_reply = message.get('quick_reply')

        if quick_reply:
            return self.quick_reply_event(sender_id, message)

        return apigraph.send_message(
            sender_id,
            {
                'text': message.get('text')
            }
        )

    def quick_reply_event(self, sender_id, message):
        quick_reply = message.get('quick_reply')
        payload = quick_reply.get('payload')

        if payload == 'RED_COLOR':
            return apigraph.send_message(
                sender_id,
                {
                    'text': 'Escogiste el color rojo'
                }
            )

        if payload == 'GREEN_COLOR':
            return apigraph.send_message(
                sender_id,
                {
                    'text': 'Escogiste el color verde'
                }
            )
