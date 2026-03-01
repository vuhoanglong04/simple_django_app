# This file contains intentional bugs and code smells for SonarQube testing

import os
import pickle
import subprocess

# Security Hotspot: Hardcoded password
PASSWORD = "admin123"
SECRET_KEY = "my-super-secret-key-12345"
API_KEY = "sk-1234567890abcdef"

# Bug: SQL Injection vulnerability
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return query

# Bug: Command injection
def run_command(user_input):
    os.system("echo " + user_input)
    subprocess.call(user_input, shell=True)

# Bug: Insecure deserialization
def load_data(data):
    return pickle.loads(data)

# Code smell: Empty function
def do_nothing():
    pass

# Code smell: Unused variable
def unused_vars():
    x = 10
    y = 20
    z = 30
    return x

# Bug: Division by zero potential
def divide(a, b):
    return a / b

# Code smell: Too many parameters
def complex_function(a, b, c, d, e, f, g, h, i, j):
    return a + b + c + d + e + f + g + h + i + j

# Code smell: Duplicate code
def calculate_area_1(length, width):
    result = length * width
    print("Area calculated")
    return result

def calculate_area_2(length, width):
    result = length * width
    print("Area calculated")
    return result

# Bug: Mutable default argument
def append_to_list(item, list_param=[]):
    list_param.append(item)
    return list_param

# Code smell: Nested too deep
def deeply_nested(a):
    if a > 0:
        if a > 10:
            if a > 20:
                if a > 30:
                    if a > 40:
                        return "very deep"
    return "shallow"

# Bug: Unreachable code
def unreachable():
    return True
    print("This will never execute")

# Code smell: Commented out code
# def old_function():
#     x = 1
#     y = 2
#     return x + y

# Security: Eval usage
def dangerous_eval(user_input):
    return eval(user_input)

# Security: Exec usage  
def dangerous_exec(code):
    exec(code)

# Bug: Catching too broad exception
def catch_all():
    try:
        risky_operation()
    except:
        pass

def risky_operation():
    raise ValueError("Error")

# Code smell: Magic numbers
def calculate_price(quantity):
    return quantity * 19.99 * 1.08 * 0.95

# Code smell: Long method with too many lines
def very_long_method():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t
