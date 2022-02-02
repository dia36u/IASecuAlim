import numpy as np
import pandas as pd
from database.Classes import Connection

def launchETL():
    db = Connection.connection_to_database()
    test = Connection.query_all(db, 'select * from type_activite;')
    print(test)
