from flask import Flask, render_template
# iš flask bibliotekos importuojame klasę Flask ir f-ją render_template.
app = Flask(__name__)
import requests
import json

# inicijuojame klasės Flask objektą, priskiriame kintamąjam app.

@app.route('/')
# įvelkame f-ją į flask dekoratorių. Be jo  funkcija būtų bereikšmė. Dekorato riaus parametruose nurodome, kad norėsime rezultato 127.0.0.1:8000/ url adrese."""

def bands():
    r = requests.get("http://127.0.0.1:8000/bands")
    bands = json.loads(r.text)
    return render_template('bands.html', bands=bands)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)