from Flags import Flags

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

#from sklearn.compose import ColumnTransformer
#from sklearn.preprocessing import StandardScaler, OneHotEncoder
#from sklearn.impute import SimpleImputer
#from sklearn.pipeline import Pipeline

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

bases_treino = []
bases_flags = Flags.getFlagsEconomia()

for nome_base, df in bases_flags.items():

    # encontra automaticamente as colunas
    col_variacao = [c for c in df.columns if c.lower().startswith("variacao_")][0]
    col_flag = [c for c in df.columns if c.lower().startswith("flag_")][0]

    temp = pd.DataFrame({
        "Indicador": nome_base,
        "Variacao": df[col_variacao],
        "Flag": df[col_flag]
    })

    bases_treino.append(temp)

base_treino = pd.concat(bases_treino, ignore_index=True)

print(base_treino.head())

base_treino = pd.get_dummies(
    base_treino,
    columns=["Indicador"],
    drop_first=False
)

X = base_treino.drop(columns="Flag")
Y = base_treino["Flag"]

#numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
#categorical_features = X.select_dtypes(include=['object']).columns

#numerical_transformer = Pipeline(steps=[
#    ('imputer', SimpleImputer(strategy='mean')),
#    ('scaler', StandardScaler())
#])

#categorical_transformer = Pipeline(steps=[
#    ('imputer', SimpleImputer(strategy='most_frequent')),
#    ('oneshot', OneHotEncoder(handle_unknown='ignore'))
#])

#preprocessor = ColumnTransformer(
#    transformers=[
#        ('num', numerical_transformer, numerical_features),
#        ('cat', categorical_transformer, categorical_features)
#    ])

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42
)

X_trem, X_testa, Y_trem, Y_testa = train_test_split(X, Y, test_size=0.33, random_state=42)

model.fit(X_trem, Y_trem)
y_pred = model.predict(X_testa)

print("Acurácia:", accuracy_score(Y_testa, y_pred))
print("Matrix de confusão:\n", confusion_matrix(Y_testa, y_pred))
print("Report:\n", classification_report(Y_testa, y_pred))
