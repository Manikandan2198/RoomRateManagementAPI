from django.contrib import admin

from apps.api.models import Discount, DiscountRoomRate, OverriddenRoomRate, RoomRate

# Register your models here.
admin.site.register(RoomRate)
admin.site.register(Discount)
admin.site.register(OverriddenRoomRate)
admin.site.register(DiscountRoomRate)
