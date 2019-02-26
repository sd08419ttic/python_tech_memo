#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, webbrowser
from bs4 import BeautifulSoup
import pandas as pd
from google_images_download import google_images_download
import shutil
import os
from pytube import YouTube

############################################################
# Youtube検索結果の取得処理 (下記サイトより引用)           #
# https://qiita.com/hitoribucho/items/741f0bec70fa5abe1d82 #
############################################################
class Content:
    pass

class Youtube:
    URL = 'https://www.youtube.com%s'

    @classmethod
    def url(self, path='/'):
        return self.URL % path

    @classmethod
    def url_search(self, query):
        return self.url('/results?search_query=%s') % query

    @classmethod
    def url_embed(self, vid):
        return self.url('/embed/%s') % vid

    @classmethod
    def search(self, query, num=10):
        num = min(num, 20) # 最大20件まで
        req = requests.get(self.url_search(query))
        html = req.text.encode(req.encoding).decode('utf-8', 'strict')
        soup = BeautifulSoup(html, 'html5lib')
        h3s = soup.find_all('h3', {'class': 'yt-lockup-title'})
        for h3 in h3s[:num]:
            href = h3.a.get('href')
            vid = href.split('=')[-1]
            content = Content()
            content.title = h3.a.get('title')
            content.url = self.url(href)
            content.embed = self.url_embed(vid)
            yield content
############################################################


#Google系Webサービス取得用クラス
class Class_GetGoogleWebService():

    def __init__(self):
        '''
        コンストラクタ
        '''

    def Get_GoogleWebSearch_Result(self,keyword,num=100):
        '''
        GoogleWeb検索結果と説明文の取得
        '''
        result_df = pd.DataFrame(columns=['Title','Link'] )
        title_list = []
        link_list = []

        print("Loading...")
        res = requests.get("https://google.com/search?num="+str(num)+"&q=" + " ".join(keyword))
        res.encoding = res.apparent_encoding
        res.raise_for_status()
 
        # 上位の検索結果のリンクを取得する
        soup = BeautifulSoup(res.content, "lxml")
        link_elems = soup.select('.r > a')         #タイトル・リンク
        link_elems2 = soup.select('.s > .st')      #説明文 (タイトル・リンクと一緒に表示させたかったがずれるので取得のみ)
 
        # 各結果をブラウザのタブで開く
        num_open = min(100, len(link_elems2))
        for i in range(num_open):
             tex_temp = link_elems[i].get_text()    #タイトル文字列の処理
             try:
                print(tex_temp)
             except:    #機種依存文字を含む場合はエンコード可能な文字だけを出力
                tex_temp = tex_temp.encode('cp932',"ignore")
                tex_temp = tex_temp.decode('cp932')
                print(tex_temp)

             link_temp = "https://google.com" + link_elems[i].get("href")
        
             #結果への追加
             title_list.append(tex_temp)
             link_list.append(link_temp)
             #tex_temp2 = link_elems2[i].get_text() #説明文の保存 (タイトル・リンクと一緒に表示させたかったがずれるので取得のみ)
             #try:
             #   print(tex_temp2)
             #except:    #機種依存文字を含む場合はエンコード可能な文字だけを出力
             #   tex_temp2 = tex_temp2.encode('cp932',"ignore")
             #   tex_temp2 = tex_temp2.decode('cp932')
             #   print(tex_temp2)
             #webbrowser.open("https://google.com" + link_elems[i].get("href"))

        result_df['Title'] = pd.Series(title_list)
        result_df['Link'] = pd.Series(link_list)

        return result_df


    def Get_GoogleImageSearch_Result(self,keyword,imnum=100):
        '''
        Google画像検索結果の取得 (取得した画像は実行ファイルと同じ階層のdownloadフォルダに検索ワードのフォルダを作って保存)
        '''
        imnum = int(min(99,imnum))   #100以上の場合はchrome driverの設定が必要
        target_dir =os.path.dirname(os.path.abspath(__file__))+"/downloads/"+keyword
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        response = google_images_download.googleimagesdownload()
        arguments = {"keywords":keyword,"limit":imnum,"la":"Japanese","pr":"test"}   #creating list of arguments
        response.download(arguments)
        return


    def Get_YoutubeSearch_Result(self,keyword,imnum=20):
        '''
        Youtube検索結果の取得 (取得した画像は実行ファイルと同じ階層のmovieフォルダに検索ワードのフォルダを作って保存)
        '''
        imnum = int(min(20,imnum))
        contents = list(Youtube.search(keyword, num=imnum))

        target_dir =os.path.dirname(os.path.abspath(__file__))+'/movie/'+keyword+"/"
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)

        for indx in range(len(contents)):
            tex_title = contents[indx].title.encode('cp932',"ignore")
            tex_title = tex_title.decode('cp932')
            print(tex_title)
            try:
                yt = YouTube(contents[indx].url)
                stream = yt.streams.get_by_itag(22) #MP4動画(720p)は22/ MP4音楽:140 失敗する動画はyt.streams.all()で表示後個別調整すれば取得可能
                stream.download(target_dir)
            except:
                print("error")
        return

if __name__ == '__main__':
    GetGoogleServiceFunc = Class_GetGoogleWebService()

    #Youtubeの検索結果取得 (キーワード、取得最大件数)
    GetGoogleServiceFunc.Get_YoutubeSearch_Result("dog",20)

    #Google画像検索の検索結果取得 (キーワード、取得最大件数)
    GetGoogleServiceFunc.Get_GoogleImageSearch_Result("猫",200)

    #GoogleWeb検索の検索結果取得 (キーワード、取得最大件数)
    result = GetGoogleServiceFunc.Get_GoogleWebSearch_Result("スクレイピング",30)
    result.to_csv("result.csv")
    #print(result)