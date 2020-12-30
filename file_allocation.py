import random


class File:

    def __init__(self, size, name):  # Constructor
        self.size = size
        self.name = name
        self.start = None
        self.end = None

    def display(self):  # How the console will display the allocated Files
        if self.start is None:
            print("Name: ", self.name, " Size: ", self.size, "Start: Unallocated")
        else:
            print("Name: ", self.name, " Size: ", self.size, "Start:", self.start, "End: ", self.end)


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

    def unallocated(self):  # Returns the number of unallocated blocks in memory
        return self.size - self.allocated

    def display(self):  # How the console will display the allocated memory blocks using contiguous allocation
        for i in range(self.size):
            if self.block[i] is None:
                print("Block: ", i, ", File: ", self.block[i])
            elif isinstance(self.block[i], list):
                print("Block: ", i, ", Index Table: ", self.block[i])
            else:
                print("Block: ", i, ", File: ", self.block[i].name)

    def display_linked(self):  # How the console will display the allocated memory blocks using linked allocation
        for i in range(self.size):
            if self.block[i] is None:
                print("Block: ", i, ", File: ", self.block[i])
            else:
                print("Block: ", i, ", File: ", self.block[i].data.name)

    def display_indexed(self):  # How the console will display the allocated memory blocks using indexed allocation
        for i in range(self.size):
            if self.block[i] is None:
                print("Block: ", i, ", File: ", self.block[i])
            else:
                print("Block: ", i, ", File: ", self.block[i].name)


class Node:

    def __init__(self, data, nextval):
        self.data = data
        self.nextval = nextval


class Simulator:

    def __init__(self, files, memory):  # Constructor
        self.files = files
        self.memory = memory
        self.flag = None

    def contiguous(self):
        self.flag = 1
        for file in self.files:
            if file.start is None and self.memory.unallocated() >= file.size:
                start = rng(0, self.memory.size - 1)
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
                        file.end = file.size + file.start - 1
                        break

    def linked(self):
        self.flag = 2
        for file in self.files:
            if file.start is None and self.memory.unallocated() >= file.size:
                current = None
                for i in range(0, file.size):
                    index = rng(0, self.memory.size - 1)
                    while self.memory.block[index] is not None:
                        index += 1
                        if index >= self.memory.size:
                            index = 0
                    self.memory.block[index] = Node(file, None)
                    self.memory.allocated += 1
                    if current is not None:
                        current.nextval = self.memory.block[index]
                        current = current.nextval
                    if i == 0:
                        file.start = index
                        current = self.memory.block[index]
                    if i == file.size - 1:
                        file.end = index

    def indexed(self):
        self.flag = 3
        for file in self.files:
            if file.start is None and self.memory.unallocated() >= file.size + 1:  # Check condition
                for i in range(0, file.size + 1):
                    index = rng(0, self.memory.size - 1)
                    while self.memory.block[index] is not None:
                        index += 1
                        if index >= self.memory.size:
                            index = 0
                    if i == 0:
                        file.start = index
                        self.memory.block[index] = []
                        self.memory.allocated += 1
                        continue
                    self.memory.block[index] = file
                    self.memory.block[file.start].append(index)
                    self.memory.allocated += 1

    def reset(self):  # De-allocates all memory blocks
        for i in range(0, self.memory.size):
            self.memory.block[i] = None
        self.memory.allocated = 0
        for file in self.files:
            file.start = None
            file.end = None

    def delete(self, filename):
        if self.flag is None or self.flag == 1:
            return self.delete_contiguous(filename)
        elif self.flag == 2:
            return self.delete_linked(filename)
        elif self.flag == 3:
            return self.delete_indexed(filename)

    def delete_contiguous(self, filename):  # Function that deletes File given the File's name from the user
        for file in self.files:
            if file.name == filename:
                if file.start is not None:
                    # Remove file from every memory block it is allocated to
                    for i in range(file.start, file.size + file.start):
                        self.memory.block[i] = None
                        self.memory.allocated -= 1
                self.files.remove(file)  # Removing the File from the file list
                return True
        return False

    def delete_indexed(self, filename):
        for file in self.files:
            if file.name == filename:
                if file.start is not None:
                    table = self.memory.block[file.start]
                    self.memory.block[file.start] = None
                    self.memory.allocated -= 1
                    for i in table:
                        self.memory.block[i] = None
                        self.memory.allocated -= 1
                self.files.remove(file)
                return True
        return False

    def delete_linked(self, filename):
        for file in self.files:
            if file.name == filename:
                if file.start is not None:
                    current = self.memory.block[file.start]
                    while current.nextval is not None:
                        next = current.nextval
                        del current
                        current = next
                self.files.remove(file)
                return True
        return False

    def display(self):  # Function to display the Files alongside the memory blocks
        print("Files:")
        for file in self.files:
            file.display()
        print("Blocks: ")
        self.memory.display()

    def display_linked(self):  # Function to display the Files alongside the memory blocks
        print("Files:")
        for file in self.files:
            file.display()
        print("Blocks: ")
        self.memory.display_linked()

    def display_indexed(self):  # Function to display the Files alongside the memory blocks
        print("Files:")
        for file in self.files:
            for i in range(0, file.size):
                if file.start is None:
                    print("File Block: ", file.name, i, " Not Allocated")
                    continue
                if i == (file.size - 1):
                    print("File Block: ", file.name, i, ", Memory Block: ", self.memory.block[file.start][i], ", Next Block: NONE")
                    continue
                print("File Block: ", file.name, i, ", Memory Block: ", self.memory.block[file.start][i], ", Next Block: ", self.memory.block[file.start][i+1])
        print("Blocks: ")
        self.memory.display()


def rng(start, end):  # random number generator, default seed is system time
    return random.randint(start, end)
