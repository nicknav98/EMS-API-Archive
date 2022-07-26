import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
import database

def file_to_database(file):
    engine = create_engine(database.SQLALCHEMY_DATABASE_URL)
    df = pd.read_csv(StringIO(str(file.file.read(), 'utf-8')), sep=",", engine="python", header=0)
    df.columns = ["starttime", "endtime", "energy", "unit"]
    df.insert(0, "building_name", "Inspehtorinkatu 1_A")

    df.to_sql("measurements", engine, if_exists="append", index=False)
    print("\nData inserted into database\n")
