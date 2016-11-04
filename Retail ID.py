# -*- coding:utf-8 -*-
#Srtl = "%03d" % rtl
import os, sys, fileinput, urllib2
def filesize(url): #通过HEAD分析远程文件大小
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = opener.open(request)
        response.read()
    except Exception, e:
        print '%s %s' % (url, e)
    else:
        return int(dict(response.headers).get('content-length', 0))
def down(): #rtl样例 092
	spr = "".join(["/R", rtl, ".png"]) #spr样例 /R092.png
	exia = os.path.isfile("".join([fbt, rtl, ".png"])) #请求样例 ~/Downloads/Retail/4_3/R092.png
	sx = "".join([sbn, rtl, ".png"]) #sx样例 ~/Downloads/Retail/16_9/R092.png
	exib = os.path.isfile(sx) #exia为4:3存在bool, exib为16_9
	if exia and exib : exic = True
	else: exic = False
	if exic:
		newsize = filesize("".join([dieter, "/16_9", spr]))
		oldsize = os.path.getsize(sx)
		if newsize != oldsize and newsize > 409600:
			os.system("".join(["mv -n ", sbn, rtl, ".png ", rpath, "Other", spr, " && rm ", fbt, rtl, ".png"]))
			#请求样例 mv -n ~/Downloads/Retail/R092.png ~/Downloads/Retail/Other/R092.png && rm ~/Downloads/Retail/4_3/092.png
			fb = open("".join([rpath, "List.md"]))
			newlist = fb.read().replace(("".join([rtl, ","])), ""); fb.close() #注意,不能空格替换
			fc = open("".join([rpath, "List.md"]), "w")
			fc.write(newlist); fc.close()
			exic = False
		else: print "".join(["Photos of R", rtl, " had been already downloaded or not ready yet."])
	if not exic:
		equa = ["/4_3/", "/16_9/"]
		for k in range(0, 2):
			os.system("".join(["wget -t 2 -e \"http_proxy=http://127.0.0.1:6152\" -c -P ", rpath, equa[k], " ", dieter, equa[k], spr]))
			#请求样例 wget -t(尝试次数) 2 -e(代理设置) "http_proxy=http://127.0.0.1:6152" -c(断点续传) -P(指定位置) ~/Downloads/Retail//16_9/ http://rtlimages.apple.com/cmc/dieter/store/16_9//R092.png
			k += 1
		os.system("".join(["open ", sx]))
arg = 0
rpath = "/Users/Junyi_Lou/Downloads/Retail/"
sbn = "".join([rpath, "16_9/R"]) #16:9 ~/Downloads/Retail/16_9/R
fbt = "".join([rpath, "4_3/R"]) #4:3 ~/Downloads/Retail/4_3/R
dieter = "http://rtlimages.apple.com/cmc/dieter/store"
for m in sys.argv[1:]: arg += 1
if arg == 0:
	for line in fileinput.input("".join([rpath, "List.md"])):
		for j in range (0, line.count(",")): #注意,不能空格替换
			rtl = (line.split(","))[j] #注意,不能空格替换
			down()
else:
	for j in range(1, arg + 1):
		rtl = sys.argv[j]
		down()
print