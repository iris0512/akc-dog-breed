import pandas as pd
import re
from akc_utils import *

path = "YOUR PATH HERE"

df_breeds = pd.read_csv(path+'american-kennel-club-dataset.csv',encoding= 'unicode_escape')
df_breeds.head()
df_breeds.columns
df_breeds.info()
numeric_cols = ['Affectionate With Family', 'Good With Young Children',
       'Good With Other Dogs', 'Shedding Level', 'Coat Grooming Frequency',
       'Drooling Level','Openness To Strangers',
       'Playfulness Level', 'Watchdog/Protective Nature', 'Adaptability Level',
       'Trainability Level', 'Energy Level', 'Barking Level',
       'Mental Stimulation Needs']
text_cols = ['Coat Type', 'Coat Length','Temperament','Group']
convert_cols = ['Height_Male', 'Height_Female',
       'Weight_Male', 'Weight_Female', 'Life_Expectancy']

#find unique values of numeric columns to see if it is in acceptable range (1-5)
for n in numeric_cols:
    print("column",n)
    print(df_breeds[n].unique())

#there are some nans, fill it with 0, as there is no score registered on the website on spot-checking for some 
df_breeds[numeric_cols] = df_breeds[numeric_cols].fillna(0)

#let us convert it all to integer type as there is no half point scores being assigned
df_breeds[numeric_cols] = df_breeds[numeric_cols].astype("int")

#checking text columns
for t in text_cols:
    print(t)
    print(df_breeds[t].unique())

#fill all nulls with 'N/A'
df_breeds[text_cols] = df_breeds[text_cols].fillna('NA')

df_breeds['Coat Type'] = df_breeds['Coat Type'].apply(lambda x: (" ").join(re.split('(?<=.)(?=[A-Z])',x)))
df_breeds['Coat Length'] = df_breeds['Coat Length'].apply(lambda x: (" ").join(re.split('(?<=.)(?=[A-Z])',x)))
df_breeds['Temperament'] = df_breeds['Temperament'].apply(lambda x: x.replace(" / ",","))
df_breeds['Group'] = df_breeds['Group'].apply(lambda x: re.sub("[ Â»]|[ »]"," ",x).capitalize().strip())

df_breeds[convert_cols] = df_breeds[convert_cols].fillna("Info Not Available")

#cleaning values before conversion
#df_breeds['Height_Female'] = df_breeds['Height_Female'].apply(lambda x: re.sub(" 1/2",".5",x))
df_breeds['Height_Male'] = df_breeds['Height_Male'].apply(lambda x: re.sub(" 1/2",".5",x))
df_breeds['min_height_male'],df_breeds['max_height_male'] = convert(df_breeds,'Height_Male')
df_breeds['min_height_female'],df_breeds['max_height_female'] = convert(df_breeds,'Height_Female')
df_breeds['min_weight_male'],df_breeds['max_weight_male'] = convert(df_breeds,'Weight_Male')
df_breeds['min_weight_female'],df_breeds['max_weight_female'] = convert(df_breeds,'Weight_Female')
df_breeds['min_expectancy'],df_breeds['max_expectancy'] = convert(df_breeds,'Life_Expectancy')

df_breeds.columns
df_breeds.to_csv(path+'american-kennel-dataset-cleaned.csv',index=False)