from bottle import JSONPlugin
import random
import json
import hashlib

class Uporabnik:
    def __init__(self, ime, geslo):
        self.ime = ime
        self.geslo = geslo

        self.seznam_testov = []
    
    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik        
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, seznam_testov = [])
            uporabnik.v_datoteko()
            return uporabnik

    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"


    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "seznam_testov": self.seznam_testov
        }

    def v_datoteko(self):
        with open(
            Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w"
        ) as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        seznam_testov = slovar["seznam_testov"]
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, mapa_testov)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None


# V besedilo manjkajoč podatek označimo z #. besedilo naj bo v obliki niza.
# formula naj bo v obliki niza, z enakimi spremenljivkami kot jih vpišemo v besedilo.


class Razlicica:
    def __init__(self, formula_resitve, besedilo = "", slovar_podatkov = None):
        # formula_resitve je oblike npr. "a + b + d / g"
        
        self.besedilo = besedilo
        self.resitev = self.izracunaj_resitev(formula_resitve)
        self.slovar_podatkov = slovar_podatkov # Oblike npr. {"#1" : 5, "#2" : 7, "#7" : 6}
    
    def izracunaj_resitev(self, formula):
        # funkcija v formulo v obliki niza zaporedoma vstavi podatke in nato izracuna vrednost izraza
        for spremenljivka in self.slovar_podatkov:
            formula = formula.replace(spremenljivka, str(self.slovar_podatkov[spremenljivka]))

        return eval(formula)


# x = Naloga("Besedilo # asdfasdf # asfdasdf", 5)
# for razlicica in x.seznam_razlicic:
#     print(razlicica.besedilo)   
#     print(razlicica.resitev)


class Naloga:  
    def __init__(self, besedilo = "", st_razlicic = 0, slovar_baz_podatkov = None, formula_resitve = ""):
        self.st_razlicic = st_razlicic # izberemo na zacetku koliko razlicic testov zelimo. vsaka naloga v enem testu ima ta atribut enak.
        
        self.besedilo = besedilo    # besedilo podamo v obliki niza z spremenljivkami v obliki npr. #1, #3, #7 ...
        self.st_podatkov = self.besedilo.count("#")
        
        self.formula = formula_resitve # formula je podana v obliki niza z enako poimenovanimi spremenljivkami kot v besedilu.

        self.slovar_baz_podatkov = slovar_baz_podatkov or dict() # naj bo oblike {#1 : N, #2: Z, ...} baze naj bi izbrali s klikom, kako omejim množice?
        self.seznam_razlicic = [] # v seznam potem shranimo razlicice naloge v obliki razreda

    def izberi_podatke(self):
    # funkcija iz slovarja podatkov z bazami izbere naključne podatke in jih sharni v nov slovar oblike {#1 : 4, #2 : 4,2 , ...}.

        slovar = {} 
        for x in self.slovar_baz_podatkov:
            slovar[x] = random.coice(self.slovar_baz_podatkov[x])
        return slovar  
        

    def vstavi_podatke_v_besedilo(self, podatki):
    # funkcija v besedilo vstavi konkretne podatke
    # podatki so slovar oblike npr. {"#1" : 5, "#2" : 7, "#7" : 6}

        novo_besedilo = self.besedilo

        for spremenljivka in podatki:
            novo_besedilo = novo_besedilo.replace(spremenljivka, str(podatki[spremenljivka]))
        
        return novo_besedilo


    def ustvari_razlicice(self):
    # funcija v self.seznam_razlicic shrani seznam razlicic naloge, razlicice so v obliki razreda (glej zgoraj)

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
