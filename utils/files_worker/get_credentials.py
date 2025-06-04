import csv


def get_credentials(file_path):
    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

        return rows
