#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import threading
import time
import re

###########################################
###  Serial Socket Communication Class  ###
###########################################
class Class_Serial_Socket(threading.Thread):

    ###################################
    #Connection information ##########
    COM_PORT_NAME = 'COM4'           #for Windows
    #COM_PORT_NAME = '/dev/ttyACM0'  #for Ubuntu
    BAURATE = 115200

    #############################################
    ###  Serial Communication Initialization  ###
    #############################################
    def __init__(self):
        #Initialize value for threading
        threading.Thread.__init__(self)
        self.terminate_request = False

        #Vehicle Control Signals sending to Arduino
        self.debval1 = 0.0  #initialize debag value 1
        self.debval2 = 0.0  #initialize debag value 2

        self.counter = 1.0;

        #initialize serial communication socket information
        self.ser_sock = serial.Serial(self.COM_PORT_NAME,self.BAURATE, timeout=0.01, writeTimeout=0.01)
        self.send_flg = True
        self.RECEIVE_LENGTH = 16;

        time.sleep(3)

    ####################################
    ###  Update RX data from Arduino ###
    ####################################
    def update_RX_data_from_arduino(self,str_b):
        try:
            str = str_b.decode()                 #Arduinoから受信した文字列のデコード
            #str_splitted =str.split(',')
            if (len(str) == self.RECEIVE_LENGTH):
                str_splitted = re.split('[,;]', str) 
                self.debval1 = float(str_splitted[0])      #1つ目の数字の取得
                print('debval1',self.debval1)
                self.debval2 = float(str_splitted[1])      #2つ目の数字の取得
                print('debval2',self.debval2)
        except:
            pass

    ##################################
    ###  Update TX data to Arduino ###
    ##################################
    def update_TX_buffer_to_arduino(self):
        #Generate sending buffer to Arduino
        #debug
        send_buffer = str(self.counter + 2.0)
        tempbuf = str(self.counter)
        send_buffer = send_buffer + "," + tempbuf
        send_buffer = send_buffer + ";" #for charactor end token
        self.counter = self.counter + 1.0
        if self.counter > 5.0:
            self.counter = 1.0
        try:
            self.ser_sock.write(str.encode(send_buffer))
        except Exception as e:
            print("例外args:", e.args)

        #    pass
            #print("write_error\n")

    ###############################
    ###  Main Periodic Function ###
    ###############################
    def run(self):
        while(1):
            if self.terminate_request == True:
                break;  #Finish  (User request)
            if self.send_flg == True:
                #try:
                #    self.update_TX_buffer_to_arduino()
                #except:
                #    print("Serial Communication Error (PC->Arduino)")
                self.update_TX_buffer_to_arduino()
                self.send_flg = False
            else:
                str = ""
                try:
                    str = self.ser_sock.readline()
                    self.update_RX_data_from_arduino(str)
                except:
                    print("Serial Communication Error (Arduino->PC)")
                self.send_flg = True
            time.sleep(0.050)

if __name__ == '__main__':
        sock_controler = Class_Serial_Socket()                 #Initialize Serial Communication
        sock_controler.start()