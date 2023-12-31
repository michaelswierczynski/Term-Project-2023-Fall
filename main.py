season_dates = {
    '2020-2021': {'start': '11/04/2020', 'end': '04/04/2021'},
    '2021-2022': {'start': '11/04/2021', 'end': '04/04/2022'},
    '2022-2023': {'start': '11/04/2022', 'end': '04/04/2023'},
    '2023-2024': {'start': '11/01/2023', 'end': '12/04/2023'},
}

import json
from datetime import datetime

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def filter_data_by_season(data, start_date, end_date):
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y')

    seasonal_data = []
    for date_dict in data:
        for date_str, date_data in date_dict.items():
            if start_datetime <= datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') <= end_datetime:
                if 'data' in date_data:
                    seasonal_data.extend(date_data['data'])
                elif 'next_timestamp' in date_data and isinstance(date_data['next_timestamp'], dict) and 'data' in date_data['next_timestamp']:
                    seasonal_data.extend(date_data['next_timestamp']['data'])
    return seasonal_data

def compare_bookmakers(data):
    bookmakers_data = {}

    for game in data:
        game_id = game['id']
        bookmakers_data[game_id] = {'bookmakers': {}, 'spreads_favored': {}, 'spreads_underdog': {}, 'adjusted_spreads_favored': {}, 'adjusted_spreads_underdog': {}}

        for bookmaker in game['bookmakers']:
            outcomes = bookmaker['markets'][0]['outcomes']

            if len(outcomes) == 2:
                favored_team_outcome = next((outcome for outcome in outcomes if outcome['point'] < 0), None)
                underdog_team_outcome = next((outcome for outcome in outcomes if outcome['point'] > 0), None)

                if favored_team_outcome and underdog_team_outcome:
                    favored_spread = favored_team_outcome['point']
                    underdog_spread = underdog_team_outcome['point']

                    bookmaker_key = bookmaker['key']
                    bookmakers_data[game_id]['bookmakers'][bookmaker_key] = bookmaker['title']
                    bookmakers_data[game_id]['spreads_favored'][bookmaker_key] = favored_spread
                    bookmakers_data[game_id]['spreads_underdog'][bookmaker_key] = underdog_spread

                    favored_odds = favored_team_outcome['price']
                    underdog_odds = underdog_team_outcome['price']

                    implied_probability_favored = 1 / (favored_odds / 100 + 1)
                    implied_probability_underdog = 1 / (underdog_odds / 100 + 1)

                    adjusted_spread_favored = favored_spread / implied_probability_favored
                    adjusted_spread_underdog = underdog_spread / implied_probability_underdog

                    bookmakers_data[game_id]['adjusted_spreads_favored'][bookmaker_key] = adjusted_spread_favored
                    bookmakers_data[game_id]['adjusted_spreads_underdog'][bookmaker_key] = adjusted_spread_underdog

    return bookmakers_data

def main(season):
    json_file_path = 'odds_data.json'
    loaded_data = load_json_file(json_file_path)

    start_date_season = season_dates[season]['start']
    end_date_season = season_dates[season]['end']

    season_data = filter_data_by_season(loaded_data, start_date_season, end_date_season)

    bookmakers_data = compare_bookmakers(season_data)

    bookmaker_value_index = {}
    for game_id, game_data in bookmakers_data.items():
        for bookmaker_key, bookmaker_info in game_data['bookmakers'].items():
            adjusted_spread_favored = game_data['adjusted_spreads_favored'][bookmaker_key]
            adjusted_spread_underdog = game_data['adjusted_spreads_underdog'][bookmaker_key]

            game_score = abs(adjusted_spread_favored) + abs(adjusted_spread_underdog)

            if bookmaker_key not in bookmaker_value_index:
                bookmaker_value_index[bookmaker_key] = 0
            bookmaker_value_index[bookmaker_key] += game_score

    for bookmaker_key, total_score in sorted(bookmaker_value_index.items(), key=lambda x: x[1], reverse=True):
        print(f'{bookmaker_key}: {total_score:.2f}')


if __name__ == "__main__":
    main('2020-2021')
