from inspect import indentsize
from random import randint
import bottle
from model import *
import docx

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
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)

    predmet = bottle.request.forms.getunicode("predmet")
    letnik = bottle.request.forms.getunicode("letnik")
    st_ucencev = int(bottle.request.forms.getunicode("st_ucencev"))
    st_nalog = int(bottle.request.forms.getunicode("st_nalog"))

    index_testa = uporabnik.nov_test(Test(uporabnik.uporabnisko_ime, predmet, letnik, st_ucencev, st_nalog))
    uporabnik.v_datoteko()

    return bottle.template("nov_test_naloga.html", st_nalog=st_nalog, index_testa=index_testa, slovar_nalog=uporabnik.seznam_testov[index_testa].slovar_nalog)



@bottle.post("/uredi_besedilo/")
def uredi_besedilo():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)

    izpolnjena_naloga = int(bottle.request.forms.getunicode("izpolnjena_naloga"))
    index_testa = int(bottle.request.forms.getunicode("index_testa"))
    st_nalog = int(bottle.request.forms.getunicode("st_nalog"))
    besedilo = bottle.request.forms.getunicode("besedilo")

    uporabnik.seznam_testov[index_testa].slovar_nalog[izpolnjena_naloga].spremeni_besedilo(besedilo)
    uporabnik.v_datoteko()

    return bottle.template("nov_test_naloga.html", st_nalog=st_nalog, index_testa=index_testa, slovar_nalog=uporabnik.seznam_testov[index_testa].slovar_nalog)



@bottle.post("/uredi_podatke/")
def uredi_podatke():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)

    izpolnjena_naloga = int(bottle.request.forms.getunicode("izpolnjena_naloga"))
    index_testa = int(bottle.request.forms.getunicode("index_testa"))
    st_nalog = int(bottle.request.forms.getunicode("st_nalog"))

    formula_resitve = bottle.request.forms.getunicode("formula_resitve")

    st_podatkov = uporabnik.seznam_testov[index_testa].slovar_nalog[izpolnjena_naloga].st_podatkov
    podatki = {}
    for i in range(st_podatkov):
        b = bottle.request.forms.getunicode(f"answer{i+1}")
        z = bottle.request.forms.getunicode(f"answer{i+1}_zacetek")
        k = bottle.request.forms.getunicode(f"answer{i+1}_konec")
        podatki[f"#{i+1}"] = (b, z, k)

    naloga = uporabnik.seznam_testov[index_testa].slovar_nalog[izpolnjena_naloga]
    naloga.spremeni_slovar_baz(podatki)
    naloga.spremeni_formulo(formula_resitve)
    naloga.spremeni_stanje('KN')
    naloga.ustvari_razlicice()
    
    uporabnik.seznam_testov[index_testa].posodobi_stanje()
    uporabnik.v_datoteko()

    return bottle.template("nov_test_naloga.html", st_nalog=st_nalog, index_testa=index_testa, slovar_nalog=uporabnik.seznam_testov[index_testa].slovar_nalog)


@bottle.post("/test/")
def test():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
    index_testa = int(bottle.request.forms.getunicode("index_testa"))

    test = uporabnik.seznam_testov[index_testa]
    test.posodobi_stanje()
    slovar_nalog = test.slovar_nalog

    # for i in range(test.st_razlicic):
    #     #za vsakega učenca naredimo svojo json datoteko s testom.
    #     with open(f"{index_testa}_ucenec_{i}.json", "w") as datoteka:
    #         json.dump(test.glava, datoteka, ensure_ascii=True, indent=4)
    #         for j in test.slovar_nalog:
    #             naloga = test.slovar_nalog[j]
    #             json.dump(naloga.seznam_razlicic[i].v_slovar(), datoteka, ensure_ascii=True, indent=4)

    for i in range(test.st_razlicic):
        dokument = docx.Document()
        dokument.add_heading(test.glava, level = 1)
        for j in slovar_nalog:
            seznam_razlicic = slovar_nalog[j].seznam_razlicic
            print(seznam_razlicic)
            razlicica = seznam_razlicic[i]
            print(razlicica)
            besedilo = razlicica.besedilo()
            print(besedilo)

            dokument.add_heading(f"{j}. naloga")
            dokument.add_paragraph(f"{besedilo}")
            dokument.add_page_break()

        dokument.save(f'{index_testa}_ucenec_{i}.docx')

    return bottle.template("test.html")




@bottle.get("/arhiv/")
def arhiv_testov():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
    seznam_testov = uporabnik.seznam_testov
    return bottle.template("arhiv.html", seznam_testov = seznam_testov)


@bottle.post("/nedokoncan_test/")
def nedokoncan_test():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
    seznam_testov = uporabnik.seznam_testov

    # izpolnjena_naloga = int(bottle.request.forms.getunicode("izpolnjena_naloga"))
    index_testa = int(bottle.request.forms.getunicode("index_testa"))
    st_nalog = int(bottle.request.forms.getunicode("st_nalog"))
    

    return bottle.template("nov_test_naloga.html", st_nalog=st_nalog, index_testa=index_testa, slovar_nalog=seznam_testov[index_testa].slovar_nalog)

@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME)
    bottle.redirect("/")
    
@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='static')

if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)