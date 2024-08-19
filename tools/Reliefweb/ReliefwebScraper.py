"""
Disaster Data Extraction and Storage

This script retrieves disaster data from the ReliefWeb API for specific disaster types,
processes the data, and stores it in an Excel file.
"""

import os
import json
import requests
import pandas as pd
from anyascii import anyascii

# pylint: disable=unspecified-encoding bare-except


def get_disaster_data():
    """
    Get disaster data from the ReliefWeb API and save it to a JSON file.

    Returns:
        list: List of dictionaries containing disaster data.
    """
    url = "https://api.reliefweb.int/v1/reports?appname=jasperkoenig"
    results = []
    for disaster_name in [
        "Cold Wave",
        "Complex Emergency",
        "Drought",
        "Earthquake",
        "Epidemic",
        "Extratropical Cyclone",
        "Fire",
        "Flash Flood",
        "Flood",
        "Heat Wave",
        "Insect Infestation",
        "Land Slide",
        "Mud Slide",
        "Other",
        "Severe Local Storm",
        "Snow Avalanche",
        "Storm Surge",
        "Technological Disaster",
        "Tropical Cyclone",
        "Tsunami",
        "Volcano",
        "Wild Fire",
    ]:
        json_body = {
            "limit": 1000,
            "fields": {"include": ["id", "title", "body", "disaster_type"]},
            "preset": "latest",
            "filter": {
                "operator": "AND",
                "conditions": [
                    {"field": "disaster_type.name", "value": [f"{disaster_name}"]},
                    {"field": "language.name", "value": ["English"]},
                    {"field": "body"},
                    {"field": "format.id", "value": [10]},
                ],
            },
        }

        response = requests.post(url, json=json_body)
        data = response.json()
        results.extend(data["data"])

    # save data to file
    try:
        with open("data/disaster_reports.json", "w") as f:
            f.write(str(results))
    except:
        print("Error saving data to file")
        try:
            with open("data/disaster_reports.json", "w") as f:
                json.dump(results, f)
        except:
            print("Error saving data to file")

    return results


def store_in_excel(reponse):
    """
    This function takes the processed disaster data and stores it in an Excel file.
    Processed data includes information such as ID, title, body, disaster names, codes,
    URL, and UNDRR categories. The processed data is saved to the file "data/disaster_data_500_ea.xlsx".

    Args:
        response (list): List of dictionaries containing processed disaster data.

    Returns:
        None
    """
    data = reponse  # ["data"]
    # print(data[0])
    processed_data = []
    ids = []
    for i, item in enumerate(data):
        # try:
        id = item["fields"]["id"]
        if id in ids:
            continue
        ids.append(id)
        title = item["fields"]["title"]
        body = item["fields"]["body"]
        disaster_names = [d["name"] for d in item["fields"]["disaster_type"]]
        disaster_codes = [d["code"] for d in item["fields"]["disaster_type"]]
        UNDRR_categories = []

        for code in disaster_codes:
            mh_codes = ["CW", "DR", "EC", "FL", "HT", "MS", "ST", "AV", "SS", "TC", "TS"]
            gh_codes = ["EQ", "LS", "VO"]
            bi_codes = ["EP", "IN"]
            en_codes = ["FF", "WF"]
            tl_codes = ["AC"]

            if code in mh_codes and "MH" not in UNDRR_categories:
                UNDRR_categories.append("MH")
            if code in gh_codes and "GH" not in UNDRR_categories:
                UNDRR_categories.append("GH")
            if code in bi_codes and "BI" not in UNDRR_categories:
                UNDRR_categories.append("BI")
            if code in en_codes and "EN" not in UNDRR_categories:
                UNDRR_categories.append("EN")
            if code in tl_codes and "TL" not in UNDRR_categories:
                UNDRR_categories.append("TL")

            if code == "FR" and "TL" not in UNDRR_categories:
                if any(
                    keyword in body for keyword in ["chemical", "city", "building", "industrial"]
                ):
                    UNDRR_categories.append("TL")
            if code == "FL" and "reservoir" in body and "TL" not in UNDRR_categories:
                UNDRR_categories.append("TL")
            if code == "TS" and "GH" not in UNDRR_categories:
                if any(keyword in body for keyword in ["earthquake", "volcano"]):
                    UNDRR_categories.append("GH")
        href = item["href"]

        processed_data.append(
            [
                id,
                anyascii(title),
                anyascii(body),
                anyascii(", ".join(disaster_names)),
                anyascii(", ".join(disaster_codes)),
                anyascii(href),
                anyascii(", ".join(UNDRR_categories) if UNDRR_categories else "Other"),
            ]
        )
        # except Exception as e:
        #     print(f"Error {e} processing item {i}: {item}")

    df = pd.DataFrame(
        processed_data,
        columns=[
            "ID",
            "Title",
            "Body",
            "Disaster Names",
            "Disaster Codes",
            "URL",
            "UNDRR Categories",
        ],
    )
    df.to_excel("data/disaster_data_500_ea.xlsx", index=False)


def main():
    """
    This function serves as the main entry point for the script. It checks if the file
    'data/disaster_reports.json' exists, and if so, loads the existing data. Otherwise,
    it calls the 'get_disaster_data' function to fetch fresh data from the ReliefWeb API.
    Finally, it invokes the 'store_in_excel' function to process and store the data in an Excel file.

    Returns:
        None
    """
    if os.path.isfile("data/disaster_reports.json"):
        with open("data/disaster_reports.json", "r") as f:
            disaster_data = json.load(f)
    else:
        disaster_data = get_disaster_data()
    store_in_excel(disaster_data)


if __name__ == "__main__":
    main()
