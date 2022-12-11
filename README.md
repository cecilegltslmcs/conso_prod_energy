# Energy production and consumption in France, region by regionin real time

*Update: 11/12/2022*

This project represents a kappa architecture, which collects, stores and displays data about about energy production and consumption in France. 

## Table of contents
* [General info](#general-info)
* [Folder organisation](#folder-organisation)
* [Technologies](#technologies)
* [Setup](#setup)
* [Status](#status)
* [Credits](#credits)

## General Info

From the API of the Open Data Réseaux Energie (ODRé), data are collected with a Kafka broker. This data is processed by a Spark application before being stored in a MongoDB database. Finally, a dashboard is used to visualize the data inside the database. 
Initially, this dashboard was made using the Streamlit library. However, tools such as Streamlit are not suitable for Big Data problems. 

Therefore, a new version of the dashboard will be developed with Flask (associated with Dash and Plotly).
This application has been developed in different microservices. This process can allow us to containerize each microservice in several Docker containers.

## Folder organisation

```
└── Energy_consumption/
    └── app/
        ├── images/
        ├── packages/
            └── module_kafka.py
        ├── app.py
        ├── dashboard.py
        ├── producer.py
        ├── Dockerfile_dashboard
        ├── Dockerfile_kafka-component
        ├── Dockerfile_spark-component
        ├── Dockerfile_spark-job
        └── requirements.txt
    └── build/ --> contains files for k8s
    ├── docker-compose.yaml
    ├── .gitignore
    └── README.md
```
## Technologies

This project is created with:

- [Apache Kafka](https://kafka.apache.org/documentation/)
- [Apache Spark](https://spark.apache.org/)
- [API ODRé](https://odre.opendatasoft.com/api/v2/console)
- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/fr/)
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
