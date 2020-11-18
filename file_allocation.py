class File:

    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.start = None

    def display(self):
        if self.start is None:
            print("Name: ", self.name, " Size: ", self.size, "Start: Unallocated")
        else:
            print("Name: ", self.name, " Size: ", self.size, "Start:", self.start, "End: ", (self.size+self.start-1))


class Memory:

    def __init__(self, size):
        self.size = size
        self.allocated = 0
        self.block = []
        for i in range(size):
            self.block.append(None)

    def change_size(self, size):
        if size == 0:
            self.block = []
        elif self.size < size:
            for i in range(self.size, size):
                self.block.append(None)
        elif self.size > size:
            difference = self.size - size
            for i in range(self.size - 1, self.size - difference , -1):
                del self.block[i]
            last = self.block[-1]
            if last is not None and last.start + last.size > size:
                for i in range(size, last.start - 1, -1):
                    self.block[i] = None
        else:
            print("Same size entered, no changes made")
        self.size = size

    def unallocated(self):
        return self.size-self.allocated

    def display(self):
        count = 0
        for i in range(self.size):
            if self.block[i] is None:
                print("Block: ", i, " File: ", self.block[i])
            else:
                print("Block: ", i, " File: ", self.block[i].name)


class Simulator:

    def __init__(self, files, memory):
        self.files = files
        self.memory = memory

    def contiguous(self):
        for file in self.files:
            if file.start is None:
                start = 0
                if self.memory.unallocated() >= file.size and file.start is None:
                    while True:
                        count = 0
                        for i in range(start, start + file.size):
                            if self.memory.block[i] is None:
                                count += 1
                            else:
                                start += self.memory.block[i].size + count
                                break
                        if count == file.size:
                            # allocate
                            for i in range(start, start + file.size):
                                self.memory.block[i] = file
                                self.memory.allocated += 1
                            file.start = start
                            break

    def linked(self):
        return NotImplementedError()

    def indexed(self):
        return NotImplementedError()

    def delete(self, filename):
        for file in self.files:
            if file.name == filename:
                for i in range(file.start,file.size):
                    self.memory.block[i] = None
                self.files.remove(file)

    def display(self):
        print("Files:")
        for file in self.files:
            file.display()
        print("Blocks: ")
        self.memory.display()
