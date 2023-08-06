# extends the capability of truthiness evaluation beyond the standard Python truthiness rules to handle pandas DataFrames/Series and NumPy Arrays

## pip install istruthy

#### Tested against Windows 10 / Python 3.10 / Anaconda
```python

    Args:
        x: A value of any type.

    Returns:
        bool: True if the value is truthy, False otherwise. If an exception occurs while evaluating `x`,
              False is returned unless `x` is an empty sequence (e.g., an empty list, tuple, or string),
              in which case True is returned.



# Example
import pandas as pd
import numpy as np

v_bool = False
v_none = None
v_0_0 = 0
v_0_1 = 0.0
v_0_2 = 0j
empty_list = []
empty_tuple = ()
empty_dict = {}
empty_string = ""
empty_byte = b""
empty_bytearray = bytearray(b"")
empty_set = set()
empty_np_array = np.array([])

if not v_bool:
    print(f"1) {v_bool} is falsy")
    if not is_truthy(v_bool):
        print(f"2) {v_bool} is falsy")
else:
    print(f"1) {v_bool} is truthy")
    if is_truthy(v_bool):
        print(f"2) {v_bool} is truthy")
if not v_none:
    print(f"1) {v_none} is falsy")
    if not is_truthy(v_none):
        print(f"2) {v_none} is falsy")
else:
    print(f"1) {v_none} is truthy")
    if is_truthy(v_none):
        print(f"2) {v_none} is truthy")
if not v_0_0:
    print(f"1) {v_0_0} is falsy")
    if not is_truthy(v_0_0):
        print(f"2) {v_0_0} is falsy")
else:
    print(f"1) {v_0_0} is truthy")
    if is_truthy(v_0_0):
        print(f"2) {v_0_0} is truthy")
if not v_0_1:
    print(f"1) {v_0_1} is falsy")
    if not is_truthy(v_0_1):
        print(f"2) {v_0_1} is falsy")
else:
    print(f"1) {v_0_1} is truthy")
    if is_truthy(v_0_1):
        print(f"2) {v_0_1} is truthy")
if not v_0_2:
    print(f"1) {v_0_2} is falsy")
    if not is_truthy(v_0_2):
        print(f"2) {v_0_2} is falsy")
else:
    print(f"1) {v_0_2} is truthy")
    if is_truthy(v_0_2):
        print(f"2) {v_0_2} is truthy")
if not empty_list:
    print(f"1) {empty_list} is falsy")
    if not is_truthy(empty_list):
        print(f"2) {empty_list} is falsy")
else:
    print(f"1) {empty_list} is truthy")
    if is_truthy(empty_list):
        print(f"2) {empty_list} is truthy")
if not empty_tuple:
    print(f"1) {empty_tuple} is falsy")
    if not is_truthy(empty_tuple):
        print(f"2) {empty_tuple} is falsy")
else:
    print(f"1) {empty_tuple} is truthy")
    if is_truthy(empty_tuple):
        print(f"2) {empty_tuple} is truthy")
if not empty_dict:
    print(f"1) {empty_dict} is falsy")
    if not is_truthy(empty_dict):
        print(f"2) {empty_dict} is falsy")
else:
    print(f"1) {empty_dict} is truthy")
    if is_truthy(empty_dict):
        print(f"2) {empty_dict} is truthy")
if not empty_string:
    print(f"1) {empty_string} is falsy")
    if not is_truthy(empty_string):
        print(f"2) {empty_string} is falsy")
else:
    print(f"1) {empty_string} is truthy")
    if is_truthy(empty_string):
        print(f"2) {empty_string} is truthy")
if not empty_byte:
    print(f"1) {empty_byte} is falsy")
    if not is_truthy(empty_byte):
        print(f"2) {empty_byte} is falsy")
else:
    print(f"1) {empty_byte} is truthy")
    if is_truthy(empty_byte):
        print(f"2) {empty_byte} is truthy")
if not empty_bytearray:
    print(f"1) {empty_bytearray} is falsy")
    if not is_truthy(empty_bytearray):
        print(f"2) {empty_bytearray} is falsy")
else:
    print(f"1) {empty_bytearray} is truthy")
    if is_truthy(empty_bytearray):
        print(f"2) {empty_bytearray} is truthy")
if not empty_set:
    print(f"1) {empty_set} is falsy")
    if not is_truthy(empty_set):
        print(f"2) {empty_set} is falsy")
else:
    print(f"1) {empty_set} is truthy")
    if is_truthy(empty_set):
        print(f"2) {empty_set} is truthy")
print("----------------")
try:
    if not empty_np_array:
        print(f"1) {empty_np_array} is falsy")
        if not is_truthy(empty_np_array):
            print(f"2) {empty_np_array} is falsy")
    else:
        print(f"1) {empty_np_array} is truthy")
        if is_truthy(empty_np_array):
            print(f"2) {empty_np_array} is truthy")
except Exception:
    if not is_truthy(empty_np_array):
        print(f"2) {empty_np_array} is falsy")
    if is_truthy(empty_np_array):
        print(f"2) {empty_np_array} is truthy")

empty_np_array = pd.DataFrame()
try:
    if not empty_np_array:
        print(f"1) {empty_np_array} is falsy")
        if not is_truthy(empty_np_array):
            print(f"2) {empty_np_array} is falsy")
    else:
        print(f"1) {empty_np_array} is truthy")
        if is_truthy(empty_np_array):
            print(f"2) {empty_np_array} is truthy")
except Exception as fe:
    print(fe)
    if not is_truthy(empty_np_array):
        print(f"2) {empty_np_array} is falsy")
    if is_truthy(empty_np_array):
        print(f"2) {empty_np_array} is truthy")




1) False is falsy
2) False is falsy
1) None is falsy
2) None is falsy
1) 0 is falsy
2) 0 is falsy
1) 0.0 is falsy
2) 0.0 is falsy
1) 0j is falsy
2) 0j is falsy
1) [] is falsy
2) [] is falsy
1) () is falsy
2) () is falsy
1) {} is falsy
2) {} is falsy
1)  is falsy
2)  is falsy
1) b'' is falsy
2) b'' is falsy
1) bytearray(b'') is falsy
2) bytearray(b'') is falsy
1) set() is falsy
2) set() is falsy
----------------
1) [] is falsy
2) [] is falsy
The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
2) Empty DataFrame
Columns: []
Index: [] is falsy
C:\ProgramData\anaconda3\envs\dfdir\istruthy.py:149: DeprecationWarning: The truth value of an empty array is ambiguous. Returning False, but in future this will result in an error. Use `array.size > 0` to check that an array is not empty.
  if not empty_np_array:
C:\ProgramData\anaconda3\envs\dfdir\istruthy.py:24: DeprecationWarning: The truth value of an empty array is ambiguous. Returning False, but in future this will result in an error. Use `array.size > 0` to check that an array is not empty.
  if x:


```