from file_allocation import *

# Console Run
def cmd_run():
    # block Input
    block_num = int(input("Enter the number of blocks: "))
    # file input
    files = []
    print("Press Enter when done.")
    while True:
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
        files.append(File(int(file_size), file_name))
        print("File added.")
    simulator = Simulator(files, block_num)
    simulator.contiguous()
    print("Blocks: ")
    simulator.block.display()
    print("Files:")
    for i in files:
        i.display()


cmd_run()



