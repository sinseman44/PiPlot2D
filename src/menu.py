#!/usr/bin/env python3

import os, sys

###################################################################

class menu:
    # Main Menu :
    #  |-> Files :    Display gcode files in FTP directory
    #  |-> Commands : Display custom commands (homing, setup pen, etc ...)
    #  |-> Poweroff : Power off the system
    #  |-> Reboot :   Reboot the system

    main_menu = ['Files',
                 'Commands',
                 'Poweroff',
                 'Reboot']

    cmd_menu = ['..',
                'Homing',
                'Set up Pen',
                'Set down Pen']

    files_menu = ['..']

    def __init__(self, lcd=None, cols=0, rows=0):
        ''' constructor '''
        self.lcd = lcd
        self.max_cols = cols
        self.max_rows = rows
        self.current_cursor = 0
        self.current_menu = self.main_menu 
        for dirs,r,files in os.walk("/srv/ftp"):
            for f in files:
                if len(f) > 14:
                    f = f[:13]+'~'
                self.files_menu.append(f)

    def __refresh_menu(self):
        ''' refresh current menu '''
        pos = 0
        if self.current_cursor % self.max_rows == 0:
            pos = self.current_cursor
        else:
            pos = self.current_cursor - 1
        for idx, menu in enumerate(self.current_menu[pos:]):
            self.lcd.cursor_pos = (idx, 2)
            if menu.endswith('~'):
                menu = menu[:-1]+'\x01'
            self.lcd.write_string(menu)
            if idx == self.max_rows - 1:
                break

    def __drawing(self, filename):
        ''' drawing gcode '''
        self.lcd.clear()
        self.lcd.home()
        self.lcd.write_string("   drawing ...")
        os.system("sudo python /home/pi/PyCNC/pycnc " + os.path.join("/srv/ftp/", filename))
        self.lcd.clear()
        self.lcd.cursor_pos = (self.current_cursor % self.max_rows, 0)
        self.lcd.write_string('\x00')
        self.__refresh_menu()


    def __homing(self):
        ''' set homing command '''
        self.lcd.clear()
        self.lcd.home()
        self.lcd.write_string("   waiting ...")
        with open("/tmp/homing.gcode", 'w') as f:
            f.write("G28 (Homing)")
        os.system("sudo python /home/pi/PyCNC/pycnc /tmp/homing.gcode")
        self.lcd.clear()
        self.lcd.cursor_pos = (self.current_cursor % self.max_rows, 0)
        self.lcd.write_string('\x00')
        self.__refresh_menu()

    def __set_up_pen(self):
        ''' set up pen '''
        self.lcd.clear()
        self.lcd.home()
        self.lcd.write_string("   waiting ...")
        with open("/tmp/set_up_pen.gcode", 'w') as f:
            f.write("M300 S50 (UP Pen)")
        os.system("sudo python /home/pi/PyCNC/pycnc /tmp/set_up_pen.gcode")
        self.lcd.clear()
        self.lcd.cursor_pos = (self.current_cursor % self.max_rows, 0)
        self.lcd.write_string('\x00')
        self.__refresh_menu()

    def __set_down_pen(self):
        ''' set down pen '''
        self.lcd.clear()
        self.lcd.home()
        self.lcd.write_string("   waiting ...")
        with open("/tmp/set_down_pen.gcode", 'w') as f:
            f.write("M300 S30 (DOWN Pen)")
        os.system("sudo python /home/pi/PyCNC/pycnc /tmp/set_down_pen.gcode")
        self.lcd.clear()
        self.lcd.cursor_pos = (self.current_cursor % self.max_rows, 0)
        self.lcd.write_string('\x00')
        self.__refresh_menu()

    def init_menu(self):
        ''' display menu '''
        self.lcd.clear()
        self.lcd.cursor_pos = (self.current_cursor, 0)
        self.lcd.write_string('\x00')
        self.__refresh_menu()

    def set_down(self):
        ''' set down menu '''
        if self.current_cursor < len(self.current_menu) - 1:
            self.lcd.clear()
            self.current_cursor += 1
            self.lcd.cursor_pos = (self.current_cursor % self.max_rows, 0)
            self.lcd.write_string('\x00')
            self.__refresh_menu()

    def set_up(self):
        ''' set up menu '''
        if self.current_cursor > 0:
            self.lcd.clear()
            self.current_cursor -= 1
            self.lcd.cursor_pos = (self.current_cursor % self.max_rows, 0)
            self.lcd.write_string('\x00')
            self.__refresh_menu()

    def set_ok(self):
        ''' set ok '''
        if self.current_menu == self.main_menu:
            if self.current_menu[self.current_cursor].startswith('Commands'):
                self.current_menu = self.cmd_menu
            elif self.current_menu[self.current_cursor].startswith('Files'):
                self.current_menu = self.files_menu
                self.files_menu = ['..']
                for dirs,r,files in os.walk("/srv/ftp"):
                    for f in files:
                        if len(f) > 14:
                            f = f[:13]+'~'
                        self.files_menu.append(f)
            elif self.current_menu[self.current_cursor].startswith('Poweroff'):
                self.lcd.clear()
                self.lcd.home()
                self.lcd.write_string("   Bye Bye ...")
                os.system('sudo systemctl poweroff')
                exit(0)
            elif self.current_menu[self.current_cursor].startswith('Reboot'):
                self.lcd.clear()
                self.lcd.home()
                self.lcd.write_string("   Bye Bye ...")
                os.system('sudo systemctl reboot')
                exit(0)
            self.current_cursor = 0
            self.init_menu()
        else:
            if self.current_menu == self.cmd_menu:
                if self.current_menu[self.current_cursor].startswith('Homing'):
                    self.__homing()
                elif self.current_menu[self.current_cursor].startswith('Set up Pen'):
                    self.__set_up_pen()
                elif self.current_menu[self.current_cursor].startswith('Set down Pen'):
                    self.__set_down_pen()
            elif self.current_menu == self.files_menu:
                if not self.current_menu[self.current_cursor].startswith('..'):
                    self.__drawing(self.current_menu[self.current_cursor])

            if self.current_menu[self.current_cursor].startswith('..'):
                self.current_menu = self.main_menu
                self.current_cursor = 0
                self.init_menu()

