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

    def __init__(self, num):
        self.num = num
        self.allocated = 0
        self.block = []
        for i in range(num):
            self.block.append(None)

    def unallocated(self):
        return self.num-self.allocated

    def display(self):
        count = 0
        for i in range(self.num):
            if self.block[i] is None:
                print(i, " ", self.block[i])
            else:
                print("Block: ", i, " File: ", self.block[i].name)


class Simulator:

    def __init__(self, files, block_num):
        self.files = files
        self.block_num = block_num
        self.memory = Memory(block_num)

    def contiguous(self):
        for file in self.files:
            start = 0
            if self.memory.unallocated() >= file.size:
                while True:
                    count = 0
                    for i in range(start, start + file.size):
                        if self.memory.block[i] is None:
                            count += 1
                        else:
                            start += self.memory.block[i].size + count
                            break
                    if count == file.size:
                        for i in range(start, start + file.size):
                            self.memory.block[i] = file
                            self.memory.allocated += 1
                        file.start = start
                        break;
                        # allocate
            else:
                print(file.name, "couldn't be allocated: Insufficient Space")

    def linked(self):
        return NotImplementedError()

    def indexed(self):
        return NotImplementedError()

    def display(self):
        print("Files:")
        for file in self.files:
            file.display()
        print("Blocks: ")
        self.memory.display()
