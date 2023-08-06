# The functions that are complete and included in this file : 
# pr_1()
# pr_1_algo()
# pr_1_nb()
# pr_2()
# pr_3()
# pr_4()
# pr_4_algo()
# pr_4_nb()
# pr_5()
# pr_6()
# pr_7()
# pr_8()
# pr_9()
# pr_10()

def pr_1_algo():
    p1 = '''
import pandas as pd
import itertools

class FindS():      
    def train(self, X, target):
        self.h = ['Φ', 'Φ', 'Φ', 'Φ', 'Φ', 'Φ']
        for idx, x in X.iterrows():            
            if target[idx] == "No":     
                continue
            
            x.reset_index(drop=True, inplace=True)  
            for i, attr in enumerate(x):           
                if self.h[i] == 'Φ':
                    self.h[i] = attr
                elif self.h[i] != attr:
                    self.h[i] = '?'
    
class ListThenEliminate():
    def train(self, X, target):
        self.__unique_attributes = [list(li) for li in list(X.apply(pd.Series.unique))]
        for li in self.__unique_attributes:
            li.append('?')
            li.append('Φ')
        self.__H = list(itertools.product(*self.__unique_attributes))
        
        # Vector Space containg hypotheses each consistent of all the training examples
        self.VectorSpace = []
        
        for h in self.__H:
            if self.__is_consistent(h, (X, target)) == True:
                self.VectorSpace.append(h)
    
    def __is_consistent(self, h, D):
        for idx, x in D[0].iterrows():
            self.__prediction = self.__predict(h, x)
            if self.__prediction == True and D[1][idx] == False:
                return False
            if self.__prediction == False and D[1][idx] == True:
                return False
                    
        return True
    
    def __predict(self, h, x):
        for i, attr in enumerate(x):
            if h[i] == 'Φ':
                return False
            if h[i] == '?':
                continue
            if h[i] != x[i]:
                return False
            
        return True
        '''
    p1 = print(p1)
    return p1

def pr_1_nb():
    p1 = '''
import pandas as pd
import numpy as np
from concept_learning import FindS, ListThenEliminate

data = pd.read_csv("../../Data/enjoysport.csv")

display(data)

X = data.copy()

target = X["EnjoySport"]

display(target)

X = X.iloc[:,:-1]

display(X)

# Applying Find-S Algorithm to Get Specific Hypothesis

display(target)

find_S = FindS()
find_S.train(X, target)

print("The specific hypothesis is", find_S.h)

# Applying LIST-THEN-ELIMINATION Algorithm to Get Specific Hypothesis

target = target.apply(lambda x: True if x == "Yes" else False)

list_then_eliminate = ListThenEliminate()
list_then_eliminate.train(X, target)

display(list_then_eliminate.VectorSpace)
'''
    p1 = print(p1)
    return p1

def pr_1():
    pr1 =  print(pr_1_algo(),pr_1_nb())
    return pr1
    
def pr_2():
    p2 = '''
import pandas as pd
import numpy as np

data = pd.read_csv("../../Data/enjoysport.csv")

display(data)

X = np.array(data.iloc[:,0:-1])
display(X)

target = np.array(data.iloc[:,-1])
display(target)

def train(X, target):
    specific_h = X[0].copy()
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    
    print("\nInitialization:\nSpecific Boundry: {}\nGeneral Boundry: {}".format(
        specific_h, general_h))
    
    for i, h in enumerate(X):
        print("\nAfter Instance #", i+1 , ":", h, "[POSITIVE]" if target[i] == "Yes" else "[NEGATIVE]")
        
        if target[i] == "Yes":
            for x in range(len(specific_h)): 
                if h[x]!= specific_h[x]:                    
                    specific_h[x] ='?'                     
                    general_h[x][x] ='?'

        elif target[i] == "No":            
            for x in range(len(specific_h)): 
                if h[x]!= specific_h[x]:                    
                    general_h[x][x] = specific_h[x]                
                else:                    
                    general_h[x][x] = '?'        

        print("Specific Bundary:", specific_h)         
        print("Generic Boundary:", general_h)

    
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:   
        general_h.remove(['?', '?', '?', '?', '?', '?']) 

    return specific_h, general_h 


specific_boundry, general_boundry = train(X, target)print("Hypothesis in Specific Boundry:", specific_boundry, "\n")
print("Hypotheses in General Boundry:", general_boundry)
'''
    p2 = print(p2)
    return p2

def pr_3():
    p3 = '''
    import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import matplotlib.pyplot as plt

# Having a Quick Look into the Data

housing = pd.read_csv("../../Data/housing/housing.csv")

display(housing)

print(housing.info())

print(housing.ocean_proximity.value_counts())

display(housing.describe())

print("There are", sum(housing.duplicated()), "duplicates in the datsset")

housing.hist(bins=50, figsize=(15,8))
plt.show()

# Creating Test Set

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

# Preparing Data

housing = train_set.drop("median_house_value", axis=1)
housing_labels = train_set["median_house_value"].copy()

# Handling Missing Values

imputer = SimpleImputer(strategy="median")
housing_num = housing.drop("ocean_proximity", axis=1)
X_train_num = imputer.fit_transform(housing_num)

#Scaling Features

std_scaler = StandardScaler()
X_train_num = std_scaler.fit_transform(X_train_num)

print("Shape of the transformed dataset with only numerical attributes is", X_train_num.shape)

# Encoding Categorical Attributes

cat_encoder = OneHotEncoder(sparse=False)
housing_cat = housing[["ocean_proximity"]]
X_train_cat = cat_encoder.fit_transform(housing_cat)

print(X_train_cat)

print(cat_encoder.categories_)

# Combining Transformed Data

X_train = np.append(X_train_num, X_train_cat, axis=1)

display(
    pd.DataFrame(
        X_train, 
        index=housing_num.index,
        columns=list(housing_num.columns)+list(cat_encoder.categories_[0])
    )
)

# Transforming Test Data

housing_test = test_set.drop("median_house_value", axis=1)

housing_test_labels = test_set["median_house_value"].copy()

# Handling Missing Values

housing_test_num = housing_test.drop("ocean_proximity", axis=1)

X_test_num = imputer.transform(housing_test_num)

# Scaling Features

X_test_num = std_scaler.transform(X_test_num)

# Encoding Categorical Attributes

housing_test_cat = housing_test[["ocean_proximity"]]
X_test_cat = cat_encoder.transform(housing_test_cat)

# Combining Transformed Data

X_test = np.append(X_test_num, X_test_cat, axis=1)

display(
    pd.DataFrame(
        X_test, 
        index=housing_test_num.index,
        columns=list(housing_test_num.columns)+list(cat_encoder.categories_[0])
    )
)
    '''
    p3 = print(p3)
    return p3



def pr_4_algo():
    p4 = '''
import numpy as np

class Node:
    def __init__(self):
        self.value = ""
        self.children = []
        self.entropy = 0.0
        self.sample_count = 0
        self.isLeaf = False
        self.prediction = ""

class ID3DecisionTreeClassifier:
    def entropy(self, data, target_attrib_name):
        entropy = 0.0                   
        examples_count = data.shape[0]  
        for target_value in data[target_attrib_name].unique():
            filtered_examples_count = data[data[target_attrib_name] == target_value].shape[0]     
            entropy += -filtered_examples_count/examples_count * np.log2(filtered_examples_count/examples_count)

        return entropy
        
    def info_gain(self, data, attrib_name, target_attrib_name):
        entropy = self.entropy(data, target_attrib_name)

        sum_entropy_subsets = 0
        for attrib_val in data[attrib_name].unique():
            data_subset = data[data[attrib_name] == attrib_val]
            sum_entropy_subsets += data_subset.shape[0]/data.shape[0] * self.entropy(data_subset, target_attrib_name)

        return entropy - sum_entropy_subsets

    def fit(self, data, target_attrib_name):
        self.__tree = self.__ID3(
            data,                                                                  
            [attrib for attrib in data.columns if attrib != target_attrib_name],    
            target_attrib_name)                                                     
    
    def __ID3(self, data, attrib_names, target_attrib_name):
        root = Node()
        root.entropy = self.entropy(data, target_attrib_name)
        root.sample_count = data.shape[0]
        
        if root.entropy == 0.0:
            root.isLeaf = True
            root.prediction = data[target_attrib_name].unique()
            return root
        
        best_info_gain = 0.0
        best_attrib = ""
        
        for attrib_name in attrib_names:
            info_gain = self.info_gain(data, attrib_name, target_attrib_name)
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_attrib = attrib_name
                
        root.value = best_attrib  
        
        attrib_unique_values = data[best_attrib].unique()
        for attrib_unique_value in attrib_unique_values:
            data_subset = data[data[best_attrib] == attrib_unique_value]
            new_attrib_names = attrib_names.copy()
            new_attrib_names.remove(best_attrib)
            
            root.children.append({attrib_unique_value: self.__ID3(data_subset, new_attrib_names, target_attrib_name)})

        return root
    
    def predict(self, data):
        return self.__predict(self.__tree, data)
    
    def __predict(self, root: Node, data):
        if root.isLeaf == True:
            return root.prediction
        else:
            for child in root.children:
                if list(child.keys())[0] == data[root.value]:
                    return self.__predict(list(child.values())[0], data)

    def print_tree(self, offset = 0):
        self.__print_tree(self.__tree, offset)
        print("\nLEGENDS:")
        print("e: entropy, s: sample count, p: prediction")
            
    def __print_tree(self, root: Node, offset = 0):
        for i in range(offset):
            print("\t", end="")
            
        if root.isLeaf == True:
            print("('LEAF') [e: {:.2f}, s: {}, p: {}]".format(root.entropy, root.sample_count, root.prediction))
        
        else:
            print("({}) [e: {:.2f}, s: {}]".format(root.value, root.entropy, root.sample_count), end="")
            print()
            for child in root.children:
                for i in range(offset + 1):
                    print("\t", end="")
                print(list(child.keys())[0])                            
                self.__print_tree(list(child.values())[0], offset + 2)  
    '''
    p4 = print(p4)
    return p4



def pr_4_nb():
    p4 = '''
import pandas as pd
import numpy as np
from ID3DecisionTree import Node, ID3DecisionTreeClassifier

# Exploratory Data Analysis

data = pd.read_csv("../../Data/playtennis.csv")

display(data)

# Data Preparation

data = data[["Outlook", "Temperature", "Humidity", "Wind", "PlayTennis"]]

display(data)

# Applying ID3 Algorithm

id3DecisionTreeClassifier = ID3DecisionTreeClassifier()

id3DecisionTreeClassifier.fit(data, "PlayTennis")

id3DecisionTreeClassifier.print_tree()



test_data = {"Outlook":"Sunny", "Temperature":"Hot", "Humidity":"Normal", "Wind":"Strong"}

prediction = id3DecisionTreeClassifier.predict(test_data)

print(prediction)
    '''
    p4 = print(p4)
    return p4

def pr_4():
    return pr_4_algo(),pr_4_nb()

def pr_5():
    p5 = '''
import pandas as pd
import numpy as np

from sklearn.datasets import fetch_openml

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier

import matplotlib.pyplot as plt

# Loading Data Set

mnist = fetch_openml("mnist_784", as_frame=False)

# Exploratory Data Analysis (EDA)

print(mnist.keys())

display(mnist.data)

print(mnist.data.shape)

display(mnist.target)



for idx, image_data in enumerate(mnist.data[:100]):
    plt.subplot(10, 10, idx + 1)
    image = image_data.reshape(28, 28)
    plt.imshow(image, cmap = "binary")
    plt.axis("off")

plt.show()


display(mnist.target[:10])

# Data Preparation

X_train, X_test, y_train, y_test = train_test_split(
    mnist.data, mnist.target, test_size=0.15, stratify=mnist.target, random_state=42)



print("X_train: {}, y_train: {}".format(X_train.shape, y_train.shape))
print("X_test: {}, y_test: {}".format(X_test.shape, y_test.shape))



train_unique_labels, train_unique_label_count = np.unique(
    y_train, return_counts=True)

test_unique_labels, test_unique_label_count = np.unique(
    y_test, return_counts=True)
print("Train set distribution:\n")
train_unique_labels, np.round(train_unique_label_count/X_train.shape[0], 3)



print("Test set distribution:\n")
test_unique_labels, np.round(test_unique_label_count/X_test.shape[0], 3)


# Modeling

# Classifying with RandomForest Classifier

rf_clf = RandomForestClassifier(
    n_estimators=100, max_leaf_nodes=16, n_jobs=-1)



rf_clf_cv_accuracy = cross_val_score(
    rf_clf, X_train, y_train, scoring="accuracy", cv=5)



print("Random Forest CV Error: {} (mean) [Standard Deviation (STD): {}]".format(
    np.mean(rf_clf_cv_accuracy), np.std(rf_clf_cv_accuracy)))



# Implementing Ensembling with Bagging & DecisionTree Classifiers

bag_clf_50 = BaggingClassifier(
    DecisionTreeClassifier(splitter="random", max_leaf_nodes=16),
    n_estimators=50,
    n_jobs=-1)


bag_clf_50_cv_accuracy = cross_val_score(
    bag_clf_50, X_train, y_train, scoring="accuracy", cv=5)
print("Bagging Classifier (with 50 estimators) CV Error: {} (mean) [Standard Deviation (STD): {}]".format(
    np.mean(bag_clf_50_cv_accuracy), np.std(bag_clf_50_cv_accuracy)))


bag_clf_100 = BaggingClassifier(
    DecisionTreeClassifier(splitter="random", max_leaf_nodes=16),
    n_estimators=100,
    n_jobs=-1)


bag_clf_100_cv_accuracy = cross_val_score(
    bag_clf_100, X_train, y_train, scoring="accuracy", cv=5)


print("Bagging Classifier (with 100 estimators) CV Error: {} (mean) [Standard Deviation (STD): {}]".format(
    np.mean(bag_clf_100_cv_accuracy), np.std(bag_clf_100_cv_accuracy)))
bag_clf_100.fit(X_train, y_train)



test_predictions = bag_clf_100.predict(X_test)
print("Accuracy on Test Data:", accuracy_score(y_test, test_predictions))
'''
    p5 = print(p5)
    return p5

def pr_10():
    p10 = '''
    
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import confusion_matrix, classification_report

import matplotlib.pyplot as plt
import seaborn as sns

# Exploratory Data Analysis (EDA)

iris = load_iris()

print(iris.keys())

print(iris.data.shape)

print(iris.feature_names)

print(iris.target_names)

print(iris.target)

np.append(
    iris.data, 
    np.array(list(map(lambda i: iris.target_names[i], iris.target))).reshape(iris.data.shape[0],1),
    axis=1)[:10]

print(np.unique(iris.target, return_counts=True))

data_df = pd.DataFrame(iris.data)
data_df.columns = iris.feature_names
data_df["plant type"] = list(map(lambda i: iris.target_names[i], iris.target))

data_df.info()

data_df.describe()

sns.pairplot(data_df, hue="plant type")

# Data Preparation

X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.20, stratify=iris.target, random_state=42)

train_unique_labels, train_unique_label_count = np.unique(y_train, return_counts=True)
test_unique_labels, test_unique_label_count = np.unique(y_test, return_counts=True)
print("Train set distribution:\n")
print(train_unique_labels, np.round(train_unique_label_count/X_train.shape[0], 2))
print("\nTest set distribution:\n")
print(test_unique_labels, np.round(test_unique_label_count/X_test.shape[0], 2))

# Modeling

# Linear Support Vector Classifier (SVC)

linear_svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("linear_svc", LinearSVC(C=1, loss="hinge", random_state=42))
])

linear_svm_cross_val_scores = cross_val_score(
    linear_svm_pipeline, X_train, y_train, scoring="accuracy", cv=5, n_jobs=-1)

print("Scores: {}\nMean Score: {}, Mean Score Std. Dev.: {}".format(
    linear_svm_cross_val_scores, 
    np.mean(linear_svm_cross_val_scores), 
    np.std(linear_svm_cross_val_scores)))

# Non-linear Support Vector Classifier (SVC)

# Polynomial Features

polynomial_svm_pipeline = Pipeline([
    ("poly_features", PolynomialFeatures(degree=3)),
    ("scaler", StandardScaler()),
    ("linear_svc", LinearSVC(C=1, loss="hinge"))
    ])

polynomial_svm_cross_val_scores = cross_val_score(
    polynomial_svm_pipeline, X_train, y_train, scoring="accuracy", cv=5, n_jobs=-1)

print("Scores: {}\nMean Score: {}, Mean Score Std. Dev.: {}".format(
    polynomial_svm_cross_val_scores, 
    np.mean(polynomial_svm_cross_val_scores), 
    np.std(polynomial_svm_cross_val_scores)))

# Polynomial Kernel

# Configuring SVC with polynomial degree of 3

poly_kernel_svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("poly_kernel_svc", SVC(kernel="poly", degree=3, coef0=1, C=1))
    ])

poly_kernel_svm_cross_val_scores = cross_val_score(
    poly_kernel_svm_pipeline, X_train, y_train, scoring="accuracy", cv=5, n_jobs=-1)

print("Scores: {}\nMean Score: {}, Mean Score Std. Dev.: {}".format(
    poly_kernel_svm_cross_val_scores, 
    np.mean(poly_kernel_svm_cross_val_scores), 
    np.std(poly_kernel_svm_cross_val_scores)))

# Configuring SVC with polynomial degree of 2

poly_kernel_svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("poly_kernel_svc", SVC(kernel="poly", degree=2, coef0=1, C=1))
    ])

poly_kernel_svm_cross_val_scores = cross_val_score(
    poly_kernel_svm_pipeline, X_train, y_train, scoring="accuracy", cv=5, n_jobs=-1)

print("Scores: {}\nMean Score: {}, Mean Score Std. Dev.: {}".format(
    poly_kernel_svm_cross_val_scores, 
    np.mean(poly_kernel_svm_cross_val_scores), 
    np.std(poly_kernel_svm_cross_val_scores)))

# Gaussian Radial Basis Function (RBF) Kernel

# Configuring SVC with RBF kernel with gamma and C set to 0.1 and 1, respectively

rbf_kernel_svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("rbf_kernel_svc", SVC(kernel="rbf", gamma=0.1, C=1))
    ])

rbf_kernel_svm_cross_val_scores = cross_val_score(
    rbf_kernel_svm_pipeline, X_train, y_train, scoring="accuracy", cv=5, n_jobs=-1)

print("Scores: {}\nMean Score: {}, Mean Score Std. Dev.: {}".format(
    rbf_kernel_svm_cross_val_scores, 
    np.mean(rbf_kernel_svm_cross_val_scores), 
    np.std(rbf_kernel_svm_cross_val_scores)))

# Hyperparameter Tuning

grid_search_params = {'C':[0.1,1,10,100], 'gamma':[1,0.1,0.01,0.001]}
grid = GridSearchCV(
    SVC(),               # Classifier with default values
    grid_search_params, 
    refit = True,        # Keeps the reference to model with best parameters for later use
    n_jobs=-1,
    verbose=3
)
grid.fit(X_train, y_train)

print(grid.best_params_)

print(grid.best_score_)

# Performance Evaluation

test_predictions = grid.predict(X_test)

print("Confusion Matrix:\n", confusion_matrix(y_test, test_predictions))

print(classification_report(y_test, test_predictions))

'''
    p10 = print(p10)
    return p10

def pr_6():
    p6 = '''
import numpy as np
import pandas as pd

data = pd.read_csv("https://github.com/PradipKumarDas/Teaching/blob/master/Data/playtennis.csv?raw=true")

data.drop(["Day"], axis=1, inplace=True)

def naive_bayes_predict(data, target_name, test_instance):
    
    target_value_counts = data[target_name].value_counts().to_dict()
    
    proba_target_values = (data["PlayTennis"].value_counts()/data.shape[0]).to_dict()
    
    predicted_target_values = {}

    for target, value_count in target_value_counts.items():
        attrib_proba_given_target_proba = 1
        
        data_subset = data[data[target_name] == target]
        
        for attrib, value in test_instance.items():
            attrib_value_conditional_proba = data_subset[data_subset[attrib] == value].shape[0] / data_subset.shape[0]
            attrib_proba_given_target_proba *= attrib_value_conditional_proba
        
        target_value_proba = proba_target_values[target] * attrib_proba_given_target_proba       
        proba_target_values[target] = target_value_proba
        
    return proba_target_values

test_instance = {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Strong"}

prediction = naive_bayes_predict(data.copy(), "PlayTennis", test_instance)
print(prediction)
'''
    p6 = print(p6)
    return p6

def pr_7():
    p7 = '''
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns

#

newsgroups_train = fetch_20newsgroups(
    subset="train", 
    random_state=42)

newsgroups_test = fetch_20newsgroups(
    subset="test", 
    random_state=42)
    
# 
print("Training Sample Count:", len(newsgroups_train.data))
print("Testing Sample Count:", len(newsgroups_test.data))

# 
categories = newsgroups_train.target_names
print("Unique Category Count:", len(categories))

#
print(newsgroups_train.data[0])

#
print(categories)

#
print(newsgroups_train.target[:10])

#
print(
    list(
        map(
            lambda x: newsgroups_train.target_names[x], 
            newsgroups_train.target
        )
    )[:10]
)

#
pipeline = make_pipeline(TfidfVectorizer(), MultinomialNB())
pipeline.fit(newsgroups_train.data, newsgroups_train.target)

#
predicted_categories = pipeline.predict(newsgroups_test.data)

#
print(
    "Test Document:", newsgroups_test.data[0], 
    "\nActual Category:", newsgroups_test.target[0], 
    "\nPredicted Category:", predicted_categories[0]
)

#
accuracy_score(newsgroups_test.target, predicted_categories)

#
conf_matrix = confusion_matrix(newsgroups_test.target, predicted_categories)
sns.heatmap(
    conf_matrix.T, 
    #square = True, 
    annot=True, 
    fmt = "d", 
    xticklabels=newsgroups_train.target_names,
    yticklabels=newsgroups_train.target_names)
plt.xlabel("Actual Category")
plt.ylabel("Predicted Category")
plt.show() 

#
print(
    classification_report(
    newsgroups_test.target,
    predicted_categories, 
    target_names=categories)
)
'''
    p7 = print(p7)
    return p7

def pr_8():
    p8 = '''
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

with open("./../Data/heart_disease/processed.cleveland.attributes", "r", newline=None) as f:
    attributes = f.readline().replace('\n', '').split(',')
print(attributes)

data = pd.read_csv("./../Data/heart_disease/processed.cleveland.data", header=None, names=attributes)
display(data)

display(data.info())

print(data.ca.value_counts())
print(data.thal.value_counts())

data = data[data.ca != '?']
data = data[data.thal != '?']

data = data.convert_dtypes()
print(data.dtypes)

data.ca = pd.to_numeric(data['ca']).astype(int)
data.thal = pd.to_numeric(data['thal']).astype(int)

print(data.dtypes)

display(data)

model = BayesianNetwork([
    ('age', 'heartdisease'), 
    ('sex', 'heartdisease'),
    ('cp','heartdisease'), 
    ('exang','heartdisease'),
    ('heartdisease','restecg'),
    ('heartdisease','chol')
])

model.fit(data, estimator=MaximumLikelihoodEstimator)

inference = VariableElimination(model)

print(inference.query(variables=['heartdisease'], evidence={'restecg': 1}))

print(inference.query(variables=['heartdisease'],evidence={'cp':2}))
    '''
    p8 = print(p8)
    return p8

def pr_9():
    p9 = '''
import numpy as np
from sklearn.datasets import load_iris
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

iris = load_iris()

print(iris.keys())

print(iris.data.shape)

print(iris.feature_names)

print(iris.target_names)

X = iris.data[:, 2:]

colormap = np.array(['blue', 'orange', 'green'])

plt.scatter(X[:,0], X[:,1], c=colormap[iris.target])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("Actual Clusters")
plt.show()

model = GaussianMixture(n_components = 3, random_state=42)

model.fit(X)

predicted_labels = model.predict(X)

colormap_prediction = np.array(['purple', 'cyan', 'red'])
markers = ['o', 'v', 's']
for i, l in enumerate(predicted_labels):
    plt.plot(X[i,0], X[i,1], color=colormap_prediction[l], marker=markers[l])    
plt.show()
    '''
    p9 = print(p9)
    return p9