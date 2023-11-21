import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import datasource as ds
import tkintermapview  # 地圖
import os
import base64


# 標籤
class TKLable(tk.Label):
    def __init__(self, parents, **kwargs):
        super().__init__(parents, **kwargs)
        helv26 = tkFont.Font(family="微軟正黑體", size=12, weight="bold")
        self.config(font=helv26)


# 一般按鈕
class TKButton(tk.Button):
    def __init__(self, parents, **kwargs):
        super().__init__(parents, **kwargs)
        self.config(font=("微軟正黑體", 10, "bold"))


# 主視窗設定
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="#345678")

        title = tk.Label(self, text="Fish", bg="#345678")
        titlefont = tkFont.Font(family="微軟正黑體", size=18, weight="bold")
        title.config(font=titlefont, foreground="#FFFFFF")
        title.pack(padx=10, pady=10)

        self.KeywordFrame = ttk.Frame(self, width=800, height=500)
        self.KeywordFrame.pack(fill="both", expand=True)

        mainFrame = tk.Frame(self.KeywordFrame, width=800, height=500)
        mainFrame.pack()

        TKLable(
            mainFrame,
            text="魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚魚",
            bd=3,
        ).grid(row=0, column=0, columnspan=10)

        # 原生種判定下拉選單
        TKLable(mainFrame, text="原生種判定", bd=1).grid(row=1, column=0)
        self.FishType_dict = ds.Get_FISHTYP()
        self.FishTypeValue = tk.StringVar()
        self.FishType_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishType_dict.keys()),
            justify="center",
            textvariable=self.FishTypeValue,
        )
        self.FishType_Combo.grid(row=1, column=1)
        self.FishType_Combo.current(0)
        # 下拉選單綁定Function
        self.FishType_Combo.bind("<<ComboboxSelected>>", self.update_second_combobox)

        # 年度下拉選單
        TKLable(mainFrame, text="年度", bd=1).grid(row=1, column=2)
        self.FishYear_dict = ds.Get_FISHYEAR()
        self.FishYearValue = tk.StringVar()
        self.FishYear_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishYear_dict.keys()),
            justify="center",
            textvariable=self.FishYearValue,
        )
        self.FishYear_Combo.grid(row=1, column=3)
        self.FishYear_Combo.current(0)

        # 地圖標記下拉選單
        TKLable(mainFrame, text="地圖標記", bd=1).grid(row=1, column=4)
        self.FishMap_dict = ds.Get_MAP()
        self.FishMapValue = tk.StringVar()
        self.FishMap_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishMap_dict.keys()),
            justify="center",
            textvariable=self.FishMapValue,
        )
        self.FishMap_Combo.grid(row=1, column=5)
        self.FishMap_Combo.current(0)

        # 中文名下拉選單
        TKLable(mainFrame, text="中文名", bd=3).grid(row=1, column=6)
        self.FishName_dict = ds.Get_FISHNAME()
        self.FishNameValue = tk.StringVar()
        self.FishName_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishName_dict.keys()),
            justify="center",
            textvariable=self.FishNameValue,
        )
        self.FishName_Combo.grid(row=1, column=7)
        self.FishName_Combo.current(0)

        # 搜尋按鈕
        self.keyButton = TKButton(mainFrame, text="搜尋", command=self.KeySearch)
        self.keyButton.config(width=80, border=2)

        self.keyButton.grid(row=4, column=0, columnspan=10, pady=(5, 0), sticky="nsew")

        # Map 地圖
        map_box = tk.Canvas(self.KeywordFrame) #用一個box包住Map
        map_box.pack(fill="both", expand=True, pady=10, padx=100)

        self.map_widget = tkintermapview.TkinterMapView(
            map_box, width=100, height=800, corner_radius=0
        )
        self.map_widget.pack(fill="both", expand=True, pady=5, padx=80)
        self.map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )
        #map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(
            23.623468547617622, 120.89823983585597
        )  # 設置初始座標(中部)
        self.map_widget.set_zoom(8)

    # 下拉選單連結 Function
    def update_second_combobox(self, event):
        selected_tag = self.FishType_dict[self.FishTypeValue.get()]
        # 根据第一个下拉菜单的选项更新第二个下拉菜单的选项
        filtered_names = [
            name for name, tag in self.FishName_dict.items() if tag == selected_tag
        ]
        self.FishName_Combo["values"] = filtered_names
        self.FishName_Combo.current(0)

    # 搜尋條件 未完成 下面都是錯的----------------------------------------------------------------------------
    def KeySearch(self):
        Road = ""  # 街道名稱
        Towncode01 = ""  # 行政區
        Towncode02 = ""  # 村里
        TimeStart = ""  # 抵達時間起
        TimeEnd = ""  # 抵達時間迄

        if self.Search.get() != "":
            Road = self.Search.get()
        if self.TaipeiAreaValue.get() != "全區":
            Towncode01 = self.TaipeiAreaValue.get()
        if self.AreaVillageValue.get() != "全部":
            Towncode02 = self.AreaVillageValue.get()
        if self.TimeStart.get() != "":
            TimeStart = self.TimeStart.get().replace(":", "")
        if self.TimeEnd.get() != "":
            TimeEnd = self.TimeEnd.get().replace(":", "")
        # 抵達時間不可以只輸入一個
        if self.TimeStart.get() != "" and self.TimeEnd.get() == "":
            messagebox.showwarning("請輸入欄位", "抵達時間(迄)請勿空白", parent=self.keyButton)
            return
        elif self.TimeStart.get() == "" and self.TimeEnd.get() != "":
            messagebox.showwarning("請輸入欄位", "抵達時間(起)請勿空白", parent=self.keyButton)
            return

        # print("視窗的值:",Road,Towncode01,Towncode02,TimeStart,TimeEnd)
        keydata = []
        for item in self.garbagestation_list:
            Roadcheck = False
            Towncode01check = False
            Towncode02check = False

            x = float(item["經度"])  # 25.05081974
            y = float(item["緯度"])  # 121.5438535
            address = item["地點"]  # 臺北市中山區復興北路66號
            TaipeiArea = item["行政區"]  # 中山區
            AreaVillage = item["里別"]  # 力行里
            carNum = item["車號"]  # 119-BQ
            timeS = item["抵達時間"]  # 1700
            timeE = item["離開時間"]  # 1709

            # 都沒輸入，印全部
            if (
                Road == ""
                and Towncode01 == ""
                and Towncode02 == ""
                and TimeStart == ""
                and TimeEnd == ""
            ):
                timeS = f'{item["抵達時間"][:2]}:{item["抵達時間"][2:]}'  # 1700
                timeE = f'{item["離開時間"][:2]}:{item["離開時間"][2:]}'  # 1709
                keydata.append([address, carNum, timeS, timeE, x, y])
            else:  # 根據搜尋條件來印對應資料
                Towncode01check = TaipeiArea.__contains__(Towncode01)
                Towncode02check = AreaVillage.__contains__(Towncode02)
                Roadcheck = address.__contains__(Road)

                if Towncode01check and Towncode02check and Roadcheck:
                    # 時間區間
                    if TimeStart != "":
                        if int(float(timeS)) >= int(float(TimeStart)) and int(
                            float(timeS)
                        ) <= int(float(TimeEnd)):
                            timeS = f'{item["抵達時間"][:2]}:{item["抵達時間"][2:]}'  # 1700
                            timeE = f'{item["離開時間"][:2]}:{item["離開時間"][2:]}'  # 1709
                            keydata.append([address, carNum, timeS, timeE, x, y])
                    else:
                        timeS = f'{item["抵達時間"][:2]}:{item["抵達時間"][2:]}'  # 1700
                        timeE = f'{item["離開時間"][:2]}:{item["離開時間"][2:]}'  # 1709
                        keydata.append([address, carNum, timeS, timeE, x, y])

            # LabelFrame
            if hasattr(self, "displayFrame"):
                self.displayFrame.destroy()
            self.displayFrame = ttk.LabelFrame(
                self.KeywordFrame,
                text=f"\n查詢結果({len(keydata)}筆)",
                borderwidth=2,
                relief=tk.GROOVE,
            )
            self.displayFrame.pack(fill=tk.BOTH, padx=80, pady=(0, 30))
            if len(keydata) != 0:
                # print(keydata)
                dataFrame = CustomFrame(
                    self.displayFrame, data=keydata, map_widget=self.map_widget
                )
                dataFrame.pack(side=tk.LEFT)
            else:
                TKLable(self.displayFrame, text="oops...沒有垃圾車資訊唷").pack(
                    padx=10, pady=10
                )


# ---------------------------------------------------------------------------------


def main():
    window = Window()
    window.title("Fish")  # title
    window.resizable(0, 0)  # 禁止拖拉視窗調整視窗大小
    window.geometry("1000x900")  # 視窗大小
    window.mainloop()


if __name__ == "__main__":
    main()
