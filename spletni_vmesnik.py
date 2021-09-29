import bottle
from model import Uporabnik
# from model import *

x = None
y = None

@bottle.get("/")
def zacetna_stran():
    if x:
        a = x.ime
    else:
        a = None

    return bottle.template("prijava.html", napaka = None, uporabnisko_ime = a)

@bottle.post("/")
def zacento_ime():
    uporabnisko_ime = bottle.request.forms.get("uporabnisko_ime")
    geslo = bottle.request.forms.get("geslo")
    global x
    x = Uporabnik(uporabnisko_ime, geslo)
    bottle.redirect("/") #GET

if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)
