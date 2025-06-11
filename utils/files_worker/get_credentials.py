import csv


def get_credentials(file_path):
    creds = []
    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["should_xfail"] = row["should_xfail"].strip().lower() == "true"
            creds.append(row)
    return creds
