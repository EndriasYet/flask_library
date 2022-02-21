from sqlalchemy import create_engine
import pandas as pd

Server = 'DESKTOP-LNJG9L8\SQLEXPRESS'
Database = 'Master'
Driver = 'ODBC Driver 17for SQL Server'
Connection_string = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Connection_string)
con = engine.connect()

df=pd.read_sql_query()