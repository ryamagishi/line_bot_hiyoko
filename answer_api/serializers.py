from rest_framework import serializers

from answer_api.models import Message
from dialogflow_api.services import retrieve_answer


class MessageSerializer(serializers.ModelSerializer):
    now_reply = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'line_id', 'question', 'actual_reply', 'now_reply', 'is_unknown', 'created')

    def get_now_reply(self, instance):
        return retrieve_answer(instance.question).get('fulfillmentText')
