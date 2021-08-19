from flask import Flask
from flask import render_template, jsonify, request, redirect, send_file, url_for, make_response
from firebase import firebase
import pdfkit
import json
app = Flask(__name__)

firebase = firebase.FirebaseApplication(
    'https://wedding-invitation-52b05-default-rtdb.firebaseio.com/', None)

@app.route("/")
def display_home():
    return render_template('index.html', name='faris')

@app.route("/thanks/<confirm>")
def display_thanks(confirm):
    if confirm=='yes':
        message = 'Thank you for your response'
    else:
        message = 'We are sorry to hear that'
    return render_template('no_page.html', message=message)

@app.route('/daftar-undangan/', methods=['GET'])
def daftar_undangan():
    result = firebase.get('/Register/', '')
    #data = json.loads(result)
    return render_template('list-undangan.html')


@app.route('/daftar-pesan/', methods=['GET'])
def daftar_pesan():
    result = firebase.get('/Pesan/', '')
    # data = jsonify(result)
    return render_template('list-pesan.html')

@app.route('/pesan-buat/', methods=['POST', 'GET'])
def pesan_create():
    if request.method=='GET':
        return redirect(url_for('display_home'))
    nama = request.form['name']
    pesan = request.form['pesan']

    data = {
        'nama':nama,
        'pesan':pesan,
    }

    result = firebase.post('Pesan', data)

    return render_template('thanks.html')

@app.route('/registered/', methods=['POST','GET'])
def registered_create():
    if request.method == 'GET':
        return redirect(url_for('display_home'))
    nama = request.form['name']
    # email = request.form['email']
    # phone = request.form['phone']
    afiliasi = request.form['afiliasi']
    konfirmasi = request.form['konfirmasi']

    data = {
        'nama': nama,
        # 'email': email,
        # 'phone': phone,
        'afiliasi': afiliasi,
        'konfirmasi': konfirmasi,
    }

    result = firebase.post('Register', data)

    if konfirmasi=='Hadir' or konfirmasi=='Mungkin':
        return render_template('invitation_page.html', nama=nama, attend='yes', afiliasi=afiliasi)
    else:
        return render_template('invitation_page.html', nama=nama, attend='no', afiliasi=afiliasi)
    # return redirect(url_for('display_thanks', confirm='yes'))



@app.route('/registered/<id>/', methods=['GET'])
def get_detail(id):
    result = firebase.get('/Register/'+id+'/', '')
    nama = result['nama']
    map_link = "https://tlgur.com/d/GYwWJqm4"
    doa = "Dengan Memohon Rahmat Allah SWT Kami Bermaksud Menyelenggarakan Resepsi Pernikahan Putra-Putri Kami"
    alamat_tujuan = "Jalan Tirtohudan Raya no II, Kediri"
    tanggal_resepsi = "Minggu, 9 Desember 2021"
    pukul_resepsi = "10.00-selesai"
    tanggal_ijab = "Jumat, 7 Desember 2021"
    pukul_ijab = "08.00-10.00"
    harapan = "Kehadiran Serta Doa Restu Bapak/Ibu/Saudara/i merupakan suatu kehormatan & kebahagiaan bagi kami"

    data = {
        'nama': nama,
        'doa': doa,
        'alamat_tujuan': alamat_tujuan,
        'tanggal_resepsi': tanggal_resepsi,
        'pukul_resepsi': pukul_resepsi,
        'tanggal_ijab': tanggal_ijab,
        'pukul_ijab': pukul_ijab,
        'harapan': harapan,
        'map_link': map_link
    }

    return jsonify(data)


@app.route('/invitation-download/', methods=['GET'])
def get_invitation(id):

    data_pdf = pdfkit.from_url(
        'https://tlgur.com/d/g50bA2yG', 'micro.pdf')
    return send_file(data_pdf)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
