class CPU:
    def __init__(self):
        self.PC = 0
        self.TC = 1
        self.PS = 0
        self.mem = ([], [], [], [], [], [], [], [], [], [])
        self.R1 = ['000000000000000000000000']
        self.R2 = ['000000000000000000000000']
        self.R3 = ['000000000000000000000000']
        self.R4 = ['000000000000000000000000']
        self.registers = {'R1': self.R1, 'R2': self.R2, 'R3': self.R3, 'R4': self.R4}

    @staticmethod
    def decimal_to_bit_binary(str_num):
        int_num = int(str_num)
        k = '0'
        if (-((2 ** 23) - 1)) <= int_num <= ((2 ** 23) - 1):
            if int_num > 0:
                bin_num = bin(int_num)[2:]
                bin_num = bin_num.zfill(23)
                k = '0'
            elif int_num < 0:
                bin_num = bin(int_num)[3:]
                bin_num = bin_num.zfill(23)
                bin_num = list(bin_num)
                inverted_list = ['1' if char == '0' else '0' for char in bin_num]
                bin_num = ''.join(inverted_list)
                k = '1'
            else:
                bin_num = '000000000000000000000000'
        else:
            if int_num > 0:
                bin_num = bin(int_num)[2:]
            elif int_num < 0:
                bin_num = bin(int_num)[3:]
                bin_num = list(bin_num)
                inverted_list = ['1' if char == '0' else '0' for char in bin_num]
                bin_num = ''.join(inverted_list)

            bin_num = bin_num[-24:]

            if bin_num[0] == '0':
                bin_num = bin_num[1:]
                k = '0'
            elif bin_num[0] == '1':
                bin_num = bin_num[1:]
                bin_num = list(bin_num)
                inverted_list = ['1' if char == '0' else '0' for char in bin_num]
                bin_num = ''.join(inverted_list)
                k = '1'
            else:
                bin_num = '000000000000000000000000'

        bin_num = k + bin_num

        return bin_num

    def bin_to_hex(self, r):
        if r in self.registers and self.registers[r]:
            if int(self.registers[r][0][0]) == 0:
                main_part = int(self.registers[r][0][1:], 2)
                hex_num = self.registers[r][0][0] + hex(main_part)[2:]
                return hex_num

            elif int(self.registers[r][0][0]) == 1:
                invert_hex = list(self.registers[r][0][1:])
                inverted_list = ['1' if char == '0' else '0' for char in invert_hex]
                main_part = ''.join(inverted_list)

                main_part = int(main_part, 2)
                hex_num = self.registers[r][0][0] + hex(main_part)[2:]
                return hex_num
        else:
            raise ValueError(f"Register {r} is empty or does not exist")

    def load_function(self, r, value):
        temp = self.decimal_to_bit_binary(value)
        self.registers[r] = []
        self.registers[r].append(temp)
        self.PS = self.decimal_to_bit_binary(value)[0]

    def Load_memory_function(self, hex_num, index):
        index = int(index)
        if index < 0 or index >= 10:
            raise IndexError("Index out of range")
        else:
            target_cell = self.mem[index]
            if all(bit == 0 for bit in target_cell):
                self.mem[index].append(hex_num)
            else:
                raise ValueError("Cell is not empty")
        return 1

    def add_function(self, r1, r2):
        num_sign1 = self.registers[r1][0][1:]
        num_sign2 = self.registers[r2][0][1:]

        if self.registers[r1][0][0] == '0':
            v1 = int(num_sign1, 2)
        else:
            num_sign1 = list(num_sign1)
            inverted_list_2 = ['1' if char == '0' else '0' for char in num_sign1]
            num_sign1 = ''.join(inverted_list_2)
            v1 = int(num_sign1, 2)*(-1)

        if self.registers[r2][0][0] == '0':
            v2 = int(num_sign2, 2)
        else:
            num_sign2 = list(num_sign2)
            inverted_list_2 = ['1' if char == '0' else '0' for char in num_sign2]
            num_sign2 = ''.join(inverted_list_2)
            v2 = int(num_sign2, 2)*(-1)

        sum = v1 + v2
        sum = self.decimal_to_bit_binary(sum)

        self.registers[r1] = []
        self.registers[r1].append(sum)

        self.PS = sum[0]

        return 1

    def perform_operations(self, r, op2):
        binary_string = ''.join(self.registers[r])
        bytes = [binary_string[i:i + 4] for i in range(0, len(binary_string), 4)]
        total_sum = 0
        for byte in bytes:
            byte_sum = int(byte, 2) % 10
            total_sum += byte_sum

        op2 = int(op2)
        res = total_sum % op2
        res2 = self.decimal_to_bit_binary(res)
        self.registers[r] = []
        self.registers[r].append(res2)
        self.PS = self.decimal_to_bit_binary(res)[0]

    def pc_plus(self):
        self.PC += 1

    def tc_plus(self):
        self.TC += 1

    def output(self, com, op1, op2):
        print(f'Ins = {com} | {op1} | {op2}')
        print(f'PS: {self.PS}')
        print(f'PC: {self.PC}')
        print(f'TC: {self.TC}')
        print(f'R1: {"".join(map(str, self.registers["R1"]))}')
        print(f'R2: {"".join(map(str, self.registers["R2"]))}')
        print(f'R3: {"".join(map(str, self.registers["R3"]))}')
        print(f'R4: {"".join(map(str, self.registers["R4"]))}')
        print('---------------------------------')

    def commands(self, com, op1, op2):
        if com == 'load':
            self.load_function(op1, op2)
        elif com == 'ByteMod':
            self.perform_operations(op1, op2)
        elif com == 'add':
            self.add_function(op1, op2)
        elif com == 'loadMem':
            hex_num = [self.bin_to_hex(op1)]
            self.Load_memory_function(hex_num, op2)
            print("Memory: ", self.mem)


def main():
    cpu = CPU()
    cpu.__init__()
    program_file = "commands.txt"
    with open(program_file, "r") as f:
        program = f.readlines()

    for line in program:
        parts = line.split()
        com = parts[0]
        op1 = parts[1]
        op2 = parts[2]

        cpu.pc_plus()
        cpu.output(com, op1, op2)
        cpu.tc_plus()

        cpu.commands(com, op1, op2)

        cpu.output(com, op1, op2)

        key = input("Press ane key to continue...")
        cpu.TC = 1


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("You've ended this session")
    except BaseException:
        print("Something unexpected happened")

