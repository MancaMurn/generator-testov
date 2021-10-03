import bottle
from model import Uporabnik
# from model import *
import model

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"

x = None
y = None

@bottle.get("/")
def zacetna_stran():
    return bottle.template("prva_stran.html", napaka=None)

# @bottle.post("/")
# def zacentno_ime():
#     uporabnisko_ime = bottle.request.forms.get("uporabnisko_ime")
#     geslo = bottle.request.forms.get("geslo")
#     global x #kaj je ta global??
#     x = Uporabnik(uporabnisko_ime, geslo, seznam_testov=[])

#     return bottle.template("pozdrav_uporabnika.html", uporabnisko_ime, napaka = None)

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "prijava.html", napaka=e.args[0]
        )



@bottle.get("/registracija/")
def registracija():
    return bottle.template("registracija.html", napake=[])



@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "registracija.html", napaka=e.args[0]
        )


@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='static')


if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)