from flask import Flask, render_template, redirect, url_for, request, flash
# iš flask bibliotekos importuojame klasę Flask ir f-ją render_template.
app = Flask(__name__)
import requests
import json
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
# nustatėme, kad mūsų duomenų bazė bus šalia šio failo esants data.sqlite failas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# neseksime kiekvienos modifikacijos
db = SQLAlchemy(app)
# pilnas kelias iki šio failo.

if __name__ == '__main__':
    from forms import BandForm, RegistracijosForma, PrisijungimoForma, PaskyrosAtnaujinimoForma

login_manager = LoginManager(app)
login_manager.login_view = 'registruotis'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))

app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
# inicijuojame klasės Flask objektą, priskiriame kintamąjam app.

class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)
    token = db.Column("Žetonas", db.String, nullable=True)

@app.route("/bands")
@app.route("/")
def bands():
    r = requests.get("http://127.0.0.1:8000/bands")
    bands = json.loads(r.text)
    return render_template('bands.html', bands=bands)

@login_required
@app.route('/add_band', methods=['GET', 'POST'])
def add_band():
    form = BandForm()
    if form.validate_on_submit():
        my_token = current_user.token
        name = request.form['name']
        data = {'name': name}
        headers = {'Authorization': f'Token {my_token}'}
        r = requests.post("http://127.0.0.1:8000/bands", data=data, headers=headers)
        return redirect(url_for('bands'))
    return render_template('add_band.html', form=form)

@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('bands'))
    form = RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        vartotojas = Vartotojas(vardas=form.vardas.data, el_pastas=form.el_pastas.data, slaptazodis=koduotas_slaptazodis)
        db.session.add(vartotojas)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('bands'))
    return render_template('registruotis.html', title='Register', form=form)


@app.route("/prisijungti", methods=['GET', 'POST'])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for('bands'))
    form = PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('bands'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)

@app.route("/paskyra", methods=['GET', 'POST'])
@login_required
def paskyra():
    form = PaskyrosAtnaujinimoForma()
    if form.validate_on_submit():
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        current_user.token = form.token.data
        db.session.commit()
        flash('Tavo paskyra atnaujinta!', 'success')
        return redirect(url_for('paskyra'))
    elif request.method == 'GET':
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
        form.token.data = current_user.token
    return render_template('paskyra.html', title='Account', form=form)

@app.route("/atsijungti")
def atsijungti():
    logout_user()
    return redirect(url_for('bands'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)