#! /bin/sh
IFS=$\n
cd /home/user/The_Fappening/static/videos
for file in *.mp4
do
	echo "$file"
	ffmpeg -t 500 -ss 00:01:00 -i "$file" -r 1/20 gif/out%04d.gif
	mogrify -resize 225x170 gif/out0*.gif
	convert -delay 12x20 -loop 0 gif/out0*.gif gif/"$file".gif
	rm  gif/out*
done

mogrify -flatten -format jpg gif/*.gif

IFS=$\n
cd /home/user/The_Fappening/static/videos
for dir in */
do
	echo "$dir"
	mkdir gif/"$dir"
	cd "$dir"
	for file in *mp4
	do
		echo "$file"
		ffmpeg -t 500 -ss 00:01:00 -i "$file" -r 1/20 ../gif/"$dir"/out%04d.gif
		mogrify -resize 225x170 ../gif/"$dir"/out0*.gif
		convert -delay 12x20 -loop 0 ../gif/"$dir"/out0*.gif ../gif/"$dir"/"$file".gif
	done
	cd ..
	rm gif/"$dir"/out0*
	mogrify -flatten -format jpg gif/"$dir"/*.gif
done
