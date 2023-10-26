from flask import Flask,render_template, request, url_for, session, send_file, jsonify,Response
import os
from io import BytesIO
import zipfile

app = Flask(__name__,template_folder='templet')
app.secret_key = "hello"

@app.route("/")
def home():
    return render_template('style.html')
@app.route("/enc", methods=["GET", "POST"])
def encryption():
    if request.method == "POST" and request.form['txt'] != '':
        txt = request.form['txt']
        keyfile = request.files['existkey']
        import appmain,main_genalgo
        if keyfile.filename != '':
            key = request.files['existkey'].read()
            cip = appmain.ciphertext(key)
            encrypted_text = appmain.encrypt(txt,cip)
            filename = 'enctxt.bin'
            headers = {'content-Disposition':f'attachment; filename="{filename}"', 'Content-Type':'application/octet-stream'}
            return Response(encrypted_text, headers=headers)
        else:
            key,encrypted_text = appmain.run_encryption(txt)
            binaryfiles = [('key.bin',key),('enctxt.bin',encrypted_text)]
            zip_data = BytesIO()
            with zipfile.ZipFile(zip_data, 'w') as zipf:
                for filename, data in binaryfiles:
                    zipf.writestr(filename, data)
            zip_data.seek(0)
            return Response(zip_data, mimetype='application/zip',headers={'Content-Disposition': f'attachment; filename={txt[:10]}.zip'})
    else:
        return render_template('style.html',msg="Input a text!!!")

@app.route("/dyc",methods=["POST"])
def decryption():
    if request.method == "POST":
        enc_txt = request.files['txt'].read()
        key = request.files['key'].read()
        try:
            import appmain,main_genalgo
            decrypt_text = appmain.run_decrypt(key,enc_txt)
            return jsonify({'msg':decrypt_text})
        except:
            return jsonify({'msg':"Technical Error TryAgain"})
    else:
        return render_template("style.html")

   
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')