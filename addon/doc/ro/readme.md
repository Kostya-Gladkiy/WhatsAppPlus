# WhatsAppPlus

* Autor: Kostya Gladkiy (Ucraina)
* [Canal Telegram](https://t.me/unigramPlus)

##Informații despre posibilitatea de a face donații către dezvoltator:

Dacă ai dorința și, mai ales, posibilitatea de a sprijini dezvoltatorul acestui add-on, o poți face folosind următoarele detalii:

* PayPal: gladkiy.kostya@gmail.com.
* Sistemul ucrainean de donații: https://unigramplus.diaka.ua/donate.
* Număr card: 5169360009004502 (Gladkiy Constantine).

A fost adăugat un număr mare de comenzi rapide de la tastatură pentru o muncă productivă și confortabilă în program, care pot fi găsite mai jos.

### Caracteristici generale ale add-on-ului

* Acum, câmpul de introducere a mesajului își va schimba numele atunci când răspunzi la un mesaj.
* Au fost adăugate etichete pentru unele elemente de program care sunt citite de cititorii de ecran.

## Lista de taste rapide:

* ALT+1 - Mută focalizarea pe lista de chat-uri.
* ALT+2 - Mută focalizarea pe ultimul mesaj dintr-un chat deschis.
* ALT+D - Mută focalizarea pe câmpul de editare. Dacă focalizarea se află deja în câmpul de editare, după apăsarea tastei rapide, se va muta în locul în care se afla înainte.
* ALT+T - Anunță numele și starea unui chat deschis.
* ALT+shift+C - Efectuează un apel vocal către un grup sau un contact sau alătură-te unui apel vocal în curs de desfășurare într-un grup.
* ALT+shift+V - Efectuează un apel video către un contact sau un grup.
* ALT+Shift+Y - Răspunde apelului.
* ALT+shift+N - Refuză un apel dacă te sună cineva, sau alătură-te unui apel dacă este în desfășurare.
* ALT+A - Pornește și oprește microfonul camerei.
* ALT+V - Pornește și oprește camera.
* ALT+O - Apasă butonul "Mai multe opțiuni".
* control+R - Înregistrează și trimite un mesaj vocal.
* control+D - Anulează mesajul vocal.
* control+shift+D - Pune pe pauză/reia înregistrarea mesajului vocal.
* ALT+delete - Șterge un mesaj sau un chat.
* control+Shift+P - Deschide profilul de chat curent.
* ALT+shift+A - Apasă butonul "Atașați un fișier".
* control+shift+E - Comută modul care elimină citirea numărului de utilizator atunci când se citesc mesajele utilizatorilor care nu se află în lista de contacte.
* ALT+S - Marchează mesajul cu stea.
* ALT+F - Redirecționează mesajul.
* ALT+R - Răspunde la mesaj.
* ALT+shift+R - Marchează un chat ca fiind citit.
* control+C - Copiază mesajul, dacă acesta conține text.
* ALT+C - Afișează textul mesajului într-o fereastră popup.
* NVDA+control+W - Deschide fereastra de setări WhatsAppPlus.
* ALT+3 - Deplasează focalizarea pe eticheta "mesaje necitite".
* control+N - Apasă butonul "Chat nou".
* control+shift+A - Apasă butonul "Atașează fișier".
* ALT+L: Activează citirea automată a mesajelor noi din chat-ul curent.
* control+S: Creșteți/diminuați viteza de redare a mesajelor vocale.
* ALT+P: Redați/opriți mesajul vocal.
* ALT+U: Anunță valoarea curentă a barei de progres. Atunci când este apăsat de două ori, activează/dezactivează sonorizarea automată a indicatorilor de performanță.
* control+spațiu: Treci la modul de selecție.
* ALT+backspace: Editează mesajul pe care ești focalizat.

##Istoricul modificărilor

### Versiunea 2.1.0 ###

* S-a rezolvat problema cu citirea statusului utilizatorului.
* A fost rezolvată o problemă în care nu era posibil să se răspundă la un apel și să se respingă un apel cu o comandă rapidă de la tastatură. Reține că prescurtările de la tastatură pentru a răspunde și a respinge un apel au fost modificate în NVDA+ALT+Y și NVDA+ALT+N.
* A fost corectată funcția care citește mesajele noi în chat-ul deschis.
* A fost rezolvată o problemă în care numărul de telefon era citit în loc de numele tău în mesajele trimise.
* A fost remediată o problemă la trimiterea mesajelor vocale folosind control+R.
* A fost adăugată compatibilitatea cu NVDA 2024.1.

### Versiunea 2.0.0 ###

* A fost Adăugată o comandă rapidă de la tastatură pentru editarea mesajelor. În mod implicit, această funcție este atribuită combinației ALT+backspace.
* Focalizarea pe un mesaj care conține un fișier va citi acum numele, tipul și dimensiunea fișierului.
* Acum funcția de citire automată a mesajelor noi în chat-ul deschis funcționează corect. Reține totuși că pentru o funcționare corectă trebuie să specifici numărul de telefon și numele tău în setările WhatsAppPlus.
* Acum, funcția de citire automată a activității în chat-urile deschise va funcționa mai stabil.
* ALT+D funcționează acum corect.
* A fost rezolvat conflictul unor funcții cu add-on-ul "BluetoothAudio".

### Versiunea 1.9.0 ###

* A fost adăugată o comandă rapidă de la tastatură care deschide o listă cu toate scurtăturile WhatsAppPlus. În mod implicit, această funcție este atribuită gestului ALT+H.
* A fost reparată o eroare prin care gesturile ALT+2 și ALT+3 nu funcționau.
* A fost rezolvată o eroare prin care era imposibil să activezi unele funcții din meniul contextual folosind gesturi.
* S-a remediat o problemă în care modificarea vitezei de redare a mesajelor vocale și întreruperea redării mesajelor vocale nu funcționa întotdeauna.
* A fost reparată o eroare în care, în chat-uri, atunci când te focalizai pe mesajele trimise, în loc de cuvântul "tu", cititorul de ecran anunța un număr personal. Pentru a evita acest lucru, trebuie să specifici numărul de telefon în setările WhatsAppPlus și, după aceea, add-on-ul nu îl va mai enunța în mesaje.
* A fost rezolvată o problemă în care WhatsAppPlus cerea actualizarea pe ecrane securizate. Pentru a evita ca acest lucru să se întâmple din nou, trebuie să faceți clic pe butonul "Use currently saved settings during sign-in and on secure screens (requires administrator privileges)" (Utilizați setările salvate în prezent în timpul conectării și pe ecrane securizate (necesită privilegii de administrator)" din setările generale NVDA.
* Gestul de acceptare a unui apel a fost schimbat în ALT+shift+Y, iar gestul de refuz al unui apel a fost schimbat în ALT+shift+N. Această modificare a fost făcută pentru a se asigura că aceste gesturi nu intră în conflict cu gesturile UnigramPlus.
* Gesturile de activare/dezactivare a microfonului și a camerei în timpul unui apel funcționează acum corect.
* A fost eliminat gestul de a seta reacția la mesaje, deoarece în cele mai recente versiuni de WhatsApp, reacțiile sunt disponibile direct din meniul contextual.

### Versiunea 1.8.0

* Suplimentul a fost testat pentru a asigura compatibilitatea cu NVDA-2023.
* A fost adăugată o comandă rapidă de la tastatură pentru selectarea mesajelor. Pentru a intra în modul de selecție, apăsați Ctrl+Spațiu, apoi utilizați Spațiu pentru a selecta următorul mesaj.
* A fost adăugată o nouă funcție pentru a anunța automat activitatea într-un chat deschis. În mod implicit, această funcție este activată prin apăsarea dublă a combinației ALT+T. Acest lucru îi ajută pe utilizatori să fie la curent cu mesajele noi și cu alte activități de chat.
* Funcția care anunță automat mesajele noi din chat a fost revizuită substanțial pentru o funcționare mai stabilă. Astfel, se asigură că utilizatorii sunt anunțați de mesajele noi cu acuratețe și fiabilitate.
* Au fost adăugate etichete la unele butoane neetichetate.

### Versiunea 1.7.0

* A fost adăugată o funcție care anunță automat bara de progres dacă ești focalizat pe un mesaj.
* A fost adăugată o comandă rapidă de la tastatură pentru a anunța valoarea barei de progres dacă focalizarea este pe un mesaj. În mod implicit, combinația de taste ALT+U este atribuită acestei funcții. Dacă această combinație este apăsată de două ori, funcția de anunțare automată a indicatorilor de performanță va fi activată.
* A fost rezolvată o problemă prin care nu se putea muta focalizarea în lista de chat.
* Au fost adăugate etichete la unele elemente.

###Versiunea 1.6.0

* A fost adăugată posibilitatea de a răspunde rapid membrilor grupului. Pentru a introduce un mesaj, este suficient să scrieți simbolul "@" în câmpul de introducere a mesajului, să folosiți săgețile în sus și în jos pentru a selecta persoana căreia doriți să-i răspundeți și apoi să apăsați tasta Enter.
* A fost adăugată posibilitatea de a insera rapid emoticoane. Pentru a face acest lucru, trebuie să scrieți două puncte și numele emoticoanelor pe care doriți să le găsiți în câmpul de introducere a mesajului. Ulterior, folosiți tastele săgeată stânga și dreapta pentru a găsi emoticoanele dorite și folosiți tasta Enter pentru a le insera în câmpul de introducere a mesajului.
* În setările WhatsAppPlus, a fost adăugată o opțiune pentru a activa redarea sunetelor la înregistrarea, întreruperea și trimiterea mesajelor vocale.
* A fost schimbată comanda rapidă de la tastatură pentru deschiderea profilului conversației curente la Control+Shift+P.
* A fost adăugată localizarea în limba nepaleză.
* Au fost reparate mai multe erori, inclusiv o problemă în care citirea automată a mesajelor noi dintr-o conversație deschisă nu funcționa pentru unii utilizatori.

###Versiunea 1.5.0

* A fost adăugată o comandă rapidă de la tastatură pentru a schimba viteza de redare a mesajului vocal. Gestul implicit este ctrl+s. Gestul va funcționa numai atunci când un mesaj vocal este redat într-o conversație deschisă.
* A fost adăugată o comandă rapidă de la tastatură pentru a pune pe pauză un mesaj vocal care se redă. Gestul implicit este alt+p. Funcția va funcționa numai atunci când un mesaj vocal este redat într-un chat deschis.
* Acum, enunțarea unui mesaj nou într-un chat deschis poate fi activată nu numai până la repornirea NVDA, ci și pentru totdeauna.

###Versiunea 1.4.0

* Am adaptat addonul la cea mai recentă versiune de WhatsApp.
* A fost adăugată funcția de anunțare automată a mesajelor noi în chat. În mod implicit, această funcție este activată prin apăsarea ALT+L. Funcția rămâne activă numai până când NVDA este repornit. Pot exista probleme de stabilitate dacă sunt prea multe mesaje noi.
* A fost adăugată localizarea în limba franceză.

###Versiunea 1.3.0

* Descrierea link-urilor atașate la mesaj va fi acum citită.
* Acum va fi anunțată durata mesajelor vocale.
* Acum poți deschide link-urile atașate la mesaje apăsând spațiu.
* Au fost adăugate etichete pentru unele elemente de interfață
* Am adaptat add-on-ul la cea mai recentă versiune de WhatsApp, astfel încât toate caracteristicile să funcționeze corect.
* Au fost corectate unele erori

###Versiunea 1.2.0

* Acum, când te focalizezi pe un mesaj scris ca răspuns la un alt mesaj, va fi enunțat mai întâi textul acelui mesaj și apoi textul mesajului la care a fost trimis.
* Numele și tipul fișierelor trimise în conversație vor fi acum enunțate.
* ALT+1 funcționează acum chiar și atunci când arhiva de chat sau secțiunea de mesaje selectate este deschisă.
* ALT + săgeată stânga ajută la închiderea arhivei de chat sau a listei de mesaje selectate, dacă acestea sunt deschise.
* Acum, apăsarea comenzii control+D, pe lângă anularea mesajelor vocale, anulează și răspunsul la mesaj.
* Informațiile despre imposibilitatea de a înregistra un mesaj vocal vor fi acum raportate atunci când câmpul de introducere a mesajului nu este gol. Acest lucru va rezolva o problemă în care apăsarea comenzii control+R trimitea un mesaj text în loc să înceapă înregistrarea unui mesaj vocal.
* Au fost etichetate unele elemente care nu aveau deja etichete.

###Versiunea 1.1.0

* A fost adăugată o comandă rapidă de la tastatură pentru a naviga la mesajele necitite. Deoarece această funcție depinde de limbă, ea poate fi configurată în setările WhatsAppPlus.
* A fost adăugată o comandă rapidă de la tastatură pentru apăsarea butonului "Chat nou".
* A fost adăugată o comandă rapidă de la tastatură pentru apăsarea butonului "Atașează fișier".
* Acum, atunci când înregistrezi un mesaj vocal, sintetizatorul nu va anunța numele butoanelor de control al înregistrării.
* A fost adăugată localizarea în limbile română, sârbă, croată, spaniolă și turcă.
* Au fost adăugate etichete pentru unele elemente care nu aveau etichete pentru cititorii de ecran.
* Acum, informațiile despre reacțiile la un mesaj vor fi anunțate atunci când te focalizezi pe un mesaj.
* Acum, la redarea propriilor mesaje vocale cu bara de spațiu, nu va mai apărea o fereastră pop-up.
* Am rezolvat bug-uri minore.