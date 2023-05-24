import csv
import json

datasets = [('ads.csv', 'ads.ad'),
            ('categories.csv', 'ads.category')]


def str_to_bool(row, key):
    if key in row:
        row[key] = True if row[key] == "TRUE" else False
    return row


def csv_to_json(csv_file, model):
    with open(csv_file, encoding='utf-8') as f:
        result = [
            {"model": model, "fields": str_to_bool(row, "is_published")}
            for row in csv.DictReader(f)
        ]
    with open(csv_file.replace(".csv", ".json"), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    for dataset in datasets:
        csv_to_json(*dataset)