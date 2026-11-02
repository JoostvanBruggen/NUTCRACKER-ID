# Zoeken met één foto en betrouwbaarheidsklassen — ontwerp

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
SPDX-License-Identifier: AGPL-3.0-only

Dit is een ontwerpuitbreiding. Bestaande scores, drempels, groepsindelingen en
programmacode zijn niet gewijzigd. Er is geen website of herkenningsrun gebouwd.
De collectie heeft geen vaste fotoaantalsgrens en geen vooraf bekend groepsaantal.

## Eén foto als zoekopdracht

1. De gebruiker kiest een beschikbare collectie en biedt één zoekfoto aan.
2. De invoerlaag controleert bestandsformaat, rechtenstatus en metadata.
   Bij meerdere vogels kiest de gebruiker welke vogeldetectie gezocht moet worden.
3. Bereken alleen de detectie en zichtbare kenmerken van de zoekfoto.
4. Zoek kansrijke kandidaten in de vooraf opgebouwde collectie-index.
5. Vergelijk overeenkomstige anatomische zijden en bruikbare kenmerken van
   de zoekvogel met die kandidaten; controleer beschikbare tijd- en locatiegegevens.
6. Toon de kandidaten in volgorde van technische overeenkomst. Pas na geldige
   kalibratie kan de rangorde een geschatte identiteitskans gebruiken.
   Meng verschillende score- of kansschalen niet in één rangorde.
7. Toon per kandidaat de beschikbare foto's en kandidaatgroep, met een aparte
   sectie voor onzekere, niet beoordeelbare of uitgesloten resultaten.

De zoekfoto hoeft niet aan de collectie toegevoegd te worden. Een identiek
bestand dat al in de collectie staat wordt als duplicaat gemeld; het telt
niet als onafhankelijke bevestiging. Een overeenkomst hoeft niet in de collectie
aanwezig te zijn. De beste kandidaat mag dus nog steeds onzeker zijn.

Een blijvende index bewaart kenmerken en methodeversies. Nieuwe collectiebeelden
worden afzonderlijk verwerkt; ongewijzigde beelden worden hergebruikt.
Werk alleen de getroffen kandidaatrelaties en groepen bij, met behoud van vorige
versies en controlebesluiten. Een gewijzigde methode kan herberekening van een
deel of de hele index vereisen. Dit incrementele gedrag bestaat nog niet.

## Technische score en identiteitskans strikt scheiden

De technische overeenkomstscore beschrijft alleen de werking van een
vergelijkingsmethode. Het huidige prototype berekent zo'n score op een schaal
van 0 tot 100. Toon die later als bijvoorbeeld '95/100 technische overeenkomst;
betrouwbaarheid niet bepaald'. Dit betekent niet 95% kans op dezelfde vogel.

De bestaande HTML toont procenttekens bij technische scores; de toelichting noemt
die scores experimenteel. Die opmaak is in deze ontwerpopdracht niet aangepast.
Ook confidence voor een kopvoorstel en eye_confidence zijn heuristische
aanwijzingssterktes, geen gekalibreerde kans op een juiste kop of identiteit.

De gewenste categorieën gelden uitsluitend voor een wetenschappelijk onderbouwde
identiteitskans p binnen het geteste toepassingsgebied:

| Categorie | Kansbereik, vóór afronding | Gewenste omschrijving |
| --- | --- | --- |
| GROEN | 0,95 ≤ p ≤ 1 | VRIJWEL ZEKER DEZELFDE VOGEL |
| ORANJE | 0,80 ≤ p < 0,95 | MOGELIJK DEZELFDE VOGEL |
| GRIJS | 0 ≤ p < 0,80 | ONZEKER |

De door de eigenaar bedoelde 80–94% wordt zo zonder gat tussen 94 en 95% toegepast.
Classificeer vóór afronding: 94,9% blijft oranje. Toon altijd dat het een geschatte
kans is, samen met de kalibratieversie en geldigheidsgrenzen.
Geen geschatte waarde levert absoluut bewijs van identiteit.

Zonder geldige kalibratie blijft de kans leeg en toont de interface neutraal:
'Betrouwbaarheid niet bepaald — technische overeenkomstscore'.
Dat is geen gemeten kans onder 80%. Gebruik daarvoor geen groene of oranje
zekerheidsklasse. Bij onvoldoende kwaliteit of toepassing buiten het gevalideerde
bereik wordt de kans eveneens niet uitgegeven. Criteria daarvoor moeten tijdens
de onafhankelijke validatie worden vastgesteld.

Een uitsluiting volgens de projectregel krijgt een afzonderlijke status en
reden. Zij wordt niet verstopt door de technische score op nul te zetten.
Zo'n operationele uitsluiting is ook niet automatisch een biologisch bewezen kans nul.

## Gegevens die afzonderlijk worden opgeslagen

Onderstaande velden zijn een voorgesteld gegevensmodel, nog geen bestaande API.

| Gegeven | Betekenis |
| --- | --- |
| query_detection_id, candidate_detection_id | Verwijzing naar de twee vogels in de beelden |
| technical_score, score_scale, comparison_version | Ongewijzigde technische score, schaal en gebruikte methode |
| identity_probability | Geschatte kans op hetzelfde individu; leeg als niet onderbouwd |
| probability_status, calibration_version, applicability | Waarom een kans beschikbaar, onbekend of niet toepasbaar is; toepassingsgebied |
| compared_regions | Welke overeenkomstige regio's werkelijk vergeleken zijn |
| compared_features_a, compared_features_b, matched_features | Aantallen gevonden en gekoppelde kenmerken, per regio |
| unique_feature_count | Aantal unieke kenmerken, alleen indien betrouwbaar bepaald; anders leeg |
| comparison_quality | Scherpte, resolutie in de uitsnede, zichtbaarheid, kijkzijde, bedekking en kwaliteitsstatus |
| missing_information | Ontbrekende of onbruikbare kenmerken en metadata, met redenen |
| exclusions | Afzonderlijke uitsluitingsgronden, gebruikte waarnemingen en regelversie |
| observation_metadata | Oorspronkelijke datum/tijd, tijdzone, UTC, locatie, nauwkeurigheid, bron en beschikbaarheidsstatus |
| evidence, group_version, review_status | Onderbouwing, versie van de kandidaatgroep en afzonderlijke menselijke controle |

De huidige JSON bevat al regionale scores, features_a/features_b/matched,
region_count, matched_features, sharpness, coverage en afmetingen.
De totaaltelling matched_features kan dezelfde vlek via overlappende regio's
meermaals meetellen. Noem dit geen aantal onafhankelijke bewijsstukken.
Een nieuwe opslaglaag moet onbekende gegevens kunnen onderscheiden van nul.

## Inhoudelijke vergelijking

Vergelijk kop, nek, keel, hals en andere soortspecifiek bruikbare verenkleedkenmerken.
Beschrijf ligging, vorm, grootte en onderlinge verhoudingen van zichtbare vlekken.
Werk met overeenkomstige anatomische zijden. Onzekere kijkzijde of een niet
zichtbare regio geeft onbekend, geen automatisch verschil of gunstige overeenkomst.

Het prototype vergelijkt genormaliseerde helderheidsmaskers en kenmerkposities.
Dat is gedeeltelijke ondersteuning; echte vlekafbakening en robuuste vorm- en
groottevergelijking ontbreken. De kijkzijde is nu een grove compositieheuristiek.
Een duidelijk zichtbaar uitstekend bovensnavelpuntje wordt later een afzonderlijk
kenmerk. Bij open snavel, perspectief, onscherpte of bedekking moet het
uitstekende puntje nog steeds daadwerkelijk beoordeelbaar zijn; anders onbekend.

Een kandidaatgroep krijgt niet automatisch de hoogste kans van één fotopaar.
Een zoekfoto vergelijken met één foto en een zoekfoto vergelijken met een groep
zijn verschillende gebeurtenissen die afzonderlijke onderbouwing vragen.
Bewaar daarom het paarbewijs en de herkomst van elke groepsbeslissing.
Meer groepsfoto's mogen niet ongemerkt tot een hogere schijnzekerheid leiden.

## Tijd, locatie en de operationele 40 km/uur-regel

Bewaar de oorspronkelijke fototijd en tijdzone. De opgegeven fototijden worden
als gegeven gebruikt; zet ze voor vergelijking om naar UTC zonder de oorspronkelijke
tijd te vervangen. Een ontbrekende tijdzone of onduidelijke zomertijd blijft
onzeker. Verzin geen tijdstip voor een foto waarvan alleen de datum bekend is.

Wanneer tijd en locatie voldoende betrouwbaar en nauwkeurig bekend zijn:
- Orden de waarnemingen chronologisch.
- Bereken de hemelsbrede afstand, niet de wegafstand.
- Bereken de beschikbare tijd en de vereiste snelheid.
- Een vereiste snelheid boven 40 km/uur geeft de aparte status
  'UITGESLOTEN VOLGENS PROJECTREGEL', met afstand, tijdsverschil en reden.
- Precies 40 km/uur past binnen de regel. Vergelijk de ongeronde waarden.
- Gelijktijdige opnamen met aantoonbaar verschillende locaties zijn onder deze
  regel onverenigbaar; voorkom delen door nul.

Ontwerpvoorbeelden met betrouwbare tijden en exacte locaties:
80 kilometer in twee uur is toegestaan volgens de regel, maar bewijst geen match.
80 kilometer in één uur wordt volgens de regel uitgesloten.

Bij onnauwkeurige tijden of locaties worden tijdintervallen en locatienauwkeurigheid
meegewogen. Sluit alleen uit als zelfs de meest gunstige nog plausibele afstand
en beschikbare tijd de regel schenden. Anders luidt de uitkomst mogelijk of
niet toetsbaar; bepaal de exacte kwaliteitscriteria vóór implementatie.

Controleer ook betrouwbare vervolgwaarnemingen op de eerdere locatie.
Een nieuwe melding daar is niet vanzelf dezelfde vogel en mag niet circulair
als identiteit worden aangenomen. Ontbrekende meldingen bewijzen geen afwezigheid.
Bewaar daarom bron, koppeling aan een kandidaat, betrouwbaarheid en eventuele
conflicten apart. Vergelijkingen op dezelfde locatie mogen kandidaten ondersteunen,
maar tellen niet als de gevraagde cross-locatiebevestiging.

40 km/uur is de gekozen operationele onderzoeksgrens, geen bewezen biologische
maximumsnelheid. Deze controle is nog niet geïmplementeerd.

## Eenvoudige website — alleen ontwerp

Ontwerp vier stappen: collectie kiezen -> zoekfoto aanbieden -> vogel selecteren
indien nodig -> kandidaten bekijken.

Het resultaat toont zoekvogel en kandidaat naast elkaar, met beschikbare
regio-uitsneden. Iedere kaart bevat technische score, geschatte kans indien
onderbouwd, categorie indien van toepassing, kwaliteitsinformatie, kenmerken,
ontbrekende informatie en beschikbare datum/tijd/locatie.
Toon ontbrekende metadata expliciet als onbekend.

De gebruiker kan alle foto's van een kandidaatgroep openen en onzekere resultaten
apart beoordelen. Menselijke bevestigingen of afwijzingen worden afzonderlijk
bewaard en veranderen niet stilzwijgend eerdere automatische resultaten.
Een kandidaat-ID is geen bewezen individuele identiteit.

Een latere upload blijft standaard privé en maakt geen onderzoeksfoto openbaar.
Bewaartermijn, toegang, verwijderen en lokale of serververwerking moeten vóór
websitebouw worden vastgesteld. Een openbare broncode-uitgave is geen toestemming
om gebruikersfoto's openbaar te maken. Er is nu geen website, uploadpunt,
server of crawler toegevoegd.

## Status van de bestaande software

| Eis | Huidige ondersteuning | Nog te ontwikkelen |
| --- | --- | --- |
| Lokale collectie zonder vaste omvang | Expliciete PNG-map; geen vast aantal foto's of individuen | Andere formaten en schaalbare opslag |
| Eén foto zoeken in collectie | Niet aanwezig; één bestand in een map geeft geen echte collectiezoekfunctie | Zoekopdracht, collectie-index en kandidaatselectie |
| Kenmerkvergelijking | Helderheidsmaskers en posities in ruwe regio's | Robuuste anatomie, vlekvorm/-grootte en snavelpunt |
| Rangorde | Paarscores worden aflopend gerangschikt | Rangorde per zoekvogel en onderbouwde groepsrangorde |
| Groepen en onthouding | Experimentele kandidaatgroepen en ongegroepeerde foto's | Bijwerken van groepen, conflicten en verklaringen |
| Bewijs en kwaliteit | Enkele regionale aantallen en heuristische kwaliteitsmaten | Volledig gegevensmodel en betrouwbare kwaliteitscontrole |
| Identiteitskans en kleuren | Geen kalibratie of betrouwbaarheidsklassen | Onafhankelijke kalibratie en gecontroleerde toepassing |
| Tijd en locatie | Niet aanwezig | Metadata, UTC, afstand, chronologie en uitsluitingsregels |
| Resultaten bekijken | Statische lokale HTML met overlays en technische scores | Zoekinterface, naast-elkaarcontrole en groepsgalerij |
| Nieuwe foto's toevoegen | Verwerking opnieuw starten | Kenmerkcache, index bijwerken en hervatbare taken |
| Onafhankelijke validatie | Synthetische technische tests | Evaluatie met bekende individuen en nieuwe collecties |

Zie [VALIDATIEPLAN.md](VALIDATIEPLAN.md) voor de toetsing vóór kansuitspraken.
