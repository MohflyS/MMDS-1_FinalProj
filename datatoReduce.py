from pathlib import Path as path

# Read the Path

path_transactions = path.home() / "Desktop" / "Data" / "transactions.csv"
path_reduced = path.home() / "Desktop" / "datatoreduced.csv"
id_list = []

# Reduce the Transactions

with open(path_reduced, "w") as outfile:
  for index, line in enumerate(open(path_transactions)):
    if index == 0:
      outfile.write(line)
    elif line.split(",")[0] not in id_list:
      outfile.write(line)
      id_list.append(line.split(",")[0])
    if index == 1000000:
      break