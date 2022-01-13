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

def focal_loss(p,maximum,lam=0.5):
    # Calculate the base score for the top number of citations
    base = -(1-maximum)**lam*np.log(maximum)
    
    # If there are no citations we consider that the author received a score of half 1 citation
    if check_nan(p):
        return (base+(1-2*maximum)**lam*np.log(2*maximum))/2
    
    coef = base+(1-p)**lam*np.log(p)
    return coef


def distribute_points(base,test,sep,base_score):
    final_table = {}
    for paper in range(base.shape[0]):
        if check_nan(base.iloc[paper][test]):
            continue
        citations = base.iloc[paper]["Normalized_citations"]
        ACI_list = base.iloc[paper][test].split(sep)
        ACI_list = [ACI.strip() for ACI in ACI_list]

        #remove (1), (2), (3)
        ACI_list = [ACI for ACI in ACI_list if '(' not in ACI]
        #remove "["
        ACI_list = [ACI for ACI in ACI_list if '[' not in ACI]

        n_ACIs = len(ACI_list)
        for pos,ACI in enumerate(ACI_list):
            if ACI in final_table:
                final_table[ACI] += score(n_ACIs,pos+1)*focal_loss(citations, base_score)
            else:
                final_table[ACI] = score(n_ACIs,pos+1)*focal_loss(citations, base_score)

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

def main(filename):
    #Read database
    base = pd.read_csv(filename, sep = ",")

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

    max_citations = base["Cited by"].max()
    base["Normalized_citations"]=base["Cited by"]/max_citations
    base_score = 0.5/max_citations

    Authors_Dict = distribute_points(base,"Authors",",",base_score)
    Countries_Dict = distribute_points(base,"Countries",",",base_score)
    Institutions_Dict = distribute_points(base,"Universities",",",base_score)

    Authors_final = dict_to_df(Authors_Dict,"Authors","Scores")
    Countries_final = dict_to_df(Countries_Dict,"Countries","Scores")
    Institutions_final = dict_to_df(Institutions_Dict,"Institutions","Scores")

    Authors_final = Authors_final.sort_values("Scores", ascending=False)
    Countries_final = Countries_final.sort_values("Scores", ascending=False)
    Institutions_final = Institutions_final.sort_values("Scores", ascending=False)

    return Authors_final, Countries_final, Institutions_final

if __name__=="__main__":
    filename="/home/gustavo/python/pgref/Tutorial/HAR.csv"

    Authors_final, Countries_final, Institutions_final = main(filename)

    savepath=""
    Authors_final.to_csv(savepath+"3_authors_table.csv", index = False, sep = ';', float_format = '%.2f')
    Countries_final.to_csv(savepath+"4_countries_table.csv", index = False, sep = ';', float_format = '%.2f')
    Institutions_final.to_csv(savepath+"5_institutions_table.csv", index = False, sep = ';', float_format = '%.2f')
