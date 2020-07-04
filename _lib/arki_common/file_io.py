def read_csv_file(filename):
    import csv

    if filename.lower().endswith(".csv"):
        with open(filename) as csv_file:
            reader = csv.reader(csv_file)
            return [
                row for row in reader if row and not row[0].startswith("#")
            ]


def read_txt_file(filename):
    if filename.lower().endswith(".txt"):
        with open(filename) as f:
            lns = f.readlines()
            return [
                x.strip()
                for x in lns
                if x.strip() and not x.strip().startswith("#")
            ]  # ignore empty/commented line
