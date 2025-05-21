import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
a=pd.read_excel("cleaned_data.xlsx")
from simpletransformers.classification import ClassificationModel
a["Tip"].unique()
a['la']=pd.factorize(a.Tip)[0]
a.head()
train,test = train_test_split(a,test_size=0.3,random_state=23)
train=train[["Paylaşım","la"]]
test=test[["Paylaşım","la"]]
train["Paylaşım"]=train["Paylaşım"].apply(lambda r: str(r))
train["la"]=train["la"].astype(int)
model=ClassificationModel("bert","dbmdz/bert-base-turkish-uncased",num_labels=2,use_cuda=False,
                          args={"reprocess_input_data":True,"overwrite_output_dir":True,"num_train_epochs":2,"train_batch_size":30,"fp16":False,"output_dir":"bert_model"})
model.train_model(train)
result, model_outputs, wrong_predictions = model.eval_model(test)
sonuc = model_outputs.argmax(axis=1)
gerçek=test.la.values
sonuc[:100]
gerçek[:100]
accuracy_score(sonuc,gerçek)
#te=test.iloc[3]["Paylaşım"]
te="yardım edin bu devlet bu vergileri arttırıp resmen bizi soyuyolar bize zarar veriyorlar"
print(te)
ta=model.predict([te])
print(te)
if ta[0] ==0:
  print("eksi")
elif ta[0]==1:
  print("artı")
else:
  print("saptayamadı")