### Fork of bibliographic reference method

Fork of bibliographic reference method created by [https://github.com/lucasdanelon](https://) and [https://github.com/RBPinheiro13](https://)

If you are going to use this at scientific papers, please give credits to:

[https://reader.elsevier.com/reader/sd/pii/S2212827121004169?token=13FF2FD53E23A07D4B78C295DB4108E110303996F67CD4EFE81E87337CE08D1A9D3A76B0DDA2BF8346293587E0C778AA&originRegion=us-east-1&originCreation=20210503180239](https://)

#### Algorithm

Takes a scopus.csv file as input and generates test.csv and test2.csv

##### how to create input file

Go to [https://www.scopus.com/](https://) , research the subject that you want to analyse, filter as needed and then export such as the image shows:

![Alt text](/typical_output/scopus_selection.png?raw=True)

#### run the script old_howardnator.py

generates 3 csv:

1. authors_table
2. countries_table
3. institutions_table

###### changes

The original fork used the collumn `"Access Type"` , but now scopus uses  `"Open Access"`

obs: the script howardnator.py is supossed to be the new one, but is still being developed
