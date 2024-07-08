from django.db import models

# Create your models here.
class RoomRate(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=255)
    default_rate = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return f"{self.room_id} - {self.room_name}"


class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate,on_delete=models.CASCADE)
    overridden_rate = models.DecimalField(decimal_places=2, max_digits=10)
    stay_date = models.DateField()

    class Meta:
        unique_together = ('room_rate', 'stay_date')

    def __str__(self) -> str:
        return f"{self.room_rate.room_name} - {self.stay_date}"

class Discount(models.Model):
    FIXED = 'fixed'
    PERCENTAGE = 'percentage'

    DISCOUNT_TYPE_CHOICES = [
        (FIXED, 'Fixed'),
        (PERCENTAGE, 'Percentage'),
    ]


    discount_id = models.AutoField(primary_key=True)
    discount_name = models.CharField(max_length=255)
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default=FIXED,
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.discount_id} - {self.discount_name}"

class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate,on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room_rate', 'discount')

    def __str__(self) -> str:
        return f"{self.room_rate.room_name} {self.room_rate.room_id} - {self.discount.discount_name} {self.discount.discount_id}"



    
