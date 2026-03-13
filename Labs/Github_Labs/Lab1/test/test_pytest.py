import pytest
from src.calculator import fun1, fun2, fun3, fun4, fun5

def test_fun1():
    assert fun1(2, 3) == 5
    assert fun1(5, 0) == 5
    assert fun1(-1, 1) == 0
    assert fun1(-1, -1) == -2

def test_fun2():
    assert fun2(2, 3) == -1
    assert fun2(5, 0) == 5
    assert fun2(-1, 1) == -2
    assert fun2(-1, -1) == 0

def test_fun3():
    assert fun3(2, 3) == 6
    assert fun3(5, 0) == 0
    assert fun3(-1, 1) == -1
    assert fun3(-1, -1) == 1

def test_fun4():
    assert fun4(2, 3, 5) == 10
    assert fun4(5, 0, -1) == 4
    assert fun4(-1, -1, -1) == -3
    assert fun4(-1, -1, 100) == 98

def test_fun5():
    assert fun5(10, 2) == 5
    assert fun5(15, 3) == 5
    assert fun5(10, 0) == "Error: Division by zero"