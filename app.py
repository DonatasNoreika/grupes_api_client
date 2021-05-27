from flask import Flask, render_template, redirect, url_for, request
# iš flask bibliotekos importuojame klasę Flask ir f-ją render_template.
app = Flask(__name__)
import requests
import json
from forms import BandForm

app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
# inicijuojame klasės Flask objektą, priskiriame kintamąjam app.

@app.route("/bands")
def bands():
    r = requests.get("http://127.0.0.1:8000/bands")
    bands = json.loads(r.text)
    return render_template('bands.html', bands=bands)

@app.route('/add_band', methods=['GET', 'POST'])
def add_band():
    form = BandForm()
    if form.validate_on_submit():
        my_token = request.form['token']
        name = request.form['name']
        data = {'name': name}
        headers = {'Authorization': f'Token {my_token}'}
        r = requests.post("http://127.0.0.1:8000/bands", data=data, headers=headers)
        return redirect(url_for('bands'))
    return render_template('add_band.html', form=form)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)