from config_read import config
from os import listdir
from os.path import isfile, join
import json,io,time,re,threading,gzip
import mysql.connector

class dbconnection():
    def __init__(self):
        self.params = config()
        self.conn = None
    
    def connect(self):
        self.conn = mysql.connector.connect(**self.params)
        return self.conn

    def get_result_from_query(self,values, query,tablename=None):
        result_output = []
        connection = None
        try:
            connection = self.connect()
            cur = connection.cursor()
            cur.execute(query, tuple(values))
            columns = [col[0] for col in cur.description]
            for row in cur.fetchall():
                result_output.append(dict(zip(columns, row)))
        except (Exception) as error:
            print("Failed to fetch record in " , tablename, error)
        finally:
            # closing database connection.
            if connection:
                cur.close()
                connection.close()
                print("PostgreSQL connection is closed")
        return result_output
    
    def retrieveColumnNames(self,query,tablename=None):
        columns = []
        connection = None
        try:
            connection = self.connect()
            cur = connection.cursor()
            cur.execute(query)
            columns = [col[0] for col in cur.description]
            # for row in cur.fetchall():
            #     result_output.append(dict(zip(columns, row)))
        except (Exception) as error:
            print("Failed to fetch record in " , tablename, error)
        finally:
            # closing database connection.
            if connection:
                cur.close()
                connection.close()
                print("PostgreSQL connection is closed")
        return columns

    def insert(self,values,insert_query,tablename=None):
        connection = None
        try:
            connection = self.connect()
            cur = connection.cursor()
            print(values,insert_query)
            cur.execute(insert_query,tuple(values))
            connection.commit()
            count = cur.rowcount
            print(count, "Record inserted successfully into ",tablename)
        except (Exception) as error:
            if connection:
                connection.rollback()
            print("Failed to insert record in ", error)
        finally:
            # closing database connection.
            if connection:
                cur.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def update(self,values,update_query,tablename=None):
        connection = None
        try:
            connection = self.connect()
            cur = connection.cursor()
            cur.execute(update_query,tuple(values))
            connection.commit()
            count = cur.rowcount
            print(count, "updated the record successfully in ",tablename)
        except (Exception) as error:
            connection.rollback()
            print("Failed to update the table.", error)
        finally:
            # closing database connection.
            if connection:
                cur.close()
                connection.close()
                print("PostgreSQL connection is closed")