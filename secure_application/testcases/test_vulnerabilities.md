# Test Cases for Vulnerabilities

## Library Management System

---

## Test Case 1: SQL Injection in Search Book

**Steps:**
1. Run the application
2. Select option 5 (Search Book)
3. Enter: `' OR '1'='1`

**Expected (Secure):** Should reject the input or show no results  
**Actual (Vulnerable):** Shows ALL books in the database

**Steps (More dangerous):**
1. Select option 5
2. Enter: `' UNION SELECT 1,name,email,1 FROM members --`

**Expected:** Should fail  
**Actual:** Shows all member data including emails

---

## Test Case 2: SQL Injection in Issue Book

**Steps:**
1. Select option 6 (Issue Book)
2. Enter book ID: `1 OR 1=1`
3. Enter member ID: `1`

**Expected:** Should only find book with ID 1  
**Actual:** May return first book found due to OR condition

---

## Test Case 3: SQL Injection in Delete Member

**Steps:**
1. Select option 10 (Delete Member)
2. Enter member ID: `1 OR 1=1`

**Expected:** Should delete only member 1  
**Actual:** Deletes ALL members from database

---

## Test Case 4: Improper Input Validation - Empty Name

**Steps:**
1. Select option 1 (Register Member)
2. Press Enter without typing a name
3. Enter any email

**Expected:** Should show error "Name cannot be empty"  
**Actual:** Accepts empty name and registers member

---

## Test Case 5: Improper Input Validation - Invalid Email

**Steps:**
1. Select option 1
2. Enter name: Test
3. Enter email: notanemail

**Expected:** Should show "Invalid email format"  
**Actual:** Accepts "notanemail" as a valid email

---

## Test Case 6: Improper Input Validation - Non-numeric ID

**Steps:**
1. Select option 6 (Issue Book)
2. Enter book ID: abc

**Expected:** Should show "Please enter a number"  
**Actual:** Shows error message with SQL details (information leakage)

---

## Test Case 7: Missing Authentication - Delete without Login

**Steps:**
1. Run application (no login required)
2. Directly select option 10 (Delete Member)
3. Enter any member ID

**Expected:** Should ask for admin credentials first  
**Actual:** Deletes the member without any authentication

---

## Test Case 8: Missing Authentication - View All Members

**Steps:**
1. Run application
2. Select option 3 (Show Members)

**Expected:** Should require login to view member data  
**Actual:** Shows all member names and emails without login

---

## Test Case 9: Fine Calculation - SQL Injection

**Steps:**
1. Select option 8 (Calculate Fine)
2. Enter member ID: `0 UNION SELECT SUM(fine) FROM transactions`

**Expected:** Should validate input as integer  
**Actual:** Executes the injected SQL query
