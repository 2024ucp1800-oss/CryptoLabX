# LAB EXPERIMENT MANUAL (HANDWRITTEN VERSION)

**Experiment:** SAST Analysis of Library Management System using SonarQube  
**Subject:** Cryptography & Network Security Lab  
**Language:** Python 3 | **Tool:** SonarQube v25.6 & SonarScanner v8.1  

---

## 1. AIM
To build a console Library Management System in Python with 5 core features and 3 security vulnerabilities, and analyze it using SonarQube (SAST).

---

## 2. CORE FEATURES (5)
1. **Member Registration:** Register member with name & email.
2. **Book Issue:** Issue available book to registered member.
3. **Book Return:** Return book & calculate late return date.
4. **Fine Calculation:** Charge ₹5/day fine if borrowed >14 days.
5. **Search Books:** Search books by title keyword.

---

## 3. INTENTIONAL VULNERABILITIES (3)

### V1: SQL Injection (CWE-89)
* **Cause:** Dynamic string concatenation in SQL queries.
* **Vulnerable Line:** `query = "SELECT * FROM books WHERE title LIKE '%" + keyword + "%'"`
* **Exploit:** Entering `' OR '1'='1` dumps all books from database.
* **Fix:** Use parameterized query: `cursor.execute("SELECT ... WHERE title LIKE ?", (param,))`

### V2: Improper Input Validation (CWE-20)
* **Cause:** No sanitization or format check on user inputs (`input()`).
* **Exploit:** Accepts blank member names, invalid email formats, or string input for integer IDs.
* **Fix:** Validate email using `@` check, enforce integer parsing for IDs, check non-empty fields.

### V3: Missing Authentication (CWE-306)
* **Cause:** No login or role verification before executing system actions.
* **Exploit:** Unauthenticated users can delete members or view sensitive transaction logs directly from menu.
* **Fix:** Require username/password authentication before admin actions.

---

## 4. STEPS TO RUN SONARQUBE (SAST)

1. **Install Java 17:**
   `brew install openjdk@17`
2. **Start SonarQube Server:**
   `./sonarqube-25.6.0.109173/bin/macosx-universal-64/sonar.sh start`
3. **Install SonarScanner:**
   `brew install sonar-scanner`
4. **Configure Project (`sonar-project.properties`):**
   ```properties
   sonar.projectKey=cryptolabx-library-management
   sonar.sources=secure_application/src
   sonar.host.url=http://localhost:9000
   sonar.token=squ_ebf4966854d7f40544877daf333fabca182a810d
   ```
5. **Run Scan:**
   `sonar-scanner -Dsonar.token=squ_ebf4966854d7f40544877daf333fabca182a810d`

---

## 5. SCAN RESULTS & OBSERVATIONS

* **Lines of Code Analyzed:** 292
* **Status:** EXECUTION SUCCESS
* **Overall Rating:** Security (A), Reliability (A), Maintainability (A)

| Issue | Severity | Message | Location |
|:---|:---:|:---|:---|
| 1. Code Smell | CRITICAL | Literal `"library.db"` duplicated 11 times | `library_app.py:L5` |
| 2. Code Smell | CRITICAL | Literal `"Error:"` duplicated 5 times | `library_app.py:L150` |
| 3. Code Smell | MAJOR | Commented out code present | `library_app.py:L191` |

*Note: SonarQube Community Edition focuses on Python code smells & maintainability. Taint tracking for Python SQL injection requires commercial/addon rules.*

---

## 6. TEST CASES

| TC # | Input | Expected Output | Observed Result |
|:---:|:---|:---|:---|
| **1** | `' OR '1'='1` in Search | Reject / Empty | Dumps all books (SQLi) |
| **2** | `' UNION SELECT 1,name,email,1 FROM members --` | Reject | Exposes member data (SQLi) |
| **3** | `[Enter]` for Name | Show error | Registers blank member |
| **4** | `invalidemail` | Show error | Registers invalid email |
| **5** | `abc` for Book ID | Ask number | Crashes with DB error |
| **6** | Option 10 (Delete) | Ask Login | Deletes member without login |

---

## 7. RESULT
The Library Management System was successfully developed with 5 features and 3 vulnerabilities. SonarQube SAST analysis was executed, identifying maintainability and quality issues.
