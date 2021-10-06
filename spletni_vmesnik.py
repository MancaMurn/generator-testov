from _typeshed import Self
from typing import _get_type_hints_obj_allowed_types
import bottle
from model import *

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"

x = None
y = None

@bottle.get("/")
def zacetna_stran():
    return bottle.template("prva_stran.html", napaka=None)

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    else:
        try:
            Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
            bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
            bottle.redirect("/pozdrav_uporabnika/")
        except ValueError as e:
            return bottle.template("prva_stran.html", napaka=e)


@bottle.get("/pozdrav_uporabnika/")
def pozdrav_uporabnika():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    return bottle.template("pozdrav_uporabnika.html", uporabnisko_ime=uporabnisko_ime)



@bottle.get("/registracija/")
def registracija():
    return bottle.template("registracija.html", napake=[])

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napake="Vnesi uporabniško ime!")
    else:
        try:
            Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
            bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
            bottle.redirect("/")
        except ValueError as e:
            return bottle.template("registracija.html", napake=e)




@bottle.get("/nov_test_osnova/")
def nov_test__osnova():
    return bottle.template("nov_test_osnova.html")

@bottle.post("/nov_test_osnova/")
def glava_testa():
    predmet = bottle.request.forms.getunicode("predmet")
    letnik = bottle.request.forms.getunicode("letnik")
    st_ucencev = bottle.request.forms.getunicode("st_ucencev")
    st_nalog = int(bottle.request.forms.getunicode("st_nalog"))
    
    # Uporabnik.seznam_testov.append(Test(predmet, letnik, st_ucencev, st_nalog))
    
    return bottle.template("nov_test_naloga.html", st_nalog=st_nalog)








@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME)
    bottle.redirect("/")
    
@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='static')


if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)