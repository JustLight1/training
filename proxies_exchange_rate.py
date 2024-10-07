"""
Задача - ASGI / WSGI функция которая проксирует курс валют

Приложение должно отдавать курс валюты к доллару используя стороннее АПИ
https://api.exchangerate-api.com/v4/latest/{currency} Например, в ответ на
http://localhost:8000/USD должен возвращаться ответ вида:

{"provider":"https://www.exchangerate-api.com",
"WARNING_UPGRADE_TO_V6":"https://www.exchangerate-api.com/docs/free",
"terms":"https://www.exchangerate-api.com/terms","base":"USD",
"date":"2024-09-18","time_last_updated":1726617601,
"rates":{"USD":1,"AED":3.67,"AFN":69.45,"ALL":89.49,"AMD":387.39,
"ANG":1.79,"AOA":939.8,"ARS":962.42,"AUD":1.48,"AWG":1.79,"AZN":1.7,
"BAM":1.76,"BBD":2,"BDT":119.52,"BGN":1.76,"BHD":0.376,"BIF":2903.25,
"BMD":1,"BND":1.3,"BOB":6.92,"BRL":5.5,"BSD":1,"BTN":83.83,"BWP":13.26 ...
}}

Данные, соотвественно, для доллара должны браться из
https://api.exchangerate-api.com/v4/latest/USD
"""
import aiohttp
import json


API_URL = 'https://api.exchangerate-api.com/v4/latest/'

CURRENCIES = [
    'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN',
    'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL',
    'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY',
    'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP',
    'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS',
    'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF',
    'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD',
    'JPY', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT',
    'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD',
    'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN',
    'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK',
    'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR',
    'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD',
    'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY',
    'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND',
    'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW',
    'ZWL', 'USD'
]


async def get_currency(currency):
    try:
        url = API_URL + currency
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(e)
        return None


async def app(scope, receive, send):
    assert scope['type'] == 'http'

    path = scope['path']
    currency = path[1:]
    if str(currency).upper() in CURRENCIES:
        response = await get_currency(currency)
        if response:
            response_data = json.dumps(response).encode('utf-8')

            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', b'application/json'],
                ],
            })
            await send({
                'type': 'http.response.body',
                'body': response_data,
            })
            return
        else:
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [
                    [b'content-type', b'text/plain'],
                ],
            })
            await send({
                'type': 'http.response.body',
                'body': b'Internal Server Error',
            })
            return
    await send({
        'type': 'http.response.start',
        'status': 404,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Currency not found',
    })
