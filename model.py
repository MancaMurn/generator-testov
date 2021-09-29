from bottle import JSONPlugin
import random

class Uporabnik:
    def __init__(self, ime, geslo):
        self.ime = ime
        self.geslo = geslo

        self.seznam_nalog = []

    def shrani_uporabnika(self):
        # Poglej pretnarjevo implementacijo
        with open("uporabniki.json"):
            pass
    
    def nalozi_uporabnika(self, uporabnisko_ime):
        # Poglej pretnarjevo implementacijo
        json.load("ime datoteke")



# V besedilo naj manjkajoč podatek označijo z #. Besedilo naj bo v obliki niza.
# V kakšni obliki naj bo formula za rešitev?

class Razlicica:
    def __init__(self, formula_resitve, besedilo = "", slovar_podatkov = None):
        self.besedilo = besedilo
        self.resitev = self.izracunaj_resitev(formula_resitve)
        self.slovar_podatkov = slovar_podatkov # Oblike npr. {"#1" : 5, "#2" : 7, "#7" : 6}
    
    def izracunaj_resitev(self, formula):
        for spremenljivka in self.slovar_podatkov:
            formula = formula.replace(spremenljivka, str(self.slovar_podatkov[spremenljivka]))
        
        return eval(formula)


# x = Naloga("Besedilo # asdfasdf # asfdasdf", 5)
# for razlicica in x.seznam_razlicic:
#     print(razlicica.besedilo)   
#     print(razlicica.resitev)

class Naloga:  
    def __init__(self, besedilo = "", st_razlicic = 0, slovar_podatkov = None, formula_resitve = ""):
        self.st_razlicic = st_razlicic #izberemo na zacetku koliko razlicic testov zelimo. vsaka naloga v enem testu ima ta atribut enak.
        
        self.besedilo = besedilo    #besedilo podamo v obliki niza
        self.st_podatkov = self.besedilo.count("#")
        
        self.formula = formula_resitve #kako naj bo podana formula??

        self.slovar = slovar_podatkov or dict() #baze naj bi izbrali s klikom, kako to spravim v slovar??
        self.seznam_razlicic = []

    def izberi_podatke(self):
    # funkcija iz slovarja podatkov z bazami izbere naključne podatke in jih sharni v seznam.
        slovar = {} 
        for x in self.slovar:
            slovar[x] = random.coice(self.slovar[x])
        return slovar  
        

    def vstavi_podatke_v_besedilo(self, podatki):
    # funkcija naj bi v besedilo vstavila podatke
    # podatki so slovar oblike npr. {"#1" : 5, "#2" : 7, "#7" : 6}

        novo_besedilo = self.besedilo

        for spremenljivka in podatki:
            novo_besedilo = novo_besedilo.replace(spremenljivka, str(podatki[spremenljivka]))
        
        return novo_besedilo


    def ustvari_razlicice(self):
    # funcija v seznam shrani razlicice naloge in resitve
    # resitve so pol v klasu razlicica

        for x in range(self.st_razlicic):
            slovar_podatkov = self.izberi_podatke()
            besedilo = self.vstavi_podatke_v_besedilo(slovar_podatkov)

            razlicica = Razlicica(self.formula, besedilo, slovar_podatkov)
            self.seznam_razlicic.append(razlicica)


class Test:
    def __init__(self, glava, st_razlicic, st_nalog, seznam_nalog):
        self.glava = glava
        self.st_razlicic = st_razlicic
        self.st_nalog = st_nalog        #kako preberem st_nalog??
        self.naloge = self.ustvari_seznam_nalog()
    
    def ustvari_seznam_nalog(self):
        seznam = []
        for x in range(self.st_nalog):
            pass

        #kako ustvarim seznam nalog --> to bi bil potem seznam slovarjev razlicic nalog