#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import animatplot as amp

#グラフの描画
def plot_animation(ref_df):
    #X軸・Y軸のデータ取得
    X_data = 0
    Y_data = 0
    #refの経路描画
    time_data_np = np.array(ref_df["time"])
    x_np = np.array(ref_df["x"])
    y_np = np.array(ref_df["y"])
    sensor_1_np = np.array(ref_df["sensor1"])
    sensor_2_np = np.array(ref_df["sensor2"])
    sensor_3_np = np.array(ref_df["sensor3"])

    Xs_log =np.asarray([x_np[t:t+10] for t in range(len(time_data_np)-10)]) #X軸データ × 時間軸 分の配列
    Ys_log =[y_np[t:t+10] for t in range(len(time_data_np)-10)]             #Y軸データ × 時間軸 分の配列
    sensor_1_log =[sensor_1_np[t:t+10] for t in range(len(time_data_np)-10)]
    sensor_2_log =[sensor_2_np[t:t+10] for t in range(len(time_data_np)-10)]
    sensor_3_log =[sensor_3_np[t:t+10] for t in range(len(time_data_np)-10)]
    Time_log =np.asarray([time_data_np[t:t+10] for t in range(len(time_data_np)-10)])

    #subplotの描画 (X-Yの情報を3行分の画面で表示)
    ax1 = plt.subplot2grid((3,2), (0,0), rowspan=3)
    ax2 = plt.subplot2grid((3,2), (0,1))
    ax3 = plt.subplot2grid((3,2), (1,1))
    ax4 = plt.subplot2grid((3,2), (2,1))

    ax1.set_xlim([x_np.min(), x_np.max()])      #描画範囲の設定
    ax1.set_ylim([y_np.min(),y_np.max()])       #描画範囲の設定
    block = amp.blocks.Scatter(Xs_log, Ys_log,label="X_Y",ax=ax1)

    block2 = amp.blocks.Line(Time_log, sensor_1_log, label="sensor1",ax=ax2)
    block3 = amp.blocks.Line(Time_log, sensor_2_log, label="sensor2",ax=ax3)
    block4 = amp.blocks.Line(Time_log, sensor_3_log, label="sensor3",ax=ax4)

    ax2.set_xlim([time_data_np.min(), time_data_np.max()])    #描画範囲の設定
    ax2.set_ylim([sensor_1_np.min(),sensor_1_np.max()])       #描画範囲の設定
    ax3.set_xlim([time_data_np.min(), time_data_np.max()])    #描画範囲の設定
    ax3.set_ylim([sensor_1_np.min(),sensor_1_np.max()])       #描画範囲の設定
    ax4.set_xlim([time_data_np.min(), time_data_np.max()])    #描画範囲の設定
    ax4.set_ylim([sensor_1_np.min(),sensor_1_np.max()])       #描画範囲の設定
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    plt.subplots_adjust(wspace=0.4, hspace=0.6)

    anim = amp.Animation([block,block2,block3,block4])
    anim.controls()
    anim.save_gif("result")
    plt.show()


if __name__ == '__main__':
    
    csv_file_path = "data\\plotdata.csv"

    #CSVの読み込み
    ref_df = pd.read_csv(csv_file_path, encoding="utf-8-sig")    #日本語データ(Shift-Jis)を含む場合を想定
    plot_animation(ref_df)

    print("finished!")
