# Methode en beperkingen

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
SPDX-License-Identifier: AGPL-3.0-only

Het prototype stelt een ooganker en globale kopregio's voor uit donker-lichtcontrast.
Het zoekt heldere lokale kenmerken en vergelijkt hun genormaliseerde posities.
De kijkrichting is slechts een compositieheuristiek. Kader, oog en kijkzijde vragen
menselijke controle; takken en schaduw kunnen de heuristiek misleiden.

Kandidaatgroepen vereisen per onderling paar minimaal score 67, drie gedeelde
regio's en zeven gekoppelde kenmerken. De groepsopbouw is volgordeafhankelijk
en zoekt niet gegarandeerd de beste mogelijke indeling. De drempels zijn niet
wetenschappelijk gekalibreerd. Ook een hoge score is geen identiteitskans.

Een synthetische test bewijst alleen technische werking. Nauwkeurigheid,
foutpositieven, herhaalbaarheid op echte vogels en onderscheid tussen individuen
zijn niet gevalideerd. Uitsneden voegen geen nieuw detail toe.

Nog niet geïmplementeerd:
- Opnametijden, tijdzones, locaties en hemelsbrede afstanden.
- Onderscheid tussen vergelijkingen op dezelfde en verschillende locaties.
- De door de eigenaar voorgestelde werkgrens van 40 km/u.
- Vervolgwaarnemingen op een eerdere locatie.
- Beoordeling van een uitstekend bovensnavelpuntje, met uitkomst onbekend bij
  onvoldoende zicht.

Deze ontbrekende regels mogen niet als actief identificatiefilter worden
gepresenteerd. De voorgestelde snelheid is een projectregel, geen hier bewezen
biologisch maximum. Afwezigheid van meldingen bewijst geen vertrek.

Gewijzigd voor deze voorbereiding: onjuiste vaste aantallen en beoordelingen
verwijderd; consistente paarsgewijze eisen bij groepsuitbreiding; veilige CLI;
veilige bestandsverwijzingen en zelfstandig kopcontrolerapport.
Er is geen getraind model, YOLO-code, modeldownload of netwerkfunctie toegevoegd.


## Omvang, groepen en architectuur

De 72 anonieme beelden van acht bekende Notenkrakers vormen uitsluitend een
privévalidatieset. Deze aantallen zijn geen invoereis, bovengrens of instelling
voor het aantal groepen. Het prototype accepteert een expliciete lokale PNG-map
met een willekeurig positief aantal bestanden, voor zover de middelen volstaan.
Kandidaatgroepen hebben geen vooraf vastgelegd aantal; ongegroepeerd blijven is
mogelijk. De identiteitssleutel wordt niet gebruikt.

Het prototype doorloopt nog alle mogelijke paren. Daarbinnen worden bepaalde
vergelijkingen overgeslagen, maar de paarlus blijft kwadratisch groeien.
De bestaande implementatie is nog niet schaalbaar verklaard.
Efficiënte kandidaatselectie, verwerking in batches en onafhankelijke evaluatie
zijn toekomstig werk. Zie [ARCHITECTUUR.md](ARCHITECTUUR.md) voor de gescheiden
onderdelen en uitbreiding naar andere soorten en zichtbare kenmerken.


## Betrouwbaarheidsklassen en onafhankelijke toetsing — nog niet actief

De bestaande technische scores en kandidaatgroepen blijven ongewijzigd.
Er is geen omzetting van score naar identiteitskans, ook niet bij scores boven 95.
De heuristische oog-/kopzekerheid is evenmin een identiteitskans.

Een toekomstige opslaglaag scheidt technische score, geschatte kans indien
onderbouwd, vergeleken aantallen, kwaliteit en ontbrekende gegevens.
Overlappende regio's kunnen dezelfde vlek meermaals meetellen; de huidige
totaaltelling is dus geen bewezen aantal onafhankelijke kenmerken.

De door de eigenaar gekozen GROEN/ORANJE/GRIJS-klassen worden pas actief
na onafhankelijke kalibratie en toetsing binnen het geldige toepassingsgebied.
Ontbrekende informatie blijft onbekend. Tijd-/locatieconflicten krijgen later
een aparte operationele uitsluitingsreden, zonder de technische score te overschrijven.

Zie [ZOEKEN_EN_BETROUWBAARHEID.md](ZOEKEN_EN_BETROUWBAARHEID.md) en
[VALIDATIEPLAN.md](VALIDATIEPLAN.md). Dit zijn ontwerpen, geen nieuwe herkenningsrun.
