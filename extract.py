import requests
from datetime import datetime, timedelta
import json

api_key = '0e09f4fdbae623c8ffa3a5158a3db325'  # Replace with your actual API key
sport_key = 'basketball_ncaab'
regions = 'us'
markets = 'spreads'
odds_format = 'american'
# date = '2021-10-18T12:00:00Z'
start_date = datetime.strptime('2020-11-01', '%Y-%m-%d')
end_date = datetime.strptime('2023-12-05', '%Y-%m-%d')

headers = {'apiKey': api_key}

target_months = [1, 2, 3, 4, 11, 12]  
target_years = [2020, 2021, 2022, 2023]

all_data = []

for year in target_years:
    for month in target_months:
        print(f'Processing {year}-{month}')
        # Set the day to the 1st of the month
        current_date = max(datetime(year, month, 1), start_date)

        last_day_of_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        while current_date <= last_day_of_month and current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            print(f'Processing date: {date_str}')

            url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds-history/?apiKey={api_key}&regions={regions}&markets={markets}&oddsFormat={odds_format}&date={date_str}'
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                odds_data = response.json()
                print(f'Data for {date_str} retrieved successfully.')
                all_data.append({date_str: odds_data})
            else:
                print(f'There was a problem with the odds request. Status code: {response.status_code}')
                print(response.text)
            
            current_date += timedelta(days=1)

output_file = 'odds_data.json'
with open(output_file, 'w') as json_file:
        json.dump(all_data, json_file)
print(f'Data saved to {output_file}.')