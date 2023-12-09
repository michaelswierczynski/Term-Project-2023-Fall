# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# # Your existing functions and data loading here

# season_dates = {
#     '2020-2021': {'start': '11/04/2020', 'end': '04/04/2021'},
#     '2021-2022': {'start': '11/04/2021', 'end': '04/04/2022'},
#     '2022-2023': {'start': '11/04/2022', 'end': '04/04/2023'},
#     '2023-2024': {'start': '11/01/2023', 'end': '12/04/2023'},
# }

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/run_script', methods=['POST'])
# def run_script():
#     selected_season = request.args.get('season')
#     start_date = season_dates[selected_season]['start']
#     end_date = season_dates[selected_season]['end']
#     main(selected_season, start_date, end_date)
#     return "Script executed successfully"

# # Your other routes and code follow

# if __name__ == "__main__":
#     app.run(debug=True)

