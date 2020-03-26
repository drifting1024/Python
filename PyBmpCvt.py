#!/usr/bin/python

import os
import glob
import shutil
#import linecache
import tkinter

##########################################################################
##########################################################################
#
#               运行此脚本需要事先将资源文件按目录划分
#
##########################################################################
##########################################################################

#注意斜杠'/', 如果使用反斜杠'\'可能会出现错误（\UI会被识别为转义字符\U+I,即启用八进制）

#walk用法——https://www.runoob.com/python/os-walk.html

#BmpCvt命令行用法——BmpCvt 5.36c Help菜单，版本不一样，命令行参数不一样
#BmpCvt logo.bmp -convertintobestpalette -saveaslogo,1 -exit
#图片转换
def PicCvtFunc():
    BmpCnt = 0
    JpgCnt = 0
    for root, dirs, files in os.walk(RES_IMG_ROOT_PATH, topdown = False):
        for name in files:
#            print(os.path.join(root, name))
            newpath = os.path.join(root, name)
            newtype = newpath[-3:]
            newname = name[:-4]
#        png/bmp转换,图片命名中带有（）或路径有空格的，图片名需要用双引号来包含
            if newtype == 'png' or newtype == 'bmp':
                BmpCnt = BmpCnt + 1
                if newname.find('(') == -1 and newname.find(')') and newpath.find(' ')== -1:
                    cmd = "BmpCvt " + newpath + " -saveas" + newname + ".c" +",1,29" + " -exit"
                else:
                    cmd = "BmpCvt " + "\"" + newpath + "\"" + " -saveas" + "\"" + newname + ".c"  + "\"" +",1,29" + " -exit"
                os.system(cmd)
#        jpg转换,图片命名中带有（）或路径有空格的，图片名需要用双引号来包含
            if newtype == 'jpg':
                JpgCnt = JpgCnt + 1
                if newname.find('(') == -1 and newname.find(')') and newpath.find(' ')== -1:
                    cmd = "Bin2C " + newpath
                else:
                    cmd = "Bin2C " + "\"" + newpath + "\""
                os.system(cmd)
    print("Convert PNG/BMP picture num: %d"%BmpCnt)
    print("Convert JPG picture num: %d"%JpgCnt)


#源文件拷贝
def SourceCopyFunc(dstdir):
    for root, dirs, files in os.walk(RES_IMG_ROOT_PATH, topdown = False):
        for filename in files:
            path = os.path.join(root, filename)
            type = path[-1:]
            name = filename[:-4]
            print("%s"%path)
            if type == 'c':
                pos = path.find(dstdir)
                if pos != -1:
                    cwd = path[pos:]
                    newpath = os.path.join(RES_FILE_ROOT_PATH, cwd)
                    shutil.copy(path,newpath)
                    os.remove(path)
                   



#插入宏定义
def InsertMacrosFunc(dstdir, macros):
    for root, dirs, files in os.walk(dstdir, topdown = False):
            for name in files:
                filetype = name[-2:]
                if filetype == ".c":
                    name = os.path.join(root, name)
                    if name.find("fonts") == -1 and name.find("Font") == -1 and name.find("resources.c") == -1:
                        with open(name, 'r') as _objfiler:
                            _confile = _objfiler.read()
                            pos = _confile.find(macros)
                            if (pos != -1):
                                _confile = _confile[:pos] + macros +  '\n' + _confile[pos+len(macros)-1:]
                                with open(name, 'w') as _objfilew:
                                    _objfilew.write(_confile)
                            else:
                                pos = _confile.find(SEEK_STR)
                                _confile = _confile[:pos] + macros +  '\n' + _confile[pos:]
                                with open(name, 'w') as _objfilew:
                                    _objfilew.write(_confile)

#生成头文件
def GenerateHeadFile(dstdir):
    for root, dirs, files in os.walk(dstdir, topdown = False):
            for name in files:
                filetype = name[-2:]
                if filetype == ".c":
                    name = os.path.join(root, name)
                    if name.find("fonts") == -1:
                        with open(name, 'r') as _objfiler:
                            _confile = _objfiler.read()
                            pos = _confile.find("extern GUI_CONST_STORAGE GUI_BITMAP")
                            pos2 = _confile.find("static")-1
                            if (pos != -1 and pos2 != -1):
                                _confile = _confile[pos:pos2] 
                                _objfilew = open("image_flash.txt", 'a+')
                                _objfilew.write(_confile)



#拼接路径
def CombinePath():
    COMMON_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, COMMON_RES_DIR)
    THEME1_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, THEME1_RES_DIR)
    THEME2_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, THEME2_RES_DIR)
    THEME3_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, THEME3_RES_DIR)



if __name__ == "__main__":
    
    file = open("path.txt", 'r',encoding='utf-8')
    str = file.read()

    str = str[str.find("RES_IMG_ROOT_PATH"):]
    start = str.find("=")
    end = str.find("\n",start)
    RES_IMG_ROOT_PATH = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("RES_FILE_ROOT_PATH"):]
    start = str.find("=")
    end = str.find("\n",start)
    RES_FILE_ROOT_PATH = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("COMMON_RES_DIR"):]
    start = str.find("=")
    end = str.find("\n",start)
    COMMON_RES_DIR = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("THEME1_RES_DIR"):]
    start = str.find("=")
    end = str.find("\n",start)
    THEME1_RES_DIR = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("THEME2_RES_DIR"):]
    start = str.find("=")
    end = str.find("\n",start)
    THEME2_RES_DIR = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("THEME3_RES_DIR"):]
    start = str.find("=")
    end = str.find("\n",start)
    THEME3_RES_DIR = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("COMMON_SECTION_MACROS"):]
    start = str.find("=")
    end = str.find("\n",start)
    COMMON_SECTION_MACROS = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("THEME1_SECTION_MACROS"):]
    start = str.find("=")
    end = str.find("\n",start)
    THEME1_SECTION_MACROS = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("THEME2_SECTION_MACROS"):]
    start = str.find("=")
    end = str.find("\n",start)
    THEME2_SECTION_MACROS = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("THEME3_SECTION_MACROS"):]
    start = str.find("=")
    end = str.find("\n",start)
    THEME3_SECTION_MACROS = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("SEEK_STR"):]
    start = str.find("=")
    end = str.find("\n",start)
    SEEK_STR = str[start+1:end]
    str = str[end:]
    
    str = str[str.find("MACROS_INSERT_CONFIG"):]
    start = str.find("=")
    end = str.find("\n",start)
    MACROS_INSERT_CONFIG = str[start+1:end]
    str = str[end:]
    file.close()
    
    file = open("image_flash.txt", 'w')
    file.write("#ifndef _IMAGE_FLASH_H\n#define _IMAGE_FLASH_H\n\n#include \"GUI.h\"\n\n")
    file.close()

    PicCvtFunc()
    GenerateHeadFile(RES_IMG_ROOT_PATH)

    file = open("image_flash.txt", 'a+')
    file.write("\n#endif\n")
    file.close()
    
    if os.path.isfile("image_flash.h"):
        os.remove("image_flash.h")
    os.rename("image_flash.txt","image_flash.h")
    shutil.copy("./image_flash.h",os.path.join(RES_FILE_ROOT_PATH,"Include"))

    #延时3S
    os.system("ping 127.0.0.1 -n 4 >nul")
    SourceCopyFunc(COMMON_RES_DIR)
    SourceCopyFunc(THEME1_RES_DIR)
    SourceCopyFunc(THEME2_RES_DIR)
    SourceCopyFunc(THEME3_RES_DIR)
    #延时3S
    os.system("ping 127.0.0.1 -n 4 >nul")

    MACROS_INSERT_CONFIG = int(MACROS_INSERT_CONFIG)
    if MACROS_INSERT_CONFIG == 1:
        COMMON_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, COMMON_RES_DIR)
        THEME1_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, THEME1_RES_DIR)
        THEME2_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, THEME2_RES_DIR)
        THEME3_RES_DIR = os.path.join(RES_FILE_ROOT_PATH, THEME3_RES_DIR)
        InsertMacrosFunc(COMMON_RES_DIR, COMMON_SECTION_MACROS)
        InsertMacrosFunc(THEME1_RES_DIR, THEME1_SECTION_MACROS)
        InsertMacrosFunc(THEME2_RES_DIR, THEME2_SECTION_MACROS)
        InsertMacrosFunc(THEME3_RES_DIR, THEME3_SECTION_MACROS)
    else:
        os.system("ping 127.0.0.1 -n 4 >nul")
