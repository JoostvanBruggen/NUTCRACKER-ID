# Architectuur en ontwikkelrichting

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
SPDX-License-Identifier: AGPL-3.0-only

## Doel en uitgangspunten

NUTCRACKER-ID moet een algemeen hulpmiddel worden voor individuele vogelherkenning.
Het huidige prototype is een eerste technische proef, geen voltooid of
wetenschappelijk gevalideerd herkenningsprogramma.

De bestaande 72 anonieme foto's van acht bekende Notenkrakers zijn uitsluitend
een gecontroleerde privétestset. Deze aantallen zijn geen programma-instelling,
capaciteitsgrens of vooraf bekend aantal te vinden individuen. De testset blijft
apart beschikbaar voor latere wetenschappelijke validatie en wordt niet
meegeleverd. De identiteitssleutel blijft strikt gescheiden van de herkenning.

Functionele eisen:
- Een expliciet gekozen lokale fotomap is de eerste invoervorm.
- Kleine en grote collecties moeten binnen de beschikbare rekenkracht kunnen
  worden verwerkt; er komt geen vaste limiet op het aantal foto's.
- Groepen ontstaan automatisch op basis van bewijs, zonder vooraf opgegeven
  aantal individuen. Een kandidaatgroep is geen bewezen identiteit.
- Foto's of vogeluitsneden mogen ongegroepeerd blijven bij onvoldoende of
  tegenstrijdig bewijs. Een losse foto is niet automatisch een nieuw individu.
- Een website of lijst met foto-URL's wordt later een afzonderlijke invoervorm.
- Grote collecties moeten kandidaatselectie gebruiken, zodat niet ieder mogelijk
  fotopaar volledig hoeft te worden geanalyseerd.

## Zoekopdracht en betrouwbaarheidslaag

Een zoekopdracht bevat één foto en een gekozen bestaande collectie.
Dezelfde vijf onderdelen leveren detecties, zichtbare kenmerken, indexkandidaten,
verklaarbare vergelijkingen en afzonderlijke controle. De collectie-index wordt
vooraf opgebouwd en later incrementeel bijgewerkt. Een zoekfoto hoeft niet
blijvend aan de collectie toegevoegd te worden.

De vergelijkingslaag bewaart technische score, eventueel onderbouwde identiteitskans,
daadwerkelijk vergeleken kenmerken, kwaliteit, ontbrekende informatie en
uitsluitingsredenen als afzonderlijke gegevens.
Een versiegebonden kalibratie kan later onderdeel van deze laag worden.
De onafhankelijke evaluator toetst die kansuitspraken; een identiteitssleutel
hoort nooit in de herkenningsroute.

De gewenste kansklassen zijn GROEN vanaf 0,95, ORANJE vanaf 0,80 tot onder 0,95
en GRIJS onder 0,80, uitsluitend na onafhankelijke kalibratie binnen het geteste
toepassingsgebied. Zonder kalibratie blijven kansen onbekend en technische
scores neutraal. Groepsbetrouwbaarheid volgt niet automatisch uit het beste fotopaar.
Een uitsluiting volgens de operationele reistijdregel wordt apart getoond.

Een latere website biedt een privézoekfoto, vergelijking naast elkaar,
gerangschikte kandidaten, groepsgalerijen en beoordeling van onzekere uitkomsten.
Er is geen website gebouwd en de bestaande vergelijking is niet veranderd.

Het uitgewerkte [zoek- en betrouwbaarheidsontwerp](ZOEKEN_EN_BETROUWBAARHEID.md)
bevat het toekomstige gegevensmodel en een vergelijking met de huidige code.
Het [validatieplan](VALIDATIEPLAN.md) beschrijft hoe bekende individuen later
afzonderlijk kunnen worden gebruikt om kansen en groepen objectief te toetsen.

## Vijf gescheiden onderdelen

Verwerkingsroute:
invoer -> vogeldetecties -> kenmerken -> kandidaatparen en groepen -> controle.

| Onderdeel | Verantwoordelijkheid | Beoogde gegevensoverdracht |
| --- | --- | --- |
| 1. Verzamelen en inlezen | Lokale bestanden registreren; later toegestane webbronnen; herkomst, rechten en dubbele bestanden controleren | Beeldrecord met interne ID, inhoudshash, bronverwijzing, rechtenstatus en beschikbare tijd/locatie |
| 2. Vogels detecteren en afbakenen | Per beeld nul, één of meer vogels vinden; uitsneden en zichtbaarheid vastleggen | Detectierecord met beeld-ID, vogel-ID binnen het beeld, kader of masker, kijkzijde en onzekerheid |
| 3. Zichtbare kenmerken analyseren | Alleen daadwerkelijk zichtbare patronen en vormen beschrijven | Kenmerkrecord per detectie met methodeversie, soortprofiel, kenmerken, kwaliteit en onbekende onderdelen |
| 4. Vergelijken en kandidaatgroepen vormen | Kansrijke paren selecteren, bewijs vergelijken, conflicten toetsen en groepen voorstellen | Paarbewijs, kandidaatgroepen en ongegroepeerde detecties, met redenen |
| 5. Onafhankelijk controleren | Menselijke beoordeling en afzonderlijke wetenschappelijke evaluatie | Controlebesluit of evaluatierapport; de automatische uitkomst blijft herkenbaar bewaard |

De tabel is een ontwerp, nog geen geïmplementeerde module-API.
Een foto kan meerdere vogels bevatten. Daarom worden toekomstige kenmerken en
groepen aan een vogeldetectie gekoppeld, niet blind aan de hele foto.
De interface kan daarna de bijbehorende foto's samen tonen. Een foto met meerdere
vogels kan zo bij meerdere kandidaatgroepen voorkomen zonder die individuen
samen te voegen.

## Wat nu al bestaat

De huidige uitvoering staat nog grotendeels in één Python-bestand:
- Inlezen: expliciete lokale map met PNG-bestanden.
- Detectie: heuristische voorstellen voor oog, kopregio's en uitsnede;
  geen getraind vogelmodel.
- Kenmerken: helderheidsvlekken in voorgestelde regio's.
- Vergelijken: paarsgewijze scores en kandidaatgroepen, zonder vast groepsaantal;
  onvoldoende bewijs kan ongegroepeerd blijven.
- Controle: lokale HTML-overzichten en een afzonderlijke synthetische technische test.

De lokale invoer accepteert één of meer PNG's zonder vaste bovengrens in de code.
Een lege of ongeldige invoermap geeft een melding. De huidige mapinvoer is niet
recursief. Ondersteuning van andere beeldformaten is latere ontwikkeling.

De huidige uitvoering is nog niet geschikt verklaard voor grote collecties:
alle fotoparen worden doorlopen; richting en gedeelde kenmerken beperken de
verdere berekening, maar voorkomen die volledige paarlus niet.
Het aantal mogelijke paren groeit als n*(n-1)/2. Kenmerken, paren en het rapport
worden grotendeels in het geheugen opgebouwd. Er is nog geen kandidatenindex,
batchverwerking, hervatten of begrensd geheugengebruik.
Geen vaste limiet betekent dus niet dat onbeperkte aantallen praktisch werken.

## Later: efficiënte verwerking

De onderdelen moeten gegevens stapsgewijs kunnen lezen en schrijven.
Bewaar berekende kenmerken lokaal, gekoppeld aan inhoudshash, methodeversie en
instellingen, zodat ongewijzigde beelden niet telkens opnieuw worden berekend.
Werk in batches, met instelbaar geheugen-, opslag- en rekenbudget en hervatbare
taken. Rapporteer voortgang en onvolledig verwerkte invoer.

Gebruik een index van globale kenmerken om per vogel een beperkte verzameling
vergelijkingskandidaten te vinden. Voer daarna de kostbaardere vergelijking van
zichtbare kenmerken en conflicten alleen voor die kandidaten uit.
Kandidaatselectie kan echte overeenkomsten missen; meet dat verlies afzonderlijk.
Voor kleine validatiecollecties kan een volledige paarvergelijking als
referentie dienen, zonder die bij grote collecties verplicht te maken.

Schaalbare groepering moet op de geselecteerde bewijsrelaties kunnen werken.
Een complete vergelijking tussen alle leden van grote groepen mag niet alsnog
ongemerkt een verplichte volledige paaranalyse veroorzaken. Ontbrekend paarbewijs
is onbekend, geen positief of negatief bewijs. Groepen moeten kunnen worden
herbeoordeeld bij nieuwe beelden of conflicten. Het aantal groepen volgt uit
bewijs en wordt nooit gelijkgesteld aan het aantal bekende testindividuen.
De keuze van een schaalbaar algoritme en zijn drempels vraagt latere validatie.

## Uitbreiden naar andere soorten en kenmerken

Gebruik verwisselbare detectoren, kenmerkextractoren, vergelijkers en soortprofielen.
Een soortprofiel beschrijft toepasbare kenmerken en kwaliteitseisen, zonder een
vast aantal individuen of verwijzingen naar een identiteitssleutel.
Voorbeelden van toekomstige kenmerken zijn kopvlekjes, snavelvorm en andere
zichtbare patronen. Niet-zichtbare of onbetrouwbare kenmerken krijgen de status
onbekend en worden niet kunstmatig ingevuld.
Leg methodeversie en instellingen bij iedere uitkomst vast.

Tijd, locatie en snavelpuntbeoordeling zijn nog niet geïmplementeerd.
Bij latere implementatie moeten de opgegeven fototijden, tijdzones, hemelsbrede
afstanden en de door de eigenaar gekozen 40 km/u-regel expliciet worden verwerkt.
Een ruimtelijk en temporeel mogelijke verplaatsing bewijst geen identiteit.
Ontbrekende vervolgmeldingen bewijzen geen vertrek. Onvoldoende zicht op de
snavelpunt geeft onbekend; een duidelijk verschil kan tegenbewijs opleveren.
Deze voorwaarden horen bij het verklaarbare paarbewijs. Vergelijkingen op
dezelfde locatie tellen niet als bewijs voor een cross-locatiematch.

## Latere webinvoer

Webinvoer komt als afzonderlijke bronadapter vóór detectie en vergelijking.
Deze adapter voert dezelfde beeldrecords aan als lokale invoer; de herkenning
bevat geen ingebouwde crawler.

Openbaarheid of technische bereikbaarheid geeft geen automatisch download- of
hergebruiksrecht. Controleer vóór verzamelen de toepasselijke toestemming,
fotolicentie, gebruiksvoorwaarden, toegangsbeperkingen en verzoeklimieten.
Bewaar bron-URL, fotograaf, licentie en beschikbare waarnemingsgegevens.
Onzekere rechten of toegang betekenen niet verzamelen; geen omzeiling.
Ontdubbel waar mogelijk op inhoud en bron-ID. Ontbrekende herkomst blijft zichtbaar.
Er is nu geen URL-invoer, crawler, webdownload of netwerkcode toegevoegd.

## Onafhankelijke validatie en privéscheiding

De automatische verwerkingsroute leest geen ware identiteiten, sleutelbestand,
oorspronkelijke groepen of bestandsnaamcodering die zo'n identiteit prijsgeeft.
Testaantallen en bekende identiteiten mogen geen keuze van groepsaantal sturen.

Een latere afzonderlijke evaluator kan, uitsluitend na aparte toestemming,
bevroren automatische uitkomsten vergelijken met privéreferenties.
Die evaluator en referenties zijn niet nodig om de herkenning uit te voeren.
Deze opdracht opent geen sleutel en bouwt die evaluator nog niet.

Gebruik de gecontroleerde privétestset later om onder meer verkeerde
samenvoegingen, gemiste overeenkomsten, ongegroepeerde beelden en overeenkomsten
tussen locaties te meten. Houd afstelling en onafhankelijke evaluatie gescheiden;
beoordeel ook op andere collecties en individuen. Technische synthetische tests
bewijzen alleen dat uitvoerpaden werken, geen biologische herkenningskwaliteit.

## Volgende ontwikkelstappen

1. De gegevensoverdracht en losse modules uitwerken, met behoud van veilige invoer.
2. Vogelafbakening en kenmerken verbeteren; YOLO pas na de toegestane publicatie.
3. Kandidaatselectie, opslag, batches en hervatten ontwikkelen en schaal meten.
4. Uitlegbare groepering met onbekende uitkomsten en conflicten valideren.
5. Een onafhankelijke evaluator voor gecontroleerde privévalidatie ontwikkelen.
6. Webinvoer afzonderlijk uitwerken met controle op rechten en toegestane toegang.

Dit document legt het ontwerp vast. Het voegt geen runtimefunctionaliteit toe.
