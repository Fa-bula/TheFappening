#!/bin/sh
killall -9 rtorrent
rm /home/user/The_Fappening/torrent_auto_load/*torrent
rm /home/user/The_Fappening/torrent_auto_load/[0-9]*.txt
rm -r /home/user/The_Fappening/static/videos/*
rm -f ~/session/*
mkdir /home/user/The_Fappening/static/videos/gif
