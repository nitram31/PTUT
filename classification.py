from re import X
from pandas import read_csv
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import pandas as pd
from graphviz import graphviz

#Exemple : 
X = [[0,0], [1,1]] # training n_sample, n_features
Y = [0, 1] # classe set n_sample 
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,Y)

prediction = clf.predict([[2.,2.]])

print(prediction)

#Exemple 2 : 

iris = load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

## ----------- exportation 
dot_data = tree.export_graphviz(clf, out_file=None) 
graph = graphviz.Source(dot_data) 
graph.render("iris")



"""
# DecisionTreeClassifier a class capable of performing multi-class classification on a dataset

data = pd.read_csv("output.csv", sep=";")

# Training set / test set aléatoirement 
x_train = []
x_test = []
x_train, x_test = train_test_split(data, random_state=4 )

# Decision Tree

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_train, x_test)


if __name__ == "__main__":
x_test.to_csv("x_test.csv", sep=";", index=False)  # export file
x_train.to_csv("x_train.csv", sep=";", index=False) # 
"""