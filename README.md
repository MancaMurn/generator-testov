# Generator-Testov

Ta projekt je nastal kot projektna naloga pri predmetu Uvod v programiranje, na Fakulteti za matematiko in fiziko.

Generator testov je namenjen sestavljanju preprostejših računskih nalog. Program generira poljubno število različic, poljubno število nalog.

# Kako začeti
Na računaniku potrebujete python knjižnici bottle in docx.
Klonirajte repozitorij z git clone in zaženite spletni_vmesnik.py. Spletna stran se vam bo pokazala na naslovu http://127.0.0.1:8080/.

# Uporaba programa
V program se najprej prijavite oz. ragistrirati.

Če želite ustvariti nov test kliknete gumb **ustvari nov test**. Znajdete se na strani, kjer morate v prazna polja vpisati osnovne podatke o testu, ki ga želite       ustvariti. Pomembno je, da v **število nalog** in **število učencev** napišete številko.

S kilkom na gumb **potrdi** vas program preusmeri na stran, kjer zapišete navodila nalog. Spremenljive podatke v navodilu označite z **#** in zaporedno številko        podatka. 

Ko navodilo potrdite s klikom na gumb **potrdi**, se vam prikaže še okence, kjer za vsak podatek izberete bazo (**Z** za cela števila, **Q** za racionalna in **R** za realna števila) in zapišete formulo za izračun rešitev. V formuli uporabljajte iste spremenljivke kot v navodilu naloge.

Ko so vse naloge izpolnjene lahko pritinete na gumb **zaključi** in program vas preusmeri na stran, kjer si lahko naložite .docx datoteko za vsako različico            testa in datoteko z rešitvami vseh različic.

Dostopate lahko tudi do testov, ki ste jih že ustvarili s klikom na gumb **arhiv testov**. Tu so zbrani vsi končani in nedokončani test.
