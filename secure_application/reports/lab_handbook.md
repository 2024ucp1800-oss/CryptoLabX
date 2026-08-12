# Lab Assignment 3 - SAST Analysis using SonarQube

## Library Management System

**Subject:** Cryptography and Network Security Lab  
**Tool Used:** SonarQube (SAST - Static Application Security Testing)  
**Language:** Python  
**Application:** Library Management System (S.NO. 4)

---

## Objective

To develop a small console-based application with 5 core functionalities and 3 intentional security vulnerabilities. Then use a SAST tool (SonarQube) to scan the code and identify issues.

---

## What is SAST?

SAST stands for Static Application Security Testing. It analyzes source code without running the program. It checks for bugs, vulnerabilities, and code quality issues by reading the code line by line.

SonarQube is an open-source SAST tool that supports multiple languages including Python, Java, C, JavaScript etc.

---

## Application Details

### Core Functionalities

1. Member Registration - register new members with name and email
2. Book Issue - issue books to registered members
3. Book Return - return books with fine calculation
4. Fine Calculation - Rs 5 per day fine after 14 days
5. Search Books - search by book title

### 3 Intentional Vulnerabilities

**1. SQL Injection (CWE-89)**

String concatenation is used to build SQL queries instead of parameterized queries.

Vulnerable code:
```python
query = "SELECT * FROM books WHERE title LIKE '%" + keyword + "%'"
c.execute(query)
```

Safe code should be:

```python
c.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + keyword + '%',))
```

Attack example: If user enters `' OR '1'='1` it returns all books.

**2. Improper Input Validation (CWE-20)**

No validation on user inputs. Empty names, invalid emails, non-numeric IDs are all accepted.

```python
name = input("Enter member name: ")   # no check if empty
email = input("Enter member email: ") # no check for @ symbol
book_id = input("Enter book ID: ")    # no check if its a number
```

**3. Missing Authentication (CWE-306)**

No login system. Anyone can access all functions including deleting members and viewing all data without any credentials.

---

## Steps to Install and Run SonarQube

### Step 1: Install Java 17

SonarQube requires Java 17 or above.

```bash
brew install openjdk@17
```

Add to PATH:
```bash
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verify:
```bash
java -version
```

Output:
```
openjdk version "17.0.20" 2026-07-21
```

### Step 2: Download SonarQube

Download SonarQube Community Edition:
```bash
curl -LO https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-25.6.0.109173.zip
```

Unzip it:
```bash
unzip sonarqube-25.6.0.109173.zip
```

### Step 3: Start SonarQube Server

```bash
./sonarqube-25.6.0.109173/bin/macosx-universal-64/sonar.sh start
```

Output:
```
Starting SonarQube...
Started SonarQube.
```

Wait 1-2 minutes for the server to fully start. Then open browser and go to:
```
http://localhost:9000
```

### Step 4: Login to SonarQube

Default credentials:
- Username: admin
- Password: admin

It will ask to change password on first login. Change it to your new password.

### Step 5: Install SonarScanner

SonarScanner is the CLI tool that scans your code and sends results to SonarQube server.

```bash
brew install sonar-scanner
```

Verify:
```bash
sonar-scanner --version
```

### Step 6: Create Project in SonarQube

Using API:
```bash
curl -u admin:'YourPassword' -X POST \
  "http://localhost:9000/api/projects/create?name=CryptoLabX-Library-Management&project=cryptolabx-library-management"
```

Output:
```json
{"project":{"key":"cryptolabx-library-management","name":"CryptoLabX-Library-Management","qualifier":"TRK","visibility":"public"}}
```

### Step 7: Generate Authentication Token

```bash
curl -u admin:'YourPassword' -X POST \
  "http://localhost:9000/api/user_tokens/generate?name=scan-token"
```

Output:
```json
{"login":"admin","name":"scan-token","token":"squ_ebf4966854d7f40544877daf333fabca182a810d","type":"USER_TOKEN"}
```

Save this token. It is needed for scanning.

### Step 8: Create sonar-project.properties

Create this file in your project root:

```properties
sonar.projectKey=cryptolabx-library-management
sonar.projectName=CryptoLabX Library Management
sonar.projectVersion=2.0
sonar.sources=secure_application/src
sonar.language=py
sonar.sourceEncoding=UTF-8
sonar.host.url=http://localhost:9000
sonar.token=squ_ebf4966854d7f40544877daf333fabca182a810d
sonar.exclusions=**/__pycache__/**,**/*.pyc,**/.git/**
```

### Step 9: Run the Scan

```bash
cd CryptoLabX/
sonar-scanner -Dsonar.token=YOUR_TOKEN_HERE
```

Output:
```
INFO  Project key: cryptolabx-library-management
INFO  1 file indexed
INFO  Quality profile for py: Sonar way
INFO  Sensor Python Sensor [python]
INFO  1 source file to be analyzed
INFO  1/1 source file has been analyzed
INFO  ANALYSIS SUCCESSFUL
INFO  EXECUTION SUCCESS
INFO  Total time: 4.377s
```

### Step 10: View Results

Open browser:
```
http://localhost:9000/dashboard?id=cryptolabx-library-management
```

Or use API:
```bash
curl -u admin:'YourPassword' \
  "http://localhost:9000/api/issues/search?projectKeys=cryptolabx-library-management&statuses=OPEN"
```

---

## SonarQube Scan Results

### Dashboard Metrics

| Metric | Value |
|--------|-------|
| Lines of Code | 292 |
| Bugs | 0 |
| Vulnerabilities | 0 |
| Code Smells | 3 |
| Security Hotspots | 0 |
| Security Rating | A |
| Reliability Rating | A |
| Maintainability Rating | A |
| Code Coverage | 0% |

### Issues Found by SonarQube

**Issue 1: Duplicated String Literal (CRITICAL)**
- Rule: python:S1192
- Line: 5
- Message: Define a constant instead of duplicating this literal "library.db" 11 times
- The string "library.db" is used 11 times in the file. Should be stored in a variable.

**Issue 2: Duplicated String Literal (CRITICAL)**
- Rule: python:S1192
- Line: 150
- Message: Define a constant instead of duplicating this literal "Error:" 5 times
- The string "Error:" is used 5 times. Should be stored in a variable.

**Issue 3: Commented Out Code (MAJOR)**
- Rule: python:S125
- Line: 191
- Message: Remove this commented out code
- Dead code should be removed for cleanliness.

---

## Important Notes

1. SonarQube Community Edition (free version) does NOT detect SQL Injection in Python. It mainly finds code smells and maintainability issues.

2. For SQL Injection detection in Python, tools like Bandit (python-specific security scanner) are better.

3. The 3 vulnerabilities (SQL Injection, Improper Input Validation, Missing Authentication) were identified through manual code review and documented in the vulnerability report.

4. SonarQube is more effective for Java code where it can detect SQL Injection, XSS and other security vulnerabilities.

---

## Folder Structure

```
CryptoLabX/
├── secure_application/
│   ├── src/
│   │   └── library_app.py
│   ├── reports/
│   │   └── vulnerability_report.md
│   ├── screenshots/
│   ├── sast/
│   │   └── sonar-project.properties
│   ├── outputs/
│   │   ├── scan_output.txt
│   │   ├── dashboard_metrics.json
│   │   └── issues_report.json
│   ├── testcases/
│   │   └── test_vulnerabilities.md
│   └── README.md
├── analysis/
├── datasets/
├── utils/
├── main.py
├── .gitignore
└── README.md
```

---

## Commands Summary

| Purpose | Command |
|---------|---------|
| Install Java | `brew install openjdk@17` |
| Install SonarScanner | `brew install sonar-scanner` |
| Start SonarQube | `./sonarqube-25.6.0.109173/bin/macosx-universal-64/sonar.sh start` |
| Stop SonarQube | `./sonarqube-25.6.0.109173/bin/macosx-universal-64/sonar.sh stop` |
| Run Scan | `sonar-scanner -Dsonar.token=YOUR_TOKEN` |
| Check Status | `curl http://localhost:9000/api/system/status` |
| Create Project | `curl -u admin:pass -X POST "http://localhost:9000/api/projects/create?name=NAME&project=KEY"` |
| Generate Token | `curl -u admin:pass -X POST "http://localhost:9000/api/user_tokens/generate?name=TOKEN_NAME"` |
| Get Issues | `curl -u admin:pass "http://localhost:9000/api/issues/search?projectKeys=KEY"` |
| SonarQube URL | `http://localhost:9000` |

---

## Test Cases

### TC1: SQL Injection in Search
- Input: `' OR '1'='1`
- Expected: should reject
- Actual: returns all books

### TC2: Empty Name Registration
- Input: press Enter without typing
- Expected: should show error
- Actual: accepts empty name

### TC3: Invalid Email
- Input: `notanemail`
- Expected: should show invalid email
- Actual: accepts it

### TC4: Delete Without Login
- Input: directly select delete option
- Expected: should ask for credentials
- Actual: deletes member without auth

### TC5: Non-numeric Book ID
- Input: `abc` as book ID
- Expected: should say enter a number
- Actual: shows SQL error message (information leakage)

---

## Conclusion

We developed a Library Management System in Python with 5 core functionalities and 3 intentional vulnerabilities (SQL Injection, Improper Input Validation, Missing Authentication). We installed SonarQube as a SAST tool and scanned the application. SonarQube found 3 code quality issues. The security vulnerabilities were documented through manual review. This assignment helped us understand how SAST tools work and the importance of secure coding practices.
