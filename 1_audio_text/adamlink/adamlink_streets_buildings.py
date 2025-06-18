import pandas as pd


from SPARQLWrapper import SPARQLWrapper, JSON
from shapely import wkt


def main(
    queryfile: str,
    endpoint="https://api.lod.uba.uva.nl/datasets/ATM/ATM-KG/services/ATM-KG/sparql",
):

    with open(queryfile, "r") as file:
        query = file.read()

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    entries = []
    for result in results["results"]["bindings"]:

        wktString = result["wkt"]["value"]

        try:  # quick and dirty
            geometry = wkt.loads(wktString)
            latitude = geometry.centroid.y
            longitude = geometry.centroid.x
        except Exception as e:
            latitude = None
            longitude = None

        entry = {
            "adamlink_uri": result["adamlink_uri"]["value"],
            "type": result["type"]["value"],
            "preflabel": result["preflabel"]["value"],
            "wkt": wktString,
            "wikidata": result.get("wikidata", {}).get("value", None),
            "since_min": result.get("since_min", {}).get("value", None),
            "until_min": result.get("until_min", {}).get("value", None),
            "since_max": result.get("since_max", {}).get("value", None),
            "until_max": result.get("until_max", {}).get("value", None),
            "latitude": latitude,
            "longitude": longitude,
        }
        entries.append(entry)

    df = pd.DataFrame(entries)

    # save dataframe
    df.to_csv("adamlink_streets_buildings.csv", index=False)


if __name__ == "__main__":

    queryfile = "adamlink_streets_buildings.rq"
    main(queryfile)
