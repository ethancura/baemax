import pandas as pd #imprting using scikit learn
#data = 'triage_data.csv'#url fro data set
#names =['Injury type','Pain','age','Heart Rate', 'Blood Pressure Upper', 'Blood Pressure Lower','Respriatory Rate','Temperature','SPO2', 'Coma Scale', 'Potential Break', 'Laceration','Smoker','ESI']# coulmn names for the data set
esidata = pd.read_csv(r'C:\Users\Owner\AI_project\TDpythoncompatable.csv')#reading data set in to pandas data frame

X= esidata.iloc[:, 0:12]# assign data from 1st 4 counm to  x var


y=esidata.iloc[:,13]# assign data from 14th columns to y var


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.20)#assigns 80% of data to train and 20 to test

  #future scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
  #training and prediction
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(20, 30, 20), max_iter=1000)#hidden layer sizes 50 nodes each/ what do each of the numbers in the hidden leayer do?
#mlp classifer specifies the num of iterations/ default activaiton funct is relu
mlp.fit(X_train, y_train.values.ravel())
predictions =mlp.predict(X_test)

#eval
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test,predictions))#confusin martix used to help describe test preformance
print(classification_report(y_test,predictions))
