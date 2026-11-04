# Technische eindcontrole — 2 november 2026

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
SPDX-License-Identifier: AGPL-3.0-only

## Uitkomst

Deze map is voorbereid voor publicatie van het huidige experimentele prototype.
Er is niets gepubliceerd en geen repository, commit of push gemaakt.
YOLO en modellen zijn niet geïnstalleerd of gedownload.
De afzonderlijke toestemming voor publicatie ontbreekt nog.

## Uitgangspunt en wijzigingen

Uitgangspunt is de bestaande codeversie uit publicatie_voorbereiding. Deze
bevatte geen vaste kwaliteitslabels van onderzoeksfoto's. Alleen de nieuwe
publicatiemap is aangepast; de bestaande bronbestanden zijn behouden.

- Copyrightplaceholder vervangen door de bevestigde copyrightvermelding.
- Ontbrekende copyrightverwijzing ingevuld met een openbare mededeling.
  De ondertekende verklaring is niet gelezen en blijft privé.
- Onjuiste vaste vermelding van 72 beelden verwijderd.
- Geen verwerking zonder expliciete invoermap. Zonder argumenten alleen hulp.
- Ontbrekende, lege of ongeldige PNG-invoer afgewezen vóór uitvoer wordt gemaakt.
- Uitvoer binnen de invoermap wordt geweigerd.
- Startscripts werken met paden ten opzichte van hun eigen projectmap.
  Geen persoonlijke Codex-runtimepaden in de uitgave.
- Beide rapporten heten index.html.
- Koprapport heeft eigen metadata-arme invoerkopieën en lokale beeldverwijzingen.
  Bestandsnamen met spaties, # en % zijn getest.
- Kopieën dragen geen oorspronkelijke tekstmetadata of EXIF over.
  Namen en zichtbare inhoud kunnen nog privégegevens bevatten: uitvoer blijft privé.
- Elke combinatie van groepsleden moet aan de bestaande paarsgewijze drempels
  voldoen; de fout bij uitbreiding met een losse foto is hersteld.
- Zoekgebied voor oogcontrasten blijft binnen de randen van het beeld.
- Een exacte bestandenlijst en SHA-256-controle zijn toegevoegd.

## Uitgevoerde tests

Bestaande omgeving: Windows, Python 3.12.14, NumPy 2.3.5 en Pillow 12.3.0.
Deze versies zijn vastgelegd in requirements.txt. Er is niets geïnstalleerd.

De uiteindelijke unittest-run bevat 13 tests: 12 geslaagd en 1 overgeslagen.
De overgeslagen test probeert de startscripts vanuit een nieuw PowerShell-proces
te starten. Het lokale uitvoeringsbeleid blokkeert dat. De test meldt deze
beperking expliciet; het beleid is niet gewijzigd.

Daarnaast zijn beide startscripts wél getest vanuit de bestaande uitvoersessie,
met een werkmap buiten de publicatiemap en expliciete relatieve in- en uitvoer.
Beide verwerkten twee zelfgemaakte geometrische PNG's en schreven hun JSON en
index.html. Dat bewijst niet dat elk Windows-beleid PowerShell-scripts toestaat.
Gebruik bij blokkade de directe Python-opdrachten uit README.md.

De overige tests controleren:
- Hulpstart en starten zonder afbeeldingen, zonder uitvoerbestanden.
- Afwijzing van ontbrekende/lege/ongeldige invoer en onveilige uitvoerlocatie.
- Beide Python-verwerkingsmodi met uitsluitend geometrische testbeelden.
- Ongewijzigde synthetische invoerbestanden.
- Zelfstandige lokale rapportlinks, inclusief bijzondere tekens in namen.
- Geen overgenomen fotograaftekst/EXIF in koprapport-kopieën.
- Onbekende koplocatie bij een te klein beeld.
- Een groep mag geen onvoldoende ondersteund onderling paar bevatten.
- Voldoende ondersteunde paren kunnen wel een groep vormen.

Alle tijdelijke testbeelden en resultaten zijn uitsluitend voor deze controle
aangemaakt en daarna opgeruimd. Geen onderzoeksfoto is door de software verwerkt.
Alle Python-bronbestanden zijn op syntax gecontroleerd; beide startscripts
hebben nul PowerShell-syntaxfouten.

## Privacy en volledigheid

De exacte openbare bestanden staan in PUBLICATIEBESTANDEN.txt.
De definitieve publicatiecontrole vergelijkt deze lijst met alle aanwezige
bestanden, inclusief verborgen bestanden, en verifieert SHA256SUMS.
Onderzoeksbeelden, sleutels, ondertekende verklaringen, resultaten, lokale
omgevingen, computerpaden en modelbestanden horen niet bij deze uitgave.
De licentietekst en noodzakelijke eigen broncode en scripts zijn opgenomen.
Afhankelijkheden worden via requirements.txt betrokken, niet meegeleverd.

De bestaande onderzoeksbestandsnamen zijn geen onderdeel van de openbare code.
Een controle op bekende privésignalen blijft een hulpmiddel, geen bewijs dat
een toekomstige toevoeging veilig is. Elke wijziging vraagt een nieuwe beoordeling
en nieuwe hashes. Het SHA256SUMS-bestand is een controlelijst, geen digitale handtekening.

## Beperkingen

Geen schone installatie uitgevoerd; andere Python-versies en besturingssystemen
zijn niet getest. Pakketversies zijn gepind, installatiebestanden niet met hashes
vergrendeld. Er is geen volledige beveiligingsaudit van de afhankelijkheden gedaan.
HTML-verwijzingen zijn technisch gecontroleerd; de visuele rapportopmaak is
niet als afzonderlijke browsercontrole gevalideerd.

De testbeelden leverden geen bewijs van herkenningsnauwkeurigheid. Deze software
is geen gevalideerd individueel herkenningssysteem. Tijden, locaties, reistijd
en snavelpuntkenmerken zijn nog niet geïmplementeerd. De handleiding noemt dit
expliciet. Er is nog geen YOLO-integratie.

## Voor eerste YOLO-gebruik

Volgens de door de eigenaar opgegeven schriftelijke afspraak moet de volledige
toepasselijke code vóór of uiterlijk bij het eerste gebruik openbaar zijn.
Deze map is alleen lokaal voorbereid. Na afzonderlijke publicatietoestemming
moet de code werkelijk openbaar en bereikbaar worden gemaakt.
Ook nieuwe toepasselijke integratiecode, scripts en configuratie moeten uiterlijk
bij hun eerste gebruik beschikbaar zijn. Alleen een oude versie publiceren is
daarvoor onvoldoende. Daarna is een afzonderlijke installatie- en testopdracht nodig.


## Aanvulling: algemene collecties en architectuur

De architectuur en documentatie zijn verduidelijkt: de bestaande gecontroleerde
privétestset bepaalt geen foto- of groepsaantal in het algemene programma.
De actuele publicatiecode bevat geen vaste eis van precies 72 foto's en geen
vooraf ingesteld aantal individuen. De code is bij deze documentatieaanpassing
ongewijzigd gebleven. De oorspronkelijke privétestset blijft apart behouden.

Het nieuwe ARCHITECTUUR.md beschrijft vijf gescheiden onderdelen, toekomstige
schaalbare kandidaatselectie, lokale en latere toegestane webinvoer en onafhankelijke
validatie zonder sleutel in de herkenningsroute. De volledige paarlus en het
geheugengebruik van het huidige prototype zijn expliciet als beperking benoemd.

Voor deze aanvulling zijn uitsluitend syntax, documentverwijzingen, code-integriteit,
de exacte openbare bestandenlijst en de publicatiecontrole gecontroleerd.
Er is geen nieuwe herkenning, clustering of beeldtest uitgevoerd.
De eerder beschreven synthetische resultaten zijn eerdere controles, geen nieuwe run.
De bestandenlijst en hashes zijn bijgewerkt voor het nieuwe architectuurdocument.


## Ontwerpuitbreiding: één-fotozoekfunctie en betrouwbaarheidsklassen

Toegevoegd: ZOEKEN_EN_BETROUWBAARHEID.md en VALIDATIEPLAN.md.
README, architectuur en methode verwijzen nu naar de zoekroute, gescheiden
score-/kansopslag, drie voorwaardelijke kansklassen, tijdzones en de operationele
40 km/uur-toets, het websiteontwerp en onafhankelijke validatie.

De bestaande code is alleen gelezen. Er is geen score, drempel of groepsindeling
veranderd en geen herkenning, clustering of beeldtest uitgevoerd.
De identiteitssleutel is niet geopend. De bestaande synthetische testresultaten
hierboven blijven eerdere controles en zijn niet opnieuw gemeten.

Voor deze ontwerpwijziging zijn de ongewijzigde broncode, scripts en tests met
hashes gecontroleerd, alle Python-bestanden op syntax gecontroleerd en de lokale
documentverwijzingen nagekeken. De openbare bestandenlijst, .gitignore en
SHA256SUMS zijn voor de twee nieuwe documenten bijgewerkt.
Dit is geen bewijs van implementatie of gekalibreerde herkenningsnauwkeurigheid.

## Aanvulling: YOLO26n-seg/DINOv2-voorbereiding — 4 november 2026

Toegevoegd aan de lokale publicatievoorbereiding: yolo_dinov2_pipeline.py, de optionele dependencylijst, voorbeeldconfiguratie, handleiding en synthetische tests. De module heeft aparte route A (volledige foto) en route B (YOLO-masker met neutrale RGB-achtergrond), gebruikt dezelfde DINOv2 ViT-B/14 preprocess en cosine-methode en weigert niet-lokale YOLO-gewichten. De DINOv2-adapter eist de vastgezette bronrevisie en checkpointhash. Meervoudige, ontbrekende of onbruikbare maskers krijgen geen route-B-score en verschijnen in te_controleren.json.

Vier nieuwe tests slaagden met de reeds bestaande Windows/Python 3.12.14/NumPy 2.3.5/Pillow 12.3.0-omgeving. Alleen zelfgemaakte geometrische afbeeldingen en nagebootste detector/encoder zijn gebruikt. Ook de bestaande synthetische tests en de exacte openbare bestanden-/hashcontrole zijn opnieuw uitgevoerd. Er zijn geen pakketten geïnstalleerd, modellen geladen, gewichten gedownload, echte onderzoeksfoto's verwerkt of identiteitssleutels geraadpleegd.

Deze tests bewijzen geen YOLO-detectiekwaliteit, maskerkwaliteit, DINOv2-herkenningswinst of wetenschappelijke validiteit. De 0,25 detectiegrens en 0,5%–90% maskergrootte zijn alleen voorlopige kwaliteitsvlaggen. De route is niet met echte modellen getest; er is geen schone installatie getest. De privébevestiging van Ultralytics is niet meegeleverd of onafhankelijk gecontroleerd. De nieuwe toepasselijke bestanden zijn nog niet naar GitHub gepubliceerd.
