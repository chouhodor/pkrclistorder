
import os
import json
import gspread
import pprint
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ucctransporttopsecret'



#live test
scopes = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
client = gspread.authorize(creds)
#live test

'''

#local test
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('ucc-transport.json', scope)
client = gspread.authorize(creds)
#local test
'''


spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1sc9skuA6O9Jh19WaL2N_qAfw6CaabjO9BUMhb8A3-wY")
sheet = spreadsheet.sheet1 


@app.route('/', methods=['POST','GET'])
def index():


    dict_sheet = sheet.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
   
    
    cac_name = [d['CAC/PKD/Hospital'] for d in dict_sheet]
    link_gs = [d['A. Link ke Google Sheet'] for d in dict_sheet]
    file_gs = [d['B. ATAU MuatNaik Line listing'] for d in dict_sheet]
    response_form = [d['Form Response Edit URL'] for d in dict_sheet]
    ucc_status = [d['Status UCC'] for d in dict_sheet]


    def delete_link(link):
        empty = '.'
        text ='LINK'
        if link == '':
            return empty
        else:
            return text

    def disabled(hlink):
        empty = 'color:white'
        if hlink == '':
            return empty

    def tick_icon(tick):
        siap = 'color:green'
        belum = 'color:white'
        if tick == 'SIAP':
            return siap
        else:
            return belum

    return render_template('index.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    cac_name=cac_name,
    link_gs=link_gs,
    file_gs=file_gs,
    response_form=response_form,
    ucc_status=ucc_status,
    delete_link=delete_link,
    disabled=disabled,
    tick_icon=tick_icon
    )

@app.route('/form')
def form():
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfce09I5XrMIXsnSTJvmrsVuS5y8BClYhVwjK8i75EMYfwskA/viewform?usp=sf_link")

    


if __name__ == '__main__':
    app.run(debug=True)