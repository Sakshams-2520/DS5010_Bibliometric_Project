##Importing Pertinent Libraries
import operator
import Code as code
import re
import pandas as pd
import numpy as np
import itertools  
from pprint import pprint 
import statistics 
import matplotlib.pyplot as plt
import matplotlib.figure
import seaborn as sns
import networkx as nx



## Importing dataset and preprocessing
#### Importing dataset and performing some pre-processing to make data ready for Analysis
##Importing the main dataset and calling the function to initialize the required variables
   
df=pd.read_csv(r'C:\Users\13412\Downloads\combined_covid (1).csv')
code=code.Codet(df)
code.convertfunc()




## Data Analysis and Preprocessing combined
#Calling function to perform data analysis and generate the required results and store them accordingly
code.analysis()

# Calling the function yearfunc to determine the years in which year the article has been cited, 
# for how long has it been in diiscussion and the name of the authors
code.yearfunc()
   

# Evaluating various evaluation metrics
code.unique()
code.Hindex()
code.createdf()
code.rest()

# most frequent cited  authors - run thi only after unique func
code.citationauthors()


# no of authors per paper can be calculated but not exactly needed maybe
# also total no of Author appearances (sum of the above commented)

# most cited papers
code.citationpaper()
#create function for graph or list of top k sited papers


#top sources
code.sources()


#refrences
code.refrencesfunc()

#documentype 
code.doc()

#affiliations perform authors fuction befor this
code.affiliation()

#country
code.country()


#author and index keyword analysis
code.keywords()
code.keywordsind()
code.base2()

code.conv()
code.conv2()
code.base3()


code.result_topics()



##Final result consolidating the output for all the functions
code.summary(20)

#All Visual Results
code.plot()


#Country Collaboration network
code.plot_countrycollaboration()


#Keyword Cooccurence Network
code.plot_cooccurrence()


    
