# -*- coding: utf-8 -*-
# Created on 2014-12-27
# @author: Yefei
import os
import re
import sys
import urllib2


PATH = lambda *p: os.path.normpath(os.path.join(os.path.dirname(__file__), *p))

# 视频目录规则
RECORD_PATH_RULE = re.compile(r'HREF="(\d{4})Y(\d{2})M(\d{2})D(\d{2})H"', re.I)

# 视频文件规则
RECORD_FILE_RULE = re.compile(r'HREF="(\d{2})M00S.mp4"', re.I)


def check_path(*p):
    p = PATH(*p)
    if not os.path.exists(p):
        print u'创建存储目录:', p
        os.mkdir(p)


def get_file_content(filename):
    with open(PATH(filename)) as f:
        return f.read()


def get_url_content(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_record_paths(cam_ip):
    data = get_url_content('http://%s/sd/record/' % cam_ip)
    return RECORD_PATH_RULE.findall(data)


def get_record_path_videos(cam_ip, path):
    data = get_url_content('http://%s/sd/record/%s' % (cam_ip, path))
    return RECORD_FILE_RULE.findall(data)



def download(url, save_filename):
    response = urllib2.urlopen(url)
    total_size = int(response.info().getheader('Content-Length').strip())
    bytes_so_far = 0
    
    with open(save_filename, "wb") as f:
        while 1:
            chunk = response.read(8192)
            bytes_so_far += len(chunk)
            if not chunk:
                break
            
            f.write(chunk)
            
            percent = float(bytes_so_far) / total_size
            percent = round(percent * 100, 2)
            sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % (bytes_so_far, total_size, percent))
            
            if bytes_so_far >= total_size:
                sys.stdout.write('\n')


if __name__ == '__main__':
    cam_ip = get_file_content('cam-ip.txt')
    if not cam_ip:
        print u'请编辑 cam-ip.txt 文件，设置摄像机 IP 地址'
        sys.exit()
    print u'摄像机IP:', cam_ip
    
    # 取得最后保存日期
    last_date = get_file_content('last-date.txt')
    last_date = int(last_date) if last_date else 0
    
    check_path('videos')
    
    paths = get_record_paths(cam_ip)
    if not paths:
        print u'摄像机上没有任何记录'
        sys.exit()
    
    for i in paths:
        path_date = int(''.join(i) + '00')
        # 除以 100 是只比较 日期+小时
        if path_date/100 < last_date/100:
            continue
        
        # 扫描目录中的视频文件
        path_name = '%sY%sM%sD%sH' % i
        videos = get_record_path_videos(cam_ip, path_name)
        for m in videos:
            video_date = int(''.join(i) + m)
            if video_date <= last_date:
                continue
            print u'下载 %s-%s-%s %s:%s' % (i[0], i[1], i[2], i[3], m)
            
            save_ym_path_name = '%s-%s' % (i[0], i[1])
            check_path('videos', save_ym_path_name)
            check_path('videos', save_ym_path_name, i[2])
            
            save_filename = PATH('videos', save_ym_path_name, i[2], '%s-%s.mp4' % (i[3], m))
            download('http://%s/sd/record/%s/%s' % (cam_ip, path_name, '%sM00S.mp4' % m), save_filename)
            
            last_date = video_date
            with open(PATH('last-date.txt'), 'w') as f:
                f.write(str(last_date))

