# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 16:13:13 2019

@author: Marzia Catherine Azam
"""

#Import scikit-learn dataset library
from sklearn import datasets

#Load dataset
wine = datasets.load_wine()

#print the names of the features
print(wine.feature_names)

# print the label species(class_0, class_1, class_2)
print(wine.target_names)

# print the wine data (top 5 records)
print(wine.data[0:5])

# print the wine labels (0:Class_0, 1:Class_1, 2:Class_3)
print(wine.target)



import statistics 
from statistics import mode 
  
verybest_k = []

for i in range(20):

    
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3) # 70% training and 30% test

    from sklearn.neighbors import KNeighborsClassifier

    from sklearn import metrics


    



    bestScore=0.0
    accList=[]

    
    for k in range(1,10): 
    

    #Create KNN Classifier
        knn = KNeighborsClassifier(n_neighbors=k)

    #Train the model using the training sets
        knn.fit(X_train, y_train)

    #Predict the response for test dataset
        y_pred = knn.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
        print("k=" ,k, "Accuracy:",metrics.accuracy_score(y_test, y_pred))
    
        accuracy = metrics.accuracy_score(y_test, y_pred)
    
        if accuracy > bestScore:
            bestScore = accuracy
            best_k = k
            accList.append(k)
        
    print("best k is ", best_k, "with accuracy " ,bestScore)

    verybest_k.append(best_k)

print(verybest_k)
    

print("Over 20 iterations the best k for this dataset is ",mode(verybest_k))


        




    

