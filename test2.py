import psycopg2
import time



#CONNECTION = "dbname=postgres user=postgres host=172.17.0.2 port=5432 sslmode=require"
while True:
    try:
        connector=psycopg2.connect(dbname="postgres",
                                    user="postgres",
                                    password="badrT",
                                    host="localhost",
                                    port="5432")

        cursor=connector.cursor()
        print("WE MADE A SUCCESSFUL CONNECTION TO THE DATABASE")
        break
    except Exception as error:
        print("CONNECTION FAILED")
        print("ERROR : ",error)
        time.sleep(2)