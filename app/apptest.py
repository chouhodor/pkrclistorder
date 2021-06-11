
import os
import json
import gspread
import pprint
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ucctransporttopsecret'


'''
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
creds = ServiceAccountCredentials.from_json_keyfile_name('app/ucc-transport.json', scope)
client = gspread.authorize(creds)
#local test



spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1sc9skuA6O9Jh19WaL2N_qAfw6CaabjO9BUMhb8A3-wY")
sheet = spreadsheet.sheet1 



@app.route('/', methods=['POST','GET'])
def index():


    dict_sheet = sheet.get_all_records()
    for d in dict_sheet:
        d['cac'] = d.pop('CAC/PKD')
        d['pic'] = d.pop('Name PIC/Pemanggil')
        d['contact'] = d.pop('No Contact PIC/Pemanggil')
        d['status'] = d.pop('Status UCC')


    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
   
    '''
    cac_name = [d['cac'] for d in dict_sheet]
    link_gs = [d['A. Link ke Google Sheet'] for d in dict_sheet]
    file_gs = [d['B. ATAU MuatNaik Line listing'] for d in dict_sheet]
    response_form = [d['Form Response Edit URL'] for d in dict_sheet]
    ucc_status = [d['status'] for d in dict_sheet]
    

    def delete_link(link):
        empty = '.'
        text ='LINK'
        if link == '':
            return empty
        else:
            return text
    
    def delete_edit(edit):
        empty = '.'
        text ='EDIT'
        if edit == '':
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
    '''
    status_dict = ['J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10' ]
    uccform = zip(dict_sheet, status_dict)


    return render_template('index.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    status_dict=status_dict,
    uccform=uccform
    #cac_name=cac_name,
    #link_gs=link_gs,
    #file_gs=file_gs,
    #response_form=response_form,
    #ucc_status=ucc_status,
    #delete_link=delete_link,
    #disabled=disabled,
    #tick_icon=tick_icon,
    #delete_edit=delete_edit
    )

@app.route('/status', methods = ['POST'])
def status():

    status_form = request.form['status_form']
    status_id = request.form['status_id']
    sheet.update(status_id, status_form)
    if request.method == 'POST':
        return redirect(url_for('index'))
 

@app.route('/form')
def form():
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfce09I5XrMIXsnSTJvmrsVuS5y8BClYhVwjK8i75EMYfwskA/viewform?usp=sf_link")

    


if __name__ == '__main__':
    app.run(debug=True)