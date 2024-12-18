import os
import gspread
import datetime
from fastapi import FastAPI, Request
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

@app.post("/postdata/")
async def addRow(request: Request):
    try:
        now = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        json_data = await request.json()
        roll = json_data.get("roll")
        data  = json_data.get("data")
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
    
@app.get("/getrolldata/{roll}")
async def getRollData(roll):
    try:
        roll_dict = {
            "sh":"部長",
            "jb":"事業部長",
            "bc":"部長",
            "kc":"課長",
            "gl":"GL"
            }
        main_data = mainSheet.get_all_values()
        print(roll_dict[roll])
        roll_based_list = filter_by_roll(main_data,roll_dict[roll])
        return roll_based_list
    except:
        return False

def filter_by_roll(data,roll):
    return_list = []
    for i in data:
        if i[1] == roll:
            return_list.append(i)
    
    return return_list