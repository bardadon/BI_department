# BI_department

Welcome to my BI department. 

The purpose of this department is to support the analytics requirements of a DVD rental company. The BI department currently supports the following features:

## Features

### 0. Production database 
The company stores its ongoing production data in a PostgreSQL database.
![Untitled(85)](https://github.com/bardadon/BI_department/assets/65648983/5e7b5e85-67ac-4639-912d-95d3ebe57898)

### 1. Transaction Generator
Continuously inserts transactions into the company's production database.
![ezgif com-video-to-gif(1)](https://github.com/bardadon/BI_department/assets/65648983/2b5ea4ab-6afd-491e-980f-fb7440aed113)

### 2. Data Warehouse
The company's Data Warehouse is a fact table in Google BigQuery.
![Untitled(76)](https://github.com/bardadon/BI_department/assets/65648983/9a39d634-6d5f-4c25-9e15-16d1bfb7be46)


### 3. Data Pipeline
Scheduled to run every 5 minutes and transfer batches of new data to the company's Data Warehouse.
![Untitled(78)](https://github.com/bardadon/BI_department/assets/65648983/83b6d3cf-133e-4ec3-b128-ad63d5f57c8e)

### 4. Analytical Dashboards
   
##### Dashboard #1 - Customer Country
![Untitled(80)](https://github.com/bardadon/BI_department/assets/65648983/f7731d54-57af-4bb6-88ce-372fd7a0b818)

##### Dashboard #2 - Customer Activity 1
![Untitled(81)](https://github.com/bardadon/BI_department/assets/65648983/29f006ce-f25e-4465-aef3-f01caedf7b8f)

##### Dashboard #3 - Customer Activity 2
![Untitled(82)](https://github.com/bardadon/BI_department/assets/65648983/9e574154-c64e-4b0f-8553-2462c12c113f)

##### Dashboard #4 - Movies Profits
![Untitled(84)](https://github.com/bardadon/BI_department/assets/65648983/c064eee5-3aa5-4fb5-8d67-d565f81ca931)


For more detailed information, check out my Medium article:
Part 1: https://medium.com/@bdadon50/data-engineering-project-bi-department-part-1-cb6086da3662




