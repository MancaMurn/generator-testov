from bottle import JSONPlugin
import random


class Uporabnik:
    def __init__(self, ime, geslo):
        self.ime = ime
        self.geslo = geslo



class Podatek:
    def __init__(self, baza):
        self.baza = baza
    
    def izberi_vrednost(self):
        self.vrednost = random.choice(self.baza)
    

class Naloga:  
    def __init__(self, besedilo, st_naloge = 0, st_podatkov = 0):
        self.besedilo = besedilo
        self.st_naloge = st_naloge
        self.st_podatkov = st_podatkov
        self.resitev = self.izracunaj_resitev()
        self.podatki = self.ustvari_seznam_podatkov()

    # kje preberem st_podatkov

    def izracunaj_resitev(self):
        pass
    # resitev naj bi bila podana kot formula, v katero po vrsti vtavljamo seznam podatkov.
    # kako preberem formulo?

    def ustvari_seznam_podatkov(self):
        seznam = [] 
        for x in range(self.st_podatkov):
        #    seznam.append(Podatek(baza))
        #kako najdem bazo za vsak podatek po vrsti
            pass



class Test:
    def __init__(self, glava, st_testa, st_nalog, seznam_nalog):
        self.glava = glava
        self.st_testa = st_testa
        self.st_nalog = st_nalog
        self.naloge = self.ustvari_seznam_nalog()
    
    def ustvari_seznam_nalog(self):
        seznam = []
        for x in range(self.st_nalog):
        #    seznam.append(Naloga(besedilo, x, st_podatkov)
            pass