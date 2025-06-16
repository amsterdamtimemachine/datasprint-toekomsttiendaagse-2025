import sys

import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


def query(q, endpoint, OFFSET=0, LIMIT=10000):

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(q + f" OFFSET {OFFSET} LIMIT {LIMIT}")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    df = pd.DataFrame(results["results"]["bindings"])
    df = df.apply(lambda s: s.map(lambda x: x["value"] if not pd.isna(x) else ""))

    if len(df) == LIMIT:

        OFFSET += LIMIT

        new_df = query(q, endpoint, OFFSET, LIMIT)
        df = pd.concat([df, new_df])

    return df


if __name__ == "__main__":

    qfile = sys.argv[1]
    target = sys.argv[2]
    endpoint = sys.argv[3]

    if len(sys.argv) != 4:
        print(
            "Usage: python query.py <query_file> <target_file> <endpoint_url>\n"
            "Example: python query.py query.rq target.csv https://api.lod.uba.uva.nl/datasets/ATM/ATM-KG/services/ATM-KG/sparql"
        )
        sys.exit(1)

    with open(qfile, "r") as f:
        q = f.read()

    df = query(q, endpoint)

    df.to_csv(target, index=False)
