# https://developers.google.com/sheets/api/quickstart/python

import os.path
import pickle
import shutil
from pathlib import *

import requests
import yaml
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1jziwRYrrYB_NsZ4Te1EMOxbsuYSwsCqr8RG2iT9mD-A"
SAMPLE_RANGE_NAME = "Form Responses 1!A1:L"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    header = values.pop(0)

    speakers = []
    if not values:
        print("No data found.")
    else:
        for r in values:
            row = dict(zip(header, r))
            if row["I understand the conditions, and confirm I am a Katie"] != "Agree":
                continue
            if row["Action"] == "Spam":
                continue
            if row["Action"] == "Accepted":  # prevent reprocessing
                continue
            data = {
                "name": row["Your name"],
                "twitter": row["Your Twitter handle"].strip("@"),
                "link": row["Your talk video recording link"],
                "title": row["Your talk title"],
            }

            avurl = row["A link to your avatar (square)"]
            avatar = f"{data['twitter']}.png"
            data["avatar"] = avatar
            resp = requests.get(avurl, stream=True)
            with open(Path.cwd() / "img" / avatar, "wb") as out:
                shutil.copyfileobj(resp.raw, out)
            del resp

            if row["Your LinkedIn URL (if you'd prefer this over Twitter)"]:
                data["linkedin"] = row[
                    "Your LinkedIn URL (if you'd prefer this over Twitter)"
                ]
            speakers.append(data)

    print(yaml.dump(speakers))


if __name__ == "__main__":
    main()
