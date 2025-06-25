# from django.shortcuts import render
# from rest_framework import viewsets
# from subscriptions.models import SubscriptionBox
# from .serializers import SubscriptionBoxerializer
# from subscriptions.models import ScheduledItem
# from .serializers import ScheduledItemSerializer

# # Create your views here.

# class SubscriptionBoxViewSet(viewsets.ModelViewSet):
#     queryset=SubscriptionBox.objects.all()
#     serializer_class=SubscriptionBoxerializer

# class ScheduledItemViewSet(viewsets.ModelViewSet):
#     queryset=ScheduledItem.objects.all()
#     serializer_class=ScheduledItemSerializer
from django.shortcuts import render
from rest_framework import viewsets
from subscriptions.models import SubscriptionBox, ScheduledItem
from .serializers import SubscriptionBoxSerializer, ScheduledItemSerializer

# Create your views here.

class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer

class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer