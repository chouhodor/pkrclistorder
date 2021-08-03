
import os
import json
import gspread
import pprint
from datetime import datetime, timedelta
#from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials


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



'''###SUKPA###
spreadsheet_sukpa = client.open_by_url("https://docs.google.com/spreadsheets/d/1ILr17LgncRwNmGYmztu-QFdhp7MtOEm1Nnq2QORI3_I")
sukpa_sh = spreadsheet_sukpa.worksheet("HTAA")

###ILKKM###
spreadsheet_ilkkm = client.open_by_url("https://docs.google.com/spreadsheets/d/17g4wofsHYsuWBTokyY2G0ipkQsQS-eWWidvAbuN8ugM")
ilkkm_sh = spreadsheet_ilkkm.worksheet("HTAA")

###UMP###
spreadsheet_ump = client.open_by_url("https://docs.google.com/spreadsheets/d/1XYYkgr7laJCmynqWt9v-Inom6I9RNJPOEvENr88aNdA")
ump_sh = spreadsheet_ump.worksheet("HTAA")

###IKPKT###
spreadsheet_ikpkt = client.open_by_url("https://docs.google.com/spreadsheets/d/1AL7AU2uyf4al1kmnyGTE2fALVf5nAMDg7k0ogAvO0Cw")
ikpkt_sh = spreadsheet_ikpkt.worksheet("HTAA")


###KUIPSAS###
spreadsheet_kuipsas = client.open_by_url("https://docs.google.com/spreadsheets/d/1_1uJsZ_nUKGWyBtCBSNfLhFQ1tZhRpbmFwSlitTsyuk")
kuipsas_sh = spreadsheet_kuipsas.worksheet("HTAA")'''


###ILKKM###
spreadsheet_ilkkm = client.open_by_url("https://docs.google.com/spreadsheets/d/17g4wofsHYsuWBTokyY2G0ipkQsQS-eWWidvAbuN8ugM")
ilkkm_sh = spreadsheet_ilkkm.worksheet("HTAA")


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


ward_sh = ward_sheet.get_all_records()
for d in ward_sh:
    d['incaj'] = d.pop('Nama incaj yang merujuk')
    d['rujukan'] = d.pop('Sumber Rujukan')
    d['nama'] = d.pop('Nama penuh pesakit')
    d['ic'] = d.pop('No. IC')
    d['umur'] = d.pop('Umur')
    d['jantina'] = d.pop('Jantina')
    d['warganegara'] = d.pop('Warganegara')
    d['comorbid'] = d.pop('Comorbid')
    d['alamat'] = d.pop('Alamat Rumah')
    d['phone'] = d.pop('No. telefon')
    d['cat'] = d.pop('Kategori klinikal')
    d['kluster'] = d.pop('Kluster jika berkaitan')
    d['swab'] = d.pop('Tarikh swab diambil')
    d['penjaga'] = d.pop('Penjaga jika ada ')
    d['status_penjaga'] = d.pop('Status COVID-19 penjaga ')
    d['penempatan'] = d.pop('Penempatan')
    d['edit'] = d.pop('Form Response Edit URL')

#list_sheet = [list(d.values()) for d in dict_sheet]
#print(list_sheet[1])

admit_pt = ward_sheet.row_values(3)
admit_pt=admit_pt[2:-1]
ilkkm_sh.append_row(admit_pt)


