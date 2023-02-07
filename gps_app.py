import googlemaps
import pandas as pd
import glob
import tkinter

# ウィンドウの作成
root = tkinter.Tk()
root.title('位置情報取得')
root.geometry('320x150')
root.resizable(0, 0)

def save():
    api_key = api_label_entry.get()

    #ファイルリストの取得
    flie_lists = glob.glob('*.csv')
    total_number = len(flie_lists)

    processed = 0

    # fileをひとつずつ読み込む
    for file in flie_lists:
        df = pd.read_csv(file)

        gm = googlemaps.Client(key=api_key)

        #順番に検索し，「緯度」と「経度」を分けて取得
        for i, r in df.iterrows():
            res = gm.geocode(r['都道府県']+r['市区郡']+r['町名']+str(r['丁目'])+"-"+str(r['番地'])+"-"+str(r['号']))
            df.loc[i,'緯度'] = res[0]['geometry']['location']['lat']
            df.loc[i,'経度'] = res[0]['geometry']['location']['lng']
            print(i)
            print(res[0]['geometry']['location'])

        #csv上書き
        df.to_csv(file, index=None, encoding='utf-8-sig')
        processed += 1
        progress_label.config(text=f'残りは{processed}/{total_number}です')
        progress_label.update()

        if processed is total_number:
            progress_label.config(text='取得完了')
            progress_label.update()

#APIキー入力
api_label = tkinter.Label(text='APIのキー：')
api_label.grid(row=1, column=1, padx=5, pady=5)
api_label_entry = tkinter.Entry(text='')
api_label_entry.grid(row=1, column=2, padx=5, pady=5)

#処理中
progress = tkinter.Label(text='処理状況：')
progress.grid(row=2, column=1, padx=5, pady=5)
progress_label = tkinter.Label(text='')
progress_label.grid(row=2, column=2, padx=5, pady=5)

#実行
save_button = tkinter.Button(text='取得', command=save)
save_button.grid(row=3, column=2, padx=5, pady=20, ipadx=4, ipady=4)

# ウィンドウのループ処理
root.mainloop()