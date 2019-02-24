#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd
import cv2


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

    def merge_data_simlpe(self,input_pd_list):
        '''
        最もシンプルなデータのマージ (pandas concatを使った縦方向の結合)
        '''
        result = input_pd_list[0]
        for dnameindx in range(len(input_pd_list)-1) :
            result = pd.concat([result,input_pd_list[dnameindx+1]])

        result = result.reset_index(drop=True)    #インデックスを振りなおす

        return result

    def merge_data_with_filenamecol(self,input_pd_list,fname_list):
        '''
        ファイル名を新しい列として追加するマージ
        '''
        result = input_pd_list[0]

        fname, ext = os.path.splitext( os.path.basename(fname_list[0]) )    #ファイル名/拡張子の取得
        result["file_name"] = fname
        for dnameindx in range(len(input_pd_list)-1) :
            fname, ext = os.path.splitext( os.path.basename(fname_list[dnameindx+1]) )    #ファイル名/拡張子の取得
            temp_df = input_pd_list[dnameindx+1]
            temp_df["file_name"] = fname
            result = pd.concat([result,temp_df])

        result = result.reset_index(drop=True)    #インデックスを振りなおす

        return result


    def merge_data_with_merge_only_common(self,input_pd_list,fname_list):
        '''
        一番左の列の要素をキーとして各ファイルのデータを添え字付きでマージする処理 (全てのファイルにキーが存在する行のみ表示)
        '''
        result = input_pd_list[0]
        fname, ext = os.path.splitext( os.path.basename(fname_list[0]) )    #ファイル名/拡張子の取得
        ori_columns = result.columns.tolist()
        for colindx in range(len(ori_columns)-1):
            ori_columns[colindx+1] = ori_columns[colindx+1]+"_"+fname   #列名に添え字を追加
        result.columns = ori_columns
        key_name = result.columns[0]    #一番左の列をキーとする

        for dnameindx in range(len(input_pd_list)-1) :
            fname, ext = os.path.splitext( os.path.basename(fname_list[dnameindx+1]) )    #ファイル名/拡張子の取得
            temp_df = input_pd_list[dnameindx+1]
            ori_columns = temp_df.columns.tolist()
            for colindx in range(len(ori_columns)-1):
                ori_columns[colindx+1] = ori_columns[colindx+1]+"_"+fname   #列名に添え字を追加
            temp_df.columns = ori_columns
            result = pd.merge(result,temp_df,on=key_name)
        result = result.reset_index(drop=True)    #インデックスを振りなおす

        return result

    def merge_data_with_merge_all_data(self,input_pd_list,fname_list):
        '''
        一番左の列の要素をキーとして各ファイルのデータを添え字付きでマージする処理 (キーが不在の場合はNanで表示)
        '''
        result = input_pd_list[0]
        fname, ext = os.path.splitext( os.path.basename(fname_list[0]) )    #ファイル名/拡張子の取得
        ori_columns = result.columns.tolist()
        for colindx in range(len(ori_columns)-1):
            ori_columns[colindx+1] = ori_columns[colindx+1]+"_"+fname   #列名に添え字を追加
        result.columns = ori_columns
        key_name = result.columns[0]    #一番左の列をキーとする

        for dnameindx in range(len(input_pd_list)-1) :
            fname, ext = os.path.splitext( os.path.basename(fname_list[dnameindx+1]) )    #ファイル名/拡張子の取得
            temp_df = input_pd_list[dnameindx+1]
            ori_columns = temp_df.columns.tolist()
            for colindx in range(len(ori_columns)-1):
                ori_columns[colindx+1] = ori_columns[colindx+1]+"_"+fname   #列名に添え字を追加
            temp_df.columns = ori_columns
            result = pd.merge(result,temp_df,on=key_name, how='outer')
            print(result)

        result = result.reset_index(drop=True)    #インデックスを振りなおす

        return result


if __name__ == '__main__':
    input_pass_csv = "D:\\WS\\VS_project\\BlogProject\\BlogProject\\dffolder\\nendo"

    #サブフォルダまで含めた拡張子csvのファイルを読み込み
    ReadDataFunc = Class_File_Data_Reader(ext=".csv")
    data_df, filelist = ReadDataFunc.read_file_in_folder_recrussive(input_pass_csv)

    #データのマージ (シンプルマージ)
    #merged_df = ReadDataFunc.merge_data_simlpe(data_df)

    #データのマージ (一番左の列をキーとしてマージ)
    #merged_df = ReadDataFunc.merge_data_with_merge_only_common(data_df,filelist)   #キーが全てのファイルに共通して存在する場合のみ表示
    merged_df = ReadDataFunc.merge_data_with_merge_all_data(data_df,filelist)   #存在しない値をNanとして出力


