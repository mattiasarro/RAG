# Juturobot

- Juturobot** on arvutiprogramm, mis simuleerib arukat suulist või kirjalikku vestlust ühe või mitme inimesega. Teema on enamasti vaba või vähemalt mitte piiratud ühe spetsiifilise teemaga ning sellise rakenduse eesmärk on pigem meelelahutuslik kui kasutajale usaldusväärse info andmine. Heal tasemel juturobot peaks inimeses tekitama mulje, et ta vestleb teise inimesega, mitte programmiga (vt Turingi test). Juturobotid on sageli ühendatud dialoogsüsteemidega, kus nende ülesandeks on aidata süsteemi kasutajat nõuannete, informatsiooni või muu seesugusega.

Mõned juturobotid kasutavad intelligentseid loomuliku keele töötluse süsteeme, kuid paljud neist otsivad sisendist vaid võtmesõnu ning annavad andmebaasist vastuseks kõige enam sobivad võtmesõnad või mustriga sarnase vastuse.

Esimene juturobot oli 1966. aastal loodud ELIZA ning järgmised tuntud robotid olid PARRY (1972) ja RACTER (1983). Samas pakkus Michael Loren Mauldin välja mõiste "ChatterBot" alles 1994. aastal. 2022. aasta lõpul tuli välja ChatGPT, mis kogus juba esimese kahe kuuga 30 miljonit kasutajat.

    1. Taust ja areng
1950. aastal ilmus Alan Turingi kuulus artikkel "Computing Machinery and Intelligence", kus on kirjas intellekti omamise kriteerium, mida praegu tuntakse Turingi testi nime all. Kriteeriumiks on arvutiprogrammi võime matkida inimest, vesteldes kirjaliku teksti abil reaalajas teises ruumis viibiva inimesega (kohtunikuga). Test loetakse edukalt läbituks, kui kohtunik ei suuda vahet teha sellel, kas ta vestleb teise inimese või arvutiprogrammiga. Turingi väljapakutud test ajendas saksa arvutiteadlast Joseph Weizenbaumi looma programmi ELIZA, mis on esimene tuntuks saanud (ja tõenäoliselt siiani kõige tuntum) programm, mida peetakse juturobotiks. Eri allikate andmetel on ELIZA programm kirjutatud ajavahemikus 1964–1966. ELIZA vestleb kasutajaga inglise keeles ning näiliselt üsna arukalt. Programm kasutab võtmesõnade andmebaasi, kus iga võtmesõna jaoks on antud:
# järk (täisarv),
# šabloon, millega võrrelda sisendit,
# väljundi ehk vastuse spetsifikatsioon.
See juturobot otsib niisiis kasutaja sisestatud tekstist võtmesõnu, mille šabloon sobiks lausega. Nii näiteks vastab programm igale sisendile, mis sisaldab sõna "ema", lausega "räägi mulle oma perest". autor on Kenneth M. Colby. Süsteem jäljendas paranoikut. Selleks sisaldas programm ligi 6000 mustrit, mida võrdles sisendiga, et anda sobiv vastus.. Veel üks inglise keelel põhinev klassikaline juturobot on Racter (1984), mis on sarnaselt ELIZA-ga loodud lihtsaid vahendeid kasutades. Racterit on kasutatud ka ingliskeelse raamatu "The Policeman's Beard is Half Constructed" koostamisel. 2017. aastal käivitas Iisraeli ettevõte SnatchBot vestlusrobotite loomise veebisaidi, millega saab nende sõnade kohaselt teha emotsioonianalüüsi funktsiooniga roboteid.

Sügisel 2022. aastal käivitas OpenAI oma ChatGPT vestlusroboti, mis põhineb ettevõtte GPT-3 mudelil. ChatGPT oli väljalaske hetkel üks kõige arenenumaid vestlusroboteid ja seda peetakse vestlusliku AI arendamisel oluliseks verstapostiks. Mudel on treenitud suurtes kogustes inimlike vestluste peal ja suudab seetõttu kasutajatega loomulikul ja inimlikul viisil suhelda. ChatGPT-d kasutatakse sageli klienditeeninduse eesmärgil ja see suudab vastata laiale valikule teemadest esitatud küsimustele. Ametlik ChatGPT oli sageli saadaval kõrge nõudluse tõttu, mis muutis populaarseks OpenAI ametlikku API-d kasutavad vestlusäpid.

    1. Võistlused
Juturobotite klassikaline eesmärk on Turingi testi läbimine, ent võistlustel võivad olla ka muud kindlad eesmärgid. Igal aastal toimub kaks väga mainekat võistlust. Üks neist käib Loebneri auhinna nimel. 1991. aastal algatas Hugh Loebner iga-aastase Loebneri auhinna võistluse, pakkudes 100 000 USA dollarit programmile, mis läbib Turingi testi. Aastatel 2000, 2001 ja 2004 on võitnud auhindu Richard Wallace'i kirjutatud programm A.L.I.C.E. Võistlusel Chatterbox Challenge on kaks juturobotit on võitjaks tulnud  kolmel aastal: Talk-Bot (2001, 2002, 2006) ja Bildgesmythe (2008, 2009, 2011). 2012. aastal sai alguse ülemaailmne inglise keelt kõnelevate juturobotite veebipõhine võistlus Robo Chat Challenge (CBC).
Nii Loebneri auhinna võistlusel kui ka Chatterbox Challenge'i võistlusel auhinnatud juturobot on näiteks Mitsuku.

    1. Väärkasutus
Kuritahtlikke juturoboteid tarvitatakse sageli selleks, et täita jututubasid rämpsposti  ja reklaamidega. Nende abil meelitatakse ka inimestelt välja isiklikku informatsiooni, näiteks pangakonto andmeid. Kuritahtlikke juturoboteid on leitud Yahoo! Messengeri, Windows Live Messengeri, AOL Instant Messengeri ning teiste kiirsõnumivahetuse protokollidest. Lisaks on andmeid selle kohta, et juturobotit kasutati kohtinguteenust vahendaval veebilehel.

    1. Popkultuur
Juturobotid avaldavad kasvavat mõju popkultuurile. Nii on näiteks Jack Heath avaldanud 2010. aastal romaani "Must nimekiri" (ingl. Hit List). Selles teoses on juturobot endast teadlikuks saanud (n-ö ellu ärganud), kasutab e-kirju, tekstsõnumeid, internetipanka jne.

    1. Kasutusvaldkonnad

        1. ## Avalikud teenused
Avalike teenuste pakkumisel aitavad juturobotid vähendada töötajate koormust ja tõsta klientide rahulolu. Näiteks Eestis on kavas kasutusele võtta büroktratt, mis on ainulaadne juturobotite platvorm. Bürokratt on inimese ehk kasutaja jaoks võimalus virtuaalsete assistentide abil kõnekeelse suhtlusega avalikku otsest teenust ja infoteenust kasutada Näiteks Soomes on kasutusel KANTA süsteem.

        1. ## Tervishoid
Juturobotite kasutamine tervishoius on muutunud oluliseks abivahendiks patsientide juhendamisel ja vaimse tervise toetamisel. Näiteks tehisintellektil põhinevad juturobotid suudavad pakkuda isikupärastatud tervisealaseid soovitusi ning vähendada haiglate koormust, vastates korduma kippuvatele küsimustele. Samuti on neid edukalt kasutatud vaimse tervise toetamiseks, pakkudes emotsionaalset tuge ja viies läbi esmaseid vaimse tervise hindamisi. 

        1. ## Kriisihaldus
Kriisiolukordades, nagu pagulaskriisid, võivad juturobotid pakkuda operatiivset tuge, aidates andmeid koguda, inimestega suhelda ning eluliselt tähtsat teavet edastada. Näiteks Ukraina sõja pagulaskriisis on juturobotid osutunud tõhusateks abivahenditeks, parandades kommunikatsiooni ja andmehaldust.

        1. ## Turism
Turismisektoris parandavad juturobotid teenuste kvaliteeti, pakkudes reisijatele kiiret abi ja teavet. turismiinfo jagamiseks sadamates ja lennujaamades. Samuti rahvahulkade juhtimise tõhustamiseks ja palverännakute korralduse täiustamiseks.

        1. ## Haridus
Haridusvaldkonnas aitavad juturobotid tugiteenuste pakkumisel ja teavitustegevust tõhustada ning administratiivset koormust. . Soomes on samuti katsetatud koolides juturoboteid, mis aitavad õpilastel personaalset õpet.

    1. Vaata ka
- Dialoogsüsteem
- Tehisintellekt
- Keeletehnoloogia

    1. Viited

    1. Välislingid

- Alicebot
- Chatbot Racter
- Eliza Chat bot
- Jabberwacky
- Aztekium Bot
- Kyle – A Unique Learning Artificial Intelligence (AI) Chatbot
- Mitsuku Chatbot
- RFC 439 – PARRY encounters the DOCTOR

Kategooria:Tarkvara
