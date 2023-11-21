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

        # 第一個下拉選單
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
        # 區域事件判定
        #self.FishType_Combo.bind("<<ComboboxSelected>>", self.change_AreaVillage_Combo)

        # 第二個下拉選單
        # 第三個下拉選單
        # 第四個下拉選單


def main():
    window = Window()
    window.title("Fish")  # title
    window.resizable(0, 0)  # 禁止拖拉視窗調整視窗大小
    window.geometry("1300x500")  #視窗大小
    window.mainloop()


if __name__ == "__main__":
    main()
