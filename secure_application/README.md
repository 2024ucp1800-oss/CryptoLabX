# Library Management System

## Lab Assignment 3 - CryptoLabX

Console based library management system in Python.

## How to Run

```
cd secure_application/src
python3 library_app.py
```

## Features
- Register new members
- Add books
- Issue and return books
- Fine calculation (Rs 5/day after 14 days)
- Search books by title
- View members, books and transactions
- Delete members

## Vulnerabilities Found
1. SQL Injection - string concatenation used in queries
2. Improper Input Validation - no checks on user input
3. Missing Authentication - no login system

## SAST Tool
SonarQube Community Edition

## Folder Structure
```
secure_application/
├── src/              - source code
├── reports/          - vulnerability report
├── screenshots/      - sonarqube screenshots
├── sast/             - sonarqube config
├── outputs/          - scan output
├── testcases/        - test cases
└── README.md
```
