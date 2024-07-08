"""
URL configuration for room_rate_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apps.api.views.RoomRateAPIView import RoomRateListAPI, RoomRateDetailAPI
from apps.api.views.DiscountAPIView import DiscountListAPI, DiscountDetailAPI
from apps.api.views.OverriddenRoomRateAPIView import  OverriddenRoomRateDetailAPI, OverriddenRoomRatePostAPI
from apps.api.views.DiscountRoomRateAPIView import DiscountRoomRateAPI
from apps.api.views.LowestRoomRateAPIView import LowestRoomRateAPI    

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('api/dmin/', admin.site.urls),
    path('api/RoomRates/',RoomRateListAPI.as_view(),name="room-list"),
    path('api/RoomRates/<int:room_id>',RoomRateDetailAPI.as_view(),name="room-detail"),
    path('api/Discounts/',DiscountListAPI.as_view(),name="discount-list"),
    path('api/Discounts/<int:discount_id>',DiscountDetailAPI.as_view(),name="discount-detail"),
    path('api/OverriddenRoomRates/',OverriddenRoomRatePostAPI.as_view(),name="overridden-room-rate-detail"),
    path('api/OverriddenRoomRates/<int:room_id>',OverriddenRoomRateDetailAPI.as_view(),name="overridden-room-rate-detail"),
    path('api/RoomRateDiscounts/',DiscountRoomRateAPI.as_view(),name="overridden-room-rate-detail"),
    path('api/LowestRoomRates/<int:room_id>',LowestRoomRateAPI.as_view(),name="lowest-room-rate")
]

schema_view = get_schema_view(
   openapi.Info(
      title="Room Rate Management API",
      default_version='v1',
      description="A REST API to manage room rates, discounts, overridden rates and calculate lowest room rates",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="manikandan2198@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
