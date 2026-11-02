# Onafhankelijke validatie en kalibratie — ontwerp

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
SPDX-License-Identifier: AGPL-3.0-only

Dit plan is nog niet uitgevoerd. Het gebruikt nu geen identiteitssleutel en
verandert geen herkenningsscores, drempels of groepen.

## Wat moet worden aangetoond?

Toets afzonderlijk:
1. Vindt de zoekfunctie de juiste bekende vogel tussen andere vogels?
2. Wijst zij zoekvogels zonder tegenhanger in de collectie terecht niet in?
3. Kloppen geschatte identiteitskansen met de waargenomen uitkomsten?
4. Zijn kandidaatgroepen zuiver, en worden foto's van hetzelfde individu niet
   onnodig over meerdere groepen verdeeld?
5. Hoeveel correcte kandidaten mist de snelle kandidaatselectie?
6. Hoe vaak kan de software geen voldoende onderbouwd oordeel geven?

Een technische score 95 wordt niet vooraf gelijkgesteld aan kans 0,95.
Kalibratie is een apart te leren en te toetsen verband voor een bepaalde
methode, doelgroep en zoekopzet. Bepaal vooraf of een kans slaat op één fotopaar
of op aansluiting bij een kandidaatgroep; gebruik daarvoor geen ongemotiveerde
maximum- of gemiddeldepaarscore.

## Privéscheiding

De automatische verwerking ontvangt alleen beelden, toegestane metadata en
methode-instellingen. Zij ontvangt geen sleutel, bekende groepsindeling of
bestandsnaamcode waaruit de identiteit af te leiden is.

Een afzonderlijke evaluator mag pas na een nieuwe opdracht de bevroren uitkomsten
naast de privéreferentie leggen. Die referentie blijft buiten de bronuitgave,
zoekindex en herkenningscode. Bewaar technische resultaten eerst ongewijzigd;
koppel de ware identiteiten uitsluitend in de evaluator.
Menselijke controle-uitkomsten worden apart van oorspronkelijke voorspellingen
opgeslagen. Gebruik een menselijke beoordeling niet stilzwijgend als nieuwe waarheid.

De 72 anonieme foto's van acht bekende vogels blijven een gecontroleerde
privétestset. Zij bepalen niet het aantal te vinden groepen en zijn op zichzelf
geen voldoende onderbouwing voor algemene claims over andere vogels of soorten.
Zijn beelden al gebruikt voor afstelling of methodeselectie, dan tellen ze niet
als onaangeroerde eindtest. Daarvoor zijn nieuwe onafhankelijke beelden nodig.

## Ontwikkeling, kalibratie en eindtest scheiden

Leg vóór toetsing vast: doelsoort, type beelden, kwaliteitseisen, gebruik van
metadata, omvang en samenstelling van de collectie, kandidaataantal en scoreversies.

Maak afzonderlijke gegevensdelen voor:
- Ontwikkelen en kiezen van detectoren, kenmerken, regels en instellingen.
- Leren en kiezen van de omzetting van technische scores naar kansen.
- Een afgesloten eindtest waarop niets meer wordt bijgesteld.

Splits primair op individuele vogel: vogels uit de eindtest komen niet terug in
ontwikkeling of kalibratie. Binnen de eindtest moet dezelfde testvogel wel in
zowel zoekfoto als collectie kunnen voorkomen om terugvinden te kunnen toetsen.
Neem ook zoekvogels op die volledig uit de doorzochte collectie ontbreken.

Houd duplicaten, uitsneden van dezelfde opname en sterk samenhangende opnamesessies
binnen hetzelfde ontwikkel-, kalibratie- of eindtestdeel.
Maak voor de zoekproef waar mogelijk een extra scheiding tussen opnamesessies
en locaties van zoekfoto en collectie. Zo wordt het resultaat niet alleen
gedragen door bijna identieke opnamen of dezelfde achtergrond.
Een enkele willekeurige verdeling van fotoparen is hiervoor onvoldoende.

Met weinig vogels kan een vooraf vastgelegde evaluatie met wisselende uitgesloten
individuen een verkennend beeld geven. Kies instellingen dan uitsluitend binnen
de ontwikkelgedeelten. Dit vervangt geen latere externe eindtest met nieuwe vogels.

## Maak de zoekproef representatief

Gebruik zowel paren van dezelfde vogel als paren van verschillende vogels.
Neem gelijkende andere individuen, ontbrekende regio's, andere kijkhoeken,
onscherpe foto's en verschillende locaties/opnamesessies op.
Toets herkenning van een niet-aanwezige vogel en onbekende soort/beeldkwaliteit.

Test de complete route, inclusief de snelle index en gekozen hoeveelheid kandidaten.
De verhouding tussen echte en onechte matches en de collectiegrootte beïnvloeden
welke kansuitspraken voor een zoekresultaat passend zijn.
Een kans die op een kunstmatig gebalanceerde verzameling willekeurige fotoparen
is geleerd, mag niet zonder nieuwe controle op een grote zoekcollectie worden gebruikt.

Test ook de tijd- en locatiecontrole apart met gecontroleerde, fictieve metadata:
tijdzones, zomertijd, ontbrekende tijden, onnauwkeurige locaties, nul tijdsverschil,
de grens van 40 km/uur en vervolgwaarnemingen.
Een operationele uitsluiting is geen visuele fout van de patroonvergelijker;
rapporteer beide onderdelen en de gezamenlijke zoekuitkomst afzonderlijk.

## Metingen en onzekerheid

Rapporteer per onafhankelijke zoekvogel en per testsituatie:
- Of de juiste vogel bovenaan en tussen de eerste k kandidaten staat; vermeld k.
- Aandeel juiste meldingen, gemiste echte matches en onjuiste matches,
  inclusief zoekvragen zonder echte tegenhanger.
- Zuiverheid van groepen, verkeerde samenvoegingen en onnodige opsplitsingen.
- Aandeel onzekere of niet beoordeelbare gevallen en de kwaliteit van de rest.
- Gemiste kandidaten door de index en rekentijd/geheugengebruik bij groeiende collecties.

Voor kansen: vergelijk voorspelde kansintervallen met hun werkelijk juiste aandeel
in een kalibratiegrafiek. Voeg Brier-score of logverlies als aanvullende meting toe;
één van die scores alleen bewijst geen goede kalibratie.
Rapporteer aantallen en onzekerheidsintervallen per klasse en kwaliteitsgroep.
Bereken onzekerheid met rekening voor samenhang binnen vogel en opnamesessie;
duizenden paren uit een paar vogels zijn geen duizenden onafhankelijke proeven.

## Wanneer mogen de klassen worden gebruikt?

De door de eigenaar gekozen grenzen staan vast in het ontwerp:
groen vanaf 0,95; oranje vanaf 0,80 tot onder 0,95; grijs onder 0,80.
Toets vóór activering of de uitgegeven kansen daarbij passen op de afgesloten
eindtest, ook voor foutpositieven, ongeziene individuen en meerdere collectiegroottes.

Leg de aanvaardbare onzekerheid en foutmarges vooraf met de eigenaar vast.
Er wordt in dit ontwerp geen zelfgekozen minimaal aantal testfoto's of
goedkeuringspercentage ingevoerd. Bij onvoldoende onafhankelijke voorbeelden,
onbetrouwbare kalibratie of onbekend toepassingsgebied blijft de kans leeg.
Een reeks correcte groene matches bewijst geen foutloze herkenning.

Bewaar bij een vrijgegeven kalibratie de versie, proefopzet, geldigheidsgrenzen
en het toetsrapport. Veranderingen in kenmerken, detector, kandidatenselectie,
groepering of gebruikscontext vragen herbeoordeling. Publiceer alleen rapportages
waarvan privacy en rechten zijn gecontroleerd, zonder sleutel of privébeelden.

## Bronnen voor het toetsontwerp

Geraadpleegd 2 november 2026; deze documentatie verplicht niet tot gebruik of
installatie van scikit-learn:
- [Probability calibration](https://scikit-learn.org/stable/modules/calibration.html):
  kansuitspraken toetsen met kalibratiegrafieken; aanvullende scores onderscheiden
  niet vanzelf kalibratie van onderscheidend vermogen.
- [Cross-validation en gegroepeerde gegevens](https://scikit-learn.org/stable/modules/cross_validation.html):
  eindtoetsing scheiden van afstelling en samenhangende voorbeelden gescheiden
  houden bij het beoordelen van generalisatie.

De voorgestelde vogel-, sessie- en locatiesplitsingen zijn de projectgerichte
uitwerking van dit toetsplan; zij zijn nog niet toegepast.
