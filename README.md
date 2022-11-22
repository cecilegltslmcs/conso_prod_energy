# Energy production and consumption in France, region by region, from 2012 to 2022

## Table of contents
* [General info](#general-info)
* [Folder organisation](#folder-organisation)
* [Technologies](#technologies)
* [Setup](#setup)
* [Status](#status)
* [Credits](#credits)

## General Info

From the API of the Open Data Réseaux Electrique (ODRé), data are collected with a kafka broker. These data are processing by a Spark job. Then, the data are storaged in a MongoDB database. Finally, a dashboard allows to visualise the data inside the database.
All the microservices are containerized in Docker container.

## Folder organisation

```
└── Energy_consumption/
    └── app/
        ├── images/
        ├── packages/
        │   └── module_kafka.py
        ├── app.py
        ├── dashboard.py
        ├── producer.py
        ├── Dockerfile_dashboard
        ├── Dockerfile_kafka-component
        ├── Dockerfile_spark-component
        ├── Dockerfile_spark-job
        └── requirements.txt
    ├── docker-compose.yaml
    ├── .gitignore
    ├── README.md
```
## Technologies

This project is created with:

- [Apache Kafka](https://kafka.apache.org/documentation/)
- [Apache Spark](https://spark.apache.org/)
- [Docker](https://www.docker.com/)
- [MongoDB](https://www.mongodb.com/)
- [Streamlit](https://streamlit.io/)
## Setup

1) Clone the repository in your computer.
2) Run this project:
```
docker-compose up 
```
3) Access to the dashboard in your browser:
```
localhost:8501
```
## Status

- v1 : Working
## Credits

- Cécile Guillot
