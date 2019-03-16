#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import sys

#データ読み込みクラス
class Class_Img_PreProcessing():
    '''
    画像データの前処理をまとめたクラス
    '''

    def __init__(self,filepath="",cv2img = None):
        '''
        コンストラクタ (filepath=指定したパス の画像の読み込み,もしくはcv2img=numpy形式データを代入)

        '''
        if filepath !="" :  #ファイルパスが指定された場合
            self.img = cv2.imread(filepath)
        elif cv2img != None: #numpy形式データが入力された場合
            self.img = cv2img
        else:
            self,img = None

    def get_gray_img(self,color_im= "None"):
        '''
        グレースケール画像を取得する (color_im:カラー画像データ(option))
        '''
        if color_im is "None":
            if self.img is None:
                return None
            else:
                return cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            return cv2.cvtColor(color_im, cv2.COLOR_BGR2GRAY)

    def flip_img(self,mode="x"):
        '''
        画像を反転させる
        x: 横方向反転、y:縦方向反転 xy:両方向反転
        '''
        if self.img is None:
            return None
        else:
            if mode == "x": #X軸方向反転
                result = cv2.flip(self.img,1)
            elif mode == "y": #Y軸方向反転
                result = cv2.flip(self.img,0)
            elif mode == "xy": #両方向反転
                result = cv2.flip(self.img,-1)
            else:
                result = self.img
        return result

if __name__ == '__main__':

    target_ext = ['.jpg','.png','.tif']

    for indx in range(1,len(sys.argv)):
        filename = sys.argv[indx]
        root, ext = os.path.splitext(filename)
        print(ext)
        for indx2 in range(len(target_ext)):
            if ext == target_ext[indx2]:
                img_inst = Class_Img_PreProcessing(filename)
                flip_img = img_inst.flip_img(mode="x")
                gray_img = img_inst.get_gray_img(color_im = flip_img)
                cv2.imshow("Windowname",gray_img)
                cv2.waitKey(0)


