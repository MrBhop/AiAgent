from functions.run_python_file import run_python_file

print("Result from 'main.py':")
print(run_python_file("calculator", "main.py"), "\n")

print("Result from 'tests.py':")
print(run_python_file("calculator", "tests.py"), "\n")

print("Result from '../main.py':")
print(run_python_file("calculator", "../main.py"), "\n")

print("Result from 'nonexistent.py':")
print(run_python_file("calculator", "nonexistent.py"), "\n")

print("Result from 'lorem.txt':")
print(run_python_file("calculator", "lorem.txt"), "\n")
