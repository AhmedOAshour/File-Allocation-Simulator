import random
from datetime import datetime


class File:

    def __init__(self, size, name):  # Constructor
        self.size = size
        self.name = name
        self.start = None

    def display(self):  # How the console will display the allocated Files
        if self.start is None:
            print("Name: ", self.name, " Size: ", self.size, "Start: Unallocated")
        else:
            print("Name: ", self.name, " Size: ", self.size, "Start:", self.start, "End: ", (self.size+self.start-1))


class Memory:

    def __init__(self, size):  # Constructor
        self.size = size
        self.allocated = 0
        self.block = []
        for i in range(size):  # Initializing every memory block with NULL value (empty)
            self.block.append(None)

    def change_size(self, size):
        if size == 0:
            self.block = []
        elif self.size < size:  # If new size > old size, system will append new empty blocks
            for i in range(self.size, size):
                self.block.append(None)
        elif self.size > size:  # If new size < old size, system will delete difference
            difference = self.size - size  # in memory size and delete any Files that were allocated in the recently
            for i in range(self.size - 1, self.size - difference, -1):  # deleted memory blocks
                del self.block[i]
            last = self.block[-1]
            if last is not None and last.start + last.size > size:
                for i in range(size, last.start - 1, -1):
                    self.block[i] = None
        else:
            print("Same size entered, no changes made")
            return
        self.size = size

    def unallocated(self):
        return self.size-self.allocated

    def display(self):  # How the console will display the allocated memory blocks
        count = 0
        for i in range(self.size):
            if self.block[i] is None:
                print("Block: ", i, " File: ", self.block[i])
            else:
                print("Block: ", i, " File: ", self.block[i].name)


class Simulator:

    def __init__(self, files, memory):  # Constructor
        self.files = files
        self.memory = memory

    def contiguous(self):
        for file in self.files:
            if file.start is None and self.memory.unallocated() >= file.size:
                start = rng(0, self.memory.size - file.size)
                print(start)
                rngval = start
                loop_flag = True
                while loop_flag:
                    count = 0
                    flag = False
                    for i in range(start, start + file.size):
                        if flag and i >= rngval:
                            loop_flag = False
                        if i >= self.memory.size and not flag:
                            flag = True
                            break
                        if self.memory.block[i] is None:
                            count += 1
                        else:
                            start += self.memory.block[i].size + count
                            break
                    if flag:
                        start = 0
                        # due to random start if end is reached loop back to memory block 0
                    if count == file.size:
                        for i in range(start, start + file.size):  # allocate
                            self.memory.block[i] = file
                            self.memory.allocated += 1
                        file.start = start
                        break

    def linked(self):
        return NotImplementedError()

    def indexed(self):
        return NotImplementedError()

    def reset(self):
        for i in range(0, self.memory.size):
            self.memory.block[i] = None
        self.memory.allocated = 0
        for file in self.files:
            file.start = None

    def delete(self, filename):  # Function that deletes File given the File's name from the user
        for file in self.files:
            if file.name == filename:
                if file.start is not None:  # Remove file from every memory block it is allocated to
                    for i in range(file.start, file.size + file.start):
                        self.memory.block[i] = None
                        self.memory.allocated -= 1
                self.files.remove(file)  # Removing the File from the file list
                return True
        return False

    def display(self):  # Function to display the Files alongside the memory blocks
        print("Files:")
        for file in self.files:
            file.display()
        print("Blocks: ")
        self.memory.display()


def rng(start, end):
    return random.randint(start, end)
