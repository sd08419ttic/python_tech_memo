#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import cv2
import traceback
import sys
from pdf2image import convert_from_path

#http://blog.alivate.com.au/poppler-windows/ から取得したファイルを解凍し、binフォルダへのパスを追加
poppler_path = "D:\\WS\\VS_project\\BlogProject\\BlogProject\\poppler\\bin"
os.environ['path'] = os.environ['path']+poppler_path + ";"

#画像読み込みクラス
class Class_Image_Data_Reader():
    '''
    各種データ形式をpandasに読み込むクラス
    日本語データに対応 (Shift-JIS前提 xlsx⇒csvした日本語では使える)
    '''

    def __init__(self, ext="ALL"):
        '''
        コンストラクタ
        (読み込み対象とする拡張子を引数extで指定可能)
        '''
        if ext !="ALL":
            self.target_ext = [ ext ]
        else:
            self.target_ext = [".jpg",".jpeg",".png", ".avi", ".mp4", ".wmv",".pdf"]
        return

    def read_file_in_folder(self,folder_path):
        '''
        入力フォルダパス直下にあるファイルを読み込む
        各ファイルの読み込み結果(pandas dataframe)とファイル名のリストを出力
        '''
        filelist = self.get_file_path_list_in_folder(folder_path)
        result = []
        for file in filelist:
            imdata = self.read_file_autohandle(file)
            #読み込んだファイルがリストである場合 (動画/pdf)
            if isinstance(imdata, list):
                for img in imdata:
                    result.append(img)
            else:
                result.append(imdata)
        return result,filelist


    def read_file_in_folder_recrussive(self,folder_path):
        '''
        入力フォルダパスの配下(サブフォルダ含む)にあるファイルを読み込む
        各ファイルの読み込み結果(pandas dataframe)とファイル名のリストを出力
        '''
        filelist = self.get_file_path_list_in_folder_recrussive(folder_path)
        result = []
        for file in filelist:
            imdata = self.read_file_autohandle(file)
            #読み込んだファイルがリストである場合 (動画/pdf)
            if isinstance(imdata, list):
                for img in imdata:
                    result.append(img)
            else:
                result.append(imdata)
        return result,filelist

    def get_file_path_list_in_folder(self,folder_path):
        '''
        入力フォルダパス直下にあるファイルのリストを作成する
        '''
        if folder_path[-1] != "\\":
            folder_path = folder_path + "\\"
        file_full_path_list = []
        # Search_Current_Directry
        for file in os.listdir(folder_path):
            root, ext = os.path.splitext(file)
            for indx2 in range(len(self.target_ext)):
                if ext == self.target_ext[indx2]:
                    file_fullpath = folder_path + file
                    file_full_path_list.append(file_fullpath)
        return file_full_path_list

    def get_file_path_list_in_folder_recrussive(self,folder_path):
        '''
        入力フォルダパスの配下(サブフォルダ含む)にあるファイルのリストを作成する
        '''
        if folder_path[-1] != "\\":
            folder_path = folder_path + "\\"
        file_full_path_list = []
        for folder, subfolders, files in os.walk(folder_path):
            for indx in range(len(files)):
                root, ext = os.path.splitext(files[indx])
                for indx2 in range (len(self.target_ext)):
                    if ext == self.target_ext[indx2]:
                        file_fullpath = folder+'/'+ files[indx]
                        file_full_path_list.append(file_fullpath)
        return file_full_path_list


    def read_file_autohandle(self,input_path):
        '''
        入力ファイルから拡張子を自動判定してpandasに読み込む
        '''
        root, ext = os.path.splitext(input_path)  #拡張子の取得

        #拡張子毎に読み込みを実施
        if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp"):
            result = self.read_image_data(input_path)
        elif (ext == ".avi") or (ext == ".mp4") or (ext == ".wmv"):
            result = self.read_movie_data(input_path)
        elif (ext == ".pdf"):
            result = self.read_pdf_page(input_path)
        return result


    def read_image_data(self,filename):
        '''
        画像データを読みとる (jpg/png/bmp)
        '''
        result = cv2.imread(filename)
        return result

    def read_movie_data(self,filename):
        '''
        動画ファイルを読み込む(avi,mp4,flv)
        '''
        result_list = []
        try:
            cap = cv2.VideoCapture(filename)
            ret, frame = cap.read()             #最初のフレームを取得
        except:
            print(filename ,"could not loaded!")
            traceback.print_exc()
            return result_list

        indx = 0
        while (cap.isOpened()):
            ret, frame = cap.read()             #最初のフレームを取得
            if ret == True: #読み込み成功判定
                #img = cv2.cvtColor(frame, cv2.COLOR_BGR)
                result_list.append(frame)
                print("deb_movie",indx)
                indx = indx +1
            else:
                break
        cap.release()
        return result_list

    def read_pdf_page(self,filename):
        '''
        PDFファイルを画像として読み込む (ページを一括変換)
        '''
        result_list = []
        try:
            images = convert_from_path(filename)
            for indx in range(len(images)):
                img_temp = np.asarray(images[indx])
                img_temp = img_temp[:, :, ::-1].copy()    #RGB->BGR
                result_list.append(img_temp)
        except:
            print(filename, "could not loaded!")
            traceback.print_exc()
            result_list = null
        return result_list


if __name__ == '__main__':
    
    input_root_path = "D:\\WS\\VS_project\\BlogProject\\"

    #サブフォルダまで含めた拡張子csvのファイルを読み込み
    ReadImgFunc = Class_Image_Data_Reader()
    np_img, filelist = ReadImgFunc.read_file_in_folder_recrussive(input_root_path)

    for image in np_img:
        cv2.imshow("result",image)
        cv2.waitKey(0)

    print(filelist)

