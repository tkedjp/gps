import googlemaps
import pandas as pd
import glob

#ファイルリストの取得
flie_lists = glob.glob('*.csv')

# fileをひとつずつ読み込む
for file in flie_lists:
    df = pd.read_csv(file) #エラー

    gm = googlemaps.Client(key='')

    #順番に検索し，「緯度」と「経度」を分けて取得
    for i, r in df.iterrows():
        res = gm.geocode(r['都道府県']+r['市区郡']+r['町名']+str(r['丁目'])+"-"+str(r['番地'])+"-"+str(r['号']))
        df.loc[i,'緯度'] = res[0]['geometry']['location']['lat']
        df.loc[i,'経度'] = res[0]['geometry']['location']['lng']
        print(i)
        print(res[0]['geometry']['location'])

    #csv上書き
    # df.to_csv(file, index=None, encoding='shift_jis')
    df.to_csv(file, index=None, encoding='utf-8-sig')