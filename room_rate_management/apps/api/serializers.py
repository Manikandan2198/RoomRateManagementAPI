from rest_framework import serializers

from apps.api.models import Discount, DiscountRoomRate, OverriddenRoomRate, RoomRate


class RoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRate
        fields = "__all__"
    
class OverriddenRoomRateSerializer(serializers.ModelSerializer):
    room_rate = RoomRateSerializer()
    class Meta:
        model = OverriddenRoomRate
        fields = "__all__"

class OverriddenRoomRateUpdateSerializer(serializers.ModelSerializer):
    room_rate = serializers.PrimaryKeyRelatedField(queryset=RoomRate.objects.all())
    class Meta:
        model = OverriddenRoomRate
        fields = "__all__"

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"

class DiscountRoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountRoomRate
        fields = "__all__"

class LowestRoomRateListSerializer(serializers.Serializer):
    date = serializers.DateField()
    lowest_rate = serializers.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        fields = ['date', 'lowest_rate']


