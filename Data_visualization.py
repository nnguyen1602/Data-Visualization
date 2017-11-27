import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from scipy import stats
import tensorflow as tf
import seaborn as sns
from pylab import rcParams
from sklearn.model_selection import train_test_split
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from sklearn import datasets
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import pandas

# add whole data to test
pandas2ri.activate()

readRDS = robjects.r['readRDS']
df = readRDS('waterDataTraining.RDS')
df = pandas2ri.ri2py(df)

######## remove NA values
df = df.dropna()

### convert the Event column to 1 and 0
df = df*1

event = df[df["EVENT"] == 1]
normal = df[df["EVENT"] == 0]

print("number of events:",np.shape(event))
print("number of normal:",np.shape(normal))

############################ feature importannt #######################
# divide into data and target
df = df.drop(['Time'], axis=1)
target = df["EVENT"]
data = df.drop(['EVENT'], axis=1)

model = ExtraTreesClassifier()
model.fit(data, target)
# display the relative importance of each attribute
#print(model.feature_importances_)
#print(df.DataFrame.header(2))
importances = model.feature_importances_
std = np.std([tree.feature_importances_ for tree in model.estimators_],
             axis=0)
indices = np.argsort(-importances)
plt.figure()
plt.title("Feature importances")
plt.barh(range(data.shape[1]), importances[indices],
       color="g", xerr=std[indices]) #, align="center"
# If you want to define your own labels,
# change indices to a list of labels on the following line.
# the real column position ['Tp', 'Cl', 'pH', 'Redox', 'Leit', 'Trueb', 'Cl_2', 'Fm', 'Fm_2']
# you need to rearrange the name with the correct feature importance position
indices = ['Redox', 'Cl_2', 'pH', 'Cl', 'Leit', 'Tp', 'Trueb', 'Fm_2', 'Fm']
plt.yticks(range(data.shape[1]), indices)
plt.ylim([-1, data.shape[1]])
plt.show()
print(data.describe())


##******************** univariate **********************##

########################### Histograms ###########################
data.hist()
plt.show()


########################### Density Plots ###########################
data.plot(kind='density', subplots=True, layout=(4,4), sharex=False)
plt.show()



###################### Box and Whisker Plots #########################
data.plot(kind='box', subplots=True, layout=(4,4), sharex=False, sharey=False)
plt.show()


##******************** Multivariate **********************##

###################### Correlation Matrix Plot #########################
names = ['Tp', 'Cl', 'pH', 'Redox', 'Leit', 'Trueb', 'Cl_2', 'Fm', 'Fm_2']
correlations = data.corr()
# plot correlation matrix
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlations, vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,9,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(names)
ax.set_yticklabels(names)
plt.show()

######################## Scatterplot Matrix ###########################
from pandas.tools.plotting import scatter_matrix
names = ['Tp', 'Cl', 'pH', 'Redox', 'Leit', 'Trueb', 'Cl_2', 'Fm', 'Fm_2']
scatter_matrix(data)
plt.show()
