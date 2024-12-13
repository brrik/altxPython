import os
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials


def addRow(roll, data):
    try:
        now = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        mainSheet.append_row([now, roll, data])
        return True
    except:
        return False


Auth = "./norse-lotus-423606-i2-353a26d9cd49.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Auth
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(Auth, scope)
Client = gspread.authorize(credentials)

SpreadSheet = Client.open_by_key("1eTYSRjB5TpIXwJQVCFCn8V32wZ_kPK1etwqgvaEa5Oo")
mainSheet = SpreadSheet.worksheet("Main")

x = addRow("部長", "テストデータ")
if x:
    print("登録完了")
else:
    print("Error")