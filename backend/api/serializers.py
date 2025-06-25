from rest_framework import serializers
from subscriptions.models import SubscriptionBox
from subscriptions.models import ScheduledItem

class SubscriptionBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubscriptionBox
        fields="__all__"

class ScheduledItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=ScheduledItem
        fields="__all__"