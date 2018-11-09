from django.urls import path

from answer_api.views import MessageList, MessageDetail

app_name = 'answer_api'
urlpatterns = [
    path('messages/', MessageList.as_view(), name='message_list'),
    path('messages/<int:pk>', MessageDetail.as_view(), name='message_detail'),
]
