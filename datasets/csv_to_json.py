import csv
import json

datasets = [('ad.csv', 'ads.ad'),
            ('category.csv', 'ads.category'),
            ('location.csv', 'users.location'),
            ('user.csv', 'users.user'), ]


def replaces(row):
    if "is_published" in row:
        row["is_published"] = True if row["is_published"] == "TRUE" else False
    if "location_id" in row:
        row["locations"] = [row.pop("location_id")]
    return row


def csv_to_json(csv_file, model):
    with open(csv_file, encoding='utf-8') as f:
        result = [
            {"model": model, "fields": replaces(row)}
            for row in csv.DictReader(f)
        ]
    with open(csv_file.replace(".csv", ".json"), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    for dataset in datasets:
        csv_to_json(*dataset)
