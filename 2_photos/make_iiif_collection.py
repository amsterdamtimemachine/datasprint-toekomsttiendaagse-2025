import os
import json
import pandas as pd
import iiif_prezi3
import geojson
import shapely.wkt

iiif_prezi3.config.configs["helpers.auto_fields.AutoLang"].auto_lang = "nl"

PREFIX = (
    "https://amsterdamtimemachine.github.io/datasprint-toekomsttiendaagse-2025/iiif/"
)


def process_saa():
    """
    Process the SAA (Stadsarchief Amsterdam) collection.

    Photos in this collection have metadata on the photo (Canvas) level.
    Due to missing inventory number or other grouping information, the
    photos are grouped by year-month.

    Example DataFrame structure:
        access,context,record,digitalDocument,title,inventory,creationDate,startDate,endDate,description,file_name,iiif_info_json
        https://id.archief.amsterdam/resources/records/10868a3b-782e-a51a-66ce-d35d4441db81/accessibility_and_rights,https://id.archief.amsterdam/resources/records/10868a3b-782e-a51a-66ce-d35d4441db81/context,https://id.archief.amsterdam/10868a3b-782e-a51a-66ce-d35d4441db81,https://id.archief.amsterdam/resources/records/10868a3b-782e-a51a-66ce-d35d4441db81/assets/a27ae9af-8d3f-3ecf-aa5a-f4c1a10033a3,Amstel 29 (zijgevel),https://id.archief.amsterdam/d35793bb-d290-0e1b-e053-b784100abd1f,https://dataruimteamsterdam.nl/.well-known/genid/0e44ac20e1594dd4a1e806b40ca76e5e,1954-11-01,1954-11-30,Hoek Waterlooplein,010009003214.jp2,https://stadsarchiefamsterdam.memorix.io/resources/records/media/10868a3b-782e-a51a-66ce-d35d4441db81/iiif/3/57358964/info.json

        item,record,address,wktAddress,addressLabel,street,wktStreet,streetLabel
        https://ams-migrate.memorix.io/resources/records/1294d8bf-adca-efdc-c453-c6cbb2e08406,https://id.archief.amsterdam/1294d8bf-adca-efdc-c453-c6cbb2e08406,https://adamlink.nl/geo/address/A204950,POINT(4.9075602 52.3841182),Buiksloterweg 9,https://adamlink.nl/geo/street/buiksloterweg/638,"MULTILINESTRING((4.903992072716 52.382597372813,4.9053939252784 52.383207200572,4.9061256692709 52.383531511925,4.9061908277037 52.383571915579,4.9062728650064 52.383645974706),(4.9033849141527 52.382747936167,4.9034604521045 52.382729199843,4.9036535236217 52.382660423661,4.9038076624576 52.382608699671,4.9039241155898 52.382593060039,4.903992072716 52.382597372813),(4.9033152843175 52.382293890435,4.903992072716 52.382597372813),(4.9030862184522 52.382577558282,4.903107560001 52.38263134694,4.9031575266184 52.382677190644,4.9032492044971 52.382719187294,4.9033280159975 52.382735615265,4.9033849141527 52.382747936167),(4.9033152843175 52.382293890435,4.9031160449366 52.382456858758,4.9030846016468 52.382523850255,4.9030862184522 52.382577558282),(4.907185386924 52.383962421208,4.9072293522078 52.383971587081,4.907346852407 52.383972063234,4.9073909149825 52.383972241761,4.9074348803187 52.383981407558,4.9075373041424 52.384017773163,4.9082097273237 52.384317088141,4.9082535960973 52.38433524092,4.9082680896008 52.384353274891,4.9081912532737 52.384667532879),(4.9068306470876 52.384167699476,4.9069783016422 52.384096396863,4.9070522260589 52.384051758202,4.907185386924 52.383962421208),(4.9062728650064 52.383645974706,4.9064249489675 52.383653755396,4.9064836012082 52.383662981171,4.9065714334945 52.383690300707,4.907185386924 52.383962421208),(4.9063847669168 52.384559550424,4.906538848323 52.384540537807,4.9066601654178 52.384568451538,4.9070748187808 52.384746085105,4.9076444043213 52.38497988852,4.9077470249807 52.384998279371,4.9078202699815 52.38501655123,4.9089361606312 52.385057013574,4.9091122214773 52.385075699795,4.9093469372192 52.38510361011,4.9095374927022 52.385140329534,4.9097573275866 52.385186154367,4.9099183143989 52.38524072932,4.9101816339545 52.385340654654,4.9115119735261 52.385930204393,4.9126226961973 52.386455945477,4.9129001406367 52.386609847334,4.9129585097633 52.386646031762),(4.9062728650064 52.383645974706,4.9062774899491 52.383707082755,4.9063050129272 52.383877960455,4.906316191632 52.38420156234,4.9063290274042 52.384372380377,4.9063569408252 52.384507308908,4.9063847669168 52.384559550424),(4.914302367977 52.387352443614,4.9153671800678 52.388057728641,4.9157171330646 52.388301789303,4.9159503416772 52.388473483119,4.9165337050414 52.388871260129,4.9171022942829 52.389277963229,4.9171896678708 52.389350211308,4.9173935089377 52.389521785669,4.9176554430527 52.389756503631),(4.9129585097633 52.386646031762,4.9131788360814 52.386646913807,4.9132520860541 52.386665182305,4.9136175688729 52.386828422413,4.9137344049402 52.386891803245,4.9138805224503 52.386964288657,4.9139681740012 52.387009577275,4.9140119518864 52.387036715203,4.914302367977 52.387352443614),(4.9129585097633 52.386646031762,4.9130461597415 52.386691321063,4.913147921815 52.386790592815,4.9134666510039 52.387205301013),(4.9139616510915 52.387620712767,4.9141822699263 52.387594631092,4.9142556177466 52.387603911681,4.9143141809989 52.387622120864,4.9143726484559 52.387649317304,4.914897518472 52.388019905975,4.9154952685722 52.388444708553,4.9161803057841 52.388950744203,4.9168364566596 52.389411722758,4.9169093313767 52.389465938133),(4.9135499821915 52.387655017803,4.9139616510915 52.387620712767),(4.9169093313767 52.389465938133,4.9170408684859 52.389529374009,4.9175383082054 52.389720088548,4.9176554430527 52.389756503631),(4.9176554430527 52.389756503631,4.9178155998447 52.389891953398,4.9179175702024 52.389973246434,4.9179753771369 52.390063352089,4.9181912520007 52.390486627241,4.918249155224 52.390567745469,4.9182781544448 52.390603810929,4.9183217484155 52.390648921821,4.9183947220184 52.390694148988,4.9185258848589 52.390793532344,4.9186570482874 52.390892915554,4.9187300226341 52.390938142512,4.9187443326228 52.390974149754,4.9189906433478 52.391298679453,4.9191790512686 52.391542090892,4.9192225522063 52.39159618873,4.9192657686629 52.391677248404,4.9193231062969 52.391812289795,4.9194816636714 52.392100521087,4.9196830619722 52.392505760795,4.9198845586861 52.392902012847,4.9201005602359 52.393316297027,4.9203167551234 52.39371260622,4.9205181683452 52.39411784439,4.9207195852401 52.394523082188,4.920935696988 52.394928377445,4.9212671704599 52.39554084207),(4.9206467310898 52.399478251971,4.9204048921319 52.399294283837,4.9203173990664 52.399231025521,4.9202591020554 52.399185857516,4.9202302850012 52.399131818054,4.9201868701591 52.399068733388,4.9201159645868 52.398825787411,4.9201169116836 52.398735914693,4.9201328353049 52.398619138089,4.9201634512047 52.398502419407,4.9201934987845 52.398439624351,4.9202384279684 52.398358912659,4.9202832623137 52.398287188222,4.9204322674108 52.398090047243,4.920773877045 52.397740874627,4.9211895082031 52.397338066362,4.9214716775967 52.397051571386,4.921575748105 52.396935141096,4.9216055094076 52.396899307488,4.9217398121713 52.396702107046,4.9217547870553 52.396675202943,4.9217551645411 52.396639253833,4.9217555420262 52.396603304723,4.9217273854526 52.396486354652,4.9216849149073 52.396333397722,4.9215410196844 52.396045227354,4.9213680267596 52.395729979409,4.9212671704599 52.39554084207))",Buiksloterweg
    """
    df_saa = pd.read_csv("data/SAA.csv")
    df_saa_unavailable = pd.read_csv("data/SAA_Unavailable.csv")

    df_atm = pd.read_csv("data/SAA_Adamlink.csv")

    # Filter out unavailable records
    df_saa = df_saa[~df_saa["record"].isin(df_saa_unavailable["record"])]

    # intersection
    df = pd.merge(df_saa, df_atm, on="record", how="inner")

    df["year"] = pd.to_datetime(df["startDate"], errors="coerce").dt.year
    df["yearMonth"] = pd.to_datetime(df["startDate"], errors="coerce").dt.strftime(
        "%Y-%m"
    )

    df.sort_values("startDate", inplace=True)

    collection = iiif_prezi3.Collection(
        id=f"{PREFIX}saa.json", label="Stadsarchief Amsterdam (SAA)"
    )

    for year, year_df in df.groupby("year"):

        os.makedirs(f"iiif/saa/{year}", exist_ok=True)
        year_collection = iiif_prezi3.Collection(
            id=f"{PREFIX}saa/{year}.json",
            label=f"{year}",
        )

        manifests = []

        year_df.sort_values("startDate", inplace=True)

        for yearMonth, yearMonth_df in year_df.groupby("yearMonth"):

            yearMonth_df.sort_values("startDate", inplace=True)

            startDate = yearMonth_df["startDate"].iloc[0]
            month = pd.to_datetime(startDate, errors="coerce").strftime("%m")

            manifest = iiif_prezi3.Manifest(
                id=f"{PREFIX}saa/{year}/{month}.json", label=yearMonth
            )

            for record_uri, record_df in yearMonth_df.groupby("record"):
                print(f"Processing record: {record_uri}")

                title = record_df["title"].iloc[0]
                description = record_df["description"].iloc[0]
                beeldbank_uri = record_uri.replace(
                    "https://id.archief.amsterdam/",
                    "https://beta.archief.amsterdam/detail/",
                )

                # Create a NavPlace if address and street are available

                addresses, addressesLabels, addressesWkt = (
                    record_df["address"].dropna().unique(),
                    record_df["addressLabel"].dropna().unique(),
                    record_df["wktAddress"].dropna().unique(),
                )
                streets, streetsLabels, streetsWkt = (
                    record_df["street"].dropna().unique(),
                    record_df["streetLabel"].dropna().unique(),
                    record_df["wktStreet"].dropna().unique(),
                )

                features = []
                if addresses.size > 0:
                    for address, addressLabel, addressWkt in zip(
                        addresses, addressesLabels, addressesWkt
                    ):
                        geometry = shapely.wkt.loads(addressWkt)
                        feature = geojson.Feature(
                            geometry=geometry,
                            properties={
                                "title": addressLabel,
                                "url": address,
                            },
                        )

                        features.append(feature)

                    navPlace = iiif_prezi3.NavPlace(features=features)
                elif streets.size > 0:
                    # If no addresses, use streets
                    for street, streetLabel, streetWkt in zip(
                        streets, streetsLabels, streetsWkt
                    ):
                        geometry = shapely.wkt.loads(streetWkt)
                        feature = geojson.Feature(
                            geometry=geometry,
                            properties={
                                "title": streetLabel,
                                "url": street,
                            },
                        )
                        features.append(feature)

                    navPlace = iiif_prezi3.NavPlace(features=features)
                else:
                    navPlace = None

                iiif_info_json = record_df["iiif_info_json"].iloc[0]
                file_name = record_df["file_name"].iloc[0]

                canvas_id = f"{PREFIX}saa/{year}/{month}/{file_name}/canvas"
                manifest.make_canvas_from_iiif(
                    url=iiif_info_json,
                    id=canvas_id,
                    anno_page_id=f"{canvas_id}/p0/page",
                    anno_id=f"{canvas_id}/p0/page/anno",
                    label=title,
                    navPlace=navPlace,
                    metadata=[
                        iiif_prezi3.KeyValueString(
                            label="Titel",
                            value={"nl": [title]},
                        ),
                        iiif_prezi3.KeyValueString(
                            label="Beschrijving",
                            value={
                                "nl": [description if pd.notna(description) else ""]
                            },
                        ),
                        # datum
                        iiif_prezi3.KeyValueString(
                            label="Datum (start)",
                            value={"nl": [startDate if pd.notna(startDate) else ""]},
                        ),
                        iiif_prezi3.KeyValueString(
                            label="Datum (einde)",
                            value={
                                "nl": [
                                    (
                                        record_df["endDate"].iloc[0]
                                        if pd.notna(record_df["endDate"].iloc[0])
                                        else ""
                                    )
                                ]
                            },
                        ),
                        # Addresses with hyperlinks
                        iiif_prezi3.KeyValueString(
                            label="Adres",
                            value={
                                "nl": [
                                    f"<a href='{address}'>{addressLabel}</a>"
                                    for address, addressLabel in zip(
                                        addresses, addressesLabels
                                    )
                                ]
                            },
                        ),
                        # Streets with hyperlinks
                        iiif_prezi3.KeyValueString(
                            label="Straat",
                            value={
                                "nl": [
                                    f"<a href='{street}'>{streetLabel}</a>"
                                    for street, streetLabel in zip(
                                        streets, streetsLabels
                                    )
                                ]
                            },
                        ),
                        # URI Beeldbank
                        iiif_prezi3.KeyValueString(
                            label="URI (Beeldbank)",
                            value={
                                "nl": [f'<a href="{beeldbank_uri}">{beeldbank_uri}</a>']
                            },
                        ),
                        iiif_prezi3.KeyValueString(
                            label="URI",
                            value={"nl": [f'<a href="{record_uri}">{record_uri}</a>']},
                        ),
                        iiif_prezi3.KeyValueString(
                            label="Bestandsnaam",
                            value={"nl": [file_name]},
                        ),
                    ],
                )

            manifests.append(manifest)

            with open(f"iiif/saa/{year}/{month}.json", "w") as outfile:
                # Edit context
                manifest_jsonld = manifest.jsonld_dict()
                manifest_jsonld["@context"] = [
                    "http://iiif.io/api/extension/navplace/context.json",
                    "http://iiif.io/api/presentation/3/context.json",
                ]

                json.dump(
                    manifest_jsonld,
                    outfile,
                    indent=2,
                )

        for manifest in manifests:
            year_collection.add_item(manifest)

        with open(f"iiif/saa/{year}.json", "w") as outfile:
            outfile.write(year_collection.json(indent=2))

        collection.add_item(year_collection)

    with open("iiif/saa.json", "w") as outfile:
        outfile.write(collection.json(indent=2))

    return collection


def process_nha():
    """
    Process the NHA (Noord-Holland Archief) collection.

    Photos in this collection have metadata on the report level, with
    individual photos grouped under each report.

    Example DataFrame structure:
        photo,hisvis_concept,report,identifier,imageObject,hisvis_conceptLabel,hisvis_gtaa,contentUrl,iiif_info_json,title,date,place,placeName,wkt,placeWikidata,concept,conceptName,gtaa
        https://hdl.handle.net/21.12102/5967940a-f645-8d26-ee75-f2caef1038d1,https://digitaalerfgoed.poolparty.biz/nha/57c77c9c-655f-ac10-9b42-d2640f84ed62,https://data.noord-hollandsarchief.nl/collection/FotopersbureauDeBoer/report/ed7a3e04-a999-1485-a82f-6e829e551b0b,NL-HlmNHA_1478_01190A02_05,https://maior-images.memorix.nl/ranh/iiif/14ba6201-cdd9-9056-13b9-6c96d26d6641,Fabriek,http://data.beeldengeluid.nl/gtaa/28194,https://maior-images.memorix.nl/ranh/iiif/14ba6201-cdd9-9056-13b9-6c96d26d6641/full/max/0/default.jpg,https://maior-images.memorix.nl/ranh/iiif/14ba6201-cdd9-9056-13b9-6c96d26d6641/info.json,Radar - Schiphol - Brandweer,1954-12,https://data.noord-hollandsarchief.nl/collection/FotopersbureauDeBoer/location/1039c7ff-d922-549c-a53c-a9f86c530712,Luchthaven Schiphol,POINT(4.7641694444444 52.3081),http://www.wikidata.org/entity/Q9694,https://digitaalerfgoed.poolparty.biz/nha/6c291529-1d3b-6d7a-8334-dc83fea8f3ba,Radar,http://data.beeldengeluid.nl/gtaa/27107

    Args:
        df (pd.DataFrame): The input DataFrame containing the NHA collection data.
    """

    df = pd.read_csv("data/NHA.csv").sort_values(["date", "identifier"])

    collection = iiif_prezi3.Collection(
        id=f"{PREFIX}nha.json",
        label="Fotopersbureau De Boer - Noord-Holland Archief (NHA)",
    )

    manifests = []

    for report_uri, report_df in df.groupby("report"):

        title = report_df["title"].iloc[0]
        date = report_df["date"].iloc[0]
        place = report_df["placeName"].iloc[0]
        place_wikidata = report_df["placeWikidata"].iloc[0]
        wkt = report_df["wkt"].iloc[0]

        if pd.notna(wkt):
            geometry = shapely.wkt.loads(wkt)
            feature = geojson.Feature(
                geometry=geometry,
                properties={
                    "title": place,
                    "url": place_wikidata if pd.notna(place_wikidata) else "",
                },
            )

            navPlace = iiif_prezi3.NavPlace(features=[feature])
        else:
            navPlace = None

        concepts = [i for i in report_df["conceptName"].unique() if pd.notna(i)]

        gtaas = [i for i in report_df["gtaa"].unique() if pd.notna(i)]

        report_identifier = report_uri.replace(
            "https://data.noord-hollandsarchief.nl/collection/FotopersbureauDeBoer/report/",
            "",
        )

        manifest = iiif_prezi3.Manifest(
            id=f"{PREFIX}nha/{report_identifier}.json",
            label=title + f" ({date})",
            metadata=[
                iiif_prezi3.KeyValueString(label="Titel", value={"nl": [title]}),
                iiif_prezi3.KeyValueString(label="Datum", value={"nl": [date]}),
                iiif_prezi3.KeyValueString(
                    label="Plaats",
                    value={
                        "nl": [
                            (
                                f'<a href="{place_wikidata}">{place}</a>'
                                if pd.notna(place_wikidata)
                                else place
                            )
                        ]
                    },
                ),
                iiif_prezi3.KeyValueString(
                    label="Concept",
                    value={"nl": [", ".join(concepts)]},
                ),
                iiif_prezi3.KeyValueString(
                    label="GTAA",
                    value={"nl": [", ".join(gtaas)]},
                ),
            ],
        )

        if navPlace:
            manifest.navPlace = navPlace

        for photo_uri, photo_df in report_df.groupby("photo"):

            print(f"Processing photo: {photo_uri}")

            identifier = photo_df["identifier"].iloc[0]
            iiif_info_json = photo_df["iiif_info_json"].iloc[0]

            canvas_id = f"{PREFIX}{report_identifier}/{identifier}/canvas"
            manifest.make_canvas_from_iiif(
                url=iiif_info_json,
                id=canvas_id,
                anno_page_id=f"{canvas_id}/p0/page",
                anno_id=f"{canvas_id}/p0/page/anno",
                label=title,
                metadata=[
                    iiif_prezi3.KeyValueString(
                        label="URI (Beeldbank)",
                        value={"nl": [f'<a href="{photo_uri}">{photo_uri}</a>']},
                    )
                ],
            )

        manifests.append(manifest)

        with open(f"iiif/nha/{report_identifier}.json", "w") as outfile:

            # Edit context
            manifest_jsonld = manifest.jsonld_dict()
            manifest_jsonld["@context"] = [
                "http://iiif.io/api/extension/navplace/context.json",
                "http://iiif.io/api/presentation/3/context.json",
            ]

            json.dump(
                manifest_jsonld,
                outfile,
                indent=2,
            )

    # Add all manifests to the collection
    for manifest in manifests:
        collection.add_item(manifest)

    with open("iiif/nha.json", "w") as outfile:
        outfile.write(collection.json(indent=2))

    return collection


def process_iisg():
    pass


def process_na():
    pass


def make_collection(target_file_path: str):

    collection = iiif_prezi3.Collection(
        id=f"{PREFIX}collection.json",
        label="Selectie foto's voor de Toekomsttiendaagse 2025 datasprint van de Amsterdam Time Machine.",
    )

    # SAA
    subcollection_saa = process_saa()
    collection.add_item(subcollection_saa)

    # NHA
    subcollection_nha = process_nha()
    collection.add_item(subcollection_nha)

    # Save!
    with open(target_file_path, "w") as outfile:
        outfile.write(collection.json(indent=2))


if __name__ == "__main__":

    make_collection("iiif/collection.json")
