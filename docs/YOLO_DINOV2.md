# YOLO26n-seg met DINOv2

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID  
SPDX-License-Identifier: AGPL-3.0-only

## Doel en grenzen

Deze optionele route vergelijkt dezelfde foto's met dezelfde DINOv2-methode:

- **Route A:** volledige originele foto.
- **Route B:** originele RGB-pixels binnen één YOLO-vogelmasker; pixels buiten het masker worden vervangen door neutraal RGB `(124, 116, 104)`.

De neutrale kleur sluit aan bij de bestaande DINOv2-proef en voorkomt een groot wit vlak dat lichte veren visueel kan laten wegvallen. Het masker verandert de veren binnen de selectie niet. Deze keuze moet biologisch nog worden geëvalueerd; de achtergrond kan nuttige context bevatten.

Een foto met nul of meerdere vogel-detecties, een lage detectiescore, een leeg/afwijkend masker of een masker dat bijna niets/bijna alles bedekt, krijgt geen route-B-vector. De grenzen (confidence 0,25; maskeroppervlak 0,5%–90%) zijn voorlopige technische signalen, geen gevalideerde kwaliteitsmaat. Controleer de maskers in het rapport. Er worden geen lichaamsdelen, zijden of individuele identiteiten afgeleid.

## Installatie na afzonderlijke goedgekeurde publicatie

De vereiste modelbestanden worden bewust niet meegeleverd. Deze route downloadt of installeert geen gewichten. Bereid na de juiste publicatie en een aparte opdracht een Python 3.12-omgeving voor en installeer de directe versies uit `requirements-yolo-dinov2.txt`. De bijbehorende DINOv2 broncode op de vastgezette revisie en de officiële checkpoints moeten lokaal beschikbaar zijn; geef die paden expliciet op. Houd rekening met de afzonderlijke licenties en voorwaarden van code, pakketten en gewichten.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-yolo-dinov2.txt
python yolo_dinov2_pipeline.py --photos .\voorbeeldfoto's --output .\resultaten-yolo-dinov2 --yolo-weights .\modellen\yolo26n-seg.pt --dinov2-repo .\modellen\dinov2 --dinov2-checkpoint .\modellen\dinov2_vitb14_pretrain.pth --threshold 0.90
```

Installeer of gebruik YOLO pas nadat de complete toepasselijke broncode openbaar is en dit is gecontroleerd, volgens de projectinstructie en de door de eigenaar gemelde schriftelijke bevestiging. Die private bevestiging is niet opgenomen of onafhankelijk gecontroleerd. De publieke Ultralytics-licentiepagina moet opnieuw worden gelezen vóór gebruik.

## Uitvoer

De opdracht maakt in een nieuwe, lege uitvoermap `beelden/`, `resultaten.json` en `rapport.html`. Uitvoer in de invoermap en overschrijven van een niet-lege map zijn geblokkeerd. Het rapport toont de originele kopie, detecties, neutrale maskerafbeelding en eventuele foutmelding. `resultaten.json` bevat alle paren, route-A- en route-B-cosines en drempelindicaties; route B is `null` als een van beide maskers niet bruikbaar is.

Cosine-overeenkomst en grens 0,90 zijn technische vergelijkingswaarden, geen identiteitskansen of bewezen matches. De drempel is alleen opgenomen om later exact dezelfde bestaande grens te kunnen bekijken; hij wordt niet tijdens deze voorbereiding afgestemd.

## Eerlijke latere vergelijking

Bewaar de bestaande lokale scores onveranderd als uitgangsmeting. Verwerk later dezelfde gecontroleerde beeldset met beide routes en bewaar alle technische scores en maskerbesluiten. Houd onderzoeksresultaten en beelden buiten deze openbare broncodebundel. Gebruik geen identiteitssleutel tijdens detectie, vectoren, drempels, afstellingen of kandidaatkeuze; de afzonderlijke evaluatie met bekende identiteiten valt buiten deze pipeline.

Bereken pas in een afzonderlijke evaluatiestap de aantallen juist/onjuist en gemist. Gebruik de identiteitssleutel niet voor detectie, vectoren, drempels, afstellingen of kandidaatkeuze. Laat instellingen ongewijzigd voor de eindcontrole; registreer aparte resultaten. Onderzoek voorbeelden waarin masker/context helpt of schaadt. Een verbeterde scoreverdeling alleen bewijst geen betere individuele herkenning.

## Tests zonder modellen

```powershell
python -B -m unittest discover -s tests -p "test_*synthetic.py" -v
```

De optionele tests maken fictieve geometrische PNG's en gebruiken nagebootste detector en encoder. Ze importeren of gebruiken Ultralytics, PyTorch, echte foto's of checkpoints niet. Succes toont alleen dat gegevensstroom, maskerafhandeling en rapportbestanden werken; geen detectiekwaliteit of herkenningswinst.

Bestandsgewichten zijn afzonderlijke artefacten, geen onderdeel van de AGPL-projectcode. Controleer vóór het verkrijgen of gebruiken van YOLO26n-seg- en DINOv2-gewichten ook de toepasselijke model-, dataset- en herdistributievoorwaarden. Deze map bevat geen gewichten of onderzoeksresultaten.

