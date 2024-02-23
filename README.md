# DSCI-560 Assignment No. 5 – Part 1

## Overview

This project is designed to extract, process, and visualize data related to oil wells from PDF documents and web sources. It involves PDF text extraction, data preprocessing, web scraping, and database operations.

## Installation

To run this project, you need Python installed on your system along with MySQL. After cloning the repository, install the required Python dependencies by running:

```bash
pip install -r requirements.txt
```

## Setup

### Database Setup

1. Ensure MySQL is installed and running on your system.
2. Create MYSQL database and user with the necessary permissions

```sql
CREATE DATABASE lab05;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON your_database_name.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

3. Uppdate the 'db_config' dictionary in each script with your database connection details.

### Tessaract OCR Setup

Install Tesseract OCR on your system. Follow the installation guide for your operating system here.
Update the path to the Tesseract executable in extract.py to match your installation.

## Usage

Run the following scripts in order to extract, preprocess, and visualize the data:

1. PDF Extraction:
```bash
python extract.py
```

2. Web Scraping:
```bash
python extract.py
```

3. Data Preprocessing:
```bash
python extract.py
```

4. Database Operations:
The 'db_operations.py' script contains functions used by other scripts to interact with the database

