#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
 
SCREEN_SIZE = (640, 480)  # 画面サイズ (横/縦)
 

MODE = "HAT"    #KEY:キーボード
                #JOY:ジョイスティックアナログバー(左)
                #HAT:ハットスイッチ(方向ボタン)

STEP = 10       #キーボード/ハットスイッチの反応の良さ

if __name__ == '__main__':
    # Pygameを初期化
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)   # SCREEN_SIZEの画面を作成
    pygame.display.set_caption("window test")       # Windowタイトルの設定
    X_CENTER = int(SCREEN_SIZE[0]/2)
    Y_CENTER = int(SCREEN_SIZE[1]/2)
    [circle_x, circle_y] = [X_CENTER, Y_CENTER]     #円の初期位置を設定

    pygame.joystick.init()
    try:
        joy = pygame.joystick.Joystick(0) # create a joystick instance
        joy.init() # init instance
        print("Joystick Name: " + joy.get_name())
        print("Number of Button : " + str(joy.get_numbuttons()))
        print("Number of Axis : " + str(joy.get_numaxes()))
        print("Number of Hats : " + str(joy.get_numhats()))

    except pygame.error:
        print ('Joystick was not detected!')

    # 画面描画ループ
    while True:
        screen.fill((0,0,0))     # 画面を青色で塗りつぶす
        # イベント処理
        for event in pygame.event.get():    #×ボタンによる終了
            if event.type == QUIT:  # 終了イベント
                sys.exit()

        if MODE == "KEY":
            #  キーボード状態の取得
            pressed_keys = pygame.key.get_pressed()
            # 押されているキーに応じて画像を移動
            if pressed_keys[K_LEFT]:
                circle_x = circle_x - STEP
            if pressed_keys[K_RIGHT]:
                circle_x = circle_x + STEP
            if pressed_keys[K_UP]:
                circle_y = circle_y - STEP
            if pressed_keys[K_DOWN]:
                circle_y = circle_y + STEP

        elif MODE == "JOY":
            #ジョイスティック(アナログバー左スティック)状態の取得
            circle_x = int((joy.get_axis(0)+1) * X_CENTER)    #joystick(横軸)の方向キーはは-1～1の範囲で取得できる
            circle_y = int((joy.get_axis(1)+1) * Y_CENTER)    #joystick(縦軸)の方向キーはは-1～1の範囲で取得できる
            # axis(2)はL2/R2キーに対応
            #ジョイスティック(アナログバー右スティック)状態の取得
            #circle_x = int((joy.get_axis(3)+1) * X_CENTER)    #joystick(横軸)の方向キーはは-1～1の範囲で取得できる
            #circle_y = int((joy.get_axis(4)+1) * Y_CENTER)    #joystick(縦軸)の方向キーはは-1～1の範囲で取得できる


        elif MODE == "HAT":
            #方向ボタン (ハットスイッチ)
            hat_input = joy.get_hat(0)

            if hat_input[0] == -1:
                circle_x = circle_x - STEP
            elif hat_input[0] == 1:
                circle_x = circle_x + STEP
            if hat_input[1] == 1:
                circle_y = circle_y - STEP
            elif hat_input[1] == -1:
                circle_y = circle_y + STEP


        #描画範囲の上下限チェック
        if circle_x< 0:
            circle_x = 0
        elif circle_x > SCREEN_SIZE[0]:
            circle_x = SCREEN_SIZE[0]

        if circle_y< 0:
            circle_y = 0
        elif circle_y > SCREEN_SIZE[1]:
            circle_y = SCREEN_SIZE[1]

        #描画
        pygame.draw.circle(screen, (255,0,0), (circle_x,circle_y), 10)
        pygame.display.update()  # 画面を更新
        pygame.time.wait(30)     # 30msec 待ち
        

