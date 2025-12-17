# Personal Finance Dashboard  
### Streamlit • SQLite • AI • Speech-to-Text

A full-stack personal finance tracking application built with **Streamlit** and **SQLite**, designed to help users log income and expenses, visualize monthly trends, and interact with their data using **AI-assisted natural language input and speech-to-text**.

This project was developed as part of **CPSC-350**.

## Overview

The goal of this project was to build an end-to-end data-driven application that balances **data integrity**, and **user-friendly interaction**. The system supports structured financial data storage while easing the user experience through AI-powered input methods.

## Running the Application

### Prerequisites
- Python 3.10 or newer
- pip (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/A-Maherr/CPSC350Project.git
cd CPSC350Project
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run the Application
```bash
streamlit run Main.py
```
## API Key Configuration

This application uses AI-powered parsing to convert free-form or spoken expense input into structured data.  
To enable these features, an **API key is required**.

### Streamlit Secrets

The project uses Streamlit’s built-in secrets management.

Add your API key to the existing file:

```text
.streamlit/secrets.toml
```

## Core Features

### Income and Expense Management
- Monthly income logging
- Categorized expense tracking using a normalized schema
- Safeguards to prevent duplicate monthly entries

### Interactive Data Visualization
- Income vs. expense comparisons
- Monthly and yearly trend analysis
- Stacked category breakdowns using accessible color palettes

### AI and Speech-to-Text Integration
- Converts spoken or free-form text into structured expense records
- Extracts categories, amounts, and dates automatically
- Reduces manual data entry and improves usability

### Backend Logic and Data Integrity
- Normalized SQLite database design
- SQL aggregation logic for monthly summaries
- Validation layers to ensure consistent and reliable data

---

## Tech Stack

**Frontend / UI**  
- Streamlit

**Backend**  
- Python

**Database**  
- SQLite

**AI**  
- LLM-based expense parsing using OpenAI's ChatGPT

**Speech-to-Text**  
- Voice input → text → structured data pipeline (Using OpenAI's Whisper)

**Visualization**  
- Altair / Streamlit charts

---

## Database Schema

```text
Users
 └── id (PK)
 └── username

Income
 └── user_id (FK)
 └── monthly_income
 └── date (YYYY-MM)

Expense_type
 └── id (PK)
 └── category_name

Expenses
 └── user_id (FK)
 └── expense_type_id (FK)
 └── amount
 └── date (YYYY-MM)
```
