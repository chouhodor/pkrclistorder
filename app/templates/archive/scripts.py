@app.route('/worklist', methods=['POST','GET'])
def worklist():


    dict_sheet = sheet.get_all_records()
    ward_sh = ward_sheet.get_all_records()

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
        d['kluster'] = d.pop('Kluster jika berkaitan')
        d['swab'] = d.pop('Tarikh swab diambil')
        d['penjaga'] = d.pop('Penjaga jika ada ')
        d['status_penjaga'] = d.pop('Status COVID-19 penjaga ')
        d['penempatan'] = d.pop('Penempatan')
        d['edit'] = d.pop('Form Response Edit URL')
    
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
    wadform = zip(ward_sh, num_range)


    return render_template('worklist.html',  
    dict_sheet = dict_sheet,
    ward_sh=ward_sh,
    date_times=date_times,
    uccform=uccform,
    wadform=wadform,
    delete_link=delete_link,
    catatan_dot=catatan_dot,
    catatan_empty=catatan_empty
    )