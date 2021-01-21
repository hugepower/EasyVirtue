'''
Author: hugepower
Date: 2021-01-16 21:13:02
LastEditTime: 2021-01-17 10:45:55
LastEditors: Please set LastEditors
Description: macOS系统上获取当前使用的输入法
'''
import plistlib,os,time

def get_AppleCurrentKeyboardLayoutInputSourceID():
    plist_path = os.environ['HOME'] + '/Library/Preferences/com.apple.HIToolbox.plist'
    while True:
        with open(plist_path,'rb') as f:
            AppleCurrentKeyboardLayoutInputSourceID = plistlib.load(f)['AppleCurrentKeyboardLayoutInputSourceID']
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            if AppleCurrentKeyboardLayoutInputSourceID == "com.apple.keylayout.ABC":
                print("当前是【ABC】输入法！%s" %current_time)
            elif AppleCurrentKeyboardLayoutInputSourceID == "com.apple.keylayout.PinyinKeyboard":
                print("当前是【拼音】输入法！%s" %current_time)
            else:
                print("当前是未知的输入法！%s" %current_time)
        time.sleep(5)

if __name__ == "__main__":
    get_AppleCurrentKeyboardLayoutInputSourceID()