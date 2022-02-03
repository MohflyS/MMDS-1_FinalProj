vw train.vw -c -k --passes 40 -l 0.85 -f model.vw --loss_function quantile --quantile_tau 0.6
vw test.vw -t -i model.vw -p shop.preds.txt

with open(submission, "w") as outfile:
  for index, line in enumerate(open("Data/testHistory.csv")):
    if index == 0:
      outfile.write( "id,repeatProbability\n" )
    else:
      row = line.strip().split(",")
      if row[0] not in preds:
        outfile.write(row[0]+",0\n")
      else:
        outfile.write(row[0]+","+preds[row[0]]+"\n")

# Model Making and Training and Learning
# -------------------------------------------------------------------------------------------
# Model Making and Training and Learning

import vowpalwabbit

model = vowpalwabbit.Workspace(quiet=True)
for line in open('/content/drive/MyDrive/Data/train.vw'):
  model.learn(line)

for line in open('/content/drive/MyDrive/Data/test.vw'):
  prediction = model.predict(line)
  print(prediction)