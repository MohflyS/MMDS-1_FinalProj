from pathlib import Path as path
from datetime import datetime, date
from collections import defaultdict

# Read the Path

path_offers = path.home() / "Desktop" / "Data" / "offers.csv"
path_testHistory = path.home() / "Desktop" / "Data" / "testHistory.csv"
path_trainHistory = path.home() / "Desktop" / "Data" / "trainHistory.csv"
path_transactions = path.home() / "Desktop" / "datatoreduced.csv"

path_out_train = path.home() / "Desktop" / "train.vw"
path_out_test = path.home() / "Desktop" / "test.vw"

# Day Difference Function

def diff_days(date1,date2):
	date_format = "%Y-%m-%d"
	x1 = datetime.strptime(date1, date_format)
	x2 = datetime.strptime(date2, date_format)
	diff = x2 - x1
	return diff.days

# Make Offers Dictonary

offers = {}
for index, line in enumerate(open(path_offers)):
  if index == 0:
    continue
  else:
    row = line.strip().split(",")
    offers[row[0]] = row

# Make Train Dictonary

train_ids = {}
for index, line in enumerate(open(path_trainHistory)):
  if index == 0:
    continue
  else:
    row = line.strip().split(",")
    train_ids[row[0]] = row

# Make Test Dictonary

test_ids = {}
for index, line in enumerate(open(path_testHistory)):
  if index == 0:
    continue
  else:
    row = line.strip().split(",")
    test_ids[row[0]] = row

# Gen Feature

with open(path_out_train, "w") as out_train, open(path_out_test, "w") as out_test:
  last_id = 0
  features = defaultdict(float)
  for index, line in enumerate(open(path_transactions)):
    if index == 0:
      continue
    else:
      row = line.strip().split(",")
      if last_id != row[0] and index != 1:
        if "has_bought_company" not in features:
          features['never_bought_company'] = 1
        if "has_bought_category" not in features:
          features['never_bought_category'] = 1
        if "has_bought_brand" not in features:
          features['never_bought_brand'] = 1
        if "has_bought_brand" in features and "has_bought_category" in features and "has_bought_company" in features:
          features['has_bought_brand_company_category'] = 1
        if "has_bought_brand" in features and "has_bought_category" in features:
          features['has_bought_brand_category'] = 1
        if "has_bought_brand" in features and "has_bought_company" in features:
          features['has_bought_brand_company'] = 1
        outline = ""
        test = False
        for key, value in features.items():
          if key == "label" and value == 0.5:
            outline = "1 '" + last_id + " |f" + outline
            test = True
          elif key == "label":
            outline = str(value) + " '" + last_id + " |f" + outline
          else:
            outline += " " + key + ":" + str(value)
        outline += "\n"
        if test:
          out_test.write(outline)
        else:
          out_train.write(outline)
        features = defaultdict(float)
      if row[0] in train_ids or row[0] in test_ids:
        if row[0] in train_ids:
          history = train_ids[row[0]]
          if train_ids[row[0]][5] == "t":
            features['label'] = 1
          else:
            features['label'] = 0
        else:
          history = test_ids[row[0]]
          features['label'] = 0.5
        features['offer_value'] = offers[history[2]][4]
        features['offer_quantity'] = offers[history[2]][2]
        offervalue = offers[history[2]][4]
        features['total_spend'] += float(row[10])
        if offers[history[2]][3] == row[4]:
          features['has_bought_company'] += 1.0
          features['has_bought_company_q'] += float(row[9])
          features['has_bought_company_a'] += float(row[10])
          date_diff_days = diff_days(row[6], history[-1])
          if date_diff_days < 30:
            features['has_bought_company_30'] += 1.0
            features['has_bought_company_q_30'] += float(row[9])
            features['has_bought_company_a_30'] += float(row[10])
          if date_diff_days < 60:
            features['has_bought_company_60'] += 1.0
            features['has_bought_company_q_60'] += float(row[9])
            features['has_bought_company_a_60'] += float(row[10])
          if date_diff_days < 90:
            features['has_bought_company_90'] += 1.0
            features['has_bought_company_q_90'] += float(row[9])
            features['has_bought_company_a_90'] += float(row[10])
          if date_diff_days < 180:
            features['has_bought_company_180'] += 1.0
            features['has_bought_company_q_180'] += float(row[9])
            features['has_bought_company_a_180'] += float(row[10])
        if offers[history[2]][1] == row[3]:
          features['has_bought_category'] += 1.0
          features['has_bought_category_q'] += float(row[9])
          features['has_bought_category_a'] += float(row[10])
          date_diff_days = diff_days(row[6], history[-1])
          if date_diff_days < 30:
            features['has_bought_category_30'] += 1.0
            features['has_bought_category_q_30'] += float(row[9])
            features['has_bought_category_a_30'] += float(row[10])
          if date_diff_days < 60:
            features['has_bought_category_60'] += 1.0
            features['has_bought_category_q_60'] += float(row[9])
            features['has_bought_category_a_60'] += float(row[10])
          if date_diff_days < 90:
            features['has_bought_category_90'] += 1.0
            features['has_bought_category_q_90'] += float(row[9])
            features['has_bought_category_a_90'] += float(row[10])
          if date_diff_days < 180:
            features['has_bought_category_180'] += 1.0
            features['has_bought_category_q_180'] += float(row[9])
            features['has_bought_category_a_180'] += float(row[10])
        if offers[history[2]][5] == row[5]:
          features['has_bought_brand'] += 1.0
          features['has_bought_brand_q'] += float(row[9])
          features['has_bought_brand_a'] += float(row[10])
          date_diff_days = diff_days(row[6], history[-1])
          if date_diff_days < 30:
            features['has_bought_brand_30'] += 1.0
            features['has_bought_brand_q_30'] += float(row[9])
            features['has_bought_brand_a_30'] += float(row[10])
          if date_diff_days < 60:
            features['has_bought_brand_60'] += 1.0
            features['has_bought_brand_q_60'] += float(row[9])
            features['has_bought_brand_a_60'] += float(row[10])
          if date_diff_days < 90:
            features['has_bought_brand_90'] += 1.0
            features['has_bought_brand_q_90'] += float(row[9])
            features['has_bought_brand_a_90'] += float(row[10])
          if date_diff_days < 180:
            features['has_bought_brand_180'] += 1.0
            features['has_bought_brand_q_180'] += float(row[9])
            features['has_bought_brand_a_180'] += float(row[10])
      last_id = row[0]