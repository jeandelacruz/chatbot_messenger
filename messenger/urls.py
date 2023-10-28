from django.urls import path
from .views import WebhookView, setupView

urlpatterns = [
    path('setup/', setupView.as_view(), name='setup'),
    path('webhook/', WebhookView.as_view(), name='webhook')
]