import pandas as pd
import numpy as np

#Ler a base de dados
base = pd.read_csv("scopus.csv", sep = ",")

#Retirar informacoes desnecessarias da base de dados
columns_to_drop = ["Author(s) ID","Volume","Issue",
                   "Art. No.","Page start","Page end",
                   "Page count","Link","Authors with affiliations",
                   "Abstract","Author Keywords", "Index Keywords", "References",
                   "Conference location","Conference code", "Abbreviated Source Title",
                   "Document Type", "Publication Stage", "Access Type", "Source", "EID", 
                   "Sponsors", "Conference name", "Conference date"]

base = base.drop(columns = columns_to_drop)

#Selecionar apenas artigos com DOI
base = base[base.DOI.notnull()]

#Mostrar a base de dados final
print(base)

#Criar uma base com 2 colunas: nome do autor (sem duplicatas) / score / (papers do autor)
autores = ["author", "score", np.ones((1,2))]

print(len(autores))

"""
#Contar numero de autores de cada paper
n_authors = sum(line.Authors(",")) for line in base

print(n_authors)

#score = (1.5**(n_authors - p_author)/




for i in range(base.shape[0]):
    affiliations = base.iloc[i].Affiliations
    affiliations = affiliations.split(";")
    countries = []

    for place in affiliations:
        country = place.split(",")[-1]
        countries.append(country)

    base.iloc[i].Affiliations = countries

print(base)
"""