import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sklearn

# Récupération du jeu de données
df=pd.read_csv('modele/data/export_alimconfiance.csv', sep=";")
print(df.head())
