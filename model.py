from bottle import JSONPlugin
import random




class Uporabnik:
    def __init__(self, ime, geslo):
        self.ime = ime
        self.geslo = geslo


# V besedilo naj manjkajoč podatek označijo z #. Besedilo naj bo v obliki niza.
# V kakšni obliki naj bo formula za rešitev?


class Naloga:  
    def __init__(self, besedilo = "", st_razlicic = 0, slovar_podatkov = {}, formula_resitve = ""):
        self.st_razlicic = st_razlicic #izberemo na zacetku koliko razlicic testov zelimo. vsaka naloga v enem testu ima ta atribut enak.
        
        self.besedilo = besedilo    #besedilo podamo v obliki niza
        self.st_podatkov = self.besedilo.count("#")
        
        self.formula = formula_resitve #kako naj bo podana formula??

        self.slovar = slovar_podatkov #baze naj bi izbrali s klikom, kako to spravim v slovar??


    def izberi_seznam_podatkov(self):
        seznam = [] 
        for x in self.slovar:
            seznam.append(random.coice(self.slovar[x]))
        return seznam
    # funkcija iz slovarja podatkov z bazami izbere naključne podatke in jih sharni v seznam.


    def izracunaj_resitev(self, seznam_podatkov):
        pass
    # resitev naj bi bila podana kot formula, v katero po vrsti vtavljamo seznam podatkov.
    # kako preberem formulo?


    def oblikuj_nalogo(self, seznam_podatkov):
        besedilo = self.besedilo
        podatki = seznam_podatkov
        n = 0
        for x in besedilo:
            if x == "#":
                besedilo.replace("#", str(podatki[0]))
                n += 1 
        return besedilo
    #funkcija naj bi v besedilo vstavila podatke


    def ustvari_razlicice(self):
        slovar_razlicic = {}
        for x in range(self.st_razlicic):
            podatki = self.izberi_seznam_podatkov()
            resitev = self.izracunaj_resitev(podatki)

            slovar_razlicic[self.oblikuj_nalogo(podatki)] = resitev
    # funcija v slovar shrani razlicice naloge in resitve






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