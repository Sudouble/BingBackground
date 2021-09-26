# -*- coding:gbk -*-

import os, json, time, sys, requests
import win32api, win32con, win32gui
import re
from PIL import Image, ImageDraw, ImageFont

# reload(sys)
# sys.setdefaultencoding("utf-8")

def get_page(url):
    req = requests.get(url)
    return req.content

def find_img(content):
    json_data = json.loads(content)
    image = json_data['images'][0]
    print("Get image URL")
    return image['url'], image['copyright']


def download_image(img_url, file_path):
    """
    download image from a url, save to file_path
    """
    print("Downloading Image...")
    workPath = os.getcwd()
    save_path = workPath + '\\' + file_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    suffix = img_url[img_url.rfind('.'):]
    suffix = suffix[:suffix.rfind('&')]
    img_content = requests.get(img_url).content
    print("Saving Image...")
    fname = save_path + time.strftime('%Y%m%d') + suffix
    with open(fname, 'wb') as img_file:
        img_file.write(img_content)
    return fname

def write_placesName(file_path, str_word):
    file_base_path = os.path.dirname(file_path)
    file_base_name = os.path.basename(file_path)
    final_path = file_base_path + '\\1_' + file_base_name

    img = Image.open(file_path)
    width, height = img.size

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('simsun.ttc',25)
    str_word = str_word[:str_word.rfind('(')]
    print(str_word)
    draw.text((10, height-80), str_word, fill = (0, 0 ,0), font=font, stroke_width=1) # stroke_fill=

    img.save(final_path)

    return final_path


def set_wallpaper_from_bmp(bmp_path):
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                    "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(reg_key, 'WallpaperStyle', 0, win32con.REG_SZ, '2')
    win32api.RegSetValueEx(reg_key, 'TileWallpaper', 0, win32con.REG_SZ, '0')
    # win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, 1 + 2)

def set_wallpaper(img_path):
    print("Set Wallpaper...")
    img_dir = os.path.dirname(img_path)
    bmpImage = Image.open(img_path)
    new_bmp_path = os.path.join(img_dir, 'wallpaper.bmp')
    bmpImage.save(new_bmp_path, 'BMP')
    set_wallpaper_from_bmp(new_bmp_path)

if __name__ == '__main__':
    url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    content = get_page(url)
    img_url, address = find_img(content)
    img_url  = "http://cn.bing.com" + img_url
    saved_path = download_image(img_url, 'bing_bg\\')
    saved_path = write_placesName(saved_path, address)
    # saved_path = write_placesName('D:\\Personal_\\Exe\\bing_bg\\20200316.jpg', address)
    set_wallpaper(saved_path)