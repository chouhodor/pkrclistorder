
from logging import exception
import os
import json
import gspread
import pprint
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ucctransporttopsecret'


try:
    #live test
    scopes = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)
    #live test

except:
    #local test
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('app/ucc-transport.json', scope)
    client = gspread.authorize(creds)
    #local test


spreadsheet_lo = client.open_by_url("https://docs.google.com/spreadsheets/d/1VXYj_XYbLJLYTKY2G39YEffylcKS1PTSsGMyO2YqD-8")
sheet = spreadsheet_lo.sheet1 

spreadsheet_archive = client.open_by_url("https://docs.google.com/spreadsheets/d/1O0P4xms_54-aV5O7_I6UPRp9dLc5nygP65U7Z84kHis")
archive_sheet = spreadsheet_archive.sheet1 

spreadsheet_ward = client.open_by_url("https://docs.google.com/spreadsheets/d/1IAd0NYGO8SteNL85GVHV_sawyMfvyWqlNYbKqQ8eUR0")
ward_sheet = spreadsheet_ward.sheet1 

try:
    ###ILKKM###
    spreadsheet_ilkkm = client.open_by_url("https://docs.google.com/spreadsheets/d/17g4wofsHYsuWBTokyY2G0ipkQsQS-eWWidvAbuN8ugM")
    ilkkm_sh = spreadsheet_ilkkm.worksheet("HTAA")

    ###SUKPA###
    spreadsheet_sukpa = client.open_by_url("https://docs.google.com/spreadsheets/d/1ILr17LgncRwNmGYmztu-QFdhp7MtOEm1Nnq2QORI3_I")
    sukpa_sh = spreadsheet_sukpa.worksheet("HTAA")

    ###UMP###
    spreadsheet_ump = client.open_by_url("https://docs.google.com/spreadsheets/d/1XYYkgr7laJCmynqWt9v-Inom6I9RNJPOEvENr88aNdA")
    ump_sh = spreadsheet_ump.worksheet("HTAA")

    ###KUIPSAS###
    spreadsheet_kuipsas = client.open_by_url("https://docs.google.com/spreadsheets/d/1_1uJsZ_nUKGWyBtCBSNfLhFQ1tZhRpbmFwSlitTsyuk")
    kuipsas_sh = spreadsheet_kuipsas.worksheet("HTAA")
    
except:
    pass

kuipsas_master = []
ump_master = []

'''
spreadsheet_ump = client.open_by_url("https://docs.google.com/spreadsheets/d/1TxoJOfqdByh27X67ZAgOzOrmOdXummCPK6goHDgnSIg")
ump_sh = spreadsheet_ump.worksheets()
ump_sh.pop(0)
'''




def master_df(master_list, spread_sheet):
    pkrc_sh = spread_sheet.worksheets()
    pkrc_sh.pop(0)
    for sh in pkrc_sh:
        df = pd.DataFrame(sh.get_all_records())
        num_total = len(df.index)
        try:
            df['JANTINA'].replace('L','LELAKI', inplace=True)
            df['JANTINA'].replace('Lelaki','LELAKI', inplace=True)
            num_lelaki = len(df.loc[df['JANTINA']=='LELAKI'])
        except:
            num_lelaki = 'error'

        try:
            df['JANTINA'].replace('P','PEREMPUAN', inplace=True)
            df['JANTINA'].replace('Perempuan','PEREMPUAN', inplace=True)
            num_perempuan = len(df.loc[df['JANTINA']=='PEREMPUAN'])
        except:
            num_perempuan = 'error'
        try:
            num_paeds = len(df.loc[df['UMUR'] <= 12])
        except:
            num_paeds = 'error'

        try:
            df = df.rename(columns={'KATEGORI KLINIKAL': 'CAT'})
            df['CAT'] = df['CAT'].replace(['CAT 2', 'CAT 2, MILD', 'CAT 2 MILD', 'Kategori 2: Symptomatic, no pneumonia (Mild)'], 2)
            df['CAT'] = df['CAT'].replace(['CAT 1', 'Kategori 1: Asymptomatic'], 1)
            df['CAT'] = df['CAT'].replace(['CAT 3'], 3)
        except:
            cat_1 = 'error'
            cat_2 = 'error'
            cat_3 = 'error'

        try:
            cat_1 = len(df.loc[df['CAT'] == 1])
        except:
            cat_1 = 'error'

        try:
            cat_2 = len(df.loc[df['CAT'] == 2])
        except:
            cat_2 = 'error'

        try:
            cat_3 = len(df.loc[df['CAT'] == 3])
        except:
            cat_3 = 'error'
            
        master_list.append([sh.title, num_total, num_lelaki, num_perempuan, num_paeds, cat_1, cat_2, cat_3])

    master_list = [master_list[-(i+1)] for i in range(len(master_list))]
    master_sh = spread_sheet.get_worksheet(0)


    cell_list = master_sh.range('A28:J40')
    for c in cell_list:
        c.value = ''
    master_sh.update_cells(cell_list)
    master_sh.batch_update(
    [
        {'range': 'A28:J40', 'values': master_list}
    ]
    )






@app.route('/', methods=['POST','GET'])
def index():


    dict_sheet = sheet.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
   
    for d in dict_sheet:
        d['cac'] = d.pop('CAC/PKD')
        d['pic'] = d.pop('Name PIC/Pemanggil')
        d['contact'] = d.pop('No Contact PIC/Pemanggil')
        d['male'] = d.pop('Bilangan Pesakit Lelaki')
        d['female'] = d.pop('Bilangan Pesakit Perempuan')
        d['family'] = d.pop('Bilangan keluarga')
        d['catatan'] = d.pop('Catatan')
        d['g_sheet'] = d.pop('A. Link ke Google Sheet')
        d['excel'] = d.pop('B. ATAU MuatNaik Line listing')
        d['status'] = d.pop('Status UCC')
        d['edit_response'] = d.pop('Form Response Edit URL')
    
    def delete_link(link):
        empty = ''
        text ='LINK'
        if link == '':
            return empty
        else:
            return text

  
    def delete_edit(edit):
        empty = ''
        text ='EDIT'
        if edit == '':
            return empty
        else:
            return text

    def disabled(hlink):
        empty = 'color:white'
        if hlink == '':
            return empty

    def delete_icon(icon):
        true = 'fas fa-check-circle'
        empty = ''

        if icon == '':
            return empty
        else:
            return true

    def tick_icon(tick):
        siap = 'color:green'
        masalah = 'color:orange'
        terima = 'color:white'
        if tick == 'SIAP':
            return siap
        elif tick == 'MASALAH':
            return masalah
        else:
            return terima
    
    return render_template('index.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    delete_link=delete_link,
    disabled=disabled,
    tick_icon=tick_icon,
    delete_edit=delete_edit,
    delete_icon=delete_icon
    )


@app.route('/worklist', methods=['POST','GET'])
def worklist():


    dict_sheet = sheet.get_all_records()

    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    for d in dict_sheet:
        d['cac'] = d.pop('CAC/PKD')
        d['pic'] = d.pop('Name PIC/Pemanggil')
        d['pic'] = d['pic'].title()
        d['contact'] = d.pop('No Contact PIC/Pemanggil')
        d['male'] = d.pop('Bilangan Pesakit Lelaki')
        d['female'] = d.pop('Bilangan Pesakit Perempuan')
        d['family'] = d.pop('Bilangan keluarga')
        d['catatan'] = d.pop('Catatan')
        d['g_sheet'] = d.pop('A. Link ke Google Sheet')
        d['excel'] = d.pop('B. ATAU MuatNaik Line listing')
        d['status'] = d.pop('Status UCC')

    

   
    def delete_link(link):
        empty = ''
        text ='LINK'
        if link == '':
            return empty
        else:
            return text

    def catatan_dot(dot):
        empty = 'far fa-comment fa-lg'
        dots ='far fa-comment-dots fa-lg'
        if dot == '':
            return empty
        else:
            return dots

    def catatan_empty(emp):
        empty = 'tiada'
        if emp == '':
            return empty
        else:
            return emp
    

    num_range= range(2, 50)
      
    uccform = zip(dict_sheet, num_range)


    return render_template('worklist.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    uccform=uccform,
    delete_link=delete_link,
    catatan_dot=catatan_dot,
    catatan_empty=catatan_empty
    )

@app.route('/archive', methods=['POST','GET'])
def archive():


    dict_sheet = archive_sheet.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    for d in dict_sheet:
        d['date'] = d.pop('Timestamp')
        d['cac'] = d.pop('CAC/PKD')
        d['pic'] = d.pop('Name PIC/Pemanggil')
        d['contact'] = d.pop('No Contact PIC/Pemanggil')
        d['male'] = d.pop('Bilangan Pesakit Lelaki')
        d['female'] = d.pop('Bilangan Pesakit Perempuan')
        d['family'] = d.pop('Bilangan keluarga')
        d['g_sheet'] = d.pop('A. Link ke Google Sheet')
        d['excel'] = d.pop('B. ATAU MuatNaik Line listing')
    
    def delete_link(link):
        empty = ''
        text ='LINK'
        if link == '':
            return empty
        else:
            return text

    def catatan_dot(dot):
        empty = 'far fa-comment fa-lg'
        dots ='far fa-comment-dots fa-lg'
        if dot == '':
            return empty
        else:
            return dots

    def catatan_empty(emp):
        empty = 'tiada'
        if emp == '':
            return empty
        else:
            return emp

    dict_sheet.reverse()
    


    return render_template('archive.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    delete_link=delete_link,
    catatan_dot=catatan_dot,
    catatan_empty=catatan_empty
    )


@app.route('/status', methods = ['POST'])
def status():

    status_form = request.form['status_form']
    status_id = request.form['status_id']
    sheet.update(status_id, status_form)
    if request.method == 'POST':
        return redirect(url_for('worklist'))


@app.route('/report')
def report():
    
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y")

    ###SUKPA###
    spreadsheet_sukpa = client.open_by_url("https://docs.google.com/spreadsheets/d/1ILr17LgncRwNmGYmztu-QFdhp7MtOEm1Nnq2QORI3_I")
    sukpa_sh = spreadsheet_sukpa.sheet1
    sukpa_input = sukpa_sh.row_values(4)
    sukpa_input.pop(0)
    

    ###ILKKM###
    spreadsheet_ilkkm = client.open_by_url("https://docs.google.com/spreadsheets/d/17g4wofsHYsuWBTokyY2G0ipkQsQS-eWWidvAbuN8ugM")
    ilkkm_sh = spreadsheet_ilkkm.sheet1
    ilkkm_input = ilkkm_sh.row_values(4)
    ilkkm_input.pop(0)

    ###UMP###
    spreadsheet_ump = client.open_by_url("https://docs.google.com/spreadsheets/d/1XYYkgr7laJCmynqWt9v-Inom6I9RNJPOEvENr88aNdA")
    ump_sh = spreadsheet_ump.sheet1
    ump_input = ump_sh.row_values(4)
    ump_input.pop(0)

    ###IKPKT###
    spreadsheet_ikpkt = client.open_by_url("https://docs.google.com/spreadsheets/d/1AL7AU2uyf4al1kmnyGTE2fALVf5nAMDg7k0ogAvO0Cw")
    ikpkt_sh = spreadsheet_ikpkt.sheet1
    ikpkt_input = ikpkt_sh.row_values(4)
    ikpkt_input.pop(0)

    ###KUIPSAS###
    spreadsheet_kuipsas = client.open_by_url("https://docs.google.com/spreadsheets/d/1_1uJsZ_nUKGWyBtCBSNfLhFQ1tZhRpbmFwSlitTsyuk")
    kuipsas_sh = spreadsheet_kuipsas.sheet1
    kuipsas_input = kuipsas_sh.row_values(4)
    kuipsas_input.pop(0)

    ###MARAN###
    spreadsheet_maran = client.open_by_url("https://docs.google.com/spreadsheets/d/1Mtig4CWF1juOwdPX8rc-PM_C49KtUsNiuKBSluXQCQU")
    maran_sh = spreadsheet_maran.sheet1
    maran_input = maran_sh.row_values(4)
    maran_input.pop(0)

    ###UNITEN###
    spreadsheet_uniten = client.open_by_url("https://docs.google.com/spreadsheets/d/1d2K9Pgpq4m5ovLXkfbG7w0jnVkspfZY0AHU7-31RoJg")
    uniten_sh = spreadsheet_uniten.sheet1
    uniten_input = uniten_sh.row_values(4)
    uniten_input.pop(0)

    ###TEMERLOH###
    spreadsheet_temerloh = client.open_by_url("https://docs.google.com/spreadsheets/d/1Z-A1NvMbMUuFMiy9-64ploCMZMU66eHobaTme6wxf88")
    temerloh_sh = spreadsheet_temerloh.sheet1
    temerloh_input = temerloh_sh.row_values(4)
    temerloh_input.pop(0)

    def number(x):
        y = list(map(int, x))
        return y

    def empty(x):
        if x == '0':
            return ' '
        else:
            return x



    zip_pkrc = zip(number(sukpa_input), number(ilkkm_input), number(ump_input), number(ikpkt_input), number(kuipsas_input), number(maran_input), number(uniten_input), number(temerloh_input))

    sum_pkrc = [w + x + y + z + a + b +c + d for (w, x, y, z, a, b, c, d) in zip_pkrc]

    return render_template('report.html',
    sukpa_input=sukpa_input,
    ilkkm_input=ilkkm_input,
    ump_input=ump_input,
    ikpkt_input=ikpkt_input,
    kuipsas_input=kuipsas_input,
    maran_input=maran_input,
    uniten_input=uniten_input,
    temerloh_input=temerloh_input,
    sum_pkrc=sum_pkrc,
    date_times=date_times,
    empty=empty
    )

        
@app.route('/padam', methods = ['POST'])
def padam():

    padam_form = int(request.form['padam_form'])
    sheet.delete_row(padam_form)
    if request.method == 'POST':
        return redirect(url_for('worklist'))


@app.route('/form')
def form():
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLSf_U8oc7xCl9dUN_j9m7SVwYtEJnbuitIQSsYfF2dw3a-oC3w/viewform?usp=sf_link")

@app.route('/panduan')
def panduan():
    return render_template('panduan.html')

@app.route('/kriteria')
def kriteria():
    return render_template('kriteria.html')

@app.route('/kuipsas')
def kuipsas():
    spreadsheet_kuipsas = client.open_by_url("https://docs.google.com/spreadsheets/d/1_oBxvYDTUQVHgmPVaP4t4DNHs6pgawBxKrR5oQguzj0")
     
    master_df(kuipsas_master, spreadsheet_kuipsas)
    return redirect (url_for('quit'))

@app.route('/quit')
def quit():
    #shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    #if shutdown_hook is not None:
    #  shutdown_hook()
    return ("Bye")

if __name__ == '__main__':
    app.run(debug=True)