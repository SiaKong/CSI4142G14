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

    #insert unique country names to country dimension
    # INSERT INTO country (country) SELECT DISTINCT country FROM master;

    #insert unique country names to country dimension
    # INSERT INTO date (year) 
    # SELECT DISTINCT year 
    # FROM master 
    # WHERE year >= 1991 AND year <= 2016;

    # INSERT INTO national_statistics (gdp_for_year, percent_pop_unemployed, percent_pop_schizophrenia, percent_pop_bipolar, percent_pop_depression, percent_pop_eating_disorder, percent_pop_drug_use)
    # SELECT DISTINCT gdp_per_year, unemployment_rate, schizophrenia, bipolar, depression, eating_disorder, drug_use
    # FROM master

    # INSERT INTO suicide_demographic (suicides_per_100k, suicide_number, population, age_range, gender)
    # SELECT suicide_per_100k, suicide_number, population, age, sex
    # FROM master

    # INSERT INTO suicide_fact_table (country_key, year_key, suicide_demographic_key)
    # SELECT c.country_key, d.year_key, s.suicide_demographic_key
    # FROM  country c, date d, suicide_demographic s, master m
    # WHERE m.id = s.suicide_demographic_key
    # AND m.country = c.country
    # AND m.year = d.year

    # UPDATE suicide_fact_table
    # SET national_statistics_key = finaljoin.national_statistics_key
    # FROM (
    # SELECT id, national_statistics_key, country_key, year_key
    # FROM 
    #     (SELECT id, country_key, year_key, unemployment_rate, gdp_per_year, schizophrenia
    #     FROM master 
    #     JOIN Country ON master.country = Country.country
    #     JOIN Date ON master.year = Date.year) AS temp
    # JOIN national_statistics ON 
    # temp.unemployment_rate = national_statistics.percent_pop_unemployed AND
    # temp.gdp_per_year = national_statistics.gdp_for_year AND
    # temp.schizophrenia = national_statistics.percent_pop_schizophrenia
    # ) AS finaljoin
    # WHERE suicide_fact_table.suicide_demographic_key = finaljoin.id

    # UPDATE suicide_fact_table
    # SET gdp_per_capita = m.gdp_per_capita
    # FROM master m
    # WHERE suicide_demographic_key = m.id

    # UPDATE suicide_fact_table
    # SET total_national_suicides = finalJoin.total_national_suicides
    # FROM
    # (
    #     SELECT temp.total_national_suicides, id
    #     FROM 
    #     (
    #         SELECT SUM(m.suicide_number) AS total_national_suicides, country, year
    #         FROM master m
    #         GROUP BY country, year
    #     ) AS temp
    #     INNER JOIN master ON master.country = temp.country
    #     AND master.year = temp.year
    # ) AS finalJoin
    # WHERE finalJoin.id = suicide_fact_table.suicide_demographic_key

    # UPDATE suicide_fact_table
    # SET national_suicides_per_100k = total_national_suicides/100000

# UPDATE suicide_fact_table
# SET suicides_per_capita = total_national_suicides / finalJoin.total_population
# FROM
# (
# 	SELECT temp.total_population, id
# 	FROM 
# 	(
# 		SELECT SUM(m.population) AS total_population, country, year
# 		FROM master m
# 		GROUP BY country, year
# 	) AS temp
# 	INNER JOIN master ON master.country = temp.country
# 	AND master.year = temp.year
# ) AS finalJoin
# WHERE finalJoin.id = suicide_fact_table.suicide_demographic_key