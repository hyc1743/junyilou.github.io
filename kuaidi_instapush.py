# -*- coding:utf-8 -*-
import sys, json, urllib2, time, datetime, os, fileinput, signal
from instapush import Instapush, App
arg = signCheck = siging = brew = tti = 0; sm = nt = binvar = ""; endl = "\n"; argv = list(range(10))

def user1(a,b): global binvar; binvar += "0"
def user2(a,b): global binvar; binvar += "1"
signal.signal(signal.SIGUSR1,user1)
signal.signal(signal.SIGUSR2,user2)
def sig_start(a,b):
	global siging, binvar; siging = 1; binvar = ""
	print 'Received Linux siganal, analyzing.'
def sig_end(a,b): 
	global siging, arg, binvar, brew; sigans = int(binvar,2); siging = 0
	print "Binary: " + binvar + "\nReceived new readid:", sigans
	arg += 1; brew += 1; argv[arg] = str(sigans); binvar = ""
signal.signal(signal.SIGCONT,sig_start)
signal.signal(signal.SIGTERM,sig_end)

def blanker(bid, notice):
	blanktime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print str(os.getpid()) + " " + blanktime + " Checked " + bid + " " + notice + ", ignore."
def pytry(tryurl):
	try: response = urllib2.urlopen(tryurl)
	except urllib2.URLError as err: 
		if hasattr(err, 'reason') or hasattr(err, 'code'): return "False"
	else: return response.read()
def home(readid):
	exsc = False; es = ""; idt = FileLocation + '/' + readid + ".txt"; exi = os.path.isfile(idt)
	if exi:
		for line in fileinput.input(idt): orgCounter = int(line)
		fileinput.close()
	else:
		createFile = open(idt, 'w'); createFile.write("0")
		createFile.close(); orgCounter = 0
	urla = "https://www.kuaidi100.com/autonumber/autoComNum?text=" + readid; trya = pytry(urla)
	if trya != "False": countp = trya.count("comCode")
	else: countp = 1
	if (countp - 1):
		comp = json.loads(trya)["auto"][0]["comCode"]
		urlb = "https://www.kuaidi100.com/query?type=" + comp + "&postid=" + readid; tryb = pytry(urlb)
		if tryb != "False":
			ansj = json.loads(tryb); today = datetime.datetime.now().strftime("%m月%d日")
			comtext = {'yuantong': '圆通', 'yunda': '韵达', 'shunfeng': '顺丰', 'shentong': '申通', 'zhongtong': '中通', 'jd': '京东'}
			if ansj["status"] == "200":
				erstat = 1; maxnum = tryb.count("location")
				if maxnum != orgCounter:
					result = ansj["data"]
					realComp = comtext.get(ansj["com"], "其他") + "快递"
					fTime = time.strftime("%m月%d日 %H:%M", time.strptime(result[0]["time"], "%Y-%m-%d %H:%M:%S"))
					reload(sys); sys.setdefaultencoding('utf-8')
					fContent = result[0]["context"].replace(" 【", "【").replace("】 ", "】").replace(" （", "（").replace(" ）", ")")
					signCount = fContent.count("签收") + fContent.count("感谢") + fContent.count("代收") + fContent.count("取件")
					sendCount = fContent.count("派送") + fContent.count("派件") + fContent.count("准备") + fContent.count("正在")
					if signCount > 0 and sendCount < 1: es = "[签收] "; exsc = maxnum
					fileRefresh = open(idt, 'w'); fileRefresh.write(str(maxnum)); fileRefresh.close()
					app = App(appid = AppID, secret = AppSecret)
					app.notify(event_name = 'kuaidi', trackers = {'rc': realComp, 'ri': readid, 'ft': fTime, 'fc': fContent})
				else: blanker(readid, "has no update")
			else: blanker(readid, "returned code " + ansj["status"])
		else: blanker(readid, "has web connect error")
	else: blanker(readid, "returned no auto-company")
	global tti; tti += 1; return exsc
for m in sys.argv[1:]: arg += 1; brew = arg;
AppID = "585e4e62a4c48a05d607b545" # GitHub users please notice:
AppSecret = "a32883f25245516940ea6b9f9b80fa54" # AppSecret only uses for private.
TimeInterval = int(sys.argv[1])*60
FileLocation = sys.argv[2]
for r in range (1, arg + 1): argv[r] = sys.argv[r]
print endl + "Start with PID " + str(os.getpid()) + "." + endl + "Time interval will be " + sys.argv[1] + "min." + endl
while True:
	if not siging:
		checkbrew = str(argv).count("-")
		for n in range(3, arg + 1):
			readid = argv[n]
			if readid != "-": stat = home(readid)
			else: stat = 0
			if stat:
				print "Checked " + str(readid) + " signed, " + str(stat) + " updates in total recorded, refreshed " + str(tti) + " times."
				argv[n] = "-"; os.system("rm " + FileLocation + '/' + readid + ".txt")
		if checkbrew == (brew - 2): break
		time.sleep(TimeInterval)
	if checkbrew == (brew - 2): break
for ntm in range (1, 45): nt = nt + "="
st = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print endl + "Summary:" + endl + nt + endl + st + " All " + str(brew-2) + " packages signed, exit." + endl + nt
