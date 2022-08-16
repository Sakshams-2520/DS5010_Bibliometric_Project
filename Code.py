##Importing Pertinent Libraries
import operator
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
from wordcloud import WordCloud
from country_list import countries_for_language


##Installing the external Libraries
#! pip install WordCloud
#! pip install country-list

class Codet:
        
            
    def __init__(self,df):
        self.df=df
    ##Declaring all the empty dictionaries and lists for us to store the subsequent results into
        self.results={}
        self.l=[] 
        self.di={} # authors name with fractionalized value
        self.d2={} # authors name with no of papers published
        self.firstauthor=[]
        self.sigleauthored=[]
        self.year=df['Year'].tolist()
        self.distictyear={}
        self.TCitationsperYear=[]
        self.citationdf=pd.DataFrame()
        self.reflist=[]
        self.refcount=[]
        self.author=pd.DataFrame(columns=['Name','PaperCount','AuthorFrac'])
        self.authorlist=[]
        self.nAUperPaper=[]
        self.citcount={}
        self.firstAuthAff={}
        self.aff={}
        self.aff2={}
        self.affFrac={}
        self.list1=[]
        self.res={}
        self.aasa={}
        self.a1={}
        self.a2={}
        self.firstauthorcountry=[]
        self.countrycount={}
        self.countrycitation={}
        self.countrydf=pd.DataFrame()
        self.countryname=[]
        self.singlecountry={}
        self.multicountry={}
        self.countrydf2=pd.DataFrame()
        self.citcount2={}
        self.hindexlist={}
        self.gindexlist={}
        self.i10indexlist={}
        self.citationarray=pd.DataFrame()
        self.srdff=[]
        self.citationperyear={}
        self.dfyear=pd.DataFrame()
        self.authorkeywords=[]
        self.distinctauthkey={}
        self.indexkeywords=[]
        self.distinctindexkey={}
        self.totalcitationsauthkeywords={}
        self.totalcitationsindkeywords={}
        self.countries=[]
        
        ##Importing country names and creating a dictionary
        countries_dict = dict(countries_for_language('en'))
        self.countries=[]
        for key in countries_dict.values():
            self.countries.append(key)
            
        self.countrydf2=pd.DataFrame({'Name':self.countries,
                            'Article Count':[0.0]*len(self.countries),
                            'SCP':[0.0]*len(self.countries),
                            'MCP':[0.0]*len(self.countries),
                            'MCP_Ratio':[0.0]*len(self.countries),
                             'Frequency':[0.0]*len(self.countries)
                           })
        self.countrydf2.set_index(['Name'],inplace=True,drop=False)
    
        self.tlist=[]
        self.b=[]
        self.area_dict={}
        self.topsources=[]
        self.doctypecount=[]
        self.doctype=[]
        self.a=[]

    def citationauthors(self):
        #This represents the number of citations for each author for all the papers published by them in that specific domaibn
        aasa=dict(sorted(self.citcount2.items(), key=operator.itemgetter(1),reverse=True))## sorting the result
        global res
        res = dict(list(aasa.items())) ##Storing the self.results in a storage dictionary
        self.results['NoOfCitstionsPerAuthor']=res
    #     print(res)
    
    def calc_hindex(self,citations): 
    #     Calculating thr H index for 1 author
        # sorting in ascending order 
        citations.sort() 
        # iterating over the list 
        for i, cited in enumerate(citations): 
            
            # finding current result 
            result = len(citations) - i 
              
            # if result is less than or equal 
            # to cited then return result 
            if result <= cited: 
                return result 
               
        return 0
    def calc_gindex(self,citations): 
        #Calculating thr G index for 1 author
        citations.sort(reverse=True) 
    #     print(citations)
        length=len(citations)
        for i in range(0,length-1):
            length2=length-i
            sumcount=sum(citations[0:length2])
            if(sumcount>=length2*length2):
    #             print(length2)
                return length2
        return 0
    def calc_i10index(self,citations):
        #Calculating thr i10 index for 1 author
        count=0
        citations.sort(reverse=True)
        length=len(citations)
        for i in range(0,length-1):
            if(citations[i]>=10):
                count=count+1
        return count
    def Hindex(self):
        # Calculating various evaluation matrix like , Gindex, i10 index, H index for all authors
        for val in self.citcount2:
            l=self.citcount[val]
            
            if(len(l)):
                self.hindexlist[val]=self.calc_hindex(l)
                self.gindexlist[val]=self.calc_gindex(l)
                self.i10indexlist[val]=self.calc_i10index(l)
    def unique(self):
        ##Number of authors for the paper
        ##First author for all the papers
        ##Number of papers with a single author and their author names
        ##Citation count for all papers published by individual authors
        for ind in self.df.index:     
            c=self.df['Authors'][ind]
            l2=re.split("[;,]",c)
            l2 = [x.strip() for x in l2]
            if (l2[0]=="-"):
                var.append('-;'+ str(int(self.df['Year'][ind]))+  ' ; '+self.df['Source title'][ind])
                continue;
            self.firstauthor.append(l2[0])##First author for all the papers
            var=l2[0]+' ; '+str(int(self.df['Year'][ind]))+' ; '+self.df['Abbreviated Source Title'][ind] ##First author name along with year and abbreviated source title
            self.srdff.append(var)
            self.df.at[ind,'NoOfAuthors']=len(l2)
            if(len(l2)==1) :
                self.sigleauthored.extend(l2)##Number of papers with a single author and their author names
            for each in l2:
                if each in self.di.keys():
                    self.di[each]=self.di[each]+(1/len(l2))
                    self.d2[each]=self.d2[each]+1
                    self.citcount[each].append(self.df['Cited by'][ind])##Number of papers with a single author and their author names
                    self.citcount2[each]=self.citcount2[each]+self.df['Cited by'][ind]
                else:
                    self.di[each]=1/len(l2)
                    self.d2[each]=1
                    self.authorlist.append(each)
                    self.citcount[each]=[self.df['Cited by'][ind]]
                    self.citcount2[each]=self.df['Cited by'][ind]
        
            self.nAUperPaper.append(len(l2))
    
    def yearfunc(self):
        # Intializing the function yearfunc to determine to perform data analysis on year related data such as
        #in which year the article has been cited,
        # for how long has it been in discussion
        #the name of the authors, 
        #number of papers published in 1 year
        self.results['RangeYear']=int(self.df['Year'].max()-self.df['Year'].min())
    #     self.results['Years']=year
        for ind in self.df.index:
            each=self.df['Year'][ind]
            var2=self.df['Cited by'][ind]
            if each in self.distictyear.keys():
                self.distictyear[each]=int(self.distictyear[each]+1)
                self.citationperyear[each]=int(self.citationperyear[each]+var2)
            else:
                self.distictyear[each]=1
                self.citationperyear[each]=int(var2)
    
        self.results['DictictYears']=self.distictyear
        
    
    def citationpaper(self):
        # Performing data analysis on the citationa data available along with all the pertinent information; 
        yearnow=pd.datetime.now().year
        for i in range(len(self.df)):
            var=self.df["Cited by"][i]/(yearnow-self.df["Year"][i]+1)
            self.TCitationsperYear.append(var)
        self.citationdf['SR']=self.df['SR']
        self.citationdf['DOI']=self.df['DOI']
        self.citationdf['TC']=self.df['Cited by']
        self.citationdf['TCPY']=self.TCitationsperYear
        self.citationdf['Year']=self.df['Year']
        self.citationdf['Title']=self.df['Title']
        self.citationdf=self.citationdf.sort_values(by=['TC'], ascending=False)

    def refrencesfunc(self):
        # Performing data analysis on the references data like the list and count of references of each paper available along with all the pertinent information; 
        for ind in self.df.index:
            ac=self.df['References'][ind]
            l2=re.split(";",ac)
            each=l2[0]
            if(each=="-"):
                self.reflist.append('-')
                self.refcount.append(0)
            else:
                l=each.split(';')
                self.reflist.append(l2)
                self.refcount.append(len(l2))
        self.results['RefrenceList']=self.reflist
        self.results['RefrenceCount']=sum(self.refcount)
    def conv(self):
        ##Declaring the fractionalize citation count for all the author related keyword
        for ea in self.dfauth.index:
            val=self.dfauth['Keyword'][ea]
            z=int(self.totalcitationsauthkeywords[val])
            self.dfauth.at[ea,'Total Citations']=z
            x=z/self.dfauth["Articles"][ea]
            self.dfauth.at[ea,'Fractionalized Citation Count']=x
    def conv2(self):
        ##Declaring the fractionalize citation count for all the paper related keyword
        for ea in self.dfind.index:
            val=self.dfind['Keyword'][ea]
            z=int(self.totalcitationsindkeywords[val])
            self.dfind.at[ea,'Total Citations']=z
            x=z/self.dfind["Articles"][ea]
            self.dfind.at[ea,'Fractionalized Citation Count']=x
    def conv3(self,sourcescitations):
        #Calculating the total citations for each source
        for ea in self.topsources.index:
            z=int(sourcescitations[ea])
            self.topsources.at[ea,'Total Citations']=int(z)
    
    def sources(self):
        # Performing data analysis on all the sources available and use them to determine the total citation and article count 
        symbols = self.df.groupby('Source title')

        self.topsources=symbols['EID'].agg(np.count_nonzero)
        self.topsources=self.topsources.sort_values(ascending=False)
        sourcescitations=symbols['Cited by'].sum()
        sourcescitations=sourcescitations.sort_values(ascending=False)
        self.topsources=self.topsources.to_frame()
        self.conv3(sourcescitations)
        self.topsources=self.topsources.rename(columns={'EID': 'Article Count'})
    
    def rest(self):
        
        self.df['SR']=self.srdff
        self.d2 = sorted(self.d2.items(), key=operator.itemgetter(1),reverse=True)
        self.di = sorted(self.di.items(), key=operator.itemgetter(1),reverse=True)

        self.results['NoOfAuthors']=len(self.d2)
        self.results['Authors']=self.d2
        self.results['AuthorFrac']=self.di
        self.results['FirstAuthors']=self.firstauthor
        self.results['SingleAuthored']=self.sigleauthored
        self.results['N_author_per_paper']=self.nAUperPaper
        self.results['Authorappearances']=sum(self.nAUperPaper)
        self.author=self.author.sort_values(by=['PaperCount'], ascending=False)

        self.dfyear=self.dfyear.sort_values(by=['Year'], ascending=False) 
        self.author=self.author.sort_values(by=['PaperCount'], ascending=False)
        
        
    def createdf(self):
        ## Creating a dataframe from a list about the total info of each author
        self.author['Name']=self.authorlist
        i=0
        for e in self.authorlist:
            self.author.at[i,'PaperCount']=self.d2[e]
            self.author.at[i,'AuthorFrac']=self.di[e]
            self.author.at[i,'CitationCount']=self.citcount2[e]
            self.author.at[i,'Hindex']=self.hindexlist[e]
            self.author.at[i,'Gindex']=self.gindexlist[e]
            self.author.at[i,'I10index']=self.i10indexlist[e]
            
            i=i+1
        i=0
      
        for ea in self.distictyear:
            self.dfyear.at[i,'Year']=int(ea)
            z=int(self.distictyear[ea])
            x=int(self.citationperyear[ea])
            self.dfyear.at[i,'Article Count']=z
            self.dfyear.at[i,'Citation Count']=x
            self.dfyear.at[i,'Avg Citations per Article']=x/z
            
            i=i+1


    def doc(self):
        ##Performing analysis on the different document types present in the dataset like article, book chapter, review, etc
        self.doctype = self.df.groupby('Document Type')
        self.doctypecount=self.doctype['Document Type'].agg(np.count_nonzero)
        papercount=self.df.shape[0]/1000
        if(papercount<10):
            papercount=10
        othercount=0
        for each in self.doctypecount.keys():
    #         print(each)
            if(self.doctypecount[each]<=papercount):
                othercount=othercount+self.doctypecount[each]
                del self.doctypecount[each]
        self.doctypecount['Others']=othercount
    #     print(doctypecount)
    def affiliation(self):
        ##Determing the affiliatiion count and the affiliation fractinalized count for all the affiliated authors and also calculating the first author affiliation count
        for ind in self.df.index: 
            q=self.df['Authors with affiliations'][ind].split(';')
            name=q[0].split(',')[0]
            
            c=self.df['Authors'][ind]
            l2=(re.split("[;,]",c))
            l2 = [x.strip() for x in l2]
            if (l2[0]=="-"):
                continue;
            
            self.list1.append(name)
    
            for each in q:
                if each in self.a1.keys():
                    self.a1[each]=self.a1[each]+(1/len(q))
                    self.a2[each]=self.a2[each]+1
                else:
                    self.a1[each]=1/len(q)
                    self.a2[each]=1
    
                    
                    

        affCount=dict( sorted(self.a2.items(), key=operator.itemgetter(1),reverse=True))    
        affFrac=dict( sorted(self.a1.items(), key=operator.itemgetter(1),reverse=True))    
        i=0
        for e in self.firstauthor:
            self.firstAuthAff[e]=self.list1[i]
            i=i+1
            
        self.results['AffiliationCount']=affCount
        self.results['AffiliationFractionalized']=affFrac
        self.results['FirstAuthAff']=self.firstAuthAff
    
        
    def country(self):
        ##Performing data analysis on all the countries where papers were published 
        #and using that to evaluate
            #Avg Article Citations
            #Total Citations
            #Article Count
        #Also to determine if there was any collaboration of authprs of different countries and hence checking the multi country publication
            #Country_Name
            #Article Count
            #SCP
            #MCP
            #MCP_Ratio
            #Frequency
        
        # Trying to find Country
        for ind in self.df.index:
            i=self.df['Authors with affiliations'][ind]
            w=self.df['Cited by'][ind]
            if(i=='-' or len(i)==0):
                continue
            d=i.split(';')
            dd=d[0].split(',')
            lendd=len(dd)
            var=dd[lendd-1]
            var=str.strip(var)
            self.firstauthorcountry.append(str.strip(var))
            if var in self.countrycount.keys():
                self.countrycount[var]=self.countrycount[var]+1
                self.countrycitation[var]=self.countrycitation[var]+w
            else:
                self.countryname.append(str.strip(var))
                self.countrycount[var]=1
                self.countrycitation[var]=+w
                self.singlecountry[str.strip(var)]=0
                self.multicountry[str.strip(var)]=0
            conuntryval=var
            tempcountlist=[]
            flag=0
            for value in d:
                c=value.split(',')
                length=len(c)
                var2=c[length-1]
                tempcountlist.append(str.strip(var2))
    
            tempcountlist = [value for value in tempcountlist if value in self.countries] 
            tempcountlist=self.uniquel(tempcountlist)
           
                    
                
            if (len(tempcountlist)==1):
                if tempcountlist[0] in self.singlecountry.keys():
                    self.countrydf2.at[tempcountlist[0],'SCP']=self.countrydf2.at[tempcountlist[0],'SCP']+1
                    self.countrydf2.at[tempcountlist[0],'Article Count']=self.countrydf2.at[tempcountlist[0],'Article Count']+1
            else:
                for i in tempcountlist:
                    if i in self.multicountry.keys():
                        self.countrydf2.at[i,'MCP']=self.countrydf2.at[i,'MCP']+1
                        self.countrydf2.at[i,'Article Count']=self.countrydf2.at[i,'Article Count']+1
        
                self.tlist.append(tempcountlist)
            
        self.countrydf['Name']=self.countryname
        
        i=0
        for ind in self.countryname:
            a=self.countrycitation[ind]
            b=self.countrycount[ind]
            self.countrydf.at[i,'Avg Article Citations']=a/b
            self.countrydf.at[i,'Total Citations']=a
            self.countrydf.at[i,'Article Count']=b
            i=i+1
        
            
            
        sumvar=sum(self.countrydf2['Article Count'])
        for i in self.countrydf2.index:
    #        
            b=self.countrydf2.at[i,'Article Count']
    #         
            self.countrydf2.at[i,'Frequency']=float(b/sumvar)
            a=self.countrydf2.at[i,'SCP']
            c=self.countrydf2.at[i,'MCP']
    #         
            if a==0:
                self.countrydf2.at[i,'MCP_Ratio']=0.0
            else:
                self.countrydf2.at[i,'MCP_Ratio']=float(c)/float(a)
        self.countrydf=self.countrydf.sort_values(by=['Total Citations'], ascending=False)

    
    def base2(self):
        self.df['Author Keywords List']=self.authorkeywords
        self.df['Index Keywords List']=self.indexkeywords
        self.df['Refrence List']=self.results['RefrenceList']
        self.df['No of Refrences']=self.refcount

        self.distinctauthkey = sorted(self.distinctauthkey.items(), key=operator.itemgetter(1),reverse=True)
        self.distinctindexkey = sorted(self.distinctindexkey.items(), key=operator.itemgetter(1),reverse=True)
        self.totalcitationsauthkeywords= dict(sorted(self.totalcitationsauthkeywords.items(), key=operator.itemgetter(1),reverse=True))
        self.totalcitationsindkeywords= dict(sorted(self.totalcitationsindkeywords.items(), key=operator.itemgetter(1),reverse=True))

        self.dfauth = pd.DataFrame(self.distinctauthkey, columns =['Keyword', 'Articles'])
        self.dfind = pd.DataFrame(self.distinctindexkey, columns =['Keyword', 'Articles'])
        
    def base3(self):
        self.countrydf2=self.countrydf2.sort_values(by=['Article Count'], ascending=False)

    
    def keywords(self):
        ##Determining all the author related keywords to understand what topics the authors researches in
        for ind in self.df.index:
            c=self.df['Author Keywords'][ind]
            cit=self.df['Cited by'][ind]
            l2=re.split(';',c)
    #         for e in l2:
    #             print(e.strip())
            l2 = [x.strip().upper() for x in l2]
            if (l2[0]=="-"):
                self.authorkeywords.append('-')
                continue
            self.authorkeywords.append(l2)
            for each in l2:
                if each in self.distinctauthkey.keys():
                    self.distinctauthkey[each]=self.distinctauthkey[each]+1
                    self.totalcitationsauthkeywords[each]=self.totalcitationsauthkeywords[each]+cit
                else:
                    self.distinctauthkey[each]=1
                    self.totalcitationsauthkeywords[each]=cit
                    
    def keywordsind(self):
        #Determining all the paper related keywords to understand what keywords the paper revolves about
        for ind in self.df.index:  
            d=self.df['Index Keywords'][ind]
            cit=self.df['Cited by'][ind]
            l3=re.split(';',d)
    #         for e in l2:
    #             print(e.strip())
            l3 = [x.strip().upper() for x in l3]
            if (l3[0]=="-"):
                self.indexkeywords.append('-')
                continue
            self.indexkeywords.append(l3)
            for each in l3:
                if each in self.distinctindexkey.keys():
                    self.distinctindexkey[each]=self.distinctindexkey[each]+1
                    self.totalcitationsindkeywords[each]=self.totalcitationsindkeywords[each]+cit
                else:
                    self.distinctindexkey[each]=1
                    self.totalcitationsindkeywords[each]=cit
    def uniquel(self,list1):
        #Creates a unique list of all the records
        # intilize a null list 
        unique_list = [] 
          
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(str.strip(x)) 
        # print list 
        return  unique_list
    
    def convertfunc(self):
        #Function performing data prepreprocessing on the extracted data, making it ready for analysis
        
        self.df["Year"].fillna(0, inplace = True) 
        self.df["Volume"].fillna(0, inplace = True) 
        self.df["Issue"].fillna(0, inplace = True) 
        self.df["Art. No."].fillna(0, inplace = True) 
        self.df["Page start"].fillna(0, inplace = True) 
        self.df["Page end"].fillna(0, inplace = True) 
        self.df["Page count"].fillna(0, inplace = True) 
        self.df["Cited by"].fillna(0, inplace = True) 
        self.df.fillna('-',inplace=True)
        self.df['Authors'] = self.df['Authors'].str.upper()
        self.df["Authors"]= self.df.apply(lambda x: x['Authors'].replace('.', ''), axis=1)
        self.df["Authors"]= self.df["Authors"].replace(',', ';', regex = True)
        self.df['Authors with affiliations'].fillna('-',inplace=True)   
    def analysis(self): 
        self.results['Articlecount']=self.df.shape[0]  
    

    def citation(self,mode="author",k=10):
        #Searching for citation details based on different search parameters
        lista=[]
        if(mode=="article"):
            for i in range(0,k):
                var=self.citationdf['SR'][i]
                var+=self.citationdf['DOI'][i]
                lista.append(var)
            df111=pd.DataFrame()
            df111['Article Name']=lista
            df111['Citation Count']=self.citationdf['TC'][0:k].tolist()
            print(df111)
            
        elif(mode=="author"):
            out=dict(list(self.results['NoOfCitstionsPerAuthor'].items())[0: k])
            out = sorted(out.items(), key=operator.itemgetter(1),reverse=True)
            pprint(out)
    def articles(self,k=10):
        #Diplaying the most impactful articles based on citation counts per year
        print('\n\nMOST IMPACTFUL ARTICLES BASED ON CITATIONS \n')
        print(self.citationdf[0:k].to_string(index=False))
        
    def author_details(self,name="*"):
        #Searching for author details based on different search parameters
        if(name=="*"):
            print(self.author.head(10))
            
            
        elif (isinstance(name, int)):
            for ind in self.df.index: 
                var3=''
                c=self.df['Author(s) ID'][ind]
                l2=re.split("[;,]",c)
                l2 = [x.strip() for x in l2]
                d=self.df['Authors'][ind]
                l3=re.split("[;,]",d)
                l3 = [x.strip() for x in l3]
                if (l2[0]=="-"):
                    continue;
                for each,each2 in zip(l2,l3):
                    try:
                        if(each==''):
                            each=0
                        if(int(each)==name):
                            print(each2)
                    except:
                        continue
                          
                
        else:
            name.strip().upper()
            print(self.author.loc[self.author['Name'] .str.contains(name)])
            
    def author_paper_analysis(self,name="*"):
        #Searching for each paper details for the inputed author 
        if(name=="*"):
            print("Give author name nin function")
            return
        else:
            name.strip().upper()
            print('\nPAPERS PUBLISHED BY AUTHOR \n\n')
            ab=[]
            b=[]
            ce=[]
            d=[]
            e=[]
            for ind in self.df.index: 
                index2=0
                c=self.df['Authors'][ind]
                l2=(re.split("[;,]",c))
                l2 = [x.strip() for x in l2]
                if (l2[0]=="-"):
                    continue;
                if (name in l2):
    
                    ab.append(l2)
                    b.append(self.df['Title'][ind] )
                    ce.append(self.df['Source title'][ind] )
                    d.append(self.df['Year'][ind])
                    e.append(self.df['Cited by'][ind])
        #             index2=index2+1
            self.citationarray['Authors']=ab
            self.citationarray['Title']=b
            self.citationarray['Source']=ce
            self.citationarray['Year']= d
            self.citationarray['Citations']=e
            print(self.citationarray.sort_values(by=['Year','Citations'], ascending=(False,False)))
    def article_details(self,name="*"):
        #Printing relevent article details for the author
        if(name=="*"):
            print(self.citationdf.head(10))
        else:
            name=name.strip()
            print(self.citationdf.loc[self.citationdf['DOI'].str.contains(name)])
    
    
    
    def result_topics(self):
        for each in self.results:
            print(each)
    
    ## Final Textual Results
    
    def summary(self,k=10):
        
        
        ##Generating the summary of the dataset along with all the relevant results for all the functions
        print("BASIC INFORMATION \n")
        print('Articles published over '+ str(self.results['RangeYear']) + ' years from '+str(int(self.df['Year'].min()))+' to '+str(int(self.df['Year'].max())))
        print('Total no of Articles                  :           '+str(self.results['Articlecount']))
        print('Total no of Sources                   :          ',len(self.topsources))
        print('Average citations per documents       :          ',round(statistics.mean(self.df['Cited by']),4))
        print('Average citations per year per doc    :          ',round(statistics.mean(self.TCitationsperYear),4))
        print('Total No of Refrences                 :          ',sum(self.df['No of Refrences']))
        
        print('\n\nKEYWORDS\n')
        print('Keywords                              :          ',len(self.distinctindexkey))
        print('Authors keywords                      :          ',len(self.distinctauthkey))
        
        
        print('\n\nAUTHOR INFORMATION \n\nTotal no of Authors                   :           '+str(self.results['NoOfAuthors']))
        print('Total no of Author Appearances        :           '+str(self.results['Authorappearances']))
        v=len(np.unique(self.results['SingleAuthored']))
        print('Authors of Single-authored documents  :           '+str(v))
        print('Authors of Multi-authored documents   :           '+ str(self.results['NoOfAuthors']-v))
        
              
              
        print('No of Single-authored documents       :           '+str(len(self.results['SingleAuthored'])))
        print('Average Documents per Author          :          ',round(self.results['Articlecount']/self.results['NoOfAuthors'],4))
        print('Authors per Document                  :          ',round(self.results['NoOfAuthors']/self.results['Articlecount'],4))
        
        print('Co-Authors per Documents              :          ',(round(statistics.mean(self.nAUperPaper),4)))
        print('Collaboration Index                   :          ',round((self.results['NoOfAuthors']-v)/sum(self.nAUperPaper),4))
        
    
        
        print('\n\nNo of Articles each Year OR Annual Scientific Production')
        print(self.dfyear)
            
        aa=(self.results['DictictYears'][int(self.df['Year'].max())]/self.results['DictictYears'][int(self.df['Year'].min())])
        print('\n')
        pprint(self.doctypecount)
    
        
        print('\n\nMOST PRODUCTIVE AUTHORS\n')
        print(self.author[['Name','PaperCount','AuthorFrac']][0:10].to_string(index=False)) 
        
        print('\n\nMOST RELEVENT SOURCES\n')
        print(self.topsources[0:10])
        
        print('\n\nMOST IMPACTFUL ARTICLES BASED ON CITATIONS \n')
        print(self.citationdf[['SR','DOI','TC','TCPY']][0:10].to_string(index=False))
        
        print('\n\nMOST IMPACTFUL COUNTRIES \n')
        print(self.countrydf[0:10].to_string(index=False))
        
        print('\n\nCOUNTRY COLLABORATION\n')
        
        print(self.countrydf2.sort_values(by=['Article Count'], ascending=False)[0:10].to_string(index=False))
        
        
        print('\n\nTOP AUTHOR KEYWORDS\n')
        pprint(self.dfauth.head(10))
        
        print('\n\nTOP USED KEYWORDS\n')
        pprint(self.dfind.head(10))
        
        
        
        print('\n\nTOP 15 AUTHORS WITH HIGHEST CITATIONS AMONGST ALL PAPERS\n')
        self.citation('author',15)
        print('\n\nTOP 15 ARTICLES WITH HIGHEST CITATIONS AMONGST ALL PAPERS\n')
        self.citation('article',15)
        print('\n\nMOST IMPACTFUL ARTICLES BASED ON CITATIONS OVER EVERY YEAR\n')
        self.articles(5)
        print('\n\ABILITY TO SEARCH INFO FOR A PARTICULAR AUTHOR\n\n')
        self.author_details(name='WANG Y')
        print('\n\nABILITY TO SEARCH INFO FOR A PARTICULAR AUTHOR USING AUTHOR ID\n')
        self.author_details(name=57208348441)
        print('\n\nDELINEATING THE AUTHOR DETAILS FOR EVERY AUTHOR BASED ON THEIR PAPER COUNT\n')
        self.author_details()
        print('\n\nALL DETAILS OF PAPERS PUBLISHED BY A SPECIFIC AUTHOR\n')
        self.author_paper_analysis('WANG Y')
        print('\n\nDELINEATING THE ARTICLE DETAILS FOR EVERY ARTICLE\n')
        self.article_details()
        print('\n\nDELINEATING ARTICLE DETAILS USING ARTICLE ID \n')
        self.article_details('10.1093/cvr/cvaa')
    
    
    
    
    
    
    ## Final Visualizations
    
    def plot_author(self,k=10):
        # Plotting the Authors vs their Article count and Fractionalized Value
        cdf=self.author.head(10)
        fig, ax1 = plt.subplots(figsize=(10,6))
        plt.xticks(rotation=30)
        ax1.xaxis.set_tick_params(pad = 10) 
    
        sns.barplot(x='Name', y='PaperCount',data=cdf, palette='winter')
        ax1.tick_params(axis='y')
        plt.ylabel("No of Articles Published",size=15) 
        plt.xlabel("Author Name",size=15)
        ax2 = ax1.twinx()
        ax2 = sns.lineplot(x='Name', y='CitationCount', data = cdf,sort=False,color='red',alpha=0.7,linewidth = 5)
        ax2.tick_params(axis='y',color='red')
        plt.legend(labels=['Citation Count'],loc="upper right")
    
        plt.ylabel("Author Fractionalized Value",size=15) 
        plt.draw()
        
        
    def plot_doctype(self):
        # Plotting the count of different Document Types
        plt.figure(figsize=(10,7))
        my_circle=plt.Circle( (0,0), 0.6, color='white')
        plt.pie(self.doctypecount,labels=self.doctypecount.keys())
        plt.legend(labels=self.doctypecount.keys(),loc="upper right",title="Types",bbox_to_anchor=(1, 0, 0.3, 1),fontsize=10)
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        plt.title("Document Types",size=25) 
        plt.draw()
    def plot_countrypublications(self,k=10):
        # Plotting the Most Productive Countries based on MCP and SCP 
        plt.figure(figsize=(12,6))
        self.a2=self.countrydf2.sort_values(by=['SCP']+['MCP'], ascending=False)
        plt.barh(self.a2[0:k]['Name'],self.a2[0:k]['SCP'],label='Single Country Publication')
        plt.barh(self.a2[0:k]['Name'],self.a2[0:k]['MCP'],label='Multi Country Publication')
        plt.xlabel('No of Publications',size=15)
        plt.ylabel('Countries',size=15)
        plt.legend(labels=['SCP','MCP'],loc="upper right",title="Collaboration")
        plt.title('Most Productive Countries',size=25)
        plt.draw()
    def annualproduction(self):
        # Plotting the Annual Scientitific Production
        plt.figure(figsize=(12,6))
        plt.plot(self.dfyear['Year'],self.dfyear['Article Count'], color='red', marker='o')
        plt.fill_between(self.dfyear['Year'],self.dfyear['Article Count'], color='orange',alpha=0.2)
        plt.locator_params(axis="x", integer=True)
        plt.title('Annual Scientitific Production', fontsize=14)
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('No of Articles', fontsize=14)
        plt.grid(True)
        plt.draw()
    def citations_per_year(self):
        # Plotting the Average Article Citations per Year and the Average Total Citations per Year
        plt.figure(figsize=(15,6))
        plt.subplot(121)
        plt.plot(self.dfyear['Year'],self.dfyear['Avg Citations per Article'], color='red',label='Avg Article per Year')
        plt.fill_between(self.dfyear['Year'],self.dfyear['Avg Citations per Article'], color='red',alpha=0.4,label='Avg Article per Year')
        plt.locator_params(axis="x", integer=True)
        plt.title('Average Article Citations per Year',size=25)
        plt.subplot(122)
        plt.plot(self.dfyear['Year'],self.dfyear['Citation Count'], color='blue',label="Avg Citation per Year")
        plt.fill_between(self.dfyear['Year'],self.dfyear['Citation Count'], color='blue',alpha=0.4,label="Avg Citation per Year")
        plt.locator_params(axis="x", integer=True)
        plt.title('Average Total Citations per Year',size=25)
        plt.draw()
    
    def plot_country(self,k=10): 
        # Plotting Article count and the Average Citations per article for top countries
        cdf=self.countrydf.sort_values(by=['Article Count'], ascending=False).head(10)
        fig, ax1 = plt.subplots(figsize=(10,6))
        plt.xticks(rotation=30)
        sns.barplot(x='Name', y='Article Count',data=cdf, palette='winter')
        ax1.tick_params(axis='y')
        plt.ylabel("Country Article Count ",size=15) 
        plt.xlabel("Country Name",size=15)
        ax2 = ax1.twinx()
        ax2 = sns.lineplot(x='Name', y='Avg Article Citations', data = cdf,sort=False, color='red',alpha=0.7,linewidth = 5)
        ax2.tick_params(axis='y',color='red')
        plt.legend(labels=['Avg Article Citations'],loc="upper right")
        plt.ylabel("Average Citations per article  ",size=15) 
        plt.draw()
    
        
        
    def keywordcloud(self):
       # Word cloud depicting the most common words in the papers
        wordcloud = WordCloud(height=10000, width=10000, background_color='white')
        wordcloud = wordcloud.generate(' '.join(self.df['Author Keywords'].tolist()))
        plt.figure(figsize=(12,12))
        plt.imshow(wordcloud)
        plt.title("Most common words in the papers")
        plt.axis('off')
        plt.show()
        
    def plot(self):
        #Plotting all the base visualizations
        self.plot_author(10)
        self.plot_doctype()
        self.plot_countrypublications(10)
        self.annualproduction()
        self.citations_per_year()
        self.plot_country()
        self.keywordcloud()
    
    
    
    
    
    
    
    def func(self):
        #Prepping data for Network graphs
        self.countrydf2=self.countrydf2.sort_values(by=['Article Count'], ascending=False)
        countrys=self.countrydf2.head(50).index
        
        
        for ind in range(len(self.tlist)):
            self.tlist[ind]=self.uniquel(self.tlist[ind])
            self.tlist[ind]=[value for value in self.tlist[ind] if value in countrys] 
        
        
        for ind in range(len(self.tlist)):
            self.tlist[ind]=[value for value in self.tlist[ind] if value in self.countries] 
        
        
        u = pd.get_dummies(pd.DataFrame(self.tlist), prefix='', prefix_sep='').sum(level=0, axis=1)
        
        v = u.T.dot(u)
        v.values[np.tril(np.ones(v.shape)).astype(np.bool)] = 0
        
        
        self.a = v.stack()
        self.a = self.a[self.a >= 1].rename_axis(('source', 'target')).reset_index(name='weight')
        
        for ind in self.a.index:
            if(self.a['weight'][ind]<=20):
                self.a.drop([ind],inplace = True)
        
        self.a=self.a.sort_values(by=['weight'], ascending=False)
        
        
        self.b=self.a['source']
        self.b=self.b.append(self.a['target'])
        self.b=self.uniquel(self.b)
        
        
        self.area_dict = dict(zip(self.countrydf.Name, self.countrydf['Article Count']))
        
    
    
    
    
    ## Graph Vizualizations
        
    ## Country collaboration networks
    def plot_countrycollaboration(self):
            self.func()
            #Add nodes
            plt.clf()
            plt.figure(figsize=(20,20)) 
            G = nx.Graph() #Create a graph object called G
            node_list = self.b
            for node in node_list:
                G.add_node(node)
    
            pos=nx.random_layout(G) 
            nx.draw_networkx_nodes(G, pos = pos, node_color = 'green', alpha = 0.8, node_size = [self.area_dict[s] for s in G.nodes()])
    
            # adding labels to nodes
            labels = {}
            for node_name in node_list:
                labels[str(node_name)] =str(node_name)
            nx.draw_networkx_labels(G,pos,labels,font_size=16,font_weight='bold',font_color='black')
    
            #Adding the edges
            for ind in self.a.index:
                G.add_edge(self.a['source'][ind],self.a['target'][ind],weight=self.a['weight'][ind])
    
            all_weights = []
            #Iterate through the graph nodes to gather all the weights
            for (node1,node2,data) in G.edges(data=True):
                all_weights.append(data['weight']) #we'll use this when determining edge thickness
    
            #Get unique weights
            unique_weights = list(set(all_weights))
    
            #Plot the edges
            for weight in unique_weights:
                weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
                width = weight*len(node_list)*9.0/sum(all_weights)
                nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width,edge_color="#263341",alpha=0.8)
    
            #Plot the graph
            plt.show()     
    
    
    
    
    
    
    ## Keyword co-occurrence networks
    def plot_cooccurrence(self):
            self.func()
            #Add nodes
            plt.clf()
            plt.figure(figsize=(20,20))    
            G = nx.Graph() #Create a graph object called G
            node_list = self.b
            for node in node_list:
                G.add_node(node)
    
            pos=nx.spring_layout(G, k=0.42, iterations=17) 
            nx.draw_networkx_nodes(G, pos = pos, node_color = 'r', alpha = 0.8, node_size = [self.area_dict[s] for s in G.nodes()])
    
            # adding labels to nodes
            labels = {}
            for node_name in node_list:
                labels[str(node_name)] =str(node_name)
            nx.draw_networkx_labels(G,pos,labels,font_size=16)
    
    
    
            #Adding the edges
            for ind in self.a.index:
                G.add_edge(self.a['source'][ind],self.a['target'][ind],weight=self.a['weight'][ind])
    
            all_weights = []
            #Iterate through the graph nodes to gather all the weights
            for (node1,node2,data) in G.edges(data=True):
                all_weights.append(data['weight']) #we'll use this when determining edge thickness
    
            #Get unique weights
            unique_weights = list(set(all_weights))
    
            #Plot the edges
            for weight in unique_weights:
                weighted_edges = 2*[(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
                width = weight*len(node_list)*3.0/sum(all_weights)
                nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width)
    
    
        #Plot the graph
    plt.show()
