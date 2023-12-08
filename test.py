import json
import requests
from config import SPORTSDATA_APIKEY

api_key = SPORTSDATA_APIKEY

sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': api_key
})

sports_json = json.loads(sports_response.text)

if not sports_json['success']:
    print(
        'There was a problem with the sports request:',
        sports_json['msg']
    )

else:
    print()
    print(
        'Successfully got {} sports'.format(len(sports_json['data'])),
        'Here\'s the first sport:'
    )
    print(sports_json['data'][0])


sport_key = 'basketball_ncaab'

odds_response = requests.get('https://api.the-odds-api.com/v4/sports/{sport}/odds-history/?apiKey={apiKey}&regions={regions}&markets={markets}&date={date}', params={
    'api_key': api_key,
    'sport': sport_key,
    'region': 'us', # uk | us | eu | au
    'mkt': 'spreads' # h2h | spreads | totals
})
odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print(
        'There was a problem with the odds request:',
        odds_json['msg']
    )

else:
    # odds_json['data'] contains a list of live and 
    #   upcoming events and odds for different bookmakers.
    # Events are ordered by start time (live events are first)
    print()
    print(
        'Successfully got {} events'.format(len(odds_json['data'])),
        'Here\'s the first event:'
    )
    print(odds_json['data'][0])