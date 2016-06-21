# -*- coding:utf-8 -*-
import os
import json
import time
import sys
import requests

reload(sys)
sys.setdefaultencoding("utf-8")

def get_page(url):
    req = requests.get(url)
    return req.content

def find_img(content):
    json_data = json.loads(content)
    image = json_data['images'][0]
    return image['url'], image['copyright']


def download_image(img_url, file_path):
    """
    download image from a url, save to file_path
    """
    workPath = os.getcwd()
    save_path = workPath + '\\' + file_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    suffix = img_url[img_url.rfind('.'):]
    img_content = requests.get(img_url).content
    fname = save_path + time.strftime('%Y%m%d') + suffix
    with open(fname, 'wb') as img_file:
        img_file.write(img_content)
    return fname

if __name__ == '__main__':
    url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    content = get_page(url)
    img_url, address = find_img(content)
    saved_path = download_image(img_url, 'bing_bg\\')