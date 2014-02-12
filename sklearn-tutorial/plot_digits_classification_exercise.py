"""Classification of the digits dataset using two methods: nearest
neighbors and logistic regression. Exercise and answer was found
at http://scikit-learn.org."""

import numpy as np
from sklearn import datasets, neighbors, linear_model

digits = datasets.load_digits()

# Use the first 90% of the data as the training set
# and the last 10% of the data as the test set
n_samples = len(digits.data)
digits_X_train = digits.data[:n_samples-n_samples/10]
digits_y_train = digits.target[:n_samples-n_samples/10]
digits_X_test = digits.data[n_samples-n_samples/10:]
digits_y_test = digits.target[n_samples-n_samples/10:]

# Create and fit a nearest-neighbors classifier
knn = neighbors.KNeighborsClassifier()
knn.fit(digits_X_train, digits_y_train)

# Create and fit a logistic regression classifier
logistic = linear_model.LogisticRegression()
logistic.fit(digits_X_train, digits_y_train)

# Test the classifiers by predicting our testing data
# and comparing to the actual targets of our testing data
print "Nearest Neighbors Score: %f" % knn.score(
            digits_X_test, digits_y_test)
print "Logistic Regression Score: %f" % logistic.score(
            digits_X_test, digits_y_test)