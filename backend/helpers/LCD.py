from RPi import GPIO
import time
from typing import List


class LCDClass():
    def __init__(self, dataPins: List[int], instructionPin: int, enablePin: int, data_length: int = 8) -> None:
        self.dataPins = dataPins
        self.instructionPin = instructionPin
        self.enablePin = enablePin
        self.force_8bit = False

        self.delay = 0.0005
        if data_length in [4, 8]:
            self.datalength = data_length

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.instructionPin, GPIO.OUT)
        GPIO.setup(self.enablePin, GPIO.OUT)
        for pin in self.dataPins:
            GPIO.setup(pin, GPIO.OUT)

        GPIO.output(self.instructionPin, GPIO.HIGH)
        GPIO.output(self.enablePin, GPIO.HIGH)
        for pin in self.dataPins:
            GPIO.output(pin, GPIO.HIGH)

        self.init_lcd()

    def init_lcd(self):
        functionset = 0x28
        if self.datalength == 8:
            functionset |= 0x10
        self.force_8bit = True
        # function set of 0x38 (Data Length: 8bit, Number of lines: 2, Font (resolutie per character): 5x7)
        self.send_instruction(functionset)
        self.force_8bit = False
        # function on of 0xf (Display ON, Cursor ON, cursor Blink ON)
        self.send_instruction(0xF)
        self.clear_lcd()

    def clear_lcd(self):
        self.send_instruction(0x1)  # clear display/cursor home of 0x01

    def second_line(self):
        # print('Second line')
        # Sets cursor to position 40 (1st of second line)
        self.send_instruction(0xC0)

    def set_cursor(self, position: List[int] = [0, 0], on: bool = False, blink: bool = False):
        row = position[0]
        col = position[1]
        options = 0xC  # Start with Function and Display on
        if on:
            options |= 0x2
        if blink:
            options |= 0x1
        self.send_instruction(options)

        if row >= 0 and row < 2 and col >= 0 and col < 16:
            hexRow = row * 0x40
            hexCol = col
            position = hexRow | hexCol
            # Zet eerste bit van de 8 op 1 om te zeggen dat de cursor verzet wordt
            instruction = position | 0x80
            self.send_instruction(instruction)
        else:
            print('Invalid cursor position')

    def send_instruction(self, byte, explain: bool = False):
        # print(byte)
        GPIO.output(self.instructionPin, GPIO.LOW)
        if explain:
            self.explain_instruction_byte(byte)
        self.send_data_byte(byte)

    def send_text(self, text):
        if len(text) <= 16:
            for i in text:
                self.send_character(i)
        elif len(text) <= 32:
            for i in text[:16]:
                self.send_character(i)
            self.second_line()
            for i in text[16:]:
                self.send_character(i)
        else:
            text = ' ' * 15 + text + ' '
            for i in range(len(text)):
                self.clear_lcd()
                for j in text[:16]:
                    self.send_character(j)
                text = text[1:] + text[0]
                time.sleep(.5)

    def send_character(self, character):
        GPIO.output(self.instructionPin, GPIO.HIGH)
        byte = ord(character)
        print('character: {} (bin: {:08b})'.format(character, byte))
        self.send_data_byte(byte)

    def send_data_byte(self, byte):
        print('incoming byte: {:08b}'.format(byte))
        if self.datalength == 8 or self.force_8bit:
            for i in range(8):
                pin = self.dataPins[i]
                bit = (byte >> i) & 1
                print('pin: {}, bit: {}'.format(pin, bit))
                GPIO.output(pin, bit)
            self.clock()

        elif self.datalength == 4:
            print('4bit')
            for i in range(2):
                nibble = (byte >> (4*i)) & 0x0F
                print('Nibble {}: {:04b}'.format(i+1, nibble))
                for j in range(4):
                    pin = self.dataPins[j]
                    bit = (nibble >> j) & 1
                    print('pin: {}, bit: {}'.format(pin, bit))
                    GPIO.output(pin, bit)
                self.clock()

    def clock(self):
        time.sleep(self.delay)
        GPIO.output(self.enablePin, GPIO.LOW)
        time.sleep(self.delay)
        GPIO.output(self.enablePin, GPIO.HIGH)
        time.sleep(self.delay)

    def explain_instruction_byte(self, byte):
        binstr = '{:08b}'.format(byte)
        print('EXPLAIN BYTE: {} (0b{})'.format(hex(byte), binstr))

        if binstr.startswith('1'):
            print('1 => Set cursor position')
            print('{} |=> New cursor position: {}'.format(
                binstr[1], hex(int(binstr[1:], 2))))
            for i in binstr[2:]:
                print(f'{i} |')

        else:
            for i in range(2):
                print('0')
            if binstr[2] == '1':
                print('1 => Function set')
                print(
                    '1 => Data Length: 8 bit' if binstr[3] == '1' else '0 => Data Length: 4 bit')
                print('1 => 2 lines' if binstr[4] == '1' else '0 => 1 line')
                print(
                    '1 => character font: 5x10' if binstr[5] == '1' else '0 => character font: 5x7')
                for i in binstr[5:]:
                    print(i)

            else:
                for i in range(2):
                    print('0')
                if binstr[4] == '1':
                    print('1 => Display set')
                    print(
                        '1 => Display: ON' if binstr[5] == '1' else '0 => Display: OFF')
                    print(
                        '1 => Cursor: ON' if binstr[6] == '1' else '0 => Cursor: OFF')
                    print(
                        '1 => Cursor Blink: ON' if binstr[7] == '1' else '0 => Cursor Blink: OFF')

                else:
                    for i in range(2):
                        print('0')
                    if binstr[6] == '1':
                        print('1 => Cursor Home')
                        print(binstr[7])
                    else:
                        print('0')
                        print(
                            '1 => Clear Display & Cursor Home' if binstr[7] == '1' else '0')

        print('--------------')
