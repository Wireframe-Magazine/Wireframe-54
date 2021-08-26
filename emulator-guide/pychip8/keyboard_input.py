"""This module contains the keyboard input handling logic"""
 
import sys
import pygame
 
keys = {}
keys[pygame.K_0] = 0x0
keys[pygame.K_1] = 0x1
keys[pygame.K_2] = 0x2
keys[pygame.K_3] = 0x3
keys[pygame.K_4] = 0x4
keys[pygame.K_5] = 0x5
keys[pygame.K_6] = 0x6
keys[pygame.K_7] = 0x7
keys[pygame.K_8] = 0x8
keys[pygame.K_9] = 0x9
keys[pygame.K_a] = 0xA
keys[pygame.K_b] = 0xB
keys[pygame.K_c] = 0xC
keys[pygame.K_d] = 0xD
keys[pygame.K_e] = 0xE
keys[pygame.K_f] = 0xF
 
def handle_input(cpu=None):
    """
    This function handles control input for this program.
    """
    for event in pygame.event.get():
 
        # quit if user presses exit or closes the window
        if event.type == pygame.QUIT:
            sys.exit()
 
        # check cpu registers and inject key input
        if cpu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
 
                if event.key in keys:
                    cpu.key_down(keys[event.key])
 
            if event.type == pygame.KEYUP:
                if event.key in keys:
                    cpu.key_up(keys[event.key])
