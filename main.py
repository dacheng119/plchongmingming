# -*- coding:utf-8 -*-
#
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
# from tkinter.ttk import *
import os


def selectpath(event):
    """回调函数，用于返回用户选择的路径"""
    path_ = askdirectory()
    path.set(path_)


def cleanall(event):
    """清除所有的Entry和text的内容"""
    path.set("")
    oldExt.set("")
    newExt.set("")
    text.configure(state="normal")
    text.delete(1.0, "end")
    text.configure(state="disabled")


def cleantext():
    """清除text的内容"""
    text.configure(state="normal")
    text.delete(1.0, "end")
    text.configure(state="disabled")


def showhelp(event):
    """向Text输出本帮助信息"""
    helpInfo = """程序可以遍历指定的文件夹，对其中的文件批量修改其扩展名。

目标文件夹可以使用C:/DIR1/DIR2的形式手工输入，也可以点击选择目标文件夹按钮进行浏览选择,如果手工输入并不区分大小写。

扩展名指的是原文件的后缀，如wechat.jpg文件的扩展名是.jpg。原扩展名指的是现有的、待修改的扩展名，而新扩展名指的是重命名后的扩展名。\
无论原扩展名还是新扩展名，在输入时都要求输入圆点。

选中递归处理后，表示既要处理目标文件夹，也要处理子文件夹中的文件。反之表示仅仅处理目标文件夹，而不会处理其子文件夹。

在提供目标文件夹、原扩展名和新扩展名后，点击确认按钮,马上开始进行批量重命名，处理的结果会输出到屏幕上。如果点击清除按钮，\
表示要清空所有输入或选择的内容。点击帮助按钮会显示本帮助，双击内容可以看到更多的信息。
"""
    cleantext()
    text.configure(state="normal")
    text.insert("insert", helpInfo)
    text.configure(state="disabled")


def rename(rootdir, oldext, newext):
    """不遍历子目录，仅把当前目录的文件重命名"""
    text.configure(state="normal")
    root, dirs, files = next(os.walk(rootdir))
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == oldext:
            newName = filename + newext
            oldFile = os.path.join(root, file)
            newFile = os.path.join(root, newName)
            os.rename(oldFile, newFile)
            text.insert("insert", "{} -> {}\n\n".format(file, newName))
    text.configure(state="disabled")


def renameall(rootdir, oldext, newext):
    """遍历子目录，进行重命名"""
    text.configure(state="normal")
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            fileName, ext = os.path.splitext(file)
            if ext == oldext:
                newName = fileName + newext
                oldFile = os.path.join(root, file)
                newFile = os.path.join(root, newName)
                os.rename(oldFile, newFile)
                text.insert("insert", "{} -> {}\n\n".format(file, newName))
    text.configure(state="disabled")


def procrename(event):
    """批量重命名"""
    cleantext()
    rootdir = path.get()
    oldext = oldExt.get()
    newext = newExt.get()
    if rootdir == "" or oldext == "" or newext == "":
        showerror("错误", "目标文件夹、原后缀、新后缀\n都不能为空！")
        return

    if not os.path.exists(rootdir):
        showerror("错误", "文件夹{}不存在！".format(rootdir))
        return

    if not os.path.isdir(rootdir):
        showerror("错误", "{}不是一个文件夹！".format(rootdir))
        return

    if "\\" in rootdir:
        showerror("错误", "考虑到跨平台应用，你应该使用C:/DIR1/DIR2的形式！")

    if not oldext.startswith(".") or not newext.startswith("."):
        showerror("错误", "原后缀和新后缀必须以圆点开始，\n例如.txt是正确的，txt是错误的！")
        return

    if bianLi.get() == "1":
        renameall(rootdir, oldext, newext)
    else:
        rename(rootdir, oldext, newext)


def showabout(event):
    showinfo("About", """作者：橙子 <hebdacheng@gmail.com>
版本：1.0
版权：程序遵守GPL协议，允许任意传播。源码放在https://github.com/dacheng119/plchongmingming
致谢：本程序基于Python 3.8.5，感谢Python，感谢PyCharm!
说明：2021年1月，因新冠病毒肆虐在家隔离。无聊中完成此程序,希望能给大家带来一些便利！""")



top = Tk()
top.title("批量重命名")
top.geometry("350x500")
top.resizable(0, 0)

path = StringVar()
oldExt = StringVar()
newExt = StringVar()
bianLi = StringVar(value="1")

Label(top, text="目标文件夹").grid(row=0, column=0, pady=5, sticky="w")
Entry(top, textvariable=path, borderwidth=2).grid(row=0, column=1, pady=5)
selectButton=Button(top, text="选择目标\n\n文件夹(S)", underline=10, fg="green", font=("黑体", 12, "bold"), borderwidth=2, command=selectpath)
selectButton.grid(row=0, column=2, rowspan=3, sticky="n" + "s" + "w" + "e", padx=2, pady=5)
selectButton.bind("<Button-1>", selectpath)
selectButton.bind_all("<Alt-s>", selectpath)
selectButton.bind_all("<Alt-S>", selectpath)

Label(top, text="原扩展名").grid(row=1, column=0, sticky="w", pady=5)
Entry(top, borderwidth=2, textvariable=oldExt).grid(row=1, column=1, pady=5)
Label(top, text="新扩展名").grid(row=2, column=0, sticky="w", pady=5)
Entry(top, borderwidth=2, textvariable=newExt).grid(row=2, column=1, pady=5)
Checkbutton(top, text="递归处理", variable=bianLi).grid(row=3, sticky="w", pady=5)

sb1 = Scrollbar(top, orient="vertical")
# sb2 = Scrollbar(top,orient="horizontal")
text = Text(
    top,
    state="disabled",
    yscrollcommand=sb1.set,
    # xscrollcommand=sb2.set,
    borderwidth=2,
    width=40,
    height=24)
text.grid(row=4, column=0, columnspan=3, padx=0, pady=5)
text.bind("<Double-Button-1>", showabout)

sb1.configure(command=text.yview)
# sb2.configure(command=text.xview)
sb1.grid(row=4, column=3, sticky="ns", padx=0)
# sb2.grid(row=5,column=0,columnspan=3,sticky="we",pady=0)

okButton=Button(top, text="确  定(O)", underline=5)# command=procrename)
okButton.grid(row=6, column=0, sticky="e", ipadx=10)
okButton.bind_all("<Alt-o>", procrename)
okButton.bind_all("<Alt-O>", procrename)
okButton.bind("<Button-1>", procrename)

cleanButton = Button(top, text="清  除(C)", underline=5)
cleanButton.grid(row=6, column=1, ipadx=10)
cleanButton.bind_all("<Alt-c>", cleanall)
cleanButton.bind_all("<Alt-C>", cleanall)
cleanButton.bind("<Button-1>", cleanall)

helpButton = Button(top, text="帮  助(H)", underline=5)
helpButton.grid(row=6, column=2, sticky="w", ipadx=10)
helpButton.bind_all("<Alt-h>", showhelp)
helpButton.bind_all("<Alt-H>", showhelp)
helpButton.bind("<Button-1>", showhelp)
top.mainloop()
