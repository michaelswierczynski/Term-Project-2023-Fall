import json
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Data Preparation
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

json_file_path = 'odds_data.json'
data = load_json_file(json_file_path)


from datetime import datetime

def filter_data_by_season(data, start_date, end_date):
    # Convert start and end dates to datetime objects
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y')

    # Filter data for the specified season
    seasonal_data = []
    for date_dict in data:
        for date_str, date_data in date_dict.items():
            if start_datetime <= datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') <= end_datetime:
                if 'data' in date_data:
                    seasonal_data.extend(date_data['data'])
                elif 'next_timestamp' in date_data and isinstance(date_data['next_timestamp'], dict) and 'data' in date_data['next_timestamp']:
                    seasonal_data.extend(date_data['next_timestamp']['data'])

    return seasonal_data

# Example usage:
json_file_path = 'odds_data.json'
loaded_data = load_json_file(json_file_path)

# Specify the date range for the season
start_date_season = '11/16/2020'
end_date_season = '04/06/2021'

# Step 2: Seasonal Analysis
season_data = filter_data_by_season(loaded_data, start_date_season, end_date_season)

# Now, season_data contains the filtered data for the specified season
# print(season_data[:2])  

# def compare_bookmakers(season_data):
#     bookmakers_data = {}  # Dictionary to store bookmakers' spread data for each game

#     for game in season_data:
#         game_id = game['id']
#         bookmakers_data[game_id] = {'bookmakers': {}, 'spreads_favored': {}, 'spreads_underdog': {}}

#         for bookmaker in game['bookmakers']:
#             bookmaker_key = bookmaker['key']
#             outcomes = bookmaker['markets'][0]['outcomes']

#             # Check if there are outcomes for both favored and underdog teams
#             if len(outcomes) == 2:
#                 favored_team_outcome = next((outcome for outcome in outcomes if outcome['point'] < 0), None)
#                 underdog_team_outcome = next((outcome for outcome in outcomes if outcome['point'] > 0), None)

#                 if favored_team_outcome and underdog_team_outcome:
#                     favored_spread = favored_team_outcome['point']
#                     underdog_spread = underdog_team_outcome['point']

#                     bookmakers_data[game_id]['bookmakers'][bookmaker_key] = bookmaker['title']
#                     bookmakers_data[game_id]['spreads_favored'][bookmaker_key] = favored_spread
#                     bookmakers_data[game_id]['spreads_underdog'][bookmaker_key] = underdog_spread

#     return bookmakers_data

# Example usage:
# bookmakers_data = compare_bookmakers(season_data)

# Now, bookmakers_data contains spread information for each bookmaker for each game
# You can access the data using game IDs, bookmaker keys, and spread types
# Example: bookmakers_data[game_id]['bookmakers'][bookmaker_key]

def compare_bookmakers(data):
    bookmakers_data = {}

    for game in data:
        game_id = game['id']
        bookmakers_data[game_id] = {'bookmakers': {}, 'spreads_favored': {}, 'spreads_underdog': {}, 'adjusted_spreads_favored': {}, 'adjusted_spreads_underdog': {}}

        for bookmaker in game['bookmakers']:
            outcomes = bookmaker['markets'][0]['outcomes']

            # Check if there are two outcomes for spreads
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

                    # Calculate and store adjusted spreads
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

# # Print information for the first game as an example
# first_game_id = season_data[0]['id']

# print(f"Game ID: {first_game_id}")
# print("Bookmakers:")
# for bookmaker_key, bookmaker_title in bookmakers_data[first_game_id]['bookmakers'].items():
#     print(f"  {bookmaker_title} (Key: {bookmaker_key})")
#     print(f"    Favored Spread: {bookmakers_data[first_game_id]['spreads_favored'][bookmaker_key]}")
#     print(f"    Underdog Spread: {bookmakers_data[first_game_id]['spreads_underdog'][bookmaker_key]}")
#     print()


# Assume season_bookmakers is the result of calling compare_bookmakers on your data
# game_count = 0  # Counter for the number of games printed

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

    # # Increment the game count
    # game_count += 1
    # if game_count >= 2:
    #     break  # Stop printing after the first two games


bookmaker_value_index = {}

for game_id, game_data in bookmakers_data.items():
    for bookmaker_key, bookmaker_info in game_data['bookmakers'].items():
        adjusted_spread_favored = game_data['adjusted_spreads_favored'][bookmaker_key]
        adjusted_spread_underdog = game_data['adjusted_spreads_underdog'][bookmaker_key]

        # Calculate a score for each game based on the adjusted spreads
        game_score = abs(adjusted_spread_favored) + abs(adjusted_spread_underdog)

        # Update the cumulative score for the bookmaker
        if bookmaker_key not in bookmaker_value_index:
            bookmaker_value_index[bookmaker_key] = 0
        bookmaker_value_index[bookmaker_key] += game_score

# Display the Total Value Index for each bookmaker
for bookmaker_key, total_score in sorted(bookmaker_value_index.items(), key=lambda x: x[1], reverse=True):
    print(f'{bookmaker_key}: {total_score}')




