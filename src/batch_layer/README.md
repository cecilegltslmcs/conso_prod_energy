# Batch Layer

This batch layer is composed by three part:
- A script to ingest data and storage them in a database;
- A SQL script used to create the database "Energy consumption" with PostgreSQL;
- A dashboard realized with Streamlit and Python.

# Building of the database

In order to storage the data collect every month by the API, a database was built. The choice for this database is the PostgreSQL.
Data are structured and they are only collected in batch mode, thus it is more pertinent to use a SQL database in this case.
First, the database was built locally in order to do different tests with the differents tools. Secondly, this database will be deployed with Docker.

## Local Setting

The local development was here in order to prepare the script of building the database and the different tables belonging to this database.

## Conceptual model of the data

This is the entity/relationship schema of the database. The tool used to realise it is [Looping](https://www.looping-mcd.fr/).

![ER_Schema_Database](Images/ER_Energy_Consumption.png)

## Logical model of data

After doing the E/R schema, the LMD was realized. For this step, we used the website [Mocodo](https://www.mocodo.net/).

The result of the LMD is the following:

**CONSUMPTION** (<ins>Id_consommation</ins>, code_insee, date_enreg, heure_enreg, consommation, thermique, nucleaire, eolien, solaire, hydraulique, pompage, bioenergies, pct_thermique, pct_nucleaire, pct_eolien, pct_solaire, pct_hydraulique, pct_pompage, pct_bioenergies, _#code_insee.1_)<br>

**COVERAGE_RATE** (<ins>Id_couverture</ins>, code_insee, date_enreg, heure_eng, tco_thermique, tch_thermique, tco_nucleaire, tch_nucleaire, tco_eolien, tch_eolien, tco_solaire, tch_solaire, tco_hydraulique, tch_hydraulique, tco_bioenergies, tch_bioenergies, _#code_insee.1_)<br>

**REGION** (<ins>code_insee</ins>, libelle_region)

## Physical model of data

The physical model of data is a SQL script used to build the database. The script is readable in this part of the project. 