# WhatsAppPlus

* Autor: Kostya Gladkiy (Ukrajina)
* [Telegram kanal](https://t.me/unigramPlus)

##Informacije o mogućnosti doniranja programeru:

Ako imate želju, i što je najvažnije priliku, podržati programera ovog dodatka, možete to učiniti pomoću sljedećih podataka:

* PayPal: gladkiy.kostya@gmail.com.
* Ukrajinski sustav donacija: https://unigramplus.diaka.ua/donate.
* Broj kartice: 5169360009004502 (Gladkiy Constantine).

Dodan veliki broj tipkovničkih prečaca za produktivan i ugodan rad u programu, koji se mogu pronaći u nastavku.

### Opće značajke dodatka:

* Sada će polje za unos poruke promijeniti naziv kada odgovaramo na poruku.
* Dodane oznake za neke elemente programa koje čitaju čitači zaslona.

## Popis prečaca:

* Alt+1: Premješta fokus na popis razgovora.
* Alt+2: Premješta fokus na posljednju poruku u otvorenom razgovoru.
* Alt+D: Premješta fokus na polje za uređivanje. Ako je fokus već u polju za uređivanje, tada će se nakon pritiska tipke prečaca pomaknuti na mjesto gdje je bio prije.
* Alt+T: Najavljuje naziv i status otvorenog razgovora.
* Alt+Shift+C: Upućuje glasovni poziv grupi ili kontaktu ili se pridružite glasovnom pozivu koji je u tijeku u grupi.
* Alt+Shift+V: Upućuje videopoziv kontaktu ili grupi.
* Alt+Shift+Y: Prihvaća poziv.
* Alt+Shift+N: Pritišće gumb "Odbij poziv" ako postoji dolazni poziv ili gumb "Završi poziv" ako je poziv u tijeku.
* Alt+A: Uključuje ili isključuje mikrofon.
* Alt+V: Uključuje i isključuje kameru.
* Alt+O: Pritišće gumb "Više opcija".
* Control+R: Snimanje i slanje glasovne poruke.
* Control+D: Odbacuje glasovnu poruku.
* Control+Shift+D: Pauziranje/nastavljanje snimanja glasovne poruke.
* Alt+Delete: Briše poruku ili razgovor.
* Control+Shift+P: Otvara profil trenutnog razgovora.
* Control+Shift+E: Uključuje i isključuje način rada koji uklanja čitanje korisničkog broja prilikom čitanja poruka kontakata koji nisu na popisu kontakata.
* Alt+S: Označava poruku zvjezdicom.
* Alt+F: Prosljeđuje poruku.
* Alt+R: Odgovara na poruku.
* Alt+Shift+R: Označava razgovor kao pročitan.
* Control+C: Kopira poruku ako sadrži tekst.
* Alt+C: Prikazuje tekst poruke u skočnom prozoru.
* NVDA+Control+W: Otvara prozor postavki WhatsAppPlusa.
* Alt+3: Premješta fokus na oznaku "nepročitane poruke"
* Control+Shift+A: Pritišće gumb "Priloži".
* Alt+L: Omogućava automatsko čitanje novih poruka u trenutnom razgovoru.
* Control+S: Povećava/smanjuje reprodukciju glasovnih poruka.
* Alt+P: Reproducira/pauzira glasovnu poruku koja se trenutno reproducira.
* Alt+U: Najavljuje trenutnu vrijednost trake napretka. Kada se dvaput pritisne, uključuje/isključuje automatsko oglašavanje indikatora performansi.
* Control+Razmaknica: Prebacuje na način odabira.

## Povijest promjena

### Verzija 1.9.0

* Dodan je tipkovnički prečac koji otvara popis svih tipkovničkih prečaca WhatsAppPlus. Prema zadanim postavkama, ova je funkcija dodijeljena gesti Alt+H.
* Ispravljena je greška u kojoj geste Alt+2 i Alt+3 nisu radile.
* Ispravljena je greška zbog koje je bilo nemoguće aktivirati neke funkcije iz kontekstnog izbornika pomoću geste.
* Riješen je problem pri kojem funkcija promjene brzine reprodukcije glasovne poruke i pauziranje reprodukcije glasovne poruke nisu uvijek funkcionirale.
* Ispravljena je greška gdje je u razgovorima kada se fokusirate na vaše poslane poruke, umjesto riječi "vi", čitač zaslona izgovarao osobni broj. Kako biste to izbjegli, potrebno je navesti broj telefona u postavkama WhatsAppPlusa i nakon toga ga dodatak neće javljati na vašim porukama.
* Riješen je problem zbog kojeg je WhatsAppPlus tražio ažuriranje na sigurnim zaslonima. Kako biste spriječili da se ovo više dogodi, trebate kliknuti na gumb "Koristi trenutačno spremljene postavke na zaslonu za prijavu te na sigurnim zaslonima (zahtijeva administratorska prava)" u općim postavkama NVDA-a.
* Gesta za prihvaćanje poziva promijenjena je u Alt+Shift+Y, a gesta za odbijanje poziva promijenjena je u Alt+Shift+N. Time se osigurava da te geste nisu u sukobu s UnigramPlus gestama.
* Geste za uključivanje/isključivanje mikrofona i kamere tijekom poziva sada rade ispravno.
* Uklonjena je gesta za reagiranje na poruke, budući da su u najnovijim verzijama WhatsAppa reakcije dostupne izravno iz kontekstnog izbornika.

### Verzija 1.8.0

* Dodatak je testiran kako bi se osigurala kompatibilnost s NVDA 2023.
* Dodan je tipkovnički prečac za odabir poruka. Za ulazak u način odabira pritisnite Control+Razmaknica, a zatim koristite Razmaknicu za odabir sljedeće poruke.
* Dodana je nova funkcija za automatsko najavljivanje aktivnosti otvorenog razgovora. Prema zadanim postavkama, ova je značajka omogućena dvostrukim pritiskom kombinacije Alt+T. To pomaže korisnicima da ostanu u tijeku s novim porukama i drugim aktivnostima razgovora.
* Funkcija koja automatski najavljuje nove poruke u razgovoru znatno je revidirana radi stabilnijeg rada. Ovo osigurava da su korisnici točno i pouzdano upozoreni na nove poruke.
* Dodane su oznake nekim neoznačenim gumbima.

### Verzija 1.7.0

* Dodana je funkcija koja automatski najavljuje traku napretka ako je fokus na poruci.
* Dodan je tipkovnički prečac za prijavljivanje vrijednosti trake napretka ako je fokus na poruci. Prema zadanim postavkama ovoj funkciji dodijeljena je kombinacija tipki Alt+U. Ako ovu kombinaciju pritisnete dvaput, aktivirat će se funkcija automatskog najavljivanja indikatora performansi.
* Riješen je problem zbog kojeg se fokus nije mogao premjestiti na popis razgovora.
* Dodane su oznake nekim elementima.

###Verzija 1.6.0

* Dodana je mogućnost brzog odgovaranja članovima grupe. Za unos poruke dovoljno je u polju za unos poruke napisati simbol "@", strelicama gore i dolje odabrati kome želite odgovoriti, a zatim pritisnuti tipku Enter.
* Dodana je mogućnost brzog umetanja emotikona. Da biste to učinili, morate u polju za unos poruke napisati dvotočku i naziv emotikona kojeg želite pronaći. Kasnije pomoću tipki sa strelicama lijevo i desno pronađite željeni emotikon i pomoću tipke Enter ga umetnite u polje za unos poruke.
* U postavkama WhatsAppPlusa dodana je opcija za omogućavanje reprodukcije zvukova prilikom snimanja, slanja i pauziranja glasovnih poruka.
* Promijenjen je tipkovnički prečac za otvaranje profila trenutnog razgovora u Control+Shift+P.
* Dodana je nepalska lokalizacija.
* Ispravljeno je nekoliko grešaka, uključujući problem kada automatsko čitanje novih poruka u otvorenom razgovoru nije radilo za neke korisnike.

###Verzija 1.5.0

* Dodan je tipkovnički prečac za promjenu brzine reprodukcije glasovne poruke. Zadana gesta je Control+S. Gesta će raditi samo kada se glasovna poruka reproducira u otvorenom razgovoru.
* Dodan je tipkovnički prečac za pauziranje glasovne poruke koja se reproducira. Zadana gesta je Alt+P. Funkcija će raditi samo kada se glasovna poruka reproducira u otvorenom razgovoru.
* Sada se najava novih poruka u otvorenom razgovoru može omogućiti ne samo dok se NVDA ponovno ne pokrene, već i zauvijek.

###Verzija 1.4.0

* Prilagođen najnovijoj verziji WhatsAppa.
* Dodana je funkcija automatske najave novih poruka u razgovoru. Prema zadanim postavkama, ova se funkcija aktivira pritiskom na Alt+L. Značajka ostaje aktivna samo dok se NVDA ponovno ne pokrene. Može doći do problema sa stabilnošću ako ima previše novih poruka.
* Dodana je francuska lokalizacija.

###Verzija 1.3.0

* Sada će se pročitati opis poveznica priloženih poruci.
* Sada će biti najavljeno trajanje glasovnih poruka.
* Sada možete otvoriti poveznice priložene porukama pomoću razmaknice
* Dodane su oznake za neke elemente sučelja
* Prilagođen najnovijoj verziji WhatsAppa tako da sve funkcije rade ispravno.
* Ispravljene su neke greške.

###Verzija 1.2.0

* Sada, kada se fokusirate na poruku napisanu kao odgovor na drugu poruku, prvo će se izgovoriti tekst te poruke, a zatim tekst poruke na koju je poslana.
* Naziv i vrsta datoteka poslanih u razgovoru sada će se izgovoriti.
* Alt+1 sada radi čak i kada je otvorena arhiva razgovora ili odjeljak odabranih poruka.
* Alt+Strelica lijevo pomaže zatvoriti arhivu razgovora ili popis odabranih poruka ako su otvoreni.
* Sada pritiskom na Control+D, osim poništavanja glasovnih poruka, poništava se i odgovor na poruku.
* Informacije o nemogućnosti snimanja glasovne poruke sada će se prikazivati kada polje za unos poruke nije prazno. Ovo će riješiti problem gdje bi se pritiskom na Control+R poslala tekstualna poruka umjesto pokretanja snimanja glasovne poruke.
* Označene su neke stavke koje već nisu imale oznake.

###Verzija 1.1.0

* Dodan je tipkovnički prečac za navigaciju do nepročitanih poruka. Budući da ova značajka ovisi o jeziku, ova se značajka može konfigurirati u postavkama WhatsAppPlusa.
* Dodan je tipkovnički prečac za pritiskanje gumba "Novi razgovor".
* Dodan je tipkovnički prečac za pritiskanje gumba "Priloži".
* Sada, prilikom snimanja glasovne poruke, govorna sinteza neće objaviti nazive tipki za kontrolu snimanja.
* Dodana je arapska, talijanska, rumunjska, srpska, hrvatska, španjolska i turska lokalizacija.
* Dodane su oznake za neke elemente koji nisu imali oznake čitača zaslona.
* Sada će informacije o reakcijama na poruku biti objavljene kada se fokusirate na poruku.
* Sada kada reproducirate vlastite glasovne poruke pomoću razmaknice, skočni prozor se neće pojaviti.
* Ispravljene su manje pogreške.
