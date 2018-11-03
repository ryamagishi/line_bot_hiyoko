import json
import logging
import os
import uuid

import dialogflow
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson
from linebot.models import MessageEvent

from dialogflow_api.models import Message

UNKNOWN_ACTION = 'input.unknown'

logger = logging.getLogger(__name__)


def _get_dialogflow_session():
    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session_id = uuid.uuid4().hex
    project_id = service_account_info.get('project_id')
    session = session_client.session_path(project_id, session_id)

    return session, session_client


def retrieve_answer(event: MessageEvent):
    session, session_client = _get_dialogflow_session()

    text_input = dialogflow.types.TextInput(text=event.message.text, language_code='ja')
    query_input = dialogflow.types.QueryInput(text=text_input)

    dialogflow_response = session_client.detect_intent(session=session, query_input=query_input)

    result = json.loads(MessageToJson(dialogflow_response.query_result))

    message = Message(line_id=event.source.user_id,
                      question=result.get('queryText'),
                      actual_reply=result.get('fulfillmentText'))

    if result.get('action') == UNKNOWN_ACTION:
        message.is_unknown_now = True

    message.save()
    return message.actual_reply
