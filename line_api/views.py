import logging
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))
logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def main(request):
    body = request.body.decode('utf-8')
    signature = request.META['HTTP_X_LINE_SIGNATURE']

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error(InvalidSignatureError.message)
        Response(status=status.HTTP_400_BAD_REQUEST)

    return Response({'data': 'ok'}, status=status.HTTP_201_CREATED)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
