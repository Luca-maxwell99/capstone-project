![NHS logo](static/nhs-logo.png)

# NHS A&E Data Pipeline Project

This project is a data engineering pipeline designed to extract, transform, and load publicly available NHS Accident & Emergency (A&E) datasets into a SQL database. The goal is to surface meaningful insights through interactive visualizations using Streamlit.

## Project Overview

The pipeline will:

Extract A&E attendance data from monthly NHS CSV datasets.

Transform the data — cleaning, standardising formats, and selecting relevant fields for analysis.

Load the cleaned dataset into a structured SQL database (PostgreSQL for development, SQLite for quick local testing).

Query the database to generate insights into A&E demand and performance.

Visualise results via a Streamlit dashboard.

## Chosen Dataset

Source: NHS A&E Monthly Attendance and Emergency Admissions Dataset.

Format: CSV (monthly data).

Scope: MVP focuses solely on A&E attendances, with potential expansion to other NHS datasets later.

## Key Analytics / Business Questions

How have A&E attendances changed over time?

Which regions or hospital trusts see the highest attendances?

Are there seasonal trends in attendances (e.g., winter pressures)?

What is the proportion of patients admitted vs discharged?

## Planned Tech Stack

Python – ETL scripting

pandas – data manipulation

SQLAlchemy – database interaction

PostgreSQL / SQLite – target databases

Streamlit – interactive dashboard

Git & GitHub – version control

## Current Blockers / Challenges

Dataset is very wide (20+ columns), requiring careful selection of relevant fields.

Need to decide final database schema to balance performance and flexibility.


## MVP Checkpoint – Friday 15th

By Friday 15th, the repository will contain:

Public GitHub repo.

README with goal, dataset choice, questions, and plan.

.env.example file.

KanBan board (github project) with backlog and in-progress tasks.

Short document outlining targeted insights and branch workflow.