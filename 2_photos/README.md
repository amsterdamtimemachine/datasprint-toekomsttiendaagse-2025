# Photos

- [Photos](#photos)
  - [Introduction](#introduction)
  - [Collections](#collections)
    - [Obtaining/selecting the collections](#obtainingselecting-the-collections)
      - [Stadsarchief Amsterdam (SAA)](#stadsarchief-amsterdam-saa)
      - [Nationaal Archief (NA)](#nationaal-archief-na)
      - [Noord-Hollands Archief (NHA)](#noord-hollands-archief-nha)
      - [IISG](#iisg)
    - [Format](#format)
      - [Example structure](#example-structure)
    - [Data](#data)
    - [Scripts](#scripts)
  - [Contact](#contact)

## Introduction

<!-- Datasprint goal -->

In particular, we are interested in photos on protest and related to housing.

<!-- GTAA -->

<!-- Challenges -->

## Collections

### Obtaining/selecting the collections

#### Stadsarchief Amsterdam (SAA)

Images of the Amsterdam City Archives are all about Amsterdam.

**Source**:

- Amsterdam City Archives Open API - OAI-PMH endpoint: https://id.archief.amsterdam/oai-pmh?verb=ListRecords&metadataPrefix=rdf&set=recordType:Image
- Amsterdam Time Machine Beeldbank dataset: https://lod.uba.uva.nl/ATM/Beeldbank-SAA/

**Selection criteria**:

- There is no copyright notice on the photos. This translates to the lack of the `schema:copyrightNotice` property in the metadata.
- Images are included in a previous version of the Beeldbank dataset, hosted by the Amsterdam Time Machine: https://lod.uba.uva.nl/ATM/Beeldbank-SAA/, which is fully interlinked with Adamlink.

**Queries**:

- [`SAA.rq`](queries/SAA.rq)
- [`SAA-Adamlink.rq`](queries/SAA-Adamlink.rq)

**Statistics**:

#### Nationaal Archief (NA)

However, the SPARQL-endpoint of the National Archives does not contain the URIs of the GTAA Classification terms. Therefore, we have to search on matching string values (and assume they are unique).

Also, the way the data is modelled does not allow for selection of photos based on the copyright statement. For this reason, we only select photos from Anefo (????), for which we know that they are in the public domain.

**Endpoint**:

- https://service.archief.nl/sparql

**Selection criteria**:

- Images are classified with terms '????', '????', '????', '????', '????', '????', '????' or '????' (via `dcterms:subject` property)
- Images are linked to the GTAA Term for Amsterdam (via `???`)

**Queries**:

- [`NA.rq`](queries/NA.rq)

**Statistics**:

#### Noord-Hollands Archief (NHA)

**Source**:

- van Wissen, L., Vriend, N., Nijssen, A., Vereecken, L. and den Engelse, M. (2025) ‘FAIR Photos – Transforming a Collection of Two Million Historical Press Photos into Five Star Data’, Journal of Open Humanities Data, 11(1), p. 1. Available at: https://doi.org/10.5334/johd.271.

**Selection criteria**:

- Images are geolocated in Amsterdam or a place inside the municipality of Amsterdam (via geoquery)
- Images are taken in reports that mention Amsterdam in its title or description
-

**Queries**:

- [`NHA.rq`](queries/NHA.rq)

**Statistics**:

#### IISG

**Endpoint**:

**Selection criteria**:

- Images are about Amsterdam (via marc21 identifier: ????)
- Images are about protests (via marc21 identifier: ????)

**Queries**:

- [`IISG.rq`](queries/IISG.rq)

**Statistics**:

### Format

We model these photos as a IIIF Collection of Collections (etc.) of Manifests that each represent one or more photos that are related to each other. The way this is structure is modelled is depending on the shape of the collections and how individual photos are represented in the archival systems.

#### Example structure

### Data

### Scripts

- [`query.py`](scripts/query.py) - A script to fetch data from a SPARQL-endpint, taking the LIMIT and OFFSET parameters into account.

## Contact
