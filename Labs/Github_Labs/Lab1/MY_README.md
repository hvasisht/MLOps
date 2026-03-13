# Lab 1 - MLOps Calculator Project
**Student:** Harini Vasisht  
**Course:** IE-7374 MLOps  
**Date:** January 30, 2026  

---

## Project Overview
This lab demonstrates the fundamentals of MLOps by creating a calculator application with automated testing and CI/CD pipeline using GitHub Actions.

---

## What I Built

### Calculator Functions (src/calculator.py)
1. **fun1(x, y)** - Adds two numbers
2. **fun2(x, y)** - Subtracts y from x
3. **fun3(x, y)** - Multiplies two numbers
4. **fun4(x, y, z)** - Adds three numbers together
5. **fun5(x, y)** - Divides x by y with error handling for division by zero *(My custom addition)*

---

## My Modifications

To make this project unique, I made the following changes:

1. **Modified fun4:** Changed from combining results of fun1, fun2, fun3 to simply adding three numbers
2. **Added fun5:** Created a new division function with error handling for division by zero
3. **Enhanced testing:** Added comprehensive test cases for the new fun5 function in both pytest and unittest frameworks
4. **Personalization:** Added my name and date to the calculator file

---

## Testing

### Test Frameworks Used
- **Pytest** - Modern testing framework with simple syntax
- **Unittest** - Python's built-in testing framework

### Test Results
All 5 functions tested successfully:
- ✅ test_fun1 - Addition tests passed
- ✅ test_fun2 - Subtraction tests passed
- ✅ test_fun3 - Multiplication tests passed
- ✅ test_fun4 - Three-number addition tests passed
- ✅ test_fun5 - Division and error handling tests passed

---

## CI/CD Pipeline

### GitHub Actions Workflows
Two automated workflows run on every push to main branch:

1. **pytest_action.yml** - Runs pytest tests
2. **unittest_action.yml** - Runs unittest tests

Both workflows automatically:
- Set up Python environment
- Install dependencies
- Run all tests
- Report results (✅ green checkmark = all tests passed)

---

## Project Structure
```
Lab1/
├── src/
│   ├── calculator.py          # Main calculator functions
│   └── __init__.py
├── test/
│   ├── test_pytest.py         # Pytest test suite
│   ├── test_unittest.py       # Unittest test suite
│   └── __init__.py
├── data/                       # Data folder (empty for this lab)
├── .github/
│   └── workflows/
│       ├── pytest_action.yml  # Pytest CI/CD workflow
│       └── unittest_action.yml # Unittest CI/CD workflow
├── requirements.txt            # Project dependencies
└── MY_README.md               # This file
```

---

## How to Run

### Run Tests Locally

1. **Activate virtual environment:**
```bash
   source lab_01/bin/activate
```

2. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

3. **Run pytest:**
```bash
   pytest test/test_pytest.py -v
```

4. **Run unittest:**
```bash
   python -m unittest test.test_unittest -v
```

---

## Key Learnings

1. **Virtual Environments** - Learned to isolate project dependencies
2. **Git & GitHub** - Forking, cloning, committing, and pushing code
3. **Automated Testing** - Writing and running tests with pytest and unittest
4. **CI/CD** - Implementing continuous integration with GitHub Actions
5. **Code Modification** - Making personalized changes to demonstrate understanding

---

## GitHub Repository

[Link to Repository](https://github.com/hvasisht/MLOps/tree/main/Labs/Github_Labs/Lab1)

---

## Conclusion

This lab successfully demonstrates MLOps fundamentals including version control, automated testing, and CI/CD pipelines. All tests pass successfully, and the GitHub Actions workflows provide continuous integration for reliable code quality.