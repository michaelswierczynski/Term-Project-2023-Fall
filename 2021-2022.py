import json
import pandas as pd



def load_json_file(file_path):
    """
    Data was downloaded from Odds-api in extract file.
    Function loads file to be analyzed
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

json_file_path = 'odds_data.json'
data = load_json_file(json_file_path)

from datetime import datetime

def filter_data_by_season(data, start_date, end_date):
    """
    Function seperates the data by season with start dates and end dates.
    Season options include:
    2020-2021
    2021-2022
    2022-2023
    2023 (Current season, games up until 12/04/23)

    """
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y')

    #Consulted ChatGPT for this part
    #Was having trouble with the structure of the data dictionary and the key used for the date of games 
    #Contains timestamps, commence time (game time), updated odds times
    seasonal_data = []
    for date_dict in data:
        for date_str, date_data in date_dict.items():
            if start_datetime <= datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') <= end_datetime:
                if 'data' in date_data:
                    seasonal_data.extend(date_data['data'])
                elif 'next_timestamp' in date_data and isinstance(date_data['next_timestamp'], dict) and 'data' in date_data['next_timestamp']:
                    seasonal_data.extend(date_data['next_timestamp']['data'])

    return seasonal_data


json_file_path = 'odds_data.json'
loaded_data = load_json_file(json_file_path)

start_date_season = '11/04/2021'
end_date_season = '04/04/2022'


season_data = filter_data_by_season(loaded_data, start_date_season, end_date_season)

#TEST
# print(season_data[:2])  

def compare_bookmakers(data):
    """
    Function analyzes the spreads and their respective prices offerred by the different bookmakers within the data. 
    A dictionary is created to store each bookmakers' odds and prices for every game of the season.
    Considering most spreads will be very similar, the real value to the bettor is the prices of these spreads.
    In order to capture this, the function creates an adjusted spread, based on the implied probability given the price.
    Sportsbooks change prices based on a number of different assumptions, calculations, and demand for the given bet.
    The higher the adjusted spread, the higher the value is for the bettor.
    Main purpose is to see if one sportsbook/bookmaker consistently offers more value for bettors.
    """
    bookmakers_data = {}

    for game in data:
        game_id = game['id']
        bookmakers_data[game_id] = {'bookmakers': {}, 'spreads_favored': {}, 'spreads_underdog': {}, 'adjusted_spreads_favored': {}, 'adjusted_spreads_underdog': {}}

        for bookmaker in game['bookmakers']:
            outcomes = bookmaker['markets'][0]['outcomes']

            # Spread can be 0, even price for both teams
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


bookmakers_data = compare_bookmakers(season_data)


# TESTING
# game_count = 0  

# for game_id, game_data in bookmakers_data.items():
#     print(f"Game ID: {game_id}")
#     print("Bookmakers:")

#     for bookmaker_key, bookmaker_title in game_data['bookmakers'].items():
#         print(f"  {bookmaker_title} (Key: {bookmaker_key})")
        
#         # Print spreads
#         favored_spread = game_data['spreads_favored'][bookmaker_key]
#         underdog_spread = game_data['spreads_underdog'][bookmaker_key]
#         print(f"    Favored Spread: {favored_spread}")
#         print(f"    Underdog Spread: {underdog_spread}")

#         # Print adjusted spreads
#         adjusted_favored_spread = game_data['adjusted_spreads_favored'][bookmaker_key]
#         adjusted_underdog_spread = game_data['adjusted_spreads_underdog'][bookmaker_key]
#         print(f"    Adjusted Favored Spread: {adjusted_favored_spread}")
#         print(f"    Adjusted Underdog Spread: {adjusted_underdog_spread}")

#     print("\n" + "=" * 50 + "\n")

#     #2 games for testing
#     game_count += 1
#     if game_count >= 2:
#         break  


bookmaker_value_index = {}

for game_id, game_data in bookmakers_data.items():
    for bookmaker_key, bookmaker_info in game_data['bookmakers'].items():
        adjusted_spread_favored = game_data['adjusted_spreads_favored'][bookmaker_key]
        adjusted_spread_underdog = game_data['adjusted_spreads_underdog'][bookmaker_key]

        game_score = abs(adjusted_spread_favored) + abs(adjusted_spread_underdog)

        if bookmaker_key not in bookmaker_value_index:
            bookmaker_value_index[bookmaker_key] = 0
        bookmaker_value_index[bookmaker_key] += game_score

# Sorted Bookmaker Value Index
for bookmaker_key, total_score in sorted(bookmaker_value_index.items(), key=lambda x: x[1], reverse=True):
    print(f'{bookmaker_key}: {total_score:.2f}')





