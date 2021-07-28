import bottle
from model import Uporabnik
# from model import *

x = None

@bottle.get("/")
def zacetna_stran():
    return bottle.template("hello_world.html", uporabnik=x)

@bottle.post("/")
def zacento_ime():
    uporabnisko_ime = bottle.request.forms.get("uporabniskoIme")
    global x
    x = Uporabnik(uporabnisko_ime)
    bottle.redirect("/") #GET

if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)
