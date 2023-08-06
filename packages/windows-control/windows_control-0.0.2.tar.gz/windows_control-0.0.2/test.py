import os
import sys

# Add the path to the Rust library to the sys.path list
rust_lib_path = os.path.abspath(r'C:\Users\Administrator\Desktop\rust_lib\target\debug')
sys.path.append(rust_lib_path)

# Import the Rust library for testing
import windows_control
from windows_control import keyboard

if __name__ == "__main__":
    result = keyboard.input()
    print(result)
    result = windows_control.sum_as_string(1, 2)
    print(result)
    result = windows_control.minus_as_string(1, 2)
    print(result)