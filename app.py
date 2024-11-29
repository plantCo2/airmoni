from flask import Flask, render_template
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Flask app
app = Flask(__name__)

# Google Sheets setup
SPREADSHEET_ID = "1cdfsf-Z5fcg9m4K2FhfyzMMHd3xaxYoDFVjU2F5X45A"  # Replace with your spreadsheet ID
RANGE_NAME = "Sheet1!A:B"  # Replace with your desired sheet and range

# Function to fetch the latest 10 rows from Google Sheets
def fetch_latest_data_from_sheets():
    credentials = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    values = result.get('values', [])
    
    # Get only the last 10 rows
    latest_values = values[-10:] if len(values) > 10 else values
    return latest_values

# Flask route to display data
@app.route("/")
def display_data():
    # Fetch the latest 10 rows of data from Google Sheets
    data = fetch_latest_data_from_sheets()
    return render_template("index.html", data=data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
