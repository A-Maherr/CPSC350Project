# Personal Finance Dashboard  
### Streamlit • SQLite • AI • Speech-to-Text

A full-stack personal finance tracking application built with **Streamlit** and **SQLite**, designed to help users log income and expenses, visualize monthly trends, and interact with their data using **AI-assisted natural language input and speech-to-text**.

This project was developed as part of **CPSC-350**.

---

## Overview

The goal of this project was to build an end-to-end data-driven application that balances **backend correctness**, **data integrity**, and **user-friendly interaction**. The system supports structured financial data storage while reducing friction through AI-powered input methods.

---

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
