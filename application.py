from flask import Flask,render_template, request, url_for, session, send_file, jsonify,Response, flash
from markupsafe import Markup
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__,template_folder='templet')
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/storage'
db = SQLAlchemy(app)

class Test_table(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    time_date = db.Column(db.String(10), unique=False, nullable=False)
    enckey = db.Column(db.String(20), nullable=False)
    enctext = db.Column(db.String(), nullable=False)
    
@app.route("/")
def home():
    return render_template('encrypt.html')
@app.route("/enc", methods=["GET", "POST"])
def encryption():
    if request.method == "POST" and request.form['text'] != '':
        txt = request.form['text']
        import appmain,main_genalgo
        key,encrypted_text = appmain.run_encryption(txt)
        # print(encrypted_text)
        #store to database
        entry = Test_table(enckey=key, enctext=encrypted_text, time_date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        #Flash massage to html page
        message = Markup(f'<h2><li>Your key is : <a href="" title="Click to copy" class="copy-message">{key}</a></li></h2>')
        flash(message)
        return render_template('encrypt.html')    
    else:
        return render_template('encrypt.html')

@app.route("/dyc",methods=["GET","POST"])
def decryption():
    if request.method == "POST" and request.form['key'] != '':
        key = request.form['key']
        row = Test_table.query.filter_by(enckey=key).all()
        # print(row[0].enctext)
        # return render_template("decrypt.html")
        import appmain, main_genalgo
        decrypt_text = appmain.run_decrypt(key,row[0].enctext)
        #Flash the message to the user
        message = Markup(f'{decrypt_text}')
        flash(message)
        return render_template("decrypt.html")
    else:
        return render_template("decrypt.html")

   
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')