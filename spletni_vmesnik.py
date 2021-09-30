import bottle
from model import Uporabnik
# from model import *

x = None
y = None

@bottle.get("/")
def zacetna_stran():
    return bottle.template("prva_stran.html")

@bottle.post("/")
def zacento_ime():
    uporabnisko_ime = bottle.request.forms.get("uporabnisko_ime")
    geslo = bottle.request.forms.get("geslo")
    global x
    x = Uporabnik(uporabnisko_ime, geslo)
    bottle.redirect("/") #GET

@bottle.get("/prijava/")
def prijava():
    return bottle.template("prijava.html", napaka=None)

@bottle.get("/registracija/")
def registracija():
    return bottle.template("registracija.html", napake=[])

@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='static')

if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)