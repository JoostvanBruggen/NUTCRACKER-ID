# NUTCRACKER-ID

Experimenteel lokaal prototype voor vergelijking van lichte verenkenmerken en
voorstellen van kopuitsneden. Scores en kandidaatgroepen bewijzen geen identiteit.
Deze uitgave gebruikt NumPy en Pillow; YOLO is niet opgenomen.

## Algemeen hulpmiddel, geen vaste testomvang

Het beoogde programma ondersteunt lokale fotocollecties van verschillende omvang.
De bestaande 72 anonieme foto's van acht bekende Notenkrakers zijn uitsluitend
een gecontroleerde privétestset. Er is geen vaste eis van 72 foto's en geen
vooraf ingesteld aantal individuen. De identiteitssleutel blijft buiten de
automatische herkenning. Foto's kunnen bij onvoldoende bewijs ongegroepeerd blijven.

De huidige uitvoering accepteert een lokale PNG-map zonder vaste aantalsgrens,
maar vergelijkt nog via een volledige paarlus en gebruikt veel geheugen.
Grote collecties zijn dus een ontwikkeldoel, geen al aangetoonde capaciteit.
Website- en URL-invoer, efficiënte kandidaatselectie en verwisselbare onderdelen
worden later ontwikkeld. Openbare fototoegang geeft geen automatisch hergebruiksrecht.

Zie [de architectuur](docs/ARCHITECTUUR.md) voor de vijf gescheiden onderdelen,
de scheiding tussen huidige werking en toekomstig ontwerp, en de onafhankelijke
wetenschappelijke validatie.


Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
Licentie: AGPL-3.0-only. Zie [COPYING](COPYING) en
[COPYRIGHT-STATUS.md](COPYRIGHT-STATUS.md).

## Zoekfunctie en betrouwbaarheid — ontwerp

Het uiteindelijke programma moet met één zoekfoto vergelijkbare vogels in een
bestaande collectie vinden, kandidaten rangschikken en hun foto's, kenmerken
en beschikbare datums/tijden/locaties naast elkaar tonen. Nieuwe collectiebeelden
moeten later kunnen worden toegevoegd zonder alles opnieuw te verwerken.

De bestaande software heeft al technische paarscores, kandidaatgroepen en lokale
HTML-overzichten. Een echte één-fotozoekfunctie, blijvende index, interactieve
website en wetenschappelijk onderbouwde kansen bestaan nog niet.
De bestaande scores en groepsindelingen zijn bij deze ontwerpuitbreiding niet gewijzigd.

Pas na onafhankelijke kalibratie mogen geschatte identiteitskansen worden ingedeeld
in GROEN (95–100%: vrijwel zeker dezelfde vogel), ORANJE (80% tot onder 95%:
mogelijk dezelfde vogel) en GRIJS (onder 80%: onzeker).
Tot die tijd blijft het een technische overeenkomstscore, ook bij een hoge waarde.
Zonder onderbouwde kans wordt geen groene of oranje zekerheid toegekend.
De operationele 40 km/uur-controle komt als aparte toets met uitsluitingsreden;
ontbrekende gegevens zijn onbekend.

Zie [zoeken en betrouwbaarheid](docs/ZOEKEN_EN_BETROUWBAARHEID.md) voor het
gegevensmodel, de tijd-/locatiecontrole, het websiteontwerp en de huidige status.
Het [validatieplan](docs/VALIDATIEPLAN.md) scheidt herkenning van de privé-evaluator
en scheidt ontwikkeling, kalibratie en onafhankelijke eindtest.

## Installeren

Getest op Windows met Python 3.12.14, NumPy 2.3.5 en Pillow 12.3.0.
Andere Python-versies en besturingssystemen zijn niet als ondersteund getest.
Een gewone Python 3.12-installatie volstaat; Codex is geen vereiste.

Voer in de projectmap uit met je eigen Python 3.12:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe nutcracker_id.py --help
~~~

Een virtuele omgeving activeren of de PowerShell-uitvoeringspolicy wijzigen is
niet nodig. De installatie downloadt alleen de twee genoemde pakketten en hun
benodigde afhankelijkheden, geen modellen. Controleer hun officiële bronnen in
[docs/LICENTIES.md](docs/LICENTIES.md). Deze voorbereiding installeerde niets:
de tests gebruikten een bestaande omgeving. Een schone installatie is niet getest.

## Starten zonder foto's

~~~powershell
.\.venv\Scripts\python.exe nutcracker_id.py
.\.venv\Scripts\python.exe -B tests\test_synthetic.py
~~~

Zonder argumenten toont het programma alleen hulp en maakt het geen uitvoer.
De test maakt uitsluitend fictieve afbeeldingen in een tijdelijke map binnen
de projectmap en ruimt alleen die eigen testmap op. Er zijn geen voorbeeldfoto's
of onderzoeksgegevens meegeleverd.

## Eigen lokale afbeeldingen verwerken

Verwerking begint alleen met een expliciete invoermap. Gebruik PNG's waarvoor
je de benodigde gebruiksrechten hebt. Publicatierechten zijn alleen nodig als
je de beelden of de afgeleide rapporten daadwerkelijk openbaar wilt maken.

~~~powershell
.\.venv\Scripts\python.exe nutcracker_id.py --photos eigen_pngs --output .local-output\patronen
.\.venv\Scripts\python.exe nutcracker_id.py --crop-review --photos eigen_pngs --crop-output .local-output\kopcontrole
~~~

Beide rapporten heten index.html. De kopcontrole bevat ook kopieën van de
invoerbeelden zonder overgenomen beeldmetadata: behandel alle uitvoer als privé.
PNG-bestanden in de opgegeven map worden verwerkt, niet in onderliggende mappen.

De optionele PowerShell-startscripts staan in de hoofdmap. Ze gebruiken standaard
uitsluitend .venv\Scripts\python.exe naast de code en werken ook als de huidige
werkmap elders staat. Zonder argumenten tonen ze hulp:

~~~powershell
.\start_nutcracker_id.ps1
.\start_kopdetectie_review.ps1
.\start_nutcracker_id.ps1 -Photos eigen_pngs
.\start_kopdetectie_review.ps1 -Photos eigen_pngs
~~~

Als Windows een PowerShell-script blokkeert, gebruik dan de directe Python-opdrachten
hierboven; verander hiervoor geen beveiligingsinstellingen.

Relatieve invoer- en uitvoerpaden van deze startscripts worden ten opzichte van
de projectmap gelezen. Desgewenst kun je -PythonExecutable opgeven; er is geen
automatische keuze van een persoonlijke Codex-installatie.

## Grenzen en publicatie

Lees [de methode](docs/METHODE.md) en
[de technische controle](docs/TECHNISCHE_CONTROLE.md).
Tijden, locaties, reistijd en snavelpuntkenmerken worden nog niet gebruikt.
Een groep is uitsluitend een experimentele verzameling van vergelijkbare beelden.

Alleen de bestanden in PUBLICATIEBESTANDEN.txt horen bij deze uitgave.
Controleer die lijst en voer vlak voor publicatie uit:

~~~powershell
.\.venv\Scripts\python.exe -B scripts\controleer_publicatie.py
~~~

Deze controle weigert onverwachte bestanden, ook verborgen bestanden.
Ze vervangt geen beoordeling van rechten, inhoud en eventuele Git-geschiedenis.
De .gitignore is een extra hulpmiddel en geen beveiliging.

De publicatievoorbereiding is geen publicatie. Voor het eerste gebruik van
Ultralytics moet volgens de door de eigenaar opgegeven afspraak de volledige
toepasselijke broncode openbaar zijn. Alleen dit prototype openbaar maken dekt
geen toekomstige niet-gepubliceerde YOLO-integratie. Publiceer ook de toepasselijke
nieuwe code, scripts en configuratie uiterlijk bij het eerste gebruik.
Zie [docs/LICENTIES.md](docs/LICENTIES.md).
