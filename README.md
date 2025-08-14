![NHS logo](static/nhs-logo.png)

# NHS Data Pipeline Project

This project is a data engineering pipeline designed to extract, transform, and load publicly available NHS datasets into a SQL database. The goal is to surface meaningful insights through interactive visualizations using Streamlit.

## Project Overview

The pipeline will:
- Extract data from one or more NHS sources (e.g. hospital admissions, prescriptions, GP appointments)
- Clean and transform the data for analysis
- Load it into a structured SQL database
- Query the database to generate insights
- Present findings through a Streamlit dashboard

## Potential Data Themes

This project is still in the planning phase. Possible areas of focus include:
- Regional variation in healthcare access or outcomes
- Trends in prescription volumes or types
- Waiting times for treatments or appointments
- Hospital activity and capacity over time
- Mental health service usage

## Mental note of blockers as I go. 

I will use this section of readme to document any blockers or things I found challenging along the way, to help me write proper documentation at the end of the project. 
- Massively wide data set from A&E CSV. with 20 + columns

## Planned Tech Stack

- **Python** for ETL scripting
- **pandas / SQLAlchemy** for data manipulation and database interaction
- **PostgreSQL / SQLite** as the target database
- **Streamlit** for interactive data exploration
- **Git** for version control and collaboration

## Goals

- Build a modular, reusable ETL pipeline
- Design clear, queryable database schemas
- Create visualizations that highlight disparities, trends, or inefficiencies
- Make the project easy to extend or adapt for other NHS datasets

## Project Structure (to be finalized)
