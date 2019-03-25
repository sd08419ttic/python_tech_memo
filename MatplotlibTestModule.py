#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#波形データのGUI(Matplotlib)
def matplotlib_gui_example():
    #sns.set()
    X = np.linspace(-10, 10, 100)
    Y1 = np.sin(X) # サインの値を計算する
    Y2 = np.cos(X)
    Y3 = np.tan(X)

    #plot関数のテスト
    fig = plt.figure()              #新規フィギュア(Window)の描画
    fig.canvas.set_window_title('My title')     #Windowタイトルの設定
    fig.suptitle("Figure Title")                #Figureタイトルの設定
    fig.patch.set_facecolor('xkcd:mint green')  #Figure背景色の設定

    #折れ線グラフの表示
    #https://pythondatascience.plavox.info/matplotlib/%E6%8A%98%E3%82%8C%E7%B7%9A%E3%82%B0%E3%83%A9%E3%83%95
    ax = fig.add_subplot(2,2,1)     #subplotの追加 (行/列/描画対象インデックス)
    ax.plot(X,Y1, color='black',  linestyle='solid')        #サブプロット1の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.plot(X,Y1+0.5, color='black',  linestyle='dashed')   #サブプロット1の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.plot(X,Y1+1, color='black', linestyle='dashdot')     #サブプロット1の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.set_title('First plot')  #サブプロットタイトルの表示
    ax.set_xlabel('X')          #X軸説明文の表示
    ax.set_ylabel('Y1(sin)')    #Y軸説明文の表示
    ax.grid(True)   #Gridの表示

    #散布図の描画例
    #https://pythondatascience.plavox.info/matplotlib/%E6%95%A3%E5%B8%83%E5%9B%B3
    ax2 = fig.add_subplot(2,2,2)     #subplotの追加 (行/列/描画対象インデックス)
    ax2.scatter(X,Y2,marker="*",s=5.0,label='Y2(cos)')          #散布図1の描画 (sは点の大きさ、labelは凡例用)
    ax2.scatter(X,Y2+0.5,marker="o",s=10.0,label='Y2(cos)+0.5') #散布図2の描画 (sは点の大きさ、labelは凡例用)
    ax2.scatter(X,Y2+1,marker=".",s=1.0,label='Y2(cos)+1.0')    #散布図3の描画 (sは点の大きさ、labelは凡例用)
    ax2.set_title('Second plot')    #サブプロットタイトルの表示
    ax2.set_xlabel('X')             #X軸説明文の表示
    ax2.set_ylabel('Y2(cos)')       #Y軸説明文の表示
    ax2.legend(loc="upper right")   #凡例の表示 (locで表示位置を設定可)
    ax2.set_facecolor('lightyellow')
    fig.tight_layout()              #subplot表示位置の調整
    fig.subplots_adjust(top=0.9)

    #棒グラフの描画
    ax3 = fig.add_subplot(2,2,3)     #subplotの追加 (行/列/描画対象インデックス)
    ax3.bar(X, Y3,width=0.2)
    ax3.set_title('Third plot')  #サブプロットタイトルの表示
    ax3.set_xlabel('X')          #X軸説明文の表示
    ax3.set_ylabel('Y3(tan)')    #Y軸説明文の表示
    #データラベルの描画
    for indx in range(0,Y3.shape[0],20):
            print( Y3[indx])
            ax3.annotate('{:.2f}'.format(Y3[indx]), xy=(X[indx], Y3[indx]))


    plt.tight_layout()
    plt.show()


#波形データのGUI(Matplotlib)
def matplotlib_gui_example2():
    X = np.linspace(-10, 10, 100)
    Y1 = np.sin(X) # サインの値を計算する
    Y2 = np.cos(X)
    Y3 = np.tan(X)

    #plot関数のテスト
    fig = plt.figure()              #新規フィギュア(Window)の描画
    fig.canvas.set_window_title('My title') #Windowタイトルの設定
    fig.suptitle("Figure Title")    #フィギュアタイトルの設定

    #折れ線グラフの表示
    #https://pythondatascience.plavox.info/matplotlib/%E6%8A%98%E3%82%8C%E7%B7%9A%E3%82%B0%E3%83%A9%E3%83%95
    ax = fig.add_subplot(2,1,1)     #subplotの追加 (行/列/描画対象インデックス)
    ax.plot(X,Y1, color='black',  linestyle='solid')        #サブプロット1の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.plot(X,Y1+0.5, color='black',  linestyle='dashed')   #サブプロット2の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.plot(X,Y1+1, color='black', linestyle='dashdot')     #サブプロット3の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.set_title('First plot')  #サブプロットタイトルの表示
    ax.set_xlabel('X')          #X軸説明文の表示
    ax.set_ylabel('Y1(sin)')    #Y軸説明文の表示
    ax.grid(True)   #Gridの表示



    #散布図の描画例
    #https://pythondatascience.plavox.info/matplotlib/%E6%95%A3%E5%B8%83%E5%9B%B3
    ax2 = fig.add_subplot(2,1,2)     #subplotの追加 (行/列/描画対象インデックス)
    ax2.scatter(X,Y2,marker="*",s=5.0,label='Y2(cos)')          #散布図1の描画 (sは点の大きさ、labelは凡例用)
    ax2.scatter(X,Y2+0.5,marker="o",s=10.0,label='Y2(cos)+0.5') #散布図2の描画 (sは点の大きさ、labelは凡例用)
    ax2.scatter(X,Y2+1,marker=".",s=1.0,label='Y2(cos)+1.0')    #散布図3の描画 (sは点の大きさ、labelは凡例用)
    ax2.set_title('Second plot')    #サブプロットタイトルの表示
    ax2.set_xlabel('X')             #X軸説明文の表示
    ax2.set_ylabel('Y2(cos)')       #Y軸説明文の表示
    ax2.legend(loc="upper right")   #凡例の表示 (locで表示位置を設定可)
    fig.tight_layout()              #subplot表示位置の調整
    fig.subplots_adjust(top=0.9)

    fig2 = plt.figure()              #新規フィギュア(Window)の描画
    ax3 = fig2.add_subplot(1,1,1)     #subplotの追加 (行/列/描画対象インデックス)
    ax3.bar(X, Y3,width=0.2)
    ax3.set_title('First plot')  #サブプロットタイトルの表示
    ax3.set_xlabel('X')          #X軸説明文の表示
    ax3.set_ylabel('Y1(sin)')    #Y軸説明文の表示
    plt.tight_layout()
    plt.show()


#波形データのGUI(Seaborn)
def seaborn_gui_example():
    sns.set()
    X = np.linspace(-10, 10, 100)
    Y1 = np.sin(X) # サインの値を計算する
    Y2 = np.cos(X)
    Y3 = np.tan(X)

    #plot関数のテスト
    fig = plt.figure()              #新規フィギュア(Window)の描画
    fig.canvas.set_window_title('My title') #Windowタイトルの設定
    fig.suptitle("Figure Title")    #フィギュアタイトルの設定

    #折れ線グラフの表示
    #https://pythondatascience.plavox.info/matplotlib/%E6%8A%98%E3%82%8C%E7%B7%9A%E3%82%B0%E3%83%A9%E3%83%95
    ax = fig.add_subplot(2,1,1)     #subplotの追加 (行/列/描画対象インデックス)
    
    sns.pointplot(X,Y1, color='black', scale= 0.1, linestyles ='solid',ax= ax)        #サブプロット1の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    sns.pointplot(X,Y1+0.5, color='black', scale= 0.1, linestyles ='dashed',ax= ax)   #サブプロット2の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    sns.pointplot(X,Y1+1, color='black',scale= 0.1, linestyles ='dashdot',ax= ax)     #サブプロット3の描画 (折れ線グラフ colorは色,linestyleは線のタイプ)
    ax.set_title('First plot')  #サブプロットタイトルの表示
    ax.set_xlabel('X')          #X軸説明文の表示
    ax.set_ylabel('Y1(sin)')    #Y軸説明文の表示

    #軸の体裁を整える
    ax.set_xticks([])   #軸目盛の消去

    ax.grid(True)   #Gridの表示


    #散布図の描画例
    #https://pythondatascience.plavox.info/matplotlib/%E6%95%A3%E5%B8%83%E5%9B%B3
    ax2 = fig.add_subplot(2,1,2)     #subplotの追加 (行/列/描画対象インデックス)
    sns.regplot(X,Y2,marker="*",label='Y2(cos)',fit_reg=False,ax = ax2)          #散布図1の描画 fit_reg Falseで散布図のみ表示
    sns.regplot(X,Y2+0.5,marker="o",label='Y2(cos)+0.5',order = 20,scatter=False, ax = ax2) #散布図2の描画 (sは点の大きさ、labelは凡例用)
    sns.regplot(X,Y2+1,marker=".",label='Y2(cos)+1.0',order = 25, ax = ax2)    #散布図3の描画 (sは点の大きさ、labelは凡例用)
    ax2.set_title('Second plot')    #サブプロットタイトルの表示
    ax2.set_xlabel('X')             #X軸説明文の表示
    ax2.set_ylabel('Y2(cos)')       #Y軸説明文の表示
    ax2.legend(loc="upper right")   #凡例の表示 (locで表示位置を設定可)
    fig.tight_layout()              #subplot表示位置の調整

    fig2 = plt.figure()              #新規フィギュア(Window)の描画
    ax3 = fig2.add_subplot(1,1,1)     #subplotの追加 (行/列/描画対象インデックス)
    ax3.bar(X, Y3,width=0.2)
    ax3.set_title('First plot')  #サブプロットタイトルの表示
    ax3.set_xlabel('X')          #X軸説明文の表示
    ax3.set_ylabel('Y3(tan)')    #Y軸説明文の表示
    plt.show()



#波形データのGUI(Plotly)
def plotly_gui_example():
    pass


#波形データのGUI(Matplotlib)
def matplotlib_gui_fig_sub():

    #plot関数のテスト
    fig = plt.figure()              #新規フィギュア(Window)の描画
    fig.canvas.set_window_title('My title')     #Windowタイトルの設定
    fig.suptitle("Figure Title")                #Figureタイトルの設定
    fig.patch.set_facecolor('xkcd:mint green')  #Figure背景色の設定

    #折れ線グラフの表示
    ax = fig.add_subplot(2,2,1)     #subplotの追加 (行/列/描画対象インデックス)
    ax.set_title('First plot')  #サブプロットタイトルの表示
    ax.set_xlabel('X')          #X軸説明文の表示
    ax.set_ylabel('Y1')    #Y軸説明文の表示
    ax.grid(True)   #Gridの表示

    #散布図の描画例
    ax2 = fig.add_subplot(2,2,2)     #subplotの追加 (行/列/描画対象インデックス)
    ax2.set_title('Second plot')    #サブプロットタイトルの表示
    ax2.set_xlabel('X')             #X軸説明文の表示
    ax2.set_ylabel('Y2')       #Y軸説明文の表示
    ax2.legend(loc="upper right")   #凡例の表示 (locで表示位置を設定可)
    ax2.set_facecolor('lightyellow')
    fig.subplots_adjust(top=0.9)

    #棒グラフの描画
    ax3 = fig.add_subplot(2,2,3)     #subplotの追加 (行/列/描画対象インデックス)
    ax3.set_title('Third plot')  #サブプロットタイトルの表示
    ax3.set_xlabel('X')          #X軸説明文の表示
    ax3.set_ylabel('Y3')    #Y軸説明文の表示
    fig.tight_layout()              #subplot表示位置の調整
    plt.show()










if __name__ == '__main__':
    matplotlib_gui_example()


