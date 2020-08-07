import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Read database
base = pd.read_csv("scopus.csv", sep = ",")

#Hide unnecessary information from the database
columns_to_drop = ["Author(s) ID","Volume","Issue",
                   "Art. No.","Page start","Page end",
                   "Page count","Link","Authors with affiliations",
                   "Abstract","Author Keywords", "Index Keywords", "References",
                   "Conference location","Conference code", "Abbreviated Source Title",
                   "Document Type", "Publication Stage", "Access Type", "Source", "EID",
                   "Sponsors", "Conference name", "Conference date"]

base = base.drop(columns = columns_to_drop)

#Digital Object Identifier (DOI) filter
base = base[base.DOI.notnull()]

#Select the papers in which the author name is available
base = base[base.Authors != "[No author name available]"]

#Create a DataFrame for authors: Name / Score / N° of papers
authors_table = {}

#Define score formula
def score(n_authors, p_author):
    coef = 1.5**(n_authors - p_author)/(np.sum(1.5**(np.arange(1, n_authors + 1 ) - 1)))
    return coef

for paper in range(base.shape[0]):
    author_list = base.iloc[paper].Authors.split(",")
    author_list = [authors.strip() for authors in author_list]
    
    #remove (1), (2), (3)
    author_list = [author for author in author_list if '(' not in author]
    #remove ?
    author_list = [author for author in author_list if '[' not in author]
    
    n_authors = len(author_list)
    for pos,author in enumerate(author_list):
        if author in authors_table:
            authors_table[author] += score(n_authors,pos)
        else:
            authors_table[author] = score(n_authors,pos)

result = {}
result["Authors"] = []
result["Scores"] = []

for key,value in authors_table.items():

    result["Authors"] += [key]
    result["Scores"] += [value]

final = pd.DataFrame(data = result)

#Create a DataFrame for countries: Name / Score / N° of Affiliations
countries_table = {}

#
for paper in range(base.shape[0]):
    country_list = base.iloc[paper].Affiliations.split(",")