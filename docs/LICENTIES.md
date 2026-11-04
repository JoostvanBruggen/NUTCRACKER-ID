# Licenties en latere YOLO-stap

Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
SPDX-License-Identifier: AGPL-3.0-only

## Eigen code

De eigen toepassingscode, tests, scripts en documentatie worden aangeboden onder
AGPL-3.0-only. COPYING bevat de volledige tekst. Behoud de copyright- en
licentievermeldingen en vermeld wijzigingen. De licentie biedt geen garantie.
AGPL staat ook commercieel gebruik toe als aan de voorwaarden wordt voldaan;
het niet-commerciële onderzoeksdoel voegt geen beperking toe aan de codelicentie.

Bij verspreiding moet de toepasselijke broncode met noodzakelijke bouw-,
installatie- en uitvoerscripts beschikbaar zijn volgens COPYING.
Bij een aangepaste netwerktoepassing is ook artikel 13 van belang.
Een toekomstige webdienst vraagt daarom een nieuwe nalevingscontrole.

## Afhankelijkheden

Deze map levert geen NumPy- of Pillow-pakket, binaries of modelgewichten mee.
Installatie gebeurt vanuit de officiële pakketindex. De pakketten behouden hun
eigen auteursrechtvermeldingen en licenties; AGPL vervangt deze niet.
Bij het later bundelen van pakketten of binaries moet je ook alle daarbij
behorende licentieteksten, meldingen en eventuele bronverplichtingen meenemen.

Officiële bronnen, geraadpleegd 2 november 2026:
- [NumPy 2.3.5](https://pypi.org/project/numpy/2.3.5/)
- [Pillow 12.3.0](https://pypi.org/project/pillow/12.3.0/)
- [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)
- [Ultralytics-licentieuitleg](https://www.ultralytics.com/license)

## Privéonderzoeksgegevens

Privébeelden, identiteitssleutel, ondertekende rechtenverklaring en
onderzoeksresultaten worden niet meegeleverd. De rechten op afbeeldingen staan
los van de licentie van de programmacode. De code mag die gegevens niet
automatisch openbaar maken.

## Eerste gebruik van YOLO26n-seg

Uitgangspunt is de door de projecteigenaar gemelde schriftelijke bevestiging:
de volledige toepasselijke projectcode moet vóór of uiterlijk bij het eerste
gebruik openbaar zijn. De privébrief is niet onderzocht of meegeleverd.

Deze voorbereide map gebruikt nog geen YOLO en geeft geen zelfstandige vrijstelling
voor latere code. Na afzonderlijke toestemming:
1. Publiceer de gecontroleerde volledige toepasselijke broncode met AGPL-tekst.
2. Controleer dat deze broncode publiek en zonder inloggen bereikbaar is.
3. Stel ook alle toepasselijke YOLO-integratiecode, scripts en configuratie
   vóór of uiterlijk bij hun eerste gebruik openbaar beschikbaar.
4. Begin pas daarna, volgens de bevestigde afspraak en een nieuwe testopdracht,
   met installatie en testen van YOLO26n-seg.

Dit is de gekozen route volgens de instructie van de eigenaar, geen algemene
uitspraak dat elk privégebruik van alle AGPL-programma's verboden is.

## Optionele YOLO/DINOv2-afhankelijkheden

`requirements-yolo-dinov2.txt` noemt uitsluitend directe, vastgezette versies van PyTorch en Ultralytics plus de bestaande projectvereisten. Het is geen volledige hash-lock van alle transitieve pakketten. Deze optionele pakketten worden niet geïnstalleerd bij de basisinstallatie en er worden geen modelgewichten meegeleverd. Controleer vlak vóór installatie opnieuw de pakketmetadata, licenties en voorwaarden van de exacte versies en hun transitieve afhankelijkheden. De DINOv2-broncode en gewichten vallen onder hun eigen Apache-2.0-voorwaarden; de betreffende bron en gewichten zijn niet in deze map opgenomen.

De projecteigenaar meldt schriftelijke bevestiging van Ultralytics voor de gekozen AGPL-route. Die privébevestiging is niet bijgevoegd en is hier niet geverifieerd. Deze handleiding presenteert dit daarom als een door de eigenaar gemelde afspraak, niet als onafhankelijk vastgestelde juridische toestemming. Volgens de officiële Ultralytics-licentie-informatie moet vóór gebruik opnieuw worden vastgesteld dat de volledige toepasselijke broncode publiek beschikbaar is en aan de gekozen voorwaarden voldoet.
