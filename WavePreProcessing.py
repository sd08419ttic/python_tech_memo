#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd


#数値データの前処理用クラス
class Class_Wave_PreProcessing():
    '''
    各種波形データに前処理をするクラス
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''
        pass

    def get_only_required_columns(self,df_arg,req_columns):
        '''
        pandas dataframeからユーザーが指定取得対象とする列のみを取得する関数
        df_arg:データフレーム入力値、req_columns:取得対象とする列の名前を格納したlist
        '''
        df_new = df_arg[req_columns]

        return df_new

    def elim_error_data_from_df(self,df_arg):
        '''
        DataFrameから無効値を除去する df_arg:入力(DataFrame)
        '''
        #列数
        orig_columns = df_arg.columns   #入力したDFの列名
        col_num = len(df_arg.columns)   #入力したDFの列数
        df_new = df_arg.copy()          #出力用のDF

        #数値データできない値をNanに変換する処理
        for indx in range(col_num):
            temp_series = df_arg.iloc[:,indx].copy()
            temp_series =  pd.to_numeric(temp_series, errors='coerce')
            df_new = df_new.drop(orig_columns[indx],axis=1)
            df_new[orig_columns[indx]] = temp_series
            df_new[orig_columns[indx]] = temp_series.astype(float)

        #Nanの除去(列ごと)
        df_new = df_new.dropna(how='any')   #any:1つでもNanが含まれる場合に行ごと除去、all:1行全てNanである場合に行ごと除去

        return df_new 

    def fill_error_data_from_df(self,df_arg,mode="fixed",fixed_val=0):
        '''
        DataFrameから無効値を補間する mode:方式 ("fixed":固定値代入,fixed_val:固定値(デフォルト:0),"below":下の値,"above":上の値,"interpolate":上下平均)
        '''
        #列数
        orig_columns = df_arg.columns   #入力したDFの列名
        col_num = len(df_arg.columns)   #入力したDFの列数
        df_new = df_arg.copy()          #出力用のDF

        #数値データできない値をNanに変換する処理
        for indx in range(col_num):
            temp_series = df_arg.iloc[:,indx].copy()
            temp_series =  pd.to_numeric(temp_series, errors='coerce')
            df_new = df_new.drop(orig_columns[indx],axis=1)
            df_new[orig_columns[indx]] = temp_series

        if mode== "fixed":          #Nanの穴埋め(固定値)
            df_new = df_new.fillna(fixed_val)
        elif mode== "below":        #Nanの穴埋め(Nanの下にある値を代入)　※一番上のデータがNanの場合はそのまま残るので注意　2つ以上続くと続いた先の値を取得して代入
            df_new = df_new.fillna(method='ffill') 
        elif mode== "above":        #Nanの穴埋め(Nanの上にある値を代入)　※一番下のデータがNanの場合はそのまま残るので注意　2つ以上続くと続いた先の値を取得して代入
            df_new = df_new.fillna(method='bfill')
        else:                       #補間処理(Nanの下にある値を代入)　※一番上or下のデータがNanの場合はそのまま残るので注意
            df_new = df_new.interpolate()
        
        return df_new


    def clip_data_from_df_all(self,df_arg,min_val=None,max_val=None):
        '''
        DataFrameの上下限ガード (全体) min_val:最小値, max_val:最大値
        '''

        df_new = df_arg.clip(lower=min_val,upper  = max_val)

        return df_new

    def clip_data_from_df_col(self,df_arg,col_name=None,min_val=None,max_val=None):
        '''
        DataFrameの上下限ガード (特定の列のみ) col_name:列名, min_val:最小値, max_val:最大値
        '''
        df_new = df_arg

        if col_name is not None:
            temp_series = df_arg[col_name]
            temp_series = temp_series.clip(lower=min_val,upper  = max_val)
            df_new[col_name] = temp_series

        return df_new

if __name__ == '__main__':
    
    #参考としたデータ (kaggle datasetで公開されている車両センサー情報) https://www.kaggle.com/zhaopengyun/driving-data
    input_path = "D:\\WS\\VS_project\\BlogProject\\BlogProject\\data\\101a.csv"
    #引数usecolsで読み込み対象とするデータを選択 (1つでも存在しない場合はエラー)
    test_data = pd.read_csv(input_path, encoding="shift-jis", usecols=["position X", "position Y","position Z","yawAngle","pitchAngle","rollAngle"])

    wave_inst = Class_Wave_PreProcessing()
    #データから特定の列のみを選定する関数
    df_new = wave_inst.get_only_required_columns(test_data,["position X","position Y","yawAngle"])

    #欠損値・不正値を含む行を削除する処理
    df_new = wave_inst.elim_error_data_from_df(df_new)   #不正値の除去

    #欠損値・不正値を補間する処理
    df_new = wave_inst.fill_error_data_from_df(df_new,mode="fixed",fixed_val=1.0)   #固定値を代入
    #df_new = wave_inst.fill_error_data_from_df(df_new,mode="above")                 #上の値を代入
    #df_new = wave_inst.fill_error_data_from_df(df_new,mode="below")                 #下の値を代入
    #df_new = wave_inst.fill_error_data_from_df(df_new,mode="interpolate")           #上下の線形補間

    #上下限ガード (DataFrame全体)
    #df_new = wave_inst.clip_data_from_df_all(df_new,min_val=6.0)

    #上下限ガード (列指定)
    df_new = wave_inst.clip_data_from_df_col(df_new,col_name="position X",min_val=15.0,max_val=25.0)

    print(df_new.head())

