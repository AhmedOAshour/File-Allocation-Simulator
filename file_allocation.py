class File:

    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.start = None

    def display(self):
        print("Name: ", self.name, " Size: ", self.size, "Start:", self.start, "End: ", (self.size+self.start-1))


class Block:

    def __init__(self, num):
        self.num = num
        self.allocated = 0
        self.blocks = []
        for i in range(num):
            self.blocks.append(None)

    def unallocated(self):
        return self.num-self.allocated

    def display(self):
        count = 0
        for i in range(self.num):
            if self.blocks[i] is None:
                print(i, " ", self.blocks[i])
            else:
                print("Block: ", i, " File: ", self.blocks[i].name)


class Simulator:

    def __init__(self, files, block_num):
        self.files = files
        self.block_num = block_num
        self.block = Block(block_num)

    def contiguous(self):
        for file in self.files:
            start = 0
            if self.block.unallocated() >= file.size:
                while True:
                    count = 0
                    for i in range(start, start + file.size):
                        if self.block.blocks[i] is None:
                            count += 1
                        else:
                            start += self.block.blocks[i].size + count
                            break
                    if count == file.size:
                        for i in range(start, start + file.size):
                            self.block.blocks[i] = file
                            self.block.allocated += 1
                        file.start = start
                        break;
                        # allocate
            else:
                print(file.name, "couldnt be allocated. Insufficient Space")

    def linked(self):
        return NotImplementedError()

    def indexed(self):
        return NotImplementedError()
