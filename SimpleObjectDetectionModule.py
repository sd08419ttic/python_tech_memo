#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from matplotlib import pyplot as plt


def templete_matching(src_img,temp_img,threshold):
    '''
    テンプレートマッチング関数
    src_img:入力画像, temp_img:検出対象画像, threshold:検出敷居値(0-1)
    '''
    img_gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)        #入力画像をグレースケール変換する
    temp_gray = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)      #テンプレート画像をグレースケール変換する
    w= template.shape[1]    #テンプレート画像幅
    h= template.shape[0]    #テンプレート画像高さ

    res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)    #テンプレートマッチング,相関係数の正規化指標を利用

    res_vis = res.copy()
    res_vis[res_vis<0] = 0.0
    res_vis = np.uint8((res_vis)*100)
    cv2.imshow("score_map",res_vis)    #スコア表示
    cv2.waitKey(0)
    loc = np.where( res >= threshold)   #閾値判定
    for pt in zip(*loc[::-1]):
        cv2.rectangle(src_img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)   #結果の描画
    cv2.imshow("result",src_img)    #画面表示
    cv2.waitKey(0)


def color_cluster(src_img):
    '''
    色に基づく物体検出
    src_img:入力画像
    '''
    hsv = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV_FULL)             #hsv座標系への変換
    mask = np.zeros((hsv.shape[0],hsv.shape[1],1), dtype=np.uint8)  #画像マスクの生成
    h = hsv[:, :, 0]    #色相
    s = hsv[:, :, 1]    #彩度
    mask[((h < 20) | (h > 200)) & (s > 128)] = 255  #hsv座標系での色マスク(赤色)
    #他の色を設定する場合下記サイトなどで閾値設定する
    #https://www.peko-step.com/tool/hsvrgb.html

    #色マスクに対する輪郭抽出
    contours, hierarchy =cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contour = []

    result_img = src_img.copy()

    #輪郭抽出結果のフィルタ (非常に小さい輪郭はノイズとみなして除去))
    for indx in range(len(contours)):
        if (len(contours[indx])>20):    #輪郭が20pixel異常の長さとなる場合
            filtered_contour.append(contours[indx])
            np_contour = np.array(contours[indx]).reshape(len(contours[indx]),2)
            left_x = min(np_contour[:,0])    #輪郭の一番左となるX座標
            right_x = max(np_contour[:,0])   #輪郭の一番右となるX座標
            top_y = min(np_contour[:,1])     #輪郭の一番上となるY座標
            bottom_y = max(np_contour[:,1])  #輪郭の一番下となるY座標
            #cv2.rectangle(result_img, (left_x,top_y), (right_x, bottom_y), (0,0,255), 2)    #長方形で物体の領域を表示
            pass
    result_img = cv2.drawContours(result_img, filtered_contour, -1, (0,255,0), 3)
    cv2.imshow("result",result_img)
    cv2.waitKey(0)


def edge_cluster(src_img):
    '''
    エッジ形状に基づく物体認識
    src_img:入力画像
    '''

    #canny edge http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_canny/py_canny.html
    edges = cv2.Canny(src_img,100,200)

    #ハフ変換
    cv2.imshow("result",edges)
    cv2.waitKey(0)


    #線の検出と描画
    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    for indx in range(len(lines)):
        for rho,theta in lines[indx]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(src_img,(x1,y1),(x2,y2),(0,255,0),2)

    #円の検出と描画
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(src_img,(i[0],i[1]),i[2],(255,0,0),2)
        # draw the center of the circle
        cv2.circle(src_img,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow("result",src_img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src_img = cv2.imread('D:/WS/VS_project/BlogProject/BlogProject/img/Mandrill.bmp')   #検出の対象とする画像
    #src_img = cv2.imread('D:/WS/VS_project/BlogProject/BlogProject/img/figure_Test.png')   #検出の対象とする画像

    template = cv2.imread('D:/WS/VS_project/BlogProject/BlogProject/img/Mandrill_part.bmp')

    #テンプレートマッチング
    templete_matching(src_img,template,0.8)

    #色に基づく物体検出
    #color_cluster(src_img)

    #エッジに基づく形状検出 (Cannyエッジ検出+ハフ変換)
    #edge_cluster(src_img)
