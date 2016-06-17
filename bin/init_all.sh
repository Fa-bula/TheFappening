#!/bin/sh

# Install all required packages and create all necessary directories
SCRIPT_PATH=`pwd`
VIDEOS_DIR=$SCRIPT_PATH/../static/videos
TEMP_DIR=$SCRIPT_PATH/../.temp
# mkdir $SCRIPT_PATH/../static/videos # directory for videos
# mkdir $SCRIPT_PATH/../.temp	    # directory for .torrent files

# echo "How much space should be reserved for videos (in GB)?"
# read VIDEOS_SIZE
# echo $VIDEOS_SIZE > $SCRIPT_PATH/../.temp/free_space

# Making rtorrent config file
cp $SCRIPT_PATH/../rtorrent.rc ~/.rtorrent.rc
sed -i "s|VIDEOS_DIR|directory = $VIDEOS_DIR|g" ~/.rtorrent.rc
sed -i "s|LOGS|session = $TEMP_DIR|g" ~/.rtorrent.rc
sed -i "s|SCHEDULE|schedule = watch_directory,0,0,\"load_start=$TEMP_DIR/*.torrent\"|g" ~/.rtorrent.rc
# TODO: Adding to crontab

# sudo pip install Flask
# sudo pip install markdowni
# sudo pip install beautifulsoup4
# sudo apt-get install rtorrent
# sudo apt-get install nginx
