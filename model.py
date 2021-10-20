import random
import json
import hashlib
from fractions import Fraction

class Uporabnik:
    def __init__(self, ime, geslo, seznam_testov=None):
        self.uporabnisko_ime = ime
        self.zasifrirano_geslo = geslo

        self.seznam_testov = seznam_testov or []


    def v_slovar(self):
        testi_v_slovarju = [test.v_slovar() for test in self.seznam_testov]

        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "seznam_testov": testi_v_slovarju
        }

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        
        seznam_testov = []
        for test_v_slovarju in slovar["seznam_testov"]:
            seznam_testov.append(Test.iz_slovarja(test_v_slovarju))

        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, seznam_testov)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)

    def v_datoteko(self):
        #funkcija odpre datoteko uporabnika in vanjo zapise uporabbnikove atribute v slovarju
        with open(
            Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w"
        ) as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=True, indent=4)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

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

    def nov_test(self, test):
        self.seznam_testov.append(test)
        index_testa = len(self.seznam_testov)
        return index_testa - 1




class Razlicica:
    def __init__(self, formula, besedilo = "", slovar_podatkov = None):
        
        self.besedilo = besedilo
        self.slovar_podatkov = slovar_podatkov

        if type(formula) is str:
            self.resitev = self.izracunaj_resitev(formula) 
        else:
            self.resitev = formula

    
    def v_slovar(self):
        return {
            "besedilo" : self.besedilo,
            "resitev" : self.resitev
        }

    @staticmethod
    def iz_slovarja(slovar):
        besedilo = slovar["besedilo"]
        resitev = slovar["resitev"]

        razlicica = Razlicica(resitev, besedilo)
        return razlicica

    def izracunaj_resitev(self, formula):
        # funkcija v formulo v obliki niza zaporedoma vstavi podatke in nato izracuna vrednost izraza

        for spremenljivka in self.slovar_podatkov:
            formula = formula.replace(spremenljivka, str(self.slovar_podatkov[spremenljivka]))
        return round(eval(formula), 3)




class Naloga:  
    def __init__(self, besedilo = "", st_razlicic = 0, slovar_baz_podatkov = None, formula_resitve = ""):
        self.st_razlicic = st_razlicic
        self.besedilo = besedilo
        self.st_podatkov = self.besedilo.count("#")
        self.formula = formula_resitve

        self.slovar_baz_podatkov = slovar_baz_podatkov or dict()
        self.seznam_razlicic = [] 

        if self.besedilo == "" or self.slovar_baz_podatkov == dict() or self.formula == "":
            self.stanje = "NN"
        else:
            self.stanje = "KN"

    def v_slovar(self):
        seznam_razlicic_v_slovarju = [razlicica.v_slovar() for razlicica in self.seznam_razlicic]
        return {
            "st_razlicic" : self.st_razlicic,
            "besedilo" : self.besedilo,
            "formula_resitve" : self.formula,
            "slovar_baz_podatkov" : self.slovar_baz_podatkov,
            "seznam_razlicic" : seznam_razlicic_v_slovarju,
            "stanje" : self.stanje
        }

    @staticmethod
    def iz_slovarja(slovar):
        besedilo = slovar["besedilo"]
        formula_resitve = slovar["formula_resitve"]
        slovar_baz_podatkov = slovar["slovar_baz_podatkov"]
        st_razlicic = slovar["st_razlicic"]
        seznam_razlicic = slovar["seznam_razlicic"]  

        naloga = Naloga(besedilo, st_razlicic, slovar_baz_podatkov, formula_resitve)
        naloga.seznam_razlicic = [Razlicica.iz_slovarja(razlicica) for razlicica in seznam_razlicic]

        return naloga
            

    def spremeni_besedilo(self, novo_besedilo):
        self.besedilo = novo_besedilo
        self.st_podatkov = self.besedilo.count("#")
    
    @staticmethod
    def preveri_besedilo(besedilo):
        st_podatkov = besedilo.count("#")
        for i in range(st_podatkov):
            stevec = i + 1
            index = besedilo.index("#")
            if besedilo[index + 1] != str(stevec):
                return False
            else:
                besedilo = besedilo[(index + 1):]
        return True

    def spremeni_formulo(self, formula):
        self.formula = formula
    
    def spremeni_slovar_baz(self, slovar):
        self.slovar_baz_podatkov = slovar

    def spremeni_stanje(self, stanje):
        self.stanje = stanje

    def izberi_podatke(self):
    # funkcija iz slovarja podatkov z bazami {#1 : (R, 0, 10), #2 : (Q, 3, 10)} izbere naključne podatke in jih sharni v nov slovar oblike {#1 : 4, #2 : 4.2 , ...}.

        slovar = {}
        for podatek in self.slovar_baz_podatkov:
            mnozica_izbire = self.slovar_baz_podatkov[podatek] # nabor

            if mnozica_izbire[0] == "Z":
                    y = random.randint(int(mnozica_izbire[1]), int(mnozica_izbire[2]))
                    while y == 0: # zelo majhna verjetnost, da gre v neskončnost
                        y = random.randint(int(mnozica_izbire[1]), int(mnozica_izbire[2]))

            elif mnozica_izbire[0] == "Q":
                stevec = random.randint(int(mnozica_izbire[1]), int(mnozica_izbire[2]))
                while stevec == 0: # zelo majhna verjetnost, da gre v neskončnost
                    stevec = random.randint(int(mnozica_izbire[1]), int(mnozica_izbire[2]))
                imenovalec = random.randint(int(mnozica_izbire[1]), int(mnozica_izbire[2]))
                while imenovalec == 0:
                    imenovalec = random.randint(int(mnozica_izbire[1]), int(mnozica_izbire[2]))
                y = Fraction(stevec, imenovalec)

            elif mnozica_izbire[0] == "R":
                y = round(random.uniform(int(mnozica_izbire[1]), int(mnozica_izbire[2])), 3)
                while y == 0: #itak je skor nemogoče, ampak ok
                    y = round(random.uniform(int(mnozica_izbire[1]), int(mnozica_izbire[2])), 3)

            slovar[podatek] = y
        return slovar  
        

    def vstavi_podatke_v_besedilo(self, podatki):
    # funkcija v besedilo vstavi konkretne podatke, podatki so slovar oblike npr. {"#1" : 5, "#2" : 7, "#7" : 6}

        novo_besedilo = self.besedilo
        for spremenljivka in podatki:
            novo_besedilo = novo_besedilo.replace(spremenljivka, str(podatki[spremenljivka]))
        
        return novo_besedilo


    def ustvari_razlicice(self):
    # funcija v self.seznam_razlicic shrani seznam razlicic naloge, razlicice so v obliki razreda (glej zgoraj)

        for _ in range(self.st_razlicic):
            slovar_podatkov = self.izberi_podatke()
            besedilo = self.vstavi_podatke_v_besedilo(slovar_podatkov)

            razlicica = Razlicica(self.formula, besedilo, slovar_podatkov)
            self.seznam_razlicic.append(razlicica)




class Test:
    def __init__(self, ucitelj, predmet, letnik, st_razlicic, st_nalog, stanje = None):
        self.predmet = predmet
        self.letnik = letnik
        self.ucitelj = ucitelj

        self.st_nalog = st_nalog        
        self.st_razlicic = st_razlicic
    
        self.glava = self.ustvari_glavo_testa()
        self.slovar_nalog = {i : Naloga(st_razlicic=st_razlicic) for i in range(st_nalog)}    

        if stanje:
            self.stanje = stanje
        else:
            self.stanje = "NT"


    def v_slovar(self):
        slovar_nalog_v_slovarju =  {i : self.slovar_nalog[i].v_slovar() for i in range(self.st_nalog)}
        return {
            "predmet" : self.predmet,
            "letnik" : self.letnik,
            "ucitelj" : self.ucitelj,
            "st_razlicic" : self.st_razlicic,
            "st_nalog" : self.st_nalog,
            "slovar_nalog" : slovar_nalog_v_slovarju,
            "stanje" : self.stanje
        }

    @staticmethod
    def iz_slovarja(slovar):
        predmet = slovar["predmet"]
        letnik = slovar["letnik"]
        ucitelj = slovar["ucitelj"]
        st_razlicic = slovar["st_razlicic"]
        st_nalog = slovar["st_nalog"]
        slovar_nalog = slovar["slovar_nalog"]
        stanje = slovar["stanje"]
        
        test = Test(ucitelj, predmet, letnik, st_razlicic, st_nalog, stanje)
        test.slovar_nalog = {int(i) : Naloga.iz_slovarja(slovar_nalog[i]) for i in slovar_nalog}
        return test

    def ustvari_glavo_testa(self):
        return f"""{self.predmet}, {self.letnik}"""

    def posodobi_stanje(self):
        self.stanje = "KT"
        for i in self.slovar_nalog:
            naloga = self.slovar_nalog[i]
            if naloga.stanje == "NN":
                self.stanje = "NT"