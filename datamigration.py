import csv
import psycopg2

dbconnect = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password=""
)

cur = dbconnect.cursor()

with open('master.csv','r') as masterdata:
    master = csv.reader(masterdata)

    #insert data to master table
    line = 0
    for row in master:
        if line != 0:
            id = row[1]
            country = row[2]
            year = int(float(row[3]))
            sex = row[4]
            age = row[5]
            suicide_number = int(float(row[6]))
            population = int(float(row[7]))
            suicide_per_100k = row[8]
            gdp_per_year = int((row[9]).replace(",",""))
            gdp_per_capita = row[10]
            schizophrenia = row[12]
            bipolar = row[13]
            eating_disorder = row[14]
            drug_use = row[16]
            depression = row[17]
            unemployment_rate = row[20]
            cur.execute("INSERT INTO master (id, country, year, sex, age, suicide_number, population, suicide_per_100k, " + 
                        "gdp_per_year, gdp_per_capita, schizophrenia, bipolar, eating_disorder, drug_use, depression, unemployment_rate) " + 
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                        (id,country,year,sex,age,suicide_number,population,suicide_per_100k,gdp_per_year,gdp_per_capita,
                         schizophrenia,bipolar,eating_disorder,drug_use,depression,unemployment_rate,))
        line += 1

dbconnect.commit()
