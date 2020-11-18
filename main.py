from file_allocation import *
import os.path
from os import path
import sys


def main_menu():
    block_num = int(input("Enter the number of blocks: "))
    memory = Memory(block_num)
    files = []
    simulator = Simulator(files, memory)
    while True:
        print("Menu")
        print("1. Change number of blocks")
        print("2. Insert file")
        print("3. Delete file")
        print("4. Display allocation")
        print("5. Terminate Program")
        choice = input()
        if choice == '1':
            block_num = int(input("Enter the number of blocks: "))
            memory.change_size(block_num)

        elif choice == '2':
            option = int(input("How would you like to input your data? \n1.Manual Input \n2.File Input \n"))
            if option == 1:  # Manual Input
                # file input
                print("Press Enter when done.")
                while True:
                    flag = False
                    file_name = input("Enter file name: ")
                    if file_name == "":
                        break
                    while True:
                        file_size = input("Enter file size in blocks: ")
                        if not file_size.isnumeric():
                            print("Invalid input. File size must be an integer")
                            continue
                        break
                    # append new file object to array
                    for file in files:
                        if file.name == file_name:
                            flag = True
                            break
                    if flag:
                        continue
                    files.append(File(int(file_size), file_name))
                    print("File added.")

            elif option == 2:  # File Input
                while True:
                    file = "input.txt"
                    # file = input("Enter filename.txt: ")
                    if path.exists(file):  # Check if file exists
                        break  # If file exists, break out of the loop
                    else:
                        print("Input Error: File does not exist.")  # Loop re-iterates until readable file is found
                input_file = open(file, "r")
                files_num = int(input_file.readline())  # files_num will read 1st line as Number of files to allocate
                # file input
                for f in range(files_num):  # For files_num times, loop will iterate
                    flag = False
                    file_name = input_file.readline()
                    file_size = int(input_file.readline())
                    for file in files:
                        if file.name == file_name:
                            flag = True
                            break
                    if flag:
                        continue
                    files.append(File(int(file_size), file_name))
                input_file.close()
            else:
                print("Invalid input!\n")

        elif choice == '3':
            # Delete Files later
            name = input("enter file name")
            for file in files:
                if file.name == name:
                    simulator.delete()
            print("file not found")
            continue

        elif choice == '4':
            simulator.contiguous()
            simulator.display()

        elif choice == '5':
            sys.exit("Goodbye! See you with the A+.")
        else:
            print("Invalid input.")


main_menu()
