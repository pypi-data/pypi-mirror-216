# Decorators that provide graceful exception handling, customization of error handling behavior, error logging

## pip install ignoreexceptions

### Tested against Windows 10 / Python 3.10 / Anaconda 

The decorators break_KeyboardInterrupt, ignore_all_exceptions, and ignore_Exception 
offer several advantages in exception handling and error management. Here are some of the key advantages:

### Graceful Exception Handling: 

The decorators allow for graceful handling of exceptions by catching and controlling 
their impact on the program's execution. 
Instead of allowing exceptions to propagate and potentially crash the program, 
these decorators provide the ability to handle exceptions in a controlled manner.

### Customized Exception Handling: 

The decorators provide flexibility in defining custom exception handling behavior. 
Developers can specify alternative actions, return values, or error messages when exceptions occur. 
This allows for tailored exception handling strategies based on 
the specific needs of the application or use case.

### Error Logging and Monitoring: 

The decorators can log exceptions to a 
specified logfile, enabling error tracking, monitoring, and analysis. 
This facilitates the identification and resolution of errors by providing a 
centralized record of encountered exceptions.

### Prevent Program Termination: 

By handling exceptions, these decorators prevent the abrupt termination of the program. 
This is particularly useful in long-running processes, scripts, or automation 
tasks where a program crash would interrupt the entire workflow. 
Instead, the program can continue executing or gracefully exit 
based on the specified behavior.

### Improved User Experience: 

Graceful exception handling ensures that applications do 
not crash or display cryptic error messages to end-users. 
By providing alternative actions or error messages, the decorators can enhance 
the user experience by providing meaningful feedback or fallback mechanisms.

### Debugging and Troubleshooting: 

The decorators can be valuable during 
the debugging and troubleshooting phases of development. 
By catching and logging exceptions, developers can gain insights into 
the causes of errors, track down problematic code sections, and analyze 
the stack trace for detailed debugging information.

### Robustness and Resilience: 

These decorators contribute to the overall robustness and resilience of applications or systems. 
By handling exceptions and recovering from errors, the code becomes more fault-tolerant
and can continue functioning in the presence of unexpected events or exceptional conditions.


### Importing 

```python
from ignoreexceptions import ignore_all_exceptions, ignore_Exception, break_KeyboardInterrupt
```

### Example 1: Using break_KeyboardInterrupt decorator

```python
@break_KeyboardInterrupt
def test_while_loop():
    from time import sleep

    while True:
        print("oioi")
        sleep(1)


# In this example, the break_KeyboardInterrupt decorator is applied to the test_while_loop function.
# It ensures that if a KeyboardInterrupt exception is raised during the execution of the function,
# the loop will be interrupted and the program will not be terminated.
```


### Example 2: Using ignore_all_exceptions decorator

```python
@ignore_all_exceptions(
    v="dum**ss", print_exceptions=True, active=True, logfile="c:\\logtest.txt"
)
def divide(a, b):
    return a / b


# In this example, the ignore_all_exceptions decorator is applied to the divide function.
# It handles all exceptions that may occur during the execution of the function.
# If an exception is caught, it prints the exception, logs it to a specified logfile,
# and returns the value "dum**ss" instead of raising the exception.


```

### Example 3: Using ignore_Exception decorator

```python

@ignore_Exception(
    v=list(), print_exceptions=True, active=True, logfile="c:\\logtest.txt"
)
def process_data(l=(0, 1, 2, 3, 4, 5)):
    from random import choice

    results = []
    for _ in range(100000):
        results.append(10 / choice(l))
    return results


# The decorator @ignore_Exception(v="error occurred", print_exceptions=True, active=True, logfile='c:\\logtest.txt')
# is applied to the process_data function. It means that if any exception occurs during the execution of the function,
# the exception will be caught, printed (if print_exceptions is True), and logged to the specified logfile
# ('c:\logtest.txt'). Instead of raising the exception, the function will return the value "error occurred"
# (specified by v) as the result.
#
# Therefore, this function is designed to perform a potentially risky
# computation repeatedly and handle any exceptions that may occur during the process.

# Log file output:
# 2023/06/26 19:25:16.712902
# Traceback (most recent call last):
#   File "C:\ProgramData\anaconda3\envs\dfdir\di.py", line 125, in wrapper
#     result = func(*args, **kwargs)
#   File "C:\ProgramData\anaconda3\envs\dfdir\di.py", line 193, in process_data
#     results.append(10 / choice(l))
# ZeroDivisionError: division by zero
#
# ---------------------------

```

### Combining decorators:

```python

@break_KeyboardInterrupt
@ignore_Exception(
    v=list(), print_exceptions=True, active=True, logfile="c:\\logtest.txt"
)
def process_data2(l=(0, 1, 2, 3, 4, 5)):
    from random import choice
    from time import sleep

    results = []
    for _ in range(100000):
        sleep(1)
        results.append(10 / choice(l[1:]))
    return results
    
```