from rest_framework import serializers
from masterData.models import OrderRecieveDetail, DispatchOrder, DispatchOrderDetail
from authentication.models import ItemRecieveDetails, ItemTagging

class ItemRecieveDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRecieveDetails
        fields = "__all__"

class OrderRecieveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRecieveDetail
        fields = "__all__"

class DispatchOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchOrder
        fields = "__all__"

class DispatchOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchOrderDetail
        fields = "__all__"

class ItemTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTagging
        fields = "__all__"

class VerificationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        style={'placeholder': 'User Name', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'Password', 'placeholder': 'Password'}
    )