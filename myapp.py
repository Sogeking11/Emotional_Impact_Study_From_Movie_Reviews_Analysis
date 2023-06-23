import pandas as pd
import json




if __name__ == "__main__":
  myDf = pd.read_csv("testapi100.csv", delimiter=';', header=0)
  
  print(myDf.info())

  print(myDf.head(5))
  print(myDf['role'])
  myCols = myDf.columns
  mynewDf = myDf.drop('role', axis=1)
  print(mynewDf.head(5))


  # pour les listes keywords,countries, genres,prod_comp, accéder au film à la ligne 0

  #myDf['keywords'][0]  

  # pour la liste de dictionnaires pour le role, accéder au film à la ligne 0
  #print(myDf['role'][0][0])
  #df_role = pd.DataFrame.from_dict(myDf['role'][0])



#import ast

#list_role = ast.literal_eval(myDf['role'][0])

#df_role = pd.DataFrame.from_dict(list_role)



