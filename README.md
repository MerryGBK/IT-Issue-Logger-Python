# IT Issue Logger (Python)

A practical Python-based application designed to log, validate, and manage common IT issues.
The project simulates a simple IT support/helpdesk workflow and demonstrates structured
troubleshooting, data handling, and security-aware input validation.

---

## Overview

This tool allows users to record IT-related issues such as software, hardware, and network
problems. Each issue is stored with a timestamp and description, making it easy to review,
search, and analyse recurring problems.

The project is intended as a hands-on example of how entry-level IT and software development
skills can be applied to real-world scenarios.

---

## Features

- Log IT issues with automatic date and time
- Categorise issues by type:
  - Software
  - Hardware
  - Network
- Input validation to prevent invalid or empty entries
- View all logged issues in a clear, readable format
- Search and filter issues by type or keyword
- Persistent storage using:
  - CSV (tabular data)
  - JSON (structured data)

---

## Technologies Used

- Python
- CSV file handling
- JSON data storage
- Standard Python libraries (`datetime`, `pathlib`)

---

## How to Run

1. Clone or download the repository  
2. Open a terminal in the project directory  
3. Run the application:

```bash
python issue_logger.py
