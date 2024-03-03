from django.shortcuts import render
from django.http import JsonResponse
from trade.test1 import (
    get_data_altcoin,
    get_from_kraken_rest,
    get_from_xe,
)


def test_ftn(request):
    # kraken = Kraken(BTC=12.34, Price=45.67)
    # kraken.save()
    # data = Kraken.objects.all()
    altcoin_data, alt_qty = get_data_altcoin()
    # print("Altcoin_max_bid:", altcoin_data)
    kraken_data, kraken_qty = get_from_kraken_rest()
    # print("Kraken_min_bid:", kraken_data)
    fx_data = get_from_xe()
    kraken_price_inc_withdraw = kraken_data * (1.00015)
    interest = (
        (altcoin_data / fx_data) - (kraken_price_inc_withdraw)
    ) / kraken_price_inc_withdraw
    interest *= 100
    data = [
        {"name": "kraken", "data": kraken_price_inc_withdraw},
        {"name": "kraken_qty", "data": kraken_qty},
        {"name": "altcoin", "data": altcoin_data},
        {"name": "alt_qty", "data": alt_qty},
        {"name": "fx_data", "data": fx_data},
        {"name": "interest", "data": round(interest, 2)},
    ]

    return render(request, "trade/home.html", {"data": data})


# Rand_price = [{"price": str(get_data_altcoin())}]


def get_data(request):
    altcoin_data, alt_qty = get_data_altcoin()
    kraken_data, kraken_qty = get_from_kraken_rest()
    fx_data = get_from_xe()
    kraken_price_inc_withdraw = kraken_data * (1.00015)
    interest = (
        (altcoin_data / fx_data) - (kraken_price_inc_withdraw)
    ) / kraken_price_inc_withdraw
    interest *= 100
    data = [
        {"name": "kraken", "data": kraken_price_inc_withdraw},
        {"name": "kraken_qty", "data": kraken_qty},
        {"name": "altcoin", "data": altcoin_data},
        {"name": "alt_qty", "data": alt_qty},
        {"name": "fx_data", "data": fx_data},
        {"name": "interest", "data": round(interest, 2)},
    ]
    return JsonResponse(data, safe=False)
