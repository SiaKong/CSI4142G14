##SQL queries
These are the SQL queries written in the database to inesrt/update data. The master table is not a dimension included in the schema but is used to fetch data. The master table is a inner join of all data from all three data sources we have.

<br>
###Insert distinct country names to **country** dimension
Datas have duplicates of country values becaues there are multiple years and demographic datas associated with each country.
> **INSERT INTO** country (country) **SELECT DISTINCT** country **FROM** master;

<br>
###Insert distinct year values to **date** dimension
Datas have duplicates of year values because there are ultiple demographic datas associated with each year.
> **INSERT INTO** date (year) 
> **SELECT DISTINCT** year 
> **FROM** master 
> **WHERE** year >= 1991 **AND** year <= 2016;

<br>
###Insert data to **national_statistics** dimension
> **INSERT INTO** national_statistics (gdp_for_year, percent_pop_unemployed, percent_pop_schizophrenia, percent_pop_bipolar, percent_pop_depression, percent_pop_eating_disorder, percent_pop_drug_use)
> **SELECT DISTINCT** gdp_per_year, unemployment_rate, schizophrenia, bipolar, depression, eating_disorder, drug_use
> **FROM** master

<br>
###Insert data to **suicide_demographic** dimension
>**INSERT INTO** suicide_demographic (suicides_per_100k, suicide_number, population, age_range, gender)
>**SELECT** suicide_per_100k, suicide_number, population, age, sex
>**FROM** master

<br>
###Insert the foreign key values from primary keys of country, date, and suicidie_demographic dimensions to the fact table **suicide_fact_table**
>**INSERT INTO** suicide_fact_table (country_key, year_key, suicide_demographic_key)
>**SELECT** c.country_key, d.year_key, s.suicide_demographic_key
>**FROM**  country c, date d, suicide_demographic s, master m
>**WHERE** m.id = s.suicide_demographic_key
>**AND** m.country = c.country
>**AND** m.year = d.year

<br>
###Update the fact table to also include foreign key value from primary key of national_statistics dimension
>**UPDATE** suicide_fact_table
>**SET** national_statistics_key = finaljoin.national_statistics_key
>**FROM** (
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**SELECT** id, national_statistics_key, country_key, year_key
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**FROM** 
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(**SELECT** id, country_key, year_key, unemployment_rate, gdp_per_year, schizophrenia
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**FROM** master 
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**JOIN** Country **ON** master.country = Country.country
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**JOIN** Date **ON** master.year = Date.year) **AS** temp
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**JOIN** national_statistics **ON** 
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;temp.unemployment_rate = national_statistics.percent_pop_unemployed **AND**
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;temp.gdp_per_year = national_statistics.gdp_for_year **AND**
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;temp.schizophrenia = national_statistics.percent_pop_schizophrenia
>   ) **AS** finaljoin
>**WHERE** suicide_fact_table.suicide_demographic_key = finaljoin.id

<br>
###Update the fact table to include gdp_per_capita value
>**UPDATE** suicide_fact_table
>**SET** gdp_per_capita = m.gdp_per_capita
>**FROM** master m
>**WHERE** suicide_demographic_key = m.id

<br>
###Update the fact table to include total_national_suicides value
The *total_national_suicides* is calculated by sum of all *suicide_number* for each country each year, as we have the *suicide_number* separated by different demographics.
>**UPDATE** suicide_fact_table
>**SET** total_national_suicides = finalJoin.total_national_suicides
>**FROM**
>(
>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**SELECT** temp.total_national_suicides, id
>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**FROM** 
>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(
>        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**SELECT** **SUM**(m.suicide_number) **AS** total_national_suicides, country, year
>        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**FROM** master m
>        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**GROUP BY** country, year
>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;) **AS** temp
>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**INNER JOIN** master **ON** master.country = temp.country
>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**AND** master.year = temp.year
>) **AS** finalJoin
>**WHERE** finalJoin.id = suicide_fact_table.suicide_demographic_key

<br>
###Update the fact_table to include suicide_per_capita value
Originally the *suicide_per_capita* column was *national_suicides_per_100k*, which was calculated as (suicides / population) * 100000. It was part of the original data and we thought it would be a useful data so we decided to include it as one of our measures at first. But we changed it to *suicide_per_capita* because we decided the purpose of the calculation was unclear and thought the new column would be more appropriate since we also had *gdp_per_capita*. 

The *suicide_per_capita* is calculated by *national_total_suicide* divided by total *population* of each country for each year.
>**UPDATE** suicide_fact_table
>**SET** suicides_per_capita = total_national_suicides / finalJoin.total_population
>**FROM**
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**SELECT** temp.total_population, id
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**FROM** 
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**SELECT SUM**(m.population) **AS** total_population, country, year
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**FROM** master m
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**GROUP BY** country, year
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;) **AS** temp
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**INNER JOIN** master **ON** master.country = temp.country
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**AND** master.year = temp.year
>) **AS** finalJoin
>**WHERE** finalJoin.id = suicide_fact_table.suicide_demographic_key