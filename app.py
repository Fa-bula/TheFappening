#!/usr/bin/env python
import markdown
from flask import Markup
from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('videos'))

@app.route("/videos/")
def videos():
    root, dirs, files = os.walk('/home/user/The_Fappening/static/videos/').next()
    mp4_files = []
    mp4_files += filter(lambda x: x.endswith('.mp4'), files)
    for dir_ in dirs:
		root2, dirs2, files2 = os.walk(root + dir_ + '/').next()
		mp4_files2 = filter(lambda x: x.endswith('.mp4'), files2)
		for id, string in enumerate(mp4_files2):
			mp4_files2[id] = dir_ + '/' + string
		mp4_files += mp4_files2
    return render_template("videos.html", videos=mp4_files)

@app.route("/feedback/")
def feedback():
    return render_template("feedback.html")

@app.route("/feedback/", methods=["POST"])
def post_feedback():
    f=open("/home/user/The_Fappening/static/txt/opinions", "a")
    post=request.form["opinion"]
    f.write('1.  *' + str(datetime.datetime.now())[:-10]+"*\n")
    f.write(">_"+post.encode('utf-8')+"_\n\n")
    return redirect(url_for('feedback'))

@app.route("/about/" )
def about():
    return render_template("about.html")

@app.route("/playboy/" )
def playboy():
    return render_template("playboy.html")

@app.route("/faq/")
def faq():
    return render_template("FAQ.html")

@app.route("/videos/<name>")
@app.route("/videos/<dir_>/<name>")
def porn_video(name, dir_=''):
    return render_template("porn_video.html",video_type=name[-3:], name=name, dir_=dir_)

@app.route("/images/<name>")
def image(name):
    return render_template("image.html",name=name)
    
@app.route("/txt/<name>")
def text(name):
	f=open('/home/user/The_Fappening/static/txt/' + name, 'r')
	content=f.read()
	content = Markup(markdown.markdown(content))
	return render_template("txt.html", **locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000, threaded=True, debug=True)
