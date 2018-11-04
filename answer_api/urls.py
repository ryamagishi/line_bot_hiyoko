from django.urls import path

from answer_api.views import MessageList

app_name = 'answer_api'
urlpatterns = [
    path('messages/', MessageList.as_view(), name='messages'),
]
