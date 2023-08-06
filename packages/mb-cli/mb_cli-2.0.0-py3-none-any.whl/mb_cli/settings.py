VERSION = '2.0.0'

# change domains as you like, singed mirrors @ /mirrors.txt (always verify with their pgp @ /pgp.txt)
TOR_ADDRESS = 'https://majestictfvnfjgo5hqvmuzynak4kjl5tjs3j5zdabawe6n2aaebldad.onion/api/v1'
CLEAR_DOMAIN = 'https://majesticbank.sc/api/v1'

TOR_PROXY = 'socks5://127.0.0.1:9050'

COIN_LIST = ['XMR', 'BTC', 'FIRO', 'LTC', 'BCH', 'WOW']

REGEX_LIST = {
    "XMR": "^[48][a-zA-Z|\\d]{94}([a-zA-Z|\\d]{11})?$",
    "BTC": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",
    "FIRO": "^[a|Z|3|4][0-9A-za-z]{33}$",
    "LTC": "^(L|M|3)[A-Za-z0-9]{33}$|^(ltc1)[0-9A-Za-z]{39}$",
    "BCH": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[0-9A-Za-z]{42,42}$",
    "WOW": "^W[oW][1-9A-HJ-NP-Za-km-z]{95}"
}

# my majestic bank referral code, leave it as it is if you want to support me :D
MB_REFERRAL = 'kvqi8Q'
