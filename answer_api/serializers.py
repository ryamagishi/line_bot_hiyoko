from rest_framework import serializers

from answer_api.models import Message
from dialogflow_api.services import retrieve_answer, update_answer


class MessageSerializer(serializers.ModelSerializer):
    now_reply = serializers.SerializerMethodField()
    update_message = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = Message
        fields = ('id', 'line_id', 'question', 'actual_reply', 'now_reply', 'update_message', 'is_unknown', 'created')

    def get_now_reply(self, instance):
        return retrieve_answer(instance.question).get('fulfillmentText')

    def update(self, instance, validated_data):
        # dialogflow 更新
        update_message = validated_data.get('update_message')
        update_answer(instance.question, update_message)

        # DB 更新
        instance.is_unknown = False
        instance.save()
        return instance
