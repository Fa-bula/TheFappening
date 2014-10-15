# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 16:42:02 2014

@author: Alexander
"""

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
    
import os
import platform
import ctypes
'''
def get_free_space(folder):
    """ Return folder/drive free space (in bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        return os.statvfs('/folder').f_bavail*os.statvfs('/folder').f_bsize #к-во доступных пользователю блоков*размер блока

FREE_SPACE = float(get_free_space(""))/1024.0/1024.0/1024.0
'''

FREE_SPACE = 16.0
import urllib
f = urllib.urlopen("http://leporno.org/")
s = f.read()
n = s.find('''viewtopic.php?t=''')
l = n
x = 0
all_titles = set([])
base = open("base.txt", 'a+')
for line in base:
    all_titles.add(line)
space = 0.0
if l < 0:
	print s
while l >= 0:
    end_of_page_address = 17
    while str.isdigit( s[n + end_of_page_address]):
        end_of_page_address += 1
    print "http://leporno.org/" + s[n :n +end_of_page_address ]
    f1 = urllib.urlopen("http://leporno.org/" + s[n :n +end_of_page_address ])
    s1 = f1.read()
    #print s1
    
    n1 = s1.find("http://leporno.org/save")
    if n1 > 0:
        
    
        title_begin = s1.find("<title>") + 7
        title_end = s1.find("</title>")
        
        title = s1[title_begin:title_end]
        
        print "title:  ", title
        left = 0
        right = 0
        openned_brackets = 0
        
        while title[left] == ' ':
            left += 1
        left -= 1
       
        while left < len(title):
            left += 1
            if title[left] in set(["(", "[", "{"]):
                openned_brackets += 1
            elif title[left] in set([")", "]", "}", ":"]):
                openned_brackets -= 1
            elif openned_brackets <= 0:
               
                break
            
        while left < len(title) and title[left] == ' ':
            left += 1
    
        right = left
        while (right < len(title) and not(title[right] in set([ "[", "{"]))):
            right += 1
            
        
            
        size_begin = s1.find("Размер")
        while not str.isdigit(s1[size_begin ]):
            size_begin += 1
        size_end = s1[size_begin:].find("&nbsp;") + size_begin
        if isfloat(s1[size_begin:size_end]):
       
            current_size =float(s1[size_begin :size_end])
            print s1[size_end + 6]
            if s1[size_end + 6] == "M":
                current_size /= 1024.0
                print "CS:", current_size
            print (space + current_size <= FREE_SPACE) ,s1.find("MP4") > 0 , s1.find("MPEG4") > 0 ,(not title[left:right] + "\n" in all_titles)
            
            if (space + current_size <= FREE_SPACE) and (s1.find("MP4") > 0 or s1.find("MPEG4") > 0) and (not title[left:right] in all_titles):
                name_begin = max(s1.find("В ролях"), s1.find("Имя актрисы"),s1.find("Актриса"))
                start = s1[name_begin:].find(":")
                end = s1[name_begin + start:].find("<")
                f = open("./" + str(x) + ".txt", "w" )
                f.write(title[left:right] + "\n")
                if name_begin >= 0:
                    f.write(s1[name_begin + start + 1 : name_begin + start + end])
                f.close()
                print "ref:", s1[n1:n1+37]
                
                
                urllib.urlretrieve(s1[n1:n1+37],"/home/user/porn-server/The.Fappening/torrent_auto_load/" + str(x) + ".torrent")
                #urllib.urlretrieve(s1[n1:n1+37],"./" + str(x) + ".torrent")
                x = x + 1
                all_titles.add(title[left:right] + "\n")
                base.write(title[left:right] + "\n")
                space += current_size
    
    l = s[n+1:-1].find('''viewtopic.php?t=''')
    n = l + n + 1
base.close()

    
