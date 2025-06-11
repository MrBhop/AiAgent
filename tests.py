from functions.write_file import write_file

print("Result for 'lorem.txt':")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), "\n")

print("Result for 'main.py':")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), "\n")

print("Result for '/tmp/temp.txt':")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), "\n")
