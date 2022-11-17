# Energy consumption in France from 2012 to 2022

## Table of contents
* [General info](#general-info)
* [Folder organisation](#folder-organisation)
* [Status](#status)
* [Credits](#credits)

## General Info

This architecture is based on a lambda Big Data architecture. It includes two branches: one for the batch processing using a SQL database and one for the streming processing involving a NoSQL solution. 

![ALT](images/Global_Architecture.drawio.png)

The aim of the batch layer is to keep the data in a durable way. The database built for this part of the project will be used for creating dashboard helping to understand the energy consumption and to create machine learning models based on the historical data.
On the other side, the streaming layer is here to give information in real time about what happens concerning the energy consumption. This part needs the help of different technologies such as MongoDB (NoSQL dabatase), Kafka and Spark Streaming to do its job.

## Folder organisation

```.
└── Energy_consumption/
    └── app/
        ├── batch_layer/
        │   ├── database --> Script_database.sql
        │   ├── images
        │   ├── packages/
        │   │   ├── module_ingestion.py
        │   │   └── module_dashboard.py
        │   ├── tests/
        │   │   ├── test_module_ingestion.py
        │   │   └── test_module_dashboard.py
        │   ├── .gitignore
        │   ├── CHANGELOG.txt
        |   ├── ingestion.py
        │   ├── dashboard.py
        │   ├── README.md
        │   └── requirements.txt
        └── streaming_layer/
            ├── packages/
            │   └── module_kafka.py
            ├── tests/
            │   └── test_module_kakfa.py
            ├── .gitignore
            ├── app.py
            ├── producer.py
            ├── CHANGELOG.txt
            ├── README.md
            └── requirements.txt
    ├── .gitignore
    ├── README.md
    ├── images
    ├── sql
    ├── docker-compose.yaml
    ├── requirements.txt
```

## Status

- v1 : Streaming Layer : OK
       Correction Batch Layer : WIP

## Credits

- Cécile Guillot
