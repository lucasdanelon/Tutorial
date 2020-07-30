import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

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

# Select the papers in which the author name is available
base = base[base.Authors != "[No author name available]"]

#Mostrar a base de dados final
print(base)

#Criar um DataFrame base com 2 colunas: nome do autor (sem duplicatas) / score / (papers do autor)
autores = {}

print(autores)

def score(n_authors, p_author):
    coef = 1.5**(n_authors - p_author)/(np.sum(1.5**(np.arange(1,n_authors+1)-1)))
    return coef

for paper in range(base.shape[0]):
    author_list = base.iloc[paper].Authors.split(",")
    author_list = [authors.strip() for authors in author_list]

    author_list = [author for author in author_list if '(' not in author]
    author_list = [author for author in author_list if '[' not in author]
    #remove (1), (2), (3)
    # index = [idx for idx, string in enumerate(author_list) if '(' in string]
    # for i in index:
    #     del author_list[i]

    n_authors = len(author_list)
    for pos,author in enumerate(author_list):
        if author in autores:
            autores[author] += score(n_authors,pos)
        else:
            autores[author] = score(n_authors,pos)

result = {}
result["Authors"] = []
result["Scores"] = []

for key,value in autores.items():

    result["Authors"] += [key]
    result["Scores"] += [value]

final = pd.DataFrame(data = result)

"""
#Contar numero de autores de cada paper
n_authors = [line.Authors.split(",") for line in base]

print(n_authors)

score = (1.5**(n_authors - p_author)/




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
