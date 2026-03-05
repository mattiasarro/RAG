# Topoloogia (3D-modelleerimine)

- Topoloogia** tähendab 3D-modelleerimise valdkonnas viisi, kuidas tipud ja servad paiknevad, et moodustada hulknurkadest võre. Võre koosneb tippudest, neid ühendavatest servadest ja nende vahel olevatest tahkudest (ka hulknurgad või polügoonid), mida manipuleeritakse hulknurkse modelleerimise puhul.

3D-mudelite loomiseks kasutatakse tavaliselt kas kolme servaga tahke, ehk kolmnurki, või nelja servaga tahke, ehk nelinurki. Harvemini kasutatakse tahke, millel on rohkem kui neli serva, ehk ngoni.

3D-modelleerimise puhul määrab võre kvaliteet selle kasutatavuse. Kvaliteedi puhul peaks silmas pidama näiteks: tahkude sarnasust ruutudele, ehk minimaalseid moonutusi; võre servad peaksid järgima pinna vorme; peaks olema kasutatud võimalikult vähe tahke. Kõiki eelnevalt mainitud punkte on aga keeruline korraga rakendada, seega on sageli vajalik järeleandmisi teha kas geomeetria täpsuses või tiheduses. Kvaliteetne topoloogia on määrav faktor mudeli deformatsioonide, varjunduse ja renderdamise kiiruse osas.

    1. Ökonoomne topoloogia
Arvutusjõudluse maksimaalseks ärakasutamiseks peaks 3D-mudelitel olema tippe võimalikult vähe, aga nii palju kui vaja, et vajalik vorm saavutada. Kvaliteetne topoloogia on võre seadmine viisil, et saavutatakse piisav detailsusaste, kuid hoitakse see siiski võimalikult hõre. Eriti tähtis on kvaliteetne topoloogia animeeritud võre puhul, kus see võimaldab ka kvaliteetsemaid deformatsioone, ning tükeldatud pindade (ingl *Subdivision surface*) modelleerimisel. Kvaliteetse topoloogia loomiseks on täpseid instruktsioone keeruline luua, kuid on siiski mõned üldised juhtnöörid. Sageli käsitletakse topoloogia kontekstis servade sujuvuse ja servasilmuste mõisteid. Ehk, kvaliteetse topoloogia saavutamiseks peaksid üksteise järele asetatud servad paigutuma võimalikult sujuvalt ja saavutada tahetavat vormi võimalikult täpselt järgivalt. Servasilmuste puhul moodustavad servad suletud ringi, mis on paljude vormide puhul ka loomulik nähtus. Servasilmuste olemasolu võimaldab neid kiirelt valida, mis omakorda kiirendab UV-õmblusservade määramist. Peaks ka arvestama võre osade omavahelise tihedusega, näiteks kurvikamad pinnad tuleks katta tihedamalt kui lamedad pinnad.

Võimalikult optimaalsete mudelite ehitamisel on prioriteediks objekti siluett. Mudelite siluett on visuaalselt sageli kõige kiiremini märgatavam osa, sellel on mudeli arusaadavuse osas sageli kõige suurem mõju. Kandiline või ebamäärane objekti siluett mõjutab selle visuaalset ilmet tunduvalt rohkem kui mõni element selle objekti keskel. Samuti on võimalik mudelitele elemente luua kas tekstuuri või normaalikaardiga, ehk ilma lisa võret loomata, neid elemente pole aga silueti pealt näha. Eelneva tõttu pöörataksegi rohkem tähelepanu objektide siluettidele ja tehakse neid veidi detailsemateks kui objekti osi, mille siluetti kunagi näha ei ole. 

Kvaliteetsele topoloogiale omistatakse sageli veel järgmisi omadusi: 

- võre ei sisalda külgi, mis on üksteise peal,
- võres ei ole auke,
- võres on kõik pinnanormaalid ühte pidi,
- objektil pole külgi, mis paiknevad pinna sees ja mida pole näha,
- objektil pole üksikuid teistest eraldatud, ehk hõljuvaid tippe.

    1. Topoloogia haldamine
Iga võre kõige pisem nähtav element on tahk. Tahud võivad olla kolmnurgad, nelinurgad või ngonid. Ngonideks nimetatakse tahke, millel on rohkem kui neli serva ja tippu. Hoolimata sellest, et renderdamisel muudetakse kõik tahud kolmnurkadeks, tasub siiski eelistada kindla kuju ja paigutusega tahke. Kuna igat tahku on võimalik kolmnurkadeks jagada mitut moodi, mis omakorda võib mõjutada objekti siluetti, siis soovitatakse tahkude tipud hoida võimalikult ühel tasandil või jagada võre enne renderdamist või eksportimist käsitsi kolmnurkadeks. 

Võre loomisel peetakse parimaks tavaks eelistada nelinurkade kasutamist. Võre deformeerumisel ja tükeldatud pinna puhul käituvad nelinurgad ettearvatavamalt ja annavad kvaliteetsema tulemuse. Siiski ei peeta heaks tavaks muuta võret tihedamaks ainuüksi sellel põhjusel, et säilitada ainult nelinurkadest koosnev mudel, sellistel puhkudel kasutatakse ka kolmnurki, mis paigutatakse vähem tähtsatesse kohtadesse. 

Servasilmus on servadest moodustuv jada, kus silmus järgib iga nelja servalise ristumise puhul keskmist serva. Servasilmus lõpeb, kui jõuab mõne muu kui neljavalentse tipuni. Servasilmuse viimane serv võib, aga ei pea kohtuma selle silmuse esimese servaga. Ehk servasilmus jätkub nii kaua mööda neljavalentsete tippudega servi, kuni kohtab mõne muu valentsusega tippu. Korralikud servasilmused on kvaliteetse topoloogia üks põhilisemaid tunnuseid. Liikuva võre servad töötavad kui hinged, mille ümber küljed saavad painduda, seega on korralikud servasilmused just deformeeruva võre puhul eriti olulised, lubades sellel loomulikult väänduda, kokku tõmmata ja paisuda. 

Servasilmuste haldamiseks ja suunamiseks kasutatakse mitte neljavalentseid tippe, ehk tippe, millega ei ole ühendatud neli serva, tavaliselt kasutatakse kolme- või viievalentseid tippe. Tippe, mille valentsus ei ole neli, kutsutakse kas ebatavalisteks tippudeks või enam levinumalt poolustippudeks. Kuna poolus-tipud võivad tekitada võre varjundusse anomaaliaid, näiteks kühmukesi, siis tavaliselt pannakse nad kohtadesse, mis ei deformeeru, tasapindadele või kus võre peakski loomulikult kortsuma.

    1. Varjundus
Ngonid võivad renderdusel põhjustada veidrat varjundust, sest ka need jagatakse automaatselt kolmnurkadeks. Ainuke võimalus selle parandamiseks on topoloogiat muuta. Samuti võivad kolmnurgad ja ngonid tekitada mudeli varjunduses anomaaliaid, näiteks kühmud või lohud, mis nelinurkade kasutamisel ei tekiks.

    1. Deformatsioonid
Kvaliteetsele topoloogiale ja hästi paigutatud servasilmustele tuleks eriti suurt tähelepanu pöörata orgaaniliste mudelite puhul, mis ka deformeeruvad. Tipud ja servad peaksid paiknema kindlates kohtades, et võimaldada loomutruud võre paindumist, venimist ja kokkusurumist, kõige olulisemad on kohad, mis deformeeruvad olulisel määral, näiteks inimkeha mudeli puhul õlad, suunurgad, näpud ja küünarnukid. Tippude paigutus peaks toetama näiteks inimese mudeli puhul inimkeha loomulikku liikumist, liikumisulatust ja moonutusi. Deformatsioonide puhul peaks eriliselt vältima ngone. Orgaanilistes mudelites võib sageli eristada kumerusi ja kurve, mis on sageli mitte-geomeetriliste nurkade all, samuti näiteks näo puhul deformeerub nägu mööda neid samu jooni, mis peaks võre ehitades väljenduma ka topoloogias. Orgaanilistes mudelites esinevad kurvilised pinnad deformeeruvad sageli risti selle kurvi suunaga, seega peaks tahke ka nende tunnuste järgi joondama, et ka võre deformatsioonid oleksid võimalikult loomulikud. Seega orgaaniliste vormide järgimisel on eriti tähtis servasilmuste paigutus, mis on topoloogia poolest loomupäraselt nende orgaaniliste vomide sarnased. Servasilmused võivad võres omavahel ristuda, liituda või hargneda, oluline on aga, et need oleksid võimalikult pidevad ja sujuvad. 

    1. Tükeldatud pind
Tükaldatud pindade (ingl *subdivision surface*) puhul tükeldab tarkvara võre protseduuriliselt kõrgema tihedusega sujuvaks pinnaks. Tükeldatud pindu eelistatakse nii esteetilistel põhjustel kui ka nende omadusel tekitada sujuvaid pindu, mis on andmemahult väikesed. Üldiselt on sujuvad tükeldatud pinnad realistlikumad nii objekti silueti kui deformatsioonide poolest, lisaks toetavad need põhimõtteliselt ükskõik kui tihedat geomeetriat ilma anomaaliateta, mida võivad põhjustada madalama tihedusega võred. Võret, mille peal tükeldatud pindu rakendatakse, nimetatakse ka puuriks või kontrollvõreks. Tükeldatud pindade arvutamiseks kasutatakse eri algoritme, üks levinumaid on Catmull-Clarki meetod. Kontrollvõre punktid määravad ära tükeldatud pindade kuju ja sujuvuse, seega mõjutab tükeldatud pindu ka servasilmuste paiknemine. Teisisõnu: ka tükeldatud pindade puhul on kvaliteetne topoloogia väga oluline.

    1. Viited

Kategooria:Arvutigraafika
