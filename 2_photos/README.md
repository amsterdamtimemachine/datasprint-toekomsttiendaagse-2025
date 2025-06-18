# Photos

- [Photos](#photos)
  - [Introductie](#introductie)
  - [Collecties](#collecties)
    - [Selectie](#selectie)
      - [Stadsarchief Amsterdam (SAA)](#stadsarchief-amsterdam-saa)
      - [Nationaal Archief (NA)](#nationaal-archief-na)
      - [Noord-Hollands Archief (NHA)](#noord-hollands-archief-nha)
      - [IISG](#iisg)
    - [Format](#format)
    - [Verrijkingen](#verrijkingen)
      - [Alternatief (experimenteel)](#alternatief-experimenteel)

## Introductie

In deze sessie gaan we aan de slag met het verrijken van historische foto's uit verschillende collecties. We richten ons met name op het toevoegen van geolocaties en classificaties aan de foto's, zodat ze beter vindbaar en bruikbaar worden in de context van de Amsterdam Time Machine en andere toepassingen.

Bekijk de collectie in de Theseus Viewer:

- [`https://theseusviewer.org/?iiif-content=https%3A%2F%2Fstreetlife.amsterdamtimemachine.nl%2Fdatasprint-toekomsttiendaagse-2025%2Fiiif%2Fcollection.json`](https://theseusviewer.org/?iiif-content=https%3A%2F%2Fstreetlife.amsterdamtimemachine.nl%2Fdatasprint-toekomsttiendaagse-2025%2Fiiif%2Fcollection.json)

## Collecties

### Selectie

#### Stadsarchief Amsterdam (SAA)

We gaan ervan uit dat alle foto's in de Beeldbank van het Stadsarchief over Amsterdam gaan. Deze zijn ook al helemaal voorzien van geolocaties. Het enige dat nog ontbreekt is een classificatiesysteem zodat we ook weten waarover foto's gaan.

**Taak:**

- Voeg GTAA-classificatie toe aan de foto's.

**Bron**:

- Amsterdam City Archives Open API - OAI-PMH endpoint: https://id.archief.amsterdam/oai-pmh?verb=ListRecords&metadataPrefix=rdf&set=recordType:Image
- Amsterdam Time Machine Beeldbank dataset: https://lod.uba.uva.nl/ATM/Beeldbank-SAA/

**Selectiecriteria**:

- Er zit geen copyright op de foto's. Dit vertaalt zich naar het ontbreken van de `schema:copyrightNotice` property in de metadata.
- Afbeeldingen zijn opgenomen in een eerdere versie van de Beeldbank dataset, gehost door de Amsterdam Time Machine: https://lod.uba.uva.nl/ATM/Beeldbank-SAA/, die volledig is gelinkt met Adamlink.
- De afbeeldingen zijn daadwerkelijk opvraagbaar in het IIIF-endpoint en geven geen standaardafbeelding terug van 500x500 pixels.

**Query's**:

- [`SAA.rq`](queries/SAA.rq)
- [`SAA-Adamlink.rq`](queries/SAA-Adamlink.rq)

#### Nationaal Archief (NA)

Het SPARQL-endpoint van het Nationaal Archief werkt op het moment van schrijven niet goed mee. We laten deze collectie daarom jammer genoeg even buiten beschouwing.

Een SPARQL-query die we hadden kunnen gebruiken om Amsterdamse foto's te selecteren is de volgende: `NA.rq`(queries/NA.rq).

**Taak:**

- Voeg geolocaties toe aan de foto's.

**Endpoint**:

- https://service.archief.nl/sparql

**Selectiecriteria**:

- Afbeeldingen zijn geclassificeerd met GTAA-termen 'demonstraties', 'gebouwen', 'spandoeken', 'bijeenkomsten', 'herdenkingen', 'betogingen', 'bouwactivteiten', 'publiek' (via `dcterms:subject` property)
- Afbeeldingen zijn gelinkt aan de GTAA-term voor Amsterdam (via `http://data.beeldengeluid.nl/gtaa/31586`)
- Afbeeldingen zijn getagd als 'Direct beschikbaar' (maar hoe filteren we hierop? Het lijkt alsof alle toegankelijkheidstypes aan dezelde URI gekoppeld zijn in het endpoint)

**Query's**:

- [`NA.rq`](queries/NA.rq)

#### Noord-Hollands Archief (NHA)

Met de collectie van Fotopersbureau De Boer van het Noord-Hollands Archief (NHA) gaan we aan de slag om classificaties en geolocaties toe te voegen aan het Amsterdamse deel van de foto's. Deze collectie bevat een schat aan historische persfoto's die we van gedetailleerdere metadata willen voorzien.

**Taak:**

- Classificaties en geolocaties toevoegen aan de foto's

**Bron**:

- van Wissen, L., Vriend, N., Nijssen, A., Vereecken, L. and den Engelse, M. (2025) ‘FAIR Photos – Transforming a Collection of Two Million Historical Press Photos into Five Star Data’, Journal of Open Humanities Data, 11(1), p. 1. Available at: https://doi.org/10.5334/johd.271.

**Selectiecriteria**:

Voor nu hebben we alles binnen Amsterdam (via een geoquery) geselecteerd, omdat het NHA eerder al geolocatieinformatie aan de fotocollectie heeft toegevoegd.

Selecteren op classificatie zou kunnen door te filteren op specifieke NHA-De-Boer termen en een set van andere classificaties:

- Subject card keywords: 'Demonstatie' (sic), 'Exterieur', 'Interieur', 'Kraken', 'Bijeenkomsten', 'Gebouwen', 'Open dag en open huis', 'Bouwen, bouwputten', 'Stakingen', 'Eerste paal', 'Huizen en huizenbouw', 'Woonwagens, woonwagenkampen, woonwagenbewoners', 'Pleinen', 'Landgoederen', 'Renovatie', 'Daklozen', 'Herdenkingen', 'Vakbonden', 'Makelaars', 'Festival, festiviteiten en manifestaties', 'Nieuwbouw', 'Huizen en gebouwen', 'Eerst steen',
- HisVis classificaties: 'Binnen', 'Bouwplaats', 'Demonstratie', 'Gebouw', 'Herdenking', 'Huisje', 'Mensenmassa', 'Optocht', 'Woonkamer', 'Woonwijk'

**Query's**:

- [`NHA.rq`](queries/NHA.rq)

#### IISG

De collectie van het IISG bevat in principe foto's over demonstraties en woongerelateerde onderwerpen, maar het is vooralsnog lastig om deze foto's te selecteren. Ook is de route naar een IIIF-opvraagbaar plaatje lastig, omdat dit een extra stap vereist, maar het endpoint ook vaak slechts een plaatje van 500 pixels hoog/breed teruggeeft. We laten deze collectie daarom voor deze Datasprint buiten beschouwing.

**Endpoint**:

- https://druid.datalegend.net/IISG/iisg-kg

**Selectiecriteria**:

- Afbeeldingen gaan over Amsterdam (via marc21 identifier: https://iisg.amsterdam/authority/place/572941)

**Query's**:

- [`IISG.rq`](queries/IISG.rq)

### Format

De collecties zijn gemodelleerd als verzameling van IIIF Collecties en IIIF Manifesten en zijn via deze top-collectie bereikbaar:

- [`https://streetlife.amsterdamtimemachine.nl/datasprint-toekomsttiendaagse-2025/iiif/collection.json`](https://streetlife.amsterdamtimemachine.nl/datasprint-toekomsttiendaagse-2025/iiif/collection.json)

Deze collectie kan mooi doorgebladerd en uitgeplozen worden in de Theseus Viewer:

- [`https://theseusviewer.org/?iiif-content=https%3A%2F%2Fstreetlife.amsterdamtimemachine.nl%2Fdatasprint-toekomsttiendaagse-2025%2Fiiif%2Fcollection.json`](https://theseusviewer.org/?iiif-content=https%3A%2F%2Fstreetlife.amsterdamtimemachine.nl%2Fdatasprint-toekomsttiendaagse-2025%2Fiiif%2Fcollection.json)

### Verrijkingen

Verrijkingen houden we bij in een gedeelde spreadsheet:
* https://edu.nl/kk9np

De verrijkingen in die spreadsheet zetten we om naar Web Annotaties en slaan we op in de AnnotatieContainer van de Datasprint:
* https://annorepo.demo.netwerkdigitaalerfgoed.nl/w3c/atm-toekomsttiendaagse/

#### Alternatief (experimenteel)

De afbeeldingen kunnen ook automatisch geclassificeerd worden met behulp van AI. Een voorbeeld hiervan is te vinden in een Jupyter Notebook dat ook op Google Colab draait: 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amsterdamtimemachine/datasprint-toekomsttiendaagse-2025/blob/main/2_photos/classify_ai.ipynb)

