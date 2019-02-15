#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd


#データ読み込みクラス
class Class_File_Data_Reader():
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
            self.target_ext = [".csv",".tsv",".xls",".xlsx",".json"]
        return

    def read_file_in_folder(self,folder_path):
        '''
        入力フォルダパス直下にあるファイルを読み込む
        各ファイルの読み込み結果(pandas dataframe)とファイル名のリストを出力
        '''
        filelist = self.get_file_path_list_in_folder(folder_path)
        result = []
        for file in filelist:
            dfdata = self.read_file_autohandle(file)
            result.append(dfdata)
        return result,filelist


    def read_file_in_folder_recrussive(self,folder_path):
        '''
        入力フォルダパスの配下(サブフォルダ含む)にあるファイルを読み込む
        各ファイルの読み込み結果(pandas dataframe)とファイル名のリストを出力
        '''
        filelist = self.get_file_path_list_in_folder_recrussive(folder_path)
        result = []
        for file in filelist:
            dfdata = self.read_file_autohandle(file)
            result.append(dfdata)
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
        if ext == ".csv":
            result = self.read_csv_data(input_path)
        elif ext == ".tsv":
            result = self.read_tsv_data(input_path)
        elif (ext == ".xls") or (ext == ".xlsx"):
            result = self.read_xls_data_firstseat(input_path)
        elif ext == ".json":
            result = self.read_json_data(input_path)
        return result


    def read_csv_data(self,filename):
        '''
        csvデータを読みとる
        '''
        result = pd.read_csv(filename, encoding="shift-jis")    #日本語データ(Shift-Jis)を含む場合を想定
        return result

    def read_tsv_data(self,filename):
        '''
        tsvデータを読みとる
        '''
        result = pd.read_table(filename, encoding="shift-jis")    #日本語データ(Shift-Jis)を含む場合を想定
        return result

    def read_xls_data_firstseat(self,filename):
        '''
        xlsx or xlsファイルの1枚目のシートを読みとる
        '''
        result = pd.read_excel(filename, encoding="shift-jis")    #日本語データ(Shift-Jis)を含む場合を想定
        return result

    def read_xls_data_allsheat(self,filename):
        '''
        xlsx or xlsファイルの全てのシートを読み込む
        '''
        result = pd.read_excel(filename, encoding="shift-jis", sheetname =None)    #日本語データ(Shift-Jis)を含む場合を想定
        return result

    def read_json_data(self,filename):
        '''
        jsonファイルを読み込む
        '''
        result = pd.read_json(filename, encoding="shift-jis")    #日本語データ(Shift-Jis)を含む場合を想定
        return result


if __name__ == '__main__':
    
    input_pass_xls = "D:\\WS\\VS_project\\BlogProject\\"

    #サブフォルダまで含めた拡張子csvのファイルを読み込み
    ReadDataFunc = Class_File_Data_Reader(ext=".csv")
    data_df, filelist = ReadDataFunc.read_file_in_folder_recrussive(input_pass_xls)

