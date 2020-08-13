import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Define score formula
#n_ACIS meaning number of Authors, Countries or Institutions
#p_ACI meaning position of a determined Author, Country or Institution
def score(n_ACIs, p_ACI):
    coef = 1.5**(n_ACIs - p_ACI)/(np.sum(1.5**(np.arange(1, n_ACIs + 1 ) - 1)))
    return coef

def distribute_points(base,test):
    final_table = {}
    for paper in range(base.shape[0]):
        ACI_list = base.iloc[paper][test].split(",")
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
    
    #base["Affiliations"].apply(lambda x: str(x))
    #base[['First','Last']] = df.Name.str.split(expand=True)
    #base["Affiliations"].values.tolist()
    #base["Institutions"] = base["Affiliations"].apply(lambda x: str(x).split(";"))
    #Institutions = base["Affiliations"].values.tolist()
    #test = Institutions.apply(lambda x: str(x).split(";"))

    Authors_Dict = distribute_points(base,"Authors")
    Countries_Dict = distribute_points(base,"Countries")

    Authors_final = dict_to_df(Authors_Dict,"Authors","Scores")
    Countries_final = dict_to_df(Countries_Dict,"Countries","Scores")

    Authors_final.to_csv("test.csv")
    Countries_final.to_csv("countriestable2.csv")

if __name__=="__main__":
    main()
