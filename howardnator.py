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

base["Countries"] = base["Affiliations"].apply(lambda x: str(x).split(";").strip())


#base["Countries"] = base["Affiliations"].apply(lambda x: str(x).split(",")[-1].strip())

#base["Countries"] = base["Affiliations"].apply(lambda x: str(x).(split(";").split(",")[-1]).strip())