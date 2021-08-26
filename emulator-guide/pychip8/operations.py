"""
This module defines methods that define the different operations the CHIP-8
CPU could perform.
"""
import random
import font
 
# V[15] is used as a carry/no borrow flag for certain ops
CARRY_FLAG_ADDRESS = 0xF
 
def add_to_x(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] += opcode.nn
    cpu.general_purpose_registers[opcode.x] &= 0xFF  # restrict the value to one byte or less
 
def add_x_to_i(opcode, cpu):
    cpu.clear_arithmetic_flag()
    original_value = cpu.index_register
    result = cpu.index_register + cpu.general_purpose_registers[opcode.x]
    result &= 0xFFFF  # restrict the value to two bytes or less
 
    if result < original_value:
        cpu.set_arithmetic_flag()
 
    cpu.index_register = result
 
def add_y_to_x(opcode, cpu):
    cpu.clear_arithmetic_flag()
 
    original_value = cpu.general_purpose_registers[opcode.x]
    result = cpu.general_purpose_registers[opcode.x] + \
        cpu.general_purpose_registers[opcode.y]
 
    result &= 0xFF # restrict the value to one byte or less
 
    if result < original_value:
        cpu.set_arithmetic_flag()
 
    cpu.general_purpose_registers[opcode.x] = result
 
def take_x_from_y(opcode, cpu):
    cpu.set_arithmetic_flag()
 
    original_value = cpu.general_purpose_registers[opcode.x]
    result = cpu.general_purpose_registers[opcode.y] - \
        cpu.general_purpose_registers[opcode.x]
 
    result &= 0xFF # restrict the value to one byte or less
 
    if result > original_value:
        cpu.clear_arithmetic_flag()
 
    cpu.general_purpose_registers[opcode.x] = result
 
def take_y_from_x(opcode, cpu):
    cpu.set_arithmetic_flag()
 
    original_value = cpu.general_purpose_registers[opcode.x]
    result = cpu.general_purpose_registers[opcode.x] - \
        cpu.general_purpose_registers[opcode.y]
 
    result &= 0xFF # restrict the value to one byte or less
 
    if result > original_value:
        cpu.clear_arithmetic_flag()
 
    cpu.general_purpose_registers[opcode.x] = result
 
def bitwise_and(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] = cpu.general_purpose_registers[opcode.x] & cpu.general_purpose_registers[opcode.y]
 
def bitwise_or(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] = cpu.general_purpose_registers[opcode.x] | cpu.general_purpose_registers[opcode.y]
 
def bitwise_xor(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] = cpu.general_purpose_registers[opcode.x] ^ cpu.general_purpose_registers[opcode.y]
 
def shift_x_left(opcode, cpu):
    most_significant_bit = (cpu.general_purpose_registers[opcode.x] >> 7)
    cpu.general_purpose_registers[CARRY_FLAG_ADDRESS] = most_significant_bit
    # restrict the shifted value to one byte or less
    cpu.general_purpose_registers[opcode.x] = (
        cpu.general_purpose_registers[opcode.x] << 1) & 0xFF
 
def shift_x_right(opcode, cpu):
    least_significant_bit = cpu.general_purpose_registers[opcode.x] & 0x01
    cpu.general_purpose_registers[CARRY_FLAG_ADDRESS] = least_significant_bit
    # restrict the shifted value to one byte or less
    cpu.general_purpose_registers[opcode.x] = cpu.general_purpose_registers[opcode.x] >> 1
 
def clear_display(opcode, cpu):
    for x in range(cpu.FRAME_BUFFER_WIDTH):
        for y in range(cpu.FRAME_BUFFER_HEIGHT):
            cpu.frame_buffer[x][y] = bool()
 
def draw_sprite(opcode, cpu):
    cpu.should_draw = True
    cpu.clear_arithmetic_flag()
 
    x = cpu.general_purpose_registers[opcode.x]
    y = cpu.general_purpose_registers[opcode.y]
 
    height = opcode.n
 
    for current_row_offset in range(height):
 
        row = y + current_row_offset
        new_pixels = cpu.ram[cpu.index_register + current_row_offset]
 
        for x_offset in range(8):
 
            mask = 128 >> x_offset
 
            column = x + x_offset
 
            # make sure x and y don't go out of bounds!
            if column >= cpu.FRAME_BUFFER_WIDTH or row >= cpu.FRAME_BUFFER_HEIGHT:
                continue
 
            old_bit = cpu.frame_buffer[column][row]
            new_bit = bool(new_pixels & mask)
            bit_value = old_bit ^ new_bit
            cpu.frame_buffer[column][row] = True if bit_value else False
 
            if old_bit and new_bit:
                cpu.set_arithmetic_flag()
 
def skip_if_key_not_pressed(opcode, cpu):
    key = cpu.general_purpose_registers[opcode.x]
    if key not in cpu.keys:
        cpu.move_to_next_instruction()
 
def skip_if_key_pressed(opcode, cpu):
    key = cpu.general_purpose_registers[opcode.x]
    if key in cpu.keys:
        cpu.move_to_next_instruction()
 
def wait_for_key_press(opcode, cpu):
    if not cpu.keys:
        cpu.move_to_previous_instruction()
    else:
        cpu.general_purpose_registers[opcode.x] = sorted(cpu.keys)[0]
 
def call_function(opcode, cpu):
    cpu.stack.append(cpu.program_counter)
    cpu.program_counter = opcode.nnn
 
def goto_plus(opcode, cpu):
    cpu.program_counter = cpu.general_purpose_registers[0] + opcode.nnn
    cpu.program_counter &= 0xFFFF  # restrict the PC value to two bytes or less
 
def goto(opcode, cpu):
    cpu.program_counter = opcode.nnn
    cpu.program_counter &= 0xFFFF  # restrict the PC value to two bytes or less
 
def return_from_function(opcode, cpu):
    address = cpu.stack.pop()
    cpu.program_counter = address
 
def skip_if_equal(opcode, cpu):
    if(cpu.general_purpose_registers[opcode.x] == opcode.nn):
        cpu.move_to_next_instruction()
 
def skip_if_not_equal(opcode, cpu):
    if(cpu.general_purpose_registers[opcode.x] != opcode.nn):
        cpu.move_to_next_instruction()
 
def skip_if_x_y_equal(opcode, cpu):
    if(cpu.general_purpose_registers[opcode.x] == cpu.general_purpose_registers[opcode.y]):
        cpu.move_to_next_instruction()
 
def skip_if_x_y_not_equal(opcode, cpu):
    if(cpu.general_purpose_registers[opcode.x] != cpu.general_purpose_registers[opcode.y]):
        cpu.move_to_next_instruction()
 
def load_character_address(opcode, cpu):
    cpu.index_register = cpu.general_purpose_registers[opcode.x] * \
        font.CHAR_SIZE_IN_BYTES
 
def load_registers_zero_to_x(opcode, cpu):
    for i in range(opcode.x + 1):
        cpu.general_purpose_registers[i] = cpu.ram[cpu.index_register + i]
 
def generate_random(opcode, cpu):
    random_int = random.randint(0, 255)
    cpu.general_purpose_registers[opcode.x] = opcode.nn & random_int
 
def save_registers_zero_to_x(opcode, cpu):
    for i in range(opcode.x + 1):
        cpu.ram[cpu.index_register + i] = cpu.general_purpose_registers[i]
 
def save_x_as_bcd(opcode, cpu):
    value = cpu.general_purpose_registers[opcode.x]
    # store the most significant digit as a byte
    cpu.ram[cpu.index_register] = int(value / 100) & 0xFF
    # store the middle digit as a byte
    cpu.ram[cpu.index_register + 1] = int((value / 10) % 10) & 0xFF
    # store the least significant digit as a byte
    cpu.ram[cpu.index_register + 2] = int(value % 10) & 0xFF
 
def set_i(opcode, cpu):
    cpu.index_register = opcode.nnn
 
def set_x_to_y(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] = cpu.general_purpose_registers[opcode.y]
 
def set_x(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] = opcode.nn
 
def set_delay_timer(opcode, cpu):
    cpu.delay_timer = cpu.general_purpose_registers[opcode.x]
 
def set_sound_timer(opcode, cpu):
    pass # sound is not implemented
 
def set_x_to_delay_timer(opcode, cpu):
    cpu.general_purpose_registers[opcode.x] = cpu.delay_timer
