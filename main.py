import os
import gspread
import datetime
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware # CORS
from oauth2client.service_account import ServiceAccountCredentials

# CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Auth = "./norse-lotus-423606-i2-353a26d9cd49.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Auth
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(Auth, scope)
Client = gspread.authorize(credentials)

SpreadSheet = Client.open_by_key("1eTYSRjB5TpIXwJQVCFCn8V32wZ_kPK1etwqgvaEa5Oo")
mainSheet = SpreadSheet.worksheet("Main")

@app.get("/get/{roll}/{data}")
async def addRow(roll, data):
    try:
        now = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        mainSheet.append_row([now, roll, data])
        return True
    except:
        return False

@app.get("/getalldata")
async def getData():
    try:
        return_data = mainSheet.get_all_values()
        return return_data
    except:
        return False