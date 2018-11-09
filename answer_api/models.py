from django.db import models

import dialogflow_api


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    line_id = models.CharField(max_length=100, blank=True, default='')
    question = models.TextField()
    actual_reply = models.TextField()
    is_unknown = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
