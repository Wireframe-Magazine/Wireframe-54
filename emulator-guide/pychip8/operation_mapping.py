"""
This module defines a code that handles
mapping a 16 bit opcode value to an operation
"""
from operation_code import Opcode
import operations
 
def find_operation(word):
    "This method takes a 16 bit value representing an opcode and returns the related operation"
    opcode = Opcode(word)
 
    if word == 0x00E0:
        return operations.clear_display
 
    if word == 0x00EE:
        return operations.return_from_function
 
    if opcode.a == 0x1:
        return operations.goto
 
    if opcode.a == 0x2:
        return operations.call_function
    
    if opcode.a == 0x3:
        return operations.skip_if_equal
 
    if opcode.a == 0x4:
        return operations.skip_if_not_equal
 
    if opcode.a == 0x5:
        return operations.skip_if_x_y_equal
 
    if opcode.a == 0x6:
        return operations.set_x
 
    if opcode.a == 0x7:
        return operations.add_to_x
 
    if opcode.a == 0x8:
        if opcode.n == 0x0:
            return operations.set_x_to_y
        if opcode.n == 0x1:
            return operations.bitwise_or
        if opcode.n == 0x2:
            return operations.bitwise_and
        if opcode.n == 0x3:
            return operations.bitwise_xor
        if opcode.n == 0x4:
            return operations.add_y_to_x
        if opcode.n == 0x5:
            return operations.take_y_from_x
        if opcode.n == 0x6:
            return operations.shift_x_right
        if opcode.n == 0x7:
            return operations.take_x_from_y
        if opcode.n == 0xE:
            return operations.shift_x_left
 
    if opcode.a == 0x9:
        return operations.skip_if_x_y_not_equal
 
    if opcode.a == 0xA:
        return operations.set_i
 
    if opcode.a == 0xB:
        return operations.goto_plus
 
    if opcode.a == 0xC:
        return operations.generate_random
 
    if opcode.a == 0xD:
        return operations.draw_sprite
 
    if opcode.a == 0xE:
        if opcode.nn == 0x9E:
            return operations.skip_if_key_pressed
        if opcode.nn == 0xA1:
            return operations.skip_if_key_not_pressed
 
    if opcode.a == 0xF:
        if opcode.nn == 0x07:
            return operations.set_x_to_delay_timer
        if opcode.nn == 0x0A:
            return operations.wait_for_key_press
        if opcode.nn == 0x15:
            return operations.set_delay_timer
        if opcode.nn == 0x18:
            return operations.set_sound_timer
        if opcode.nn == 0x1E:
            return operations.add_x_to_i
        if opcode.nn == 0x29:
            return operations.load_character_address
        if opcode.nn == 0x33:
            return operations.save_x_as_bcd
        if opcode.nn == 0x55:
            return operations.save_registers_zero_to_x
        if opcode.nn == 0x65:
            return operations.load_registers_zero_to_x
 
    raise KeyError(f"Opcode {word:#06x} not present in list of valid operations")
