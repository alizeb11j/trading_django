from django.shortcuts import render
from django.http import JsonResponse
from trade.templates.trade.test1 import (
    get_data_altcoin,
    get_from_kraken_rest,
    get_from_oanda,
)


def test_ftn(request):
    # kraken = Kraken(BTC=12.34, Price=45.67)
    # kraken.save()
    # data = Kraken.objects.all()
    altcoin_data, alt_qty = get_data_altcoin()
    kraken_data, kraken_qty = get_from_kraken_rest()
    fx_data = get_from_oanda()
    kraken_price_inc_withdraw = kraken_data * (1.00015)
    interest = (
        (altcoin_data / fx_data) - (kraken_price_inc_withdraw)
    ) / kraken_price_inc_withdraw
    data = [
        {
            "site": "kraken",
            "data": kraken_price_inc_withdraw,
        },
        {
            "data": kraken_qty,
        },
        {"site": "altcoin", "data": altcoin_data},
        {"data": alt_qty},
        {"site": "oanda", "data": fx_data},
        {"data": round(interest, 4)},
    ]

    return render(request, "trade/home.html", {"data": data})


# Rand_price = [{"price": str(get_data_altcoin())}]


def get_data(request):
    altcoin_data, alt_qty = get_data_altcoin()
    kraken_data, kraken_qty = get_from_kraken_rest()
    fx_data = get_from_oanda()
    kraken_price_inc_withdraw = kraken_data * (1.00015)
    interest = (
        (altcoin_data / fx_data) - (kraken_price_inc_withdraw)
    ) / kraken_price_inc_withdraw

    data = [
        {
            "site": "kraken",
            "data": kraken_price_inc_withdraw,
        },
        {
            "data": kraken_qty,
        },
        {"site": "altcoin", "data": altcoin_data},
        {"data": alt_qty},
        {"site": "oanda", "data": fx_data},
        {"data": round(interest, 4)},
    ]
    return JsonResponse(data, safe=False)
