import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

#Define score formula
#n_ACIS meaning number of Authors, Countries or Institutions
#p_ACI meaning position of a determined Author, Country or Institution
def score(n_ACIs, p_ACI):
    coef = 1.5**(n_ACIs - p_ACI)/(np.sum(1.5**(np.arange(1, n_ACIs + 1 ) - 1)))
    return coef

def check_nan(x):
    return (x!=x)

def distribute_points(base,test,sep):
    final_table = {}
    for paper in range(base.shape[0]):
        if check_nan(base.iloc[paper][test]):
            continue
        ACI_list = base.iloc[paper][test].split(sep)
        ACI_list = [ACI.strip() for ACI in ACI_list]

        #remove (1), (2), (3)
        ACI_list = [ACI for ACI in ACI_list if '(' not in ACI]
        #remove "["
        ACI_list = [ACI for ACI in ACI_list if '[' not in ACI]

        n_ACIs = len(ACI_list)
        for pos,ACI in enumerate(ACI_list):
            if ACI in final_table:
                final_table[ACI] += score(n_ACIs,pos+1)
            else:
                final_table[ACI] = score(n_ACIs,pos+1)

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

def find_institution(base):
    inst = []
    sub = ["Universidade", "universidade",
           "University", "university",
           "Université", "université",
           "Universite", "universite",
           "Università", "università",
           "Universita", "universita",
           "Universität", "universität"
           "Universitat", "universitat"
           "Institute", "institute",
           "Corporation", "corporation",
           "Corporate research", "corporate research"
           "Research center", "Research Center", "Research Centre",
           "Polytechnic", "polytechnic"
           "Polytechnical","polytechnical"
           "Politecnico", "politecnico"]
    for paper in range(base.shape[0]):
        inst.append([])
        if check_nan(base.iloc[paper]["Affiliations"]):
            inst[paper]= ', '.join(inst[paper])
            continue
        ACI_list = base.iloc[paper]["Affiliations"].split(";")
        for aff in ACI_list:
            dept = aff.split(",")
            for d in dept:
                if any(substring in d for substring in sub):
                    inst[paper] += [d.strip()]
        inst[paper]= ', '.join(inst[paper])
    return inst

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

    base["Universities"] = find_institution(base)

    Authors_Dict = distribute_points(base,"Authors",",")
    Countries_Dict = distribute_points(base,"Countries",",")
    Institutions_Dict = distribute_points(base,"Universities",",")

    Authors_final = dict_to_df(Authors_Dict,"Authors","Scores")
    Countries_final = dict_to_df(Countries_Dict,"Countries","Scores")
    Institutions_final = dict_to_df(Institutions_Dict,"Institutions","Scores")

    Authors_final = Authors_final.sort_values("Scores", ascending=False)
    Countries_final = Countries_final.sort_values("Scores", ascending=False)
    Institutions_final = Institutions_final.sort_values("Scores", ascending=False)

    Authors_final.to_csv("authors_table.csv", index = False, sep = ';', float_format = '%.2f')
    Countries_final.to_csv("countries_table.csv", index = False, sep = ';', float_format = '%.2f')
    Institutions_final.to_csv("institutions_table.csv", index = False, sep = ';', float_format = '%.2f')

if __name__=="__main__":
    main()
