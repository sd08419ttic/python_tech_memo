#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np

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

    def resize_img_aspect_ratio(self,ratio=1.0):
        '''
        画像を拡大縮小する (比率指定)
        '''
        if self.img is None:
            return None
        else:
            result = cv2.resize(self.img , (int(self.img.shape[1]*ratio), int(self.img.shape[0]* ratio)))
        return result

    def resize_img_pix_size(self,height = 200, width = 150):
        '''
        画像を拡大縮小する (ピクセルサイズ指定)
        '''
        if self.img is None:
            return None
        else:
            result = cv2.resize(self.img , (int(width), int(height)))
        return result


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


    def trim_img_aspect_ratio(self,left=0.10, right = 0.10, up=0.10, down = 0.10):
        '''
        画像をトリミングする (左右上下それぞれでカットする部分の比率を0-1.0の間で指定)
        '''
        if self.img is None:
            return None
        else:
            left = max(min(0.5,left),0.0)
            right = max(min(0.5,right),0.0)
            up = max(min(0.5,up),0.0)
            down = max(min(0.5,down),0.0)
            left_edge = int(self.img.shape[0]*left)
            right_edge = int(self.img.shape[0] - self.img.shape[0]*right)
            up_edge = int(self.img.shape[1]*up)
            down_edge = int(self.img.shape[1] - self.img.shape[1]*down)
            result = self.img[up_edge:down_edge,left_edge:right_edge]
        return result

    def trim_img_pix_size(self,left_edge = 0, right_edge = 0,  up_edge = 0, down_edge = 0):
        '''
        画像をトリミングする (ピクセル指定。画像サイズ以上の場合は無視)
        left_edge,right_edge,up_edge,down_edge
        '''
        if self.img is None:
            return None
        else:
            left = max(min(self.img.shape[0],left_edge),0.0)
            right = max(min(self.img.shape[0],right_edge),0.0)
            up = max(min(self.img.shape[1],up_edge),0.0)
            down = max(min(self.img.shape[1],down_edge),0.0)
            result = self.img[up:down,left:right]
        return result

    def zero_padding_img(self,pad_width = 10):
        '''
        画像の境界領域をゼロ埋めする
        pad_width:パディング幅サイズ
        '''
        if self.img is None:
            return None
        else:
            PAD_COL = [0,0,0]   #ゼロパディング
            result= cv2.copyMakeBorder(self.img,pad_width,pad_width,pad_width,pad_width,cv2.BORDER_CONSTANT,value=PAD_COL)
        return result



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

    def get_binary_img(self,prm="OTSU"):
        '''
        2値化処理 prm: "OTSU":大津の2値化、"BIN":静的な2値化、"ADAPT":ローカル閾値

        '''
        if self.img is None:
            return None

        gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        if prm == "OTSU":
            _, result = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)
        elif prm == "BIN":
            _, result = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
        elif prm == "ADAPT":
            result = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 55, 20)
        else:
            result = self.img
        return result


    def get_morphology_img(self,prm="Ero",binimg="None"):
        '''
        モルフォロジー変換 prm: "Ero":収縮、"Dil":膨張、"Ope":オープニング(膨張+縮小) "Clo":"クロージング(縮小+膨張)"

        '''
        if binimg is "None":
            if self.img is None:
                return None
            gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            _, bin_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)
        else:
            bin_img = binimg

        kernel = np.ones((3,3),np.uint8)

        if prm == "Ero":
            result = cv2.erode(bin_img, kernel,iterations = 2)
        elif prm == "Dil":
            result = cv2.dilate(bin_img, kernel,iterations = 2)
        elif prm == "Ope":
            result = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
        elif prm == "Clo":
            result = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
        else:
            result = self.img
        return result

    def get_gamma_img(self,gamma=1.0):
        '''
        ガンマ補正変換 (濃淡の補正)
        gamma: 1.0がデフォルト 小さくするほど薄く白っぽく、高くするほど濃く黒っぽい画像になる

        '''
        if self.img is None:
            return None
        LTB = np.empty((1,256), np.uint8)
        for i in range(256):
            LTB[0,i] = np.clip(pow( float(i) / 255.0, gamma) * 255.0, 0, 255)   #Look Up Tableの生成
 
        result = cv2.LUT(self.img, LTB) #輝度値のガンマ補正
        return result

    def get_gausian_filter_img(self,filtsize=5):
        '''
        ガウシアンフィルタ画像：ぼかしフィルタ (ジャギーなどの低減に有効)
        filtsize:フィルタサイズ(整数型かつ奇数)
        '''
        if self.img is None:
            return None
        # Look up tableを使って画像の輝度値を変更
        result = cv2.GaussianBlur(self.img,(filtsize,filtsize),0)
        return result


    def get_sharp_filter_img(self):
        '''
        鮮鋭化フィルタ画像：ボケた画像のエッジ・テクスチャ強調に有効
        '''
        if self.img is None:
            return None
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
        result = cv2.filter2D(self.img, -1, kernel)
        return result


if __name__ == '__main__':
    path_mnist = "D:\\WS\\VS_project\\BlogProject\\BlogProject\\img\\test0003.png"
    path_lena = "D:\\WS\\VS_project\\BlogProject\\BlogProject\\img\\lena_std.tif"


    img_inst = Class_Img_PreProcessing(path_lena)
    print(img_inst.img.shape)

    gray_img  = img_inst.get_gray_img()                         #グレースケール画像取得例
    bin_img  = img_inst.get_binary_img(prm="OTSU")              #2値化例
    flip_img = img_inst.flip_img(mode="x")
    zero_padding_img = img_inst.zero_padding_img(20)

    mor_img  = img_inst.get_morphology_img(prm="Ope")        #クロージング例
    resized_img = img_inst.resize_img_pix_size(300,100)      #リサイズイメージ(ピクセル指定)
    trim_img = img_inst.trim_img_pix_size(0,2000,300,500)    #リサイズイメージ(ピクセル指定)
    ganma_img = img_inst.get_gamma_img(0.5)                  #ガンマ補正例
    gaus_img = img_inst.get_gausian_filter_img(11)           #ガウシアンフィルタ補正例
    sharp_filter_img = img_inst.get_sharp_filter_img()       #鮮鋭化フィルタ補正例
    

    cv2.imshow("Windowname",flip_img)
    cv2.waitKey(0)


