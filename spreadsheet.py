from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SPREADSHEET_ID = "1NJUT4UqRZNrPpuX9o7_83048zKwCNovLSADpNBo6Rbs"
# SHEET_NAME = "8/28-Present"
SHEET_NAME = "master"
ZSON_COL = "AH"
PLAYER_COL_MAP = {
    "BS": "AB",
    "ES": "AC",
    "HN": "AD",
    "TP": "AE",
    "YX": "AF",
    "JK": "AI",
    "TT": "AJ",
    "MN": "AM",
    "YS": "AN",
    "BU": "AO",
    "MM": "AQ",
    "AT": "AR"
}
STAKE_COL = "T"
NAME_COL = "V"

start_row = None  # row counter

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'secrets.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

api_service = build('sheets', 'v4', credentials=creds)


def write_result(scores: dict[str, float]) -> None:
    try:
        global start_row

        result = api_service.spreadsheets().values() \
            .batchUpdate(spreadsheetId=SPREADSHEET_ID, body=get_body(scores)) \
            .execute()
        print(f"{result.get('totalUpdatedCells')} cells updated.")
        start_row += 1
    except Exception as err:
        print(err)


def get_body(scores: dict[str, float]) -> dict:
    body = {
        "valueInputOption": "USER_ENTERED"
    }

    data = [{"range": get_range("T"), "values": [["1"]]}, {"range": get_range("V"), "values": [["bj"]]}]
    zson_val = sum(scores.values())
    if zson_val != 0:
        data.append({
            "range": get_range(ZSON_COL),
            "values": [[str(zson_val)]]
        })

    for k, v in scores.items():
        if v != 0:

            col = get_player_col(k)
            if col is None:
                print(f"{k} not found in player name col map, skipping")
                continue

            data.append({
                "range": get_range(col),
                "values": [[str(v)]]
            })

    body['data'] = data
    return body


def get_range(col: str) -> str:
    return f"{SHEET_NAME}!{col}{start_row}"


def get_player_col(player_name: str) -> str:
    return PLAYER_COL_MAP[player_name.upper()]
