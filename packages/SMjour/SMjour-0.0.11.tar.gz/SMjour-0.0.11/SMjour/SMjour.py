import pandas as pd
import pyspssio
import random
import clevercsv
import pyreadstat
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from google.colab import drive
from tqdm import tqdm
from IPython.display import display


def input_path(message=""):  #translate copy path of windows
  raw_s=input(message)
  raw_s=raw_s.replace(r'"','')
  print("/content/drive/Shareddrives/"+'/'.join(raw_s.split("\\")[2:]))
  return "/content/drive/Shareddrives/"+'/'.join(raw_s.split("\\")[2:])
   
def get_data(path=False,sheet_name=0):  #easy get data from MES csv   ###############################################  path y sheet_name
    #import drive
    drive.mount("/content/drive")
    #transform str and get doc
    if path:
      newpath=path
    else:
      newpath=input_path('Input path:')
    
    if (newpath.split("/")[-1].split(".")[-1] == "xlsx") or (newpath.split("/")[-1].split(".")[-1] == "xls"):
        df=pd.read_excel(newpath,sheet_name=sheet_name)
    elif (newpath.split("/")[-1].split(".")[-1] == "csv"):
        df=pd.read_csv(newpath)
    else:
        raise ValueError('Format Not Found')
    try:
      df=df.drop("Unnamed: 0",axis=1)
    except:
       pass
    try:
      df["Weeks"]=pd.to_datetime(df["Weeks"])
    except:
      pass
    
    return df
#"G:\Shared drives\Team members\Agustin\merk\00Q3\1websls\data.csv"
###########################################################################################################################################################


def to_sav(option='default',redundancy=False):  #try to read csv and parse it to sav
    #import drive
    drive.mount("/content/drive")
    newpath=input_path('Input path:')
    if (newpath.split("/")[-1].split(".")[-1] == "xlsx") or (newpath.split("/")[-1].split(".")[-1] == "xls"):
        df=pd.read_excel(newpath)
    elif (newpath.split("/")[-1].split(".")[-1] == "csv"):
        if option=='default':
          #df=pd.read_csv(newpath).reset_index()
          df = clevercsv.read_dataframe(newpath).reset_index()
          #df=df.T.reset_index().T
        elif option == 1:
          with open(newpath, "r", newline="") as fp:
            # you can use verbose=True to see what CleverCSV does
            dialect = clevercsv.Sniffer().sniff(fp.read(), verbose=False)
            fp.seek(0)
            reader = clevercsv.reader(fp, dialect)
            rows = list(reader)
          df=pd.DataFrame(rows)
          df.columns=["a"+str(i) for i in df.columns]
        elif option==2:
          df = clevercsv.read_dataframe(newpath)
        elif option==3:
          rows = clevercsv.read_table(newpath)
          df=pd.DataFrame(rows)  
    else:
        raise ValueError('Format Not Found')
    
    if redundancy:
      df=df.dropna(thresh=len(df)-round(0.99*round(len(df))), axis=1)
    display(df)
    newpath=input_path('Input folder to save:')
    randomo=random.randint(100000, 1000000)
    try:
      pyspssio.write_sav(newpath+f"/data_{randomo}.sav", df)
    except:
      pyreadstat.write_sav(df, newpath+f"/data_{randomo}.sav")
    print(f'Saved as data_{randomo}')
    print('Wait some minutes, the Google Drive is updating')
    return df

def fix_csv(option='default'): #try to fix csv
    #import drive
    drive.mount("/content/drive")
    newpath=input_path('Input path:')
    if (newpath.split("/")[-1].split(".")[-1] == "xlsx") or (newpath.split("/")[-1].split(".")[-1] == "xls"):
        df=pd.read_excel(newpath)
    elif (newpath.split("/")[-1].split(".")[-1] == "csv"):
        if option=='default':
          with open(newpath, "r", newline="") as fp:
            # you can use verbose=True to see what CleverCSV does
            dialect = clevercsv.Sniffer().sniff(fp.read(), verbose=False)
            fp.seek(0)
            reader = clevercsv.reader(fp, dialect)
            rows = list(reader)
          df=pd.DataFrame(rows)
        elif option==1:
          df = clevercsv.read_dataframe(newpath)
        elif option==2:
          rows = clevercsv.read_table(newpath)
          df=pd.DataFrame(rows)  
    else:
        raise ValueError('Format Not Found')
    
    df=df.dropna(thresh=len(df)-round(0.99*round(len(df))), axis=1)
    display(df)
    newpath=input_path('Input folder to save:')
    randomo=random.randint(100000, 1000000)
    df.to_csv(newpath+f"/data_{randomo}.csv",index=False)
    print(f'Saved as data_{randomo}')
    print('Wait some minutes, the Google Drive is updating')


#############################################################################################################################################################
#second page

def adjRsquare(pre_y,r,vars):
  l=len(pre_y)
  return 1 - (1-r2_score(pre_y, r)) * (l-1)/(l-len(vars)-1)
def getVIFs(vars,df):
  result={}
  for i in vars:
    pre_y=df[i].to_numpy()
    df_x=pd.concat([df[[j for j in vars if j!=i]],
                  
            ],axis=1)
    pre_X=df_x.to_numpy()
    # weight=df[weight_col].to_numpy()

    #hago la regresion
    reg = LinearRegression().fit(pre_X, pre_y)   #############OJOTA ,weight
    #reg = LinearRegression().fit(pre_X, pre_y)
    result[i]=1/(1-r2_score(pre_y, reg.predict(pre_X)) )
    result[i]=1/(1-adjRsquare(pre_y, reg.predict(pre_X),vars) )
  return result

#viffs
def getIndexOfCol3(var,allVIFs):
  counter=0
  index=[]
  for j in allVIFs: 
    if var in j.keys():
      index.append(counter)
    counter+=1
  return index
def getFullCombination(boolArray,colls):
  counter=0
  final=[]
  for j in boolArray:
    if j==1:
      final.append(colls[counter])
    counter+=1
  return final
def vif_distance(df,tounderstand,stochQ=1000):   #transform meta vif analisys to block modeling
  #'searchcont
  X_rand=np.random.randint(2, size=[stochQ,len(tounderstand)])
  X_rand=X_rand[np.where(X_rand.sum(axis=1)>=2)]
  allVIFs=[]

  for i in tqdm(X_rand):
    # print(i)
    randomX_cols=getFullCombination(i,tounderstand)
    allVIFs.append(getVIFs(randomX_cols,df))

  for i in allVIFs:
    for j in i.keys():
      if i[j]>3000:
        i[j]=3000
  
  interest=tounderstand

  impacten=tounderstand

  fullTest=tounderstand
  matoPato=[]
  for k in fullTest:
    var=k#x_cols[ind]
    metaY=np.array([allVIFs[i][var] for i in getIndexOfCol3(var,allVIFs)])
    metaX=X_rand[getIndexOfCol3(var,allVIFs)]
    metaReg = LinearRegression(fit_intercept=False).fit(metaX, metaY)
    # meta_betas
    normed_coef=(metaReg.coef_-metaReg.coef_.mean())/metaReg.coef_.std()
    normed_coef=metaReg.coef_
    matoPato.append(list(normed_coef))
  duff=pd.DataFrame(np.array(matoPato).transpose())
  duff.columns=fullTest
  duff.index=impacten

  duff.values[[np.arange(duff.shape[0])]*2] = 0

  to_test=interest

  to_test_index=impacten

  filtered_duff=duff.loc[to_test_index,to_test]
  simil=np.minimum(filtered_duff.to_numpy(),filtered_duff.to_numpy().T)

  simil[simil < 0] = 0
  disimil=1/simil
  disimil[disimil > 200] = 200
  disimil=np.log(disimil+1)
  n = disimil.shape[0]
  disimil[range(n), range(n)] = 0
  disimil=disimil/np.max(disimil)

  simil=1-disimil
  similitude=pd.DataFrame(simil)
  similitude.columns =tounderstand
  similitude.index=tounderstand
  return similitude



def collinearity_test(df,tounderstand=None,distance="vif"):   #full test of collinearity
  tounderstand=tounderstand if tounderstand else df.columns[2:] 
  to_test=tounderstand

  display(getVIFs(tounderstand,df))

  # set figure size
  correlation=df[to_test].corr().fillna(0)
  filter=0
  corr_numpy=correlation.to_numpy()
  indices=corr_numpy.argsort()[:,-2]
  corr_numpy
  finalIndices=[]
  for i in range(len(corr_numpy)):
    value=corr_numpy[i,indices[i]]
    if value>filter or value<-filter:
      finalIndices.append(i)
  finalIndices
  finalCorr=correlation.iloc[finalIndices,finalIndices]

  plt.figure(figsize=(10,7))

  # Generate a mask to onlyshow the bottom triangle
  mask = np.triu(np.ones_like(finalCorr, dtype=bool))

  # generate heatmap
  sns.heatmap(finalCorr, annot=True, mask=mask, vmin=-1, vmax=1,cmap="rocket_r")
  plt.title('Correlation Coefficient Of Predictors')
  plt.show()


  
  data=df[to_test]

  #block distance
  #correlations
  correlations=df[to_test].corr().fillna(0)
  if distance=="corr":
    
    similarity=abs(correlations)
  elif distance=="vif":
    similarity=vif_distance(df,tounderstand,stochQ=1000)
  

  plt.figure(figsize=(12,5))
  dissimilarity = 1 - similarity
  Z = linkage(squareform(dissimilarity), 'complete')

  dendrogram(Z, labels=to_test, orientation='top', 
            leaf_rotation=90);
  plt.tight_layout()
  plt.savefig('maybe.svg', format='svg', dpi=1200)

  ########third
  px.line(((df.groupby('Weeks').mean()-df.groupby('Weeks').mean().mean())/df.groupby('Weeks').mean().std()).reset_index(),x='Weeks',y=tounderstand).show()

