from datetime import date, datetime, timedelta
from django.db.models import Min
from apps.api.models import DiscountRoomRate, OverriddenRoomRate, RoomRate


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

"""
    Calculates lowest room rate for a given room for the date range

Parameters:
    room_rate (RoomRate): The RoomRate object.
    start_date (datetime): The start date.
    end_date (datetime): The end date.

Yields:
    datetime: The next date in the range.
"""
def get_lowest_room_rates(room_rate:RoomRate,start_date:datetime,end_date:datetime):

    #filter all the overriden room rates and discounts for the given room in the date range
    overridden_room_rates = OverriddenRoomRate.objects.filter(room_rate=room_rate).filter(stay_date__range=(start_date,end_date))
    discounts = DiscountRoomRate.objects.filter(room_rate=room_rate)
    lowest_room_rates = []

    #iterate through every day in the date range and calculate the lowest room rate in that day
    for date in daterange(start_date,end_date):

        #Filter the overridden room rate for that day. If any overriddens then use the overridden rate else use the default rate.
        overridden_room_rate_for_date = overridden_room_rates.filter(stay_date=date)
        if len(overridden_room_rate_for_date) == 0:
            lowest_rate = room_rate.default_rate
        else:
            #if multiple overriddens are there for a ram for the same day, take the lowest one
            lowest_rate = overridden_room_rate_for_date.order_by('overridden_rate').first().overridden_rate
        
        # apply the all the applicable discounts on the lowest rate and get the maximum discount value
        max_discount = 0
        for discount_query in discounts:
            final_discount_value = 0
            if discount_query.discount.discount_type == 'fixed':
                final_discount_value = discount_query.discount.discount_value
            else:
                final_discount_value = (lowest_rate * discount_query.discount.discount_value)/100
            max_discount = max(max_discount,final_discount_value)

        #subtract the maximum discount value form lowest rate to arrive at the lowest rate for the day
        lowest_rate = max((lowest_rate - max_discount),0)
        lowest_room_rates.append({"date":date.date(),"lowest_rate":lowest_rate})
    return lowest_room_rates
