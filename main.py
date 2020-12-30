from file_allocation import *
from os import path
import sys


def main_menu():
    block_num = int(input("Enter the number of blocks: "))  # User inserts block number in memory
    memory = Memory(block_num)  # Initialize memory with block_num blocks
    files = []  # Initialize file list that will store File objects
    simulator = Simulator(files, memory) # Initialize simulator that will run the file allocation simulation

    while True:
        print("Menu")  # Main Menu
        print("1. Change number of blocks")
        print("2. Insert file")
        print("3. Delete file")
        print("4. Run/Display Contiguous allocation")
        print("5. Run/Display Linked allocation")
        print("6. Run/Display Indexed allocation")
        print("7. Terminate Program")
        choice = input()
        if choice == '1':
            block_num = int(input("Enter the number of blocks: "))
            memory.change_size(block_num)  # Function that changes number of blocks in memory
            #  Function deletes any unallocated memory blocks
            #  Function also deletes any allocated memory blocks and the allocated Files

        elif choice == '2':
            option = int(input("How would you like to input your data? \n1.Manual Input \n2.File Input \n"))
            if option == 1:  # Manual Input
                # file input
                print("Press Enter when done.")
                while True:
                    flag = False
                    file_name = input("Enter file name: ")  # Initialize File name
                    if file_name == "":  # Data validation to check that File name is not empty
                        break
                    while True:
                        file_size = input("Enter file size in blocks: ")  # Initialize File size
                        if not file_size.isnumeric():  # Data validation to check if input is numeric
                            print("Invalid input. File size must be an integer")
                            continue
                        break
                    # append new file object to array
                    for file in files:
                        if file.name == file_name:  # Check that File with same name doesn't exist
                            print("File with same name already exists")
                            flag = True
                            break
                    if flag:
                        continue
                    files.append(File(int(file_size), file_name))  # Adds new File to file list with new name & size
                    print("File added.")

            elif option == 2:  # File Input
                while True:
                    filepath = "input.txt"
                    # file = input("Enter filename.txt: ")
                    if path.exists(filepath):  # Check if file exists
                        break  # If file exists, break out of the loop
                    else:
                        print("Input Error: File does not exist.")  # Loop re-iterates until readable file is found
                with open(filepath, "r") as input_file:
                    for line in input_file:
                        filedata = []
                        for word in line.split():
                            filedata.append(word)
                        flag = False
                        for file in files:
                            if file.name == filedata[0]:  # If a file name is repeated, it will be skipped
                                flag = True
                                break
                        if flag:
                            continue
                        files.append(File(int(filedata[1]), filedata[0]))
            else:
                print("Invalid input!\n")

        elif choice == '3':
            # Delete Files
            name = input("Enter File name: ")
            if simulator.delete(name):  # Deletes File with matching file.name
                print("File Deleted.")
            else:
                print("File not found.")

        elif choice == '4':  # Contiguous
            simulator.reset()
            simulator.contiguous()  # Allocates the Files using contiguous allocation
            simulator.display()  # Displays the allocated Files' names, sizes, start & end

        elif choice == '5':  # Linked
            simulator.reset()
            simulator.linked()  # Allocates the Files using contiguous allocation
            simulator.display_linked()  # Displays the allocated Files' names, sizes, start & end

        elif choice == '6':  # Indexed
            simulator.reset()
            simulator.indexed()  # Allocates the Files using contiguous allocation
            simulator.display_indexed()  # Displays the allocated Files' names, sizes, start & end

        elif choice == '7':
            sys.exit("Goodbye! See you with the A+.")
        else:
            print("Invalid input.")


main_menu()
