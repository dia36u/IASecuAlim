# REGRESSION LOGISTIQUE

""" 1.IMPORT DES LIBRAIRIES """
# librairies classiques
from matplotlib.pyplot import sca
import pandas as pd
import numpy as np

# packages scikit-learn
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
print(sklearn.__version__)
from sklearn import preprocessing
import scipy as sci

from imblearn.over_sampling import SMOTE


""" 2.IMPORT DU DATASET """
# Récupération du jeu de données
dataset=pd.read_csv('modele/data/clean/AlimConfiance_BDD_Clean.csv', sep=";")
# visualisation du jeu de données
print(dataset.head())

#dataset.drop('agrement', axis=1, inplace=True)
#dataset.drop('id_etablissement', axis=1, inplace=True)

""" 3.SEPARATION DU DATASET EN TRAIN ET TEST SET """
# Définition des variables : indépendantes/ dependantes
X = dataset.drop('niveau_hygiene', axis=1)
y = dataset['niveau_hygiene']
# Sépartion du dataset de sorte à avoir 1/3 des données dans le test set
X_tn, X_tt, y_tn, y_tt = train_test_split(X, y, test_size=300, random_state=0, stratify=y)
print('\ntrain sets size :\n',X_tn.shape, y_tn.shape,'\ntest sets size :\n',X_tn.shape, y_tn.shape )
print('\ntrain set :\n',y_tn.value_counts())

print(dataset.head())

""" 4.EQUILIBRAGE DES DONNEES DE TRAIN """
smote = SMOTE(sampling_strategy='auto', random_state=0, k_neighbors=7)
X_tn_smote, y_tn_smote = smote.fit_resample(X_tn,y_tn)
print('\ntrain sets over-sampled sizes :\n',X_tn_smote.shape, y_tn_smote.shape,'\n')
print('\ntarget train set over-sampled :\n',y_tn_smote.value_counts(),'\n')
print(X_tn_smote.describe())

""" 4.STANDARDISATION DES DONNEES D'ENTREE"""
# Instanciation
scaler = preprocessing.StandardScaler()
scaler.fit(X_tn_smote)
print('\nsacaler :',scaler)
print('scaler mean :',scaler.mean_)
print('scaler scale :',scaler.scale_,'\n')
# Transformation
X_tn_scaled = scaler.transform(X_tn_smote)
X_tn_scaled = pd.DataFrame(X_tn_scaled, index=X_tn_smote.index, columns=X_tn_smote.columns)
X_tt_scaled = scaler.transform(X_tt)
X_tt_scaled = pd.DataFrame(X_tt_scaled, index=X_tt.index, columns=X_tt.columns)
print(X_tn_scaled.describe())

""" 5.ENTRAINEMENT TRAIN SET """
# Instanciation d'un modèle de régression logistique sans pénalité
lr = LogisticRegression(penalty='none')
# Estimation des données de training
lr.fit(X_tn_scaled, y_tn_smote)

#  Dé-standardisation par les écarts-type utilisés lors de la standardisation des variables
#coefUnstd = scaler.coef_[0] / scaler.scale_

""" 6.PREDICTION TEST SET"""
y_pred = lr.predict(X_tt_scaled)

""" 7.PERFORMANCE """
print('\n',classification_report(y_tt, y_pred))
