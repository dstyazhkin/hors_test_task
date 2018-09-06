# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('postgres://fumkaqzm:oKKu9xBISbrD9D7dAx-Cb_sRWAg1nEip@horton.elephantsql.com:5432/fumkaqzm')

df = pd.read_sql_query("SELECT * FROM hors.outlets", engine)

df.head()


df['Торг_точка_чистая']=df['Торг_точка_грязная'].str.replace('[^\w\s]','') #убирает пунктуацию
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('ИП', '')
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('ОАО', '')
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('ЗАО', '')
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('ООО', '')
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('ул ', '')
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace(' ул', '') 
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace(' пер', '') 
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('пер ', '') 
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('м-н ', '') 
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace(' м-н', '') 
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace(' маг', '') 
df['Торг_точка_чистая']=df['Торг_точка_чистая'].str.replace('маг ', '') 
df['Торг_точка_чистая']=(df['Торг_точка_чистая'].str.replace(' ', '')).str.lower()
df['Торг_точка_чистая'].str.lower()

df2 = pd.DataFrame(df['Торг_точка_чистая'])
df2 = df2.drop_duplicates()
df2.reset_index(inplace = True)
df2 = df2.drop('index', axis = 1)
df2.reset_index(inplace = True)
df2.columns = ['outlet_clean_id', 'Торг_точка_чистая']

df.drop('outlet_clean_id', axis = 1, inplace = True)

df3 = (pd.merge(df, df2, on = 'Торг_точка_чистая')).sort_values(by = ['id'])
df3.drop('Торг_точка_чистая', axis = 1, inplace = True)

engine.execute(
        'CREATE TABLE hors.outlets_clean_id ('
        'id integer NOT NULL,'
        'Город_дистрибьютора varchar(14) DEFAULT NULL,'
        'Торг_точка_грязная varchar(262) DEFAULT NULL,'
        'Торг_точка_грязная_адрес varchar(245) DEFAULT null,'
        'outlet_clean_id integer DEFAULT NULL)'
)
        
        
df3.to_sql('outlets_clean_id', engine, if_exists='append', schema = 'hors', index = False)