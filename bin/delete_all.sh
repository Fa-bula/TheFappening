#!/bin/sh
echo "Deleting..."
killall -9 rtorrent
rm /home/user/The_Fappening/torrents/*torrent
rm -r /home/user/The_Fappening/static/videos/*
rm -f ~/session/*
mkdir /home/user/The_Fappening/static/videos/gif
