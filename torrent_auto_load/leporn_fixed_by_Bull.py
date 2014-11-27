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
file_with_page = urllib.urlopen("http://leporno.org/")
main_page = file_with_page.read()
n = main_page.find('''viewtopic.php?t=''')
l = n
x = 0

forbidden_words = ['.wmv', 'gay', '.flv', '.avi', '.mov', 'zoo', 'transsexual', 'shemale', 'grand']

all_titles = set([])
base = open("/home/user/The_Fappening/torrent_auto_load/base.txt", 'a+')
for line in base:
    all_titles.add(line)
space = 0.0
if l < 0:
	print main_page
while l >= 0:
    end_of_page_address = 17
    while str.isdigit( main_page[n + end_of_page_address]):
        end_of_page_address += 1
    
    file_with_child_page = urllib.urlopen("http://leporno.org/" + main_page[n :n +end_of_page_address ])
    child_page = file_with_child_page.read()
    #print child_page
    
    n1 = child_page.find("save")
    if n1 > 0:
        
    
        title_begin = child_page.find("<title>") + 7
        title_end = child_page.find("</title>")
        
        title = child_page[title_begin:title_end]
        
       
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
            
        no_forbidden_words = True
        for word in forbidden_words:
            no_forbidden_words &= (child_page.find(word) < 0)
            
        size_begin = child_page.find("Размер")
        while not str.isdigit(child_page[size_begin ]):
            size_begin += 1
        size_end = child_page[size_begin:].find("&nbsp;") + size_begin
        if isfloat(child_page[size_begin:size_end]):       
            current_size =float(child_page[size_begin :size_end])
            if child_page[size_end + 6] == "M":
                current_size /= 1024.0
                
            print "http://leporno.org/" + main_page[n :n +end_of_page_address ]
            print no_forbidden_words, (space + current_size <= FREE_SPACE), (child_page.find("MP4") > 0 or
            child_page.find("MPEG4") > 0), (not (title[left:right] + '\n') in all_titles)
      
            if no_forbidden_words and (space + current_size <= FREE_SPACE) and (child_page.find("MP4") > 0 or
            child_page.find("MPEG4") > 0) and (not (title[left:right] + '\n') in all_titles):
                
                print "title:  ", title
                print "CS:", current_size
                
                name_begin = max(child_page.find("В ролях"), child_page.find("Имя актрисы"),child_page.find("Актриса"))
                start = child_page[name_begin:].find(":")
                end = child_page[name_begin + start:].find("<")
                f = open("/home/user/The_Fappening/torrent_auto_load/" + str(x) + ".txt", "w" )
                f.write(title[left:right] + "\n")
                if name_begin >= 0:
                    f.write(child_page[name_begin + start + 1 : name_begin + start + end])
                f.close()
                print "ref:","http://leporno.org/" + child_page[n1:n1+18]
                
                
                urllib.urlretrieve("http://leporno.org/" + child_page[n1:n1+18],"/home/user/The_Fappening/torrent_auto_load/" + str(x) + ".torrent")
                #urllib.urlretrieve("http://leporno.org/" + child_page[n1:n1+18],"./" + str(x) + ".torrent")
                x = x + 1
                all_titles.add(title[left:right] + "\n")
                base.write(title[left:right] + "\n")
                space += current_size
                print "\n"
    
    l = main_page[n+1:-1].find('''viewtopic.php?t=''')
    n = l + n + 1
base.close()

