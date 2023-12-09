# Term-Project-2023-Fall
OIM3640 Term Project

"""
Team Members:
Magnus Orava
Mike Swierczynski
"""

# Sports Betting Value Index

## Overview

This project aims to determine the value offered by different sportsbooks/bookmakers during college basketball seasons. It utilizes data from the Odds-API, analyzing point spreads and odds to calculate a value index for bookmakers over specific seasons.

## How it Works

### 1. Data Processing

- The script loads sports betting data from a JSON file (`odds_data.json`).
- It filters the data based on specified start and end dates for each college basketball season.

### 2. Bookmaker Comparison

- The script compares bookmakers for each game, considering spreads and odds.
- It calculates adjusted spreads for favored and underdog teams, capturing the bookmaker's value.

### 3. Value Index Calculation

- The value index for each bookmaker is determined by summing the game scores based on adjusted spreads.
- Higher value index scores indicate sportsbooks consistently offering more appealing lines to bettors.

## Season Dates

The script uses the following season dates for filtering data:

- **2020-2021 Season:** November 4, 2020, to April 4, 2021
- **2021-2022 Season:** November 4, 2021, to April 4, 2022
- **2022-2023 Season:** November 4, 2022, to April 4, 2023
- **2023-2024 Season:** November 1, 2023, to December 4, 2023


## Results

The script generates a value index for each bookmaker during the specified season and prints the results in descending order.
