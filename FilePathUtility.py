#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import datetime
import re

#ファイルパスユーティリティ
class Class_FilePathUtility():
    '''
    ファイルパス機能に関するユーティリティ
    '''
    def __init__(self, ext="ALL"):
        '''
        コンストラクタ
        (デフォルトは全ての拡張子のファイルを探索：読み込み対象とする拡張子を引数extで指定可能)
        '''
        if ext !="ALL":
            if ext[0] != ".":
                ext = "." + ext #先頭に.を付与する
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

    def check_filename_regexp(self,filefullpathlist,pattern=None):
        '''
        ファイル命名則のチェック (正規表現)
        filefullpathlist:ファイルパスのリスト、pattern：正規表現パターン
        '''
        result_path_list = []

        for pathname in filefullpathlist:
            #ファイル名の抽出
            fname, ext = os.path.splitext( os.path.basename(pathname) )    #ファイル名/拡張子の取得

            if pattern is not None:
                result = re.match(pattern,fname)   #re.search:途中も含めた検索、re.match:先頭からの完全一致
            else:
                result = True                       #正規表現パターンを何も設定していないときは元のパスをすべて出力する
            if result:
                result_path_list.append(pathname)
        return result_path_list

    def check_file_create_date(self,filefullpathlist,mode="A", cdate = 0):
        '''
        各ファイルの作成日時が指定した日以前であるかをチェックする
        mode:A (検索日時以降に作成) :B (検索日時以前に作成))、cdate:日時 例：2018/06/06
        '''

        result_path_list = []
        conditon_dt = datetime.datetime.strptime(cdate, '%Y/%m/%d')

        for pathname in filefullpathlist:
            #作成日時
            create_time = os.path.getctime(pathname)
            create_time_dt = datetime.datetime.fromtimestamp(create_time)
            create_time_str = create_time_dt.strftime('%Y/%m/%d  %H:%M:%S')

            if mode == "A":   #ファイル作成日時の比較 (検索条件日時以前に作成)
                if conditon_dt < create_time_dt:
                    result_path_list.append(pathname)
            elif mode == "B": #ファイル作成日時の比較 (検索条件日時以後に作成)
                if conditon_dt > create_time_dt:
                    result_path_list.append(pathname)
        return result_path_list

    def check_file_update_date(self,filefullpathlist,mode="A", cdate = 0):
        '''
        各ファイルの更新日時が指定した日以前であるかをチェックする
        mode:A (検索日時以降に更新) :B (検索日時以前に更新))、cdate:日時 例：2018/06/06
        '''
        result_path_list = []
        conditon_dt = datetime.datetime.strptime(cdate, '%Y/%m/%d')

        for pathname in filefullpathlist:
            #更新日時の取得
            update_time = os.path.getmtime(pathname)
            update_time_dt = datetime.datetime.fromtimestamp(update_time)
            update_time_str = update_time_dt.strftime('%Y/%m/%d  %H:%M:%S')

            if mode == "A":   #ファイル作成日時の比較 (検索条件日時以前に更新)
                if conditon_dt < update_time_dt:
                    result_path_list.append(pathname)
            elif mode == "B": #ファイル作成日時の比較 (検索条件日時以後に更新)
                if conditon_dt > update_time_dt:
                    result_path_list.append(pathname)
        return result_path_list

    def check_file_access_date(self,filefullpathlist,mode="A", cdate = 0):
        '''
        各ファイルのアクセス日時が指定した日以前であるかをチェックする
        mode:A (検索日時以降にアクセス) :B (検索日時以前にアクセス))、cdate:日時 例：2018/06/06
        '''
        result_path_list = []
        conditon_dt = datetime.datetime.strptime(cdate, '%Y/%m/%d')

        for pathname in filefullpathlist:
            #アクセス日時の取得
            acces_time = os.path.getatime(pathname)
            acces_time_dt = datetime.datetime.fromtimestamp(acces_time)
            acces_time_str = acces_time_dt.strftime('%Y/%m/%d  %H:%M:%S')

            if mode == "A":   #アクセス日時の比較 (検索条件日時以前にアクセス)
                if conditon_dt < acces_time_dt:
                    result_path_list.append(pathname)
            elif mode == "B": #アクセス日時の比較 (検索条件日時以後にアクセス)
                if conditon_dt > acces_time_dt:
                    result_path_list.append(pathname)
        return result_path_list

    def check_file_size(self,filefullpathlist,mode="S", csize = 0):
        '''
        各ファイルが指定したサイズ(KB)と比較して条件を満たすか判断する
        mode:S (指定したサイズより小さい) :L (指定したサイズより小さい)、csize:ファイルサイズ(KB)
        '''
        result_path_list = []
        for pathname in filefullpathlist:
            #サイズの取得　(KB)
            file_size  = os.path.getsize(pathname)

            if mode == "S": #サイズの比較 (小さい)
                if file_size < csize:
                    result_path_list.append(pathname)
            elif mode == "L": #サイズの比較 (大きい)
                if file_size > csize:
                    result_path_list.append(pathname)
        return result_path_list

    def get_file_detai_info(self,filefullpathlist):
        '''
        各ファイルの詳細情報(タイムスタンプ、サイズ)情報を取得 (結果をDataFrame形式で返す)
        filefullpathlist：ファイルのフルパスリスト
        '''
        result_df = pd.DataFrame(np.zeros([len(filefullpathlist), 5]), columns=['path', 'create_date', 'access_date','update_date','size'])
        indx_num =0
        for pathname in filefullpathlist:
            #result_df['path'][indx_num] = pathname
            result_df.loc[indx_num,'path'] = pathname

            #作成日時
            create_time = os.path.getctime(pathname)
            create_time_dt = datetime.datetime.fromtimestamp(create_time)
            create_time_str = create_time_dt.strftime('%Y/%m/%d  %H:%M:%S')
            result_df.loc[indx_num,'create_date'] = create_time_str

            #アクセス日時の取得
            acces_time = os.path.getatime(pathname)
            acces_time_dt = datetime.datetime.fromtimestamp(acces_time)
            acces_time_str = acces_time_dt.strftime('%Y/%m/%d  %H:%M:%S')
            result_df.loc[indx_num,'access_date'] = acces_time_str

            #更新日時の取得
            update_time = os.path.getmtime(pathname)
            update_time_dt = datetime.datetime.fromtimestamp(update_time)
            update_time_str = update_time_dt.strftime('%Y/%m/%d  %H:%M:%S')
            result_df.loc[indx_num,'update_date'] = update_time_str

            #サイズの取得　(KB)
            file_size  = os.path.getsize(pathname)
            result_df.loc[indx_num,'size'] = file_size

            #出力結果の表示
            print(create_time_str,acces_time_str,acces_time_str,file_size)
            indx_num = indx_num + 1
        return result_df


if __name__ == '__main__':
    
    #folder_path 
    input_pass = "D:\\WS\\VS_project\\BlogProject\\"

    filpath_inst = Class_FilePathUtility(".csv")
    filepathlist = filpath_inst.get_file_path_list_in_folder_recrussive(input_pass)
    #filelist_new = filpath_inst.check_filename_regexp(filepathlist,'.*0')  #ファイル命名則のチェック
    #filelist_new = filpath_inst.check_file_create_date(filepathlist,"B",'2018/08/04')   #作成日時のチェック
    #filelist_new = filpath_inst.check_file_access_date(filepathlist,"B",'2020/08/04')  #アクセス日時のチェック
    #filelist_new = filpath_inst.check_file_update_date(filepathlist,"A",'2019/01/04')  #更新日時のチェック
    filelist_new = filpath_inst.check_file_size(filepathlist,"S",200) #ファイルサイズのチェック
    print(filelist_new)
    


