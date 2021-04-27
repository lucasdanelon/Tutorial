import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Define score formula
def score(n_elems, p_elem):
    coef = 1.5**(n_elems - p_elem)/(np.sum(1.5**(np.arange(1, n_elems + 1 ) - 1)))
    return coef

def distribute_points(base,test):
    final_table = {}
    for paper in range(base.shape[0]):
        elem_list = base.iloc[paper][test].split(",")
        elem_list = [elem.strip() for elem in elem_list]

        #remove (1), (2), (3)
        elem_list = [elem for elem in elem_list if '(' not in elem]
        #remove "["
        elem_list = [elem for elem in elem_list if '[' not in elem]

        n_elems = len(elem_list)
        for pos,elem in enumerate(elem_list):
            if elem in final_table:
                final_table[elem] += score(n_elems,pos+1)
            else:
                final_table[elem] = score(n_elems,pos+1)

    return final_table

def dict_to_df(my_dict,name1,name2):
    Results = {}
    Results[name1] = []
    Results[name2] = []
    for key,value in my_dict.items():

        Results[name1] += [key]
        Results[name2] += [value]

    final = pd.DataFrame(data = Results)
    return final

def main():
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

    base["Countries"] = base["Affiliations"].apply(lambda x: ', '.join([c.split(",")[-1].strip() for c in str(x).split(";")]))

    Authors_Dict = distribute_points(base,"Authors")
    Countries_Dict = distribute_points(base,"Countries")

    Authors_final = dict_to_df(Authors_Dict,"Authors","Scores")
    Countries_final = dict_to_df(Countries_Dict,"Countries","Scores")

    Authors_final.to_csv("authors_score.csv")
    Countries_final.to_csv("countries_score.csv")

if __name__=="__main__":
    main()
