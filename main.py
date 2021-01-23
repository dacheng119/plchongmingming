# -*- coding:utf-8 -*-
#
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.ttk import *
import os


def selectpath():
    """回调函数，用于返回用户选择的路径"""
    path_ = askdirectory()
    path.set(path_)


def cleanall():
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


def rename(rootdir, oldext, newext):
    """不遍历子目录，仅把当前目录的文件重命名"""
    n = 0
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
            n += 1
    text.configure(state="disabled")
    return n


def renameall(rootdir, oldext, newext):
    """遍历子目录，进行重命名"""
    n = 0
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
                n += 1
    text.configure(state="disabled")
    return n


def procrename():
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

    if not oldext.startswith(".") or not newext.startswith("."):
        showerror("错误", "原后缀和新后缀必须以圆点开始，\n例如.txt是正确的，txt是错误的！")
        return

    if bianLi.get() == "1":
        n = renameall(rootdir, oldext, newext)
    else:
        n = rename(rootdir, oldext, newext)
    text.configure(state="normal")
    text.insert("insert", "\n")
    text.insert("insert", "*** 总共重命名了%d个文件 ***" % n)
    text.configure(state="disabled")


def showhelp():
    showinfo("关于", """作者：橙子 <hebdacheng@gmail.com>
版本：2.0
版权：程序遵守GPL协议，允许任意传播
源码：https://github.com/dacheng119/plchongmingming

致谢：本程序基于Python 3.8.5，感谢Python!

程序可以遍历指定的文件夹，批量修改文件 的扩展名。
目标文件夹可以输入，也可以点击<选择文件夹>按钮进行浏览选择，如果手工输入并不区分大小写。\
扩展名指的是文件的后缀，无论原扩展名还是新扩展名，输入时都要求输入英文的圆点。\
选中递归处理后，表示既要处理目标文件夹，也要处理子文件夹中的文件。反之表示仅仅处理目标文件夹，而不会处理其子文件夹。

说明：2021年1月因新冠病毒肆虐在家隔离，为把所有的.ppsx文件重命名为.ppt文件，就编写了此程序。""")


top = Tk()
top.title("批量重命名")
top.geometry("310x500")
top.resizable(0, 0)

path = StringVar()
oldExt = StringVar()
newExt = StringVar()
bianLi = StringVar(value="1")

style = Style()
style.configure("Entry.TEntry", borderwidth=2)
style.configure("Button.TButton", borderwieth=2)

frame1 = Frame(top)
Label(frame1, text="目标文件夹").grid(row=0, column=0, sticky="w", padx=1, pady=2)
Label(frame1, text="原扩展名").grid(row=1, column=0, sticky="w", padx=1, pady=2)
Label(frame1, text="新扩展名").grid(row=2, column=0, sticky="w", padx=1, pady=2)
Entry(
    frame1,
    style="Entry.TEntry",
    textvariable=path).grid(
        row=0,
        column=1,
        padx=1,
        pady=2,
    sticky="w")
Entry(
    frame1,
    style="Entry.TEntry",
    textvariable=oldExt).grid(
        row=1,
        column=1,
        padx=1,
        pady=2,
    sticky="w")
Entry(
    frame1,
    style="Entry.TEntry",
    textvariable=newExt).grid(
        row=2,
        column=1,
        padx=1,
        pady=2,
    sticky="w")
selectBut = Button(
    frame1,
    text="选 择 (S) \n文 件 夹",
    command=selectpath,
    style="Button.TButton")
selectBut.grid(row=0, column=2, rowspan=3, padx=3, sticky="nswe")
selectBut.bind_all("<Alt-s>", lambda event: selectpath())
selectBut.bind_all("<Alt-S>", lambda event: selectpath())
frame1.grid(row=0, column=0, sticky="w", pady=2)

Checkbutton(
    top,
    text="递归处理",
    variable=bianLi).grid(
        row=1,
        column=0,
        sticky="w",
    pady=2)

frame2 = Frame(top)
sb1 = Scrollbar(frame2, orient="vertical")
sb2 = Scrollbar(frame2, orient="horizontal")
text = Text(
    frame2,
    state="disabled",
    wrap="none",
    yscrollcommand=sb1.set,
    xscrollcommand=sb2.set,
    borderwidth=2,
    width=40,
    height=24)
text.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky="w")

sb1.configure(command=text.yview)
sb2.configure(command=text.xview)
sb1.grid(row=0, column=2, sticky="nsw", padx=0)
sb2.grid(row=1, column=0, columnspan=2, sticky="we", pady=0)
frame2.grid(row=2, column=0, sticky="w", padx=2, pady=5)

frame3 = Frame(top)
okButton = Button(
    frame3,
    text="确  定(O)",
    underline=5,
    command=procrename,
    style="Button.TButton")
cleanButton = Button(
    frame3,
    text="清  除(C)",
    underline=5,
    command=cleanall,
    style="Button.TButton")
helpButton = Button(
    frame3,
    text="帮  助(H)",
    underline=5,
    command=showhelp,
    style="Button.TButton")
okButton.grid(row=0, column=0, sticky="w", padx=2)
cleanButton.grid(row=0, column=1, padx=12)
helpButton.grid(row=0, column=2, sticky="e", padx=2)
frame3.grid(row=3, column=0, sticky="w", padx=2, pady=5)

okButton.bind_all("<Alt-o>", lambda event: procrename())
okButton.bind_all("<Alt-O>", lambda event: procrename())

cleanButton.bind_all("<Alt-c>", lambda event: cleanall())
cleanButton.bind_all("<Alt-C>", lambda event: cleanall())

helpButton.bind_all("<Alt-h>", lambda event: showhelp())
helpButton.bind_all("<Alt-H>", lambda event: showhelp())

top.mainloop()
