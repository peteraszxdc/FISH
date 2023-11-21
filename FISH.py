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


# Treeview
class CustomFrame(tk.Frame):
    def __init__(self, parent, data=None, map_widget=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.list_data = data
        self.tree = ttk.Treeview(
            self, columns=["#1", "#2", "#3", "#4"], show="headings", height=10
        )
        self.tree.pack(side=tk.LEFT, padx=10)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("#1", text="地址")
        self.tree.heading("#2", text="車號")
        self.tree.heading("#3", text="抵達時間")
        self.tree.heading("#4", text="離開時間")

        self.tree.column("#1", width=300, anchor=tk.W)
        self.tree.column("#2", width=100, anchor="center")
        self.tree.column("#3", width=70, anchor="center")
        self.tree.column("#4", width=70, anchor="center")

        for item in self.list_data:
            self.tree.insert("", tk.END, values=item)

        def print_element(event):
            tree = event.widget
            curItem = tree.focus()
            address = tree.item(curItem)["values"][0]
            x = float(tree.item(curItem)["values"][4])
            y = float(tree.item(curItem)["values"][5])

            map_widget.set_position(x, y)
            map_widget.set_zoom(18)
            messagebox.showinfo("已完成", f"已將{address}定位到地圖！", parent=tree)

        self.tree.bind("<Double-1>", print_element)


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

        TKLable(mainFrame, text="以下可擇一搜尋，搜尋到的結果雙擊兩下可以到地圖區看到位置", bd=3).grid(
            row=0, column=0, columnspan=10
        )

        TKLable(mainFrame, text="原生種判定", bd=1).grid(row=1, column=0)
        self.TaipeiArea_dict = ds.Get_FISHTYP()
        self.TaipeiAreaValue = tk.StringVar()
        self.TaipeiArea_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.TaipeiArea_dict.keys()),
            justify="center",
            textvariable=self.TaipeiAreaValue,
        )
        self.TaipeiArea_Combo.grid(row=1, column=1)
        self.TaipeiArea_Combo.current(0)
        # 區域事件判定
        self.TaipeiArea_Combo.bind(
            "<<ComboboxSelected>>", self.change_AreaVillage_Combo
        )

        TKLable(mainFrame, text="年度", bd=1).grid(row=1, column=2)
        self.TaipeiArea_dict = ds.Get_FISHYEAR()
        # self.AreaVillageValue = tk.StringVar()
        self.AreaVillage_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.TaipeiArea_dict.keys()),
            justify="center",
            # textvariable=self.AreaVillageValue,
        )
        self.AreaVillage_Combo.grid(row=1, column=3)
        self.AreaVillage_Combo.current(0)

        TKLable(mainFrame, text="地圖標記", bd=1).grid(row=1, column=4)
        self.TaipeiArea_dict = ds.Get_MAP()
        # self.ScienceValue = tk.StringVar()
        self.Science_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.TaipeiArea_dict.keys()),
            justify="center",
            # textvariable=self.ScienceValue,
        )
        self.Science_Combo.grid(row=1, column=5)
        self.Science_Combo.current(0)

        TKLable(mainFrame, text="中文名", bd=3).grid(row=1, column=6)
        self.TaipeiArea_dict = ds.Get_FISHNAME()
        self.GenusValue = tk.StringVar()
        self.Genus_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.TaipeiArea_dict.keys()),
            justify="center",
            textvariable=self.GenusValue,
        )
        self.Genus_Combo.grid(row=1, column=7)
        self.Genus_Combo.current(0)

        self.keyButton = TKButton(mainFrame, text="搜尋", command=self.KeySearch)
        self.keyButton.config(width=80, border=2)

        self.keyButton.grid(row=4, column=0, columnspan=10, pady=(5, 0), sticky="nsew")

    def change_AreaVillage_Combo(self, event):
        towncode01 = self.TaipeiArea_dict[self.TaipeiAreaValue.get()]
        value = ds.Get_AreaVillage(towncode01)
        self.AreaVillage_Combo.config(values=value)
        self.AreaVillage_Combo.current(0)

    def KeySearch(self):
        Road = ""
        Towncode01 = ""
        Towncode02 = ""
        TimeStart = ""
        TimeEnd = ""
        Science = ""
        Genus = ""
        Species = ""

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
        if self.ScienceValue.get() != "全部":
            Science = self.ScienceValue.get()
        if self.GenusValue.get() != "全部":
            Genus = self.GenusValue.get()
        if self.SpeciesValue.get() != "全部":
            Species = self.SpeciesValue.get()

        if self.TimeStart.get() != "" and self.TimeEnd.get() == "":
            messagebox.showwarning("請輸入欄位", "抵達時間(迄)請勿空白", parent=self.keyButton)
            return
        elif self.TimeStart.get() == "" and self.TimeEnd.get() != "":
            messagebox.showwarning("請輸入欄位", "抵達時間(起)請勿空白", parent=self.keyButton)
            return

        keydata = []
        for item in self.garbagestation_list:
            Roadcheck = False
            Towncode01check = False
            Towncode02check = False
            Sciencecheck = False
            Genuscheck = False
            Speciescheck = False

            x = float(item["經度"])
            y = float(item["緯度"])
            address = item["地點"]
            TaipeiArea = item["行政區"]
            AreaVillage = item["里別"]
            carNum = item["車號"]
            timeS = item["抵達時間"]
            timeE = item["離開時間"]
            science = item.get("科", "")
            genus = item.get("屬", "")
            species = item.get("種", "")

            if (
                Road == ""
                and Towncode01 == ""
                and Towncode02 == ""
                and TimeStart == ""
                and TimeEnd == ""
                and Science == ""
                and Genus == ""
                and Species == ""
            ):
                timeS = f'{item["抵達時間"][:2]}:{item["抵達時間"][2:]}'
                timeE = f'{item["離開時間"][:2]}:{item["離開時間"][2:]}'
                keydata.append([address, carNum, timeS, timeE, x, y])
            else:
                Towncode01check = TaipeiArea.__contains__(Towncode01)
                Towncode02check = AreaVillage.__contains__(Towncode02)
                Roadcheck = address.__contains__(Road)
                Sciencecheck = science.__contains__(Science)
                Genuscheck = genus.__contains__(Genus)
                Speciescheck = species.__contains__(Species)

                if (
                    Towncode01check
                    and Towncode02check
                    and Roadcheck
                    and Sciencecheck
                    and Genuscheck
                    and Speciescheck
                ):
                    if TimeStart != "":
                        if int(float(timeS)) >= int(float(TimeStart)) and int(
                            float(timeS)
                        ) <= int(float(TimeEnd)):
                            timeS = f'{item["抵達時間"][:2]}:{item["抵達時間"][2:]}'
                            timeE = f'{item["離開時間"][:2]}:{item["離開時間"][2:]}'
                            keydata.append([address, carNum, timeS, timeE, x, y])
                    else:
                        timeS = f'{item["抵達時間"][:2]}:{item["抵達時間"][2:]}'
                        timeE = f'{item["離開時間"][:2]}:{item["離開時間"][2:]}'
                        keydata.append([address, carNum, timeS, timeE, x, y])

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
            dataFrame = CustomFrame(
                self.displayFrame, data=keydata, map_widget=self.map_widget
            )
            dataFrame.pack(side=tk.LEFT)
        else:
            TKLable(self.displayFrame, text="oops...沒有垃圾車資訊唷").pack(padx=10, pady=10)


def main():
    window = Window()
    window.title("Fish")
    window.resizable(0, 0)
    window.geometry("1300x500")
    window.mainloop()


if __name__ == "__main__":
    main()
