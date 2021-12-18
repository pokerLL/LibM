import os
import os.path

rootdir = r"C:/Users/少女口牙/Desktop/图片/tx"  # 指明被遍历的文件夹
os.chdir(rootdir)
filelist = os.listdir(rootdir)

pic = 1
for filename in filelist:  # 文件名
    print(filename)
    os.rename(filename, str(pic) + ".png")  # 重命名
    pic += 1
