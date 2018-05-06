# -*- coding: utf-8 -*-

from linepy import *
from akad import *
from bs4 import BeautifulSoup
from gtts import gTTS
import traceback
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, urllib, urllib.parse,pickle,subprocess
from multiprocessing import Pool
from datetime import datetime
from googletrans import Translator
from random import randint
print("""

\033["""+str(randint(0,1))+""";"""+str(randint(31,36))+"""mplay free\nby beach noxtian\033[0m

""")

with open('tval.pkl', 'rb') as f:
    cltoken,save1 = pickle.load(f,encoding='latin1')

if len(sys.argv) == 2 and sys.argv[1] == "reset":
    cltoken = ""
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,save1], f)
    os._exit(0)
#_____________________________________________________
if cltoken == "":
    cl = LINE()
    cltoken = cl.authToken
else:
    try:
        cl = LINE(cltoken)
    except KeyboardInterrupt as e:
        raise e
    except:
        cl = LINE()
        cltoken = cl.authToken

print("authToken: %s" % (cltoken))

oepoll = OEPoll(cl)
mid = cl.profile.mid
#_____________________________________________________

start_runtime = datetime.now()

helpuser1 = """คำสั่งทุกคำสั่งมี . นำหน้าเสมอ
-say [text] [number]
-me
-myid
-gid
-name
-myname
-time
-uptime
-speed
-mention
-save
-load
-talk [text]
-grouppict
-url [gid]
-copy @
-uid @
-me @
-pict @
-home @
-info @
-set on
-set off
-whoread
-invitetocall
-checkmention
-resetmention
-rejectall {text}
_____________________________
#!selfpython
______________________________"""

KAC = cl
#-------------------------------
user1 = mid
admin = ["KAC"]
me = cl.profile.mid
bot1 = cl.profile.mid
main = cl.profile.mid
protectname = []
protecturl = []
protection = []
autocancel = {}
autoinvite = []
autoleaveroom = []
winvite = []
#////////////////////////////////
admins = ["mid"]

wait = {
    'contact':False,
    'autoJoin':False,
    'autoCancel':{"on":True,"members":1},
    'leaveRoom':True,
    'timeline':True,
    'autoAdd':False,
    'message':"""🕸🐯тнαик Ғσя α∂∂ мє🐯🕸""",
    "lang":"JP",
    "comment":""" 🌟。 ❤。😉。🍀
    。✨ 。🎉。🌟
     ✨。＼｜／。💫 Auto Like By Beach
    🌟。／｜＼。🍻
    。🍀。 🍸。🎉。
     🌟。 💫。 🎶 💥 """,
    "likeOn":True,
    "commentOn":True,
    "commentBlack":{},
    "loop":False,
    "alwayRead":False,
}

wait2 = {
	'readMember':{},
	'readPoint':{},
	'ROM':{},
	'setTime':{}
    }

setTime = {}
setTime = wait2["setTime"]

res = {
    'num':{},
    'us':{},
    'au':{},
}

wait3 = {
    "Hhx1":True,
    "Hhx2":True,
    "Hhx3":True,
    "acommentOn":True,
    "bcommentOn":True,
    "ccommentOn":True,
    "MasterBeach":True,
}


save1 = {
    "Saved":False,
    "displayName":"",
    "statusMessage":"",
    "pictureStatus":""
}

def Cmd(string, commands): #/XXX, >XXX, ;XXX, ^XXX, %XXX, $XXX...
    tex = [""]
    for texX in tex:
        for command in commands:
            if string ==texX + command:
                return True
    return False

def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except:
        pass

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1

Rapid1To = ""
MasterBeach = ""

def Rapid1Say(mtosay):
    cl.sendMessage(Rapid1To,mtosay)

lgncall = ""
def logincall(this,pointer):
    if pointer == 0:
        status = "[1/2]"
    elif pointer == 1:
        status = "[2/2]"
    cl.sendText(lgncall,"Bot's login url "+status+": "+this)

mentmedat = {}

def bot(op):
    global start_runtime
    global lgncall
    global MasterBeach
    global user1
    global mid
    global mentmedat
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if wait["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                if (wait["message"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendMessage(op.param1,str(wait["message"]))

        if op.type == 13:
            if mid in op.param3:
                G = cl.getGroup(op.param1)
                if wait["autoJoin"] == True:
                    if wait["autoCancel"]["on"] == True:
                        if len(G.members) <= wait["autoCancel"]["members"]:
                            cl.rejectGroupInvitation(op.param1)
                        else:
                            cl.acceptGroupInvitation(op.param1)
                    else:
                        cl.acceptGroupInvitation(op.param1)

                elif wait["autoCancel"]["on"] == True:
                    if len(G.members) <= wait["autoCancel"]["members"]:
                        cl.rejectGroupInvitation(op.param1)
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                matched_list = []
                for tag in wait["blacklist"]:
                    matched_list+=[str for str in InviterX if str == tag]
                if matched_list == []:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, matched_list)
#____________________________________________________________________
        if op.type == 17:
            if wait3["acommentOn"] and "acommentOn" in wait:
                cnt = cl.getContact(op.param2)
                cl.sendMessage(op.param1,cnt.displayName + "\n" + str(wait3["acommentOn"]))
                cl.sendImageWithUrl(op.param1,"http://dl.profile.line.naver.jp/" + cnt.pictureStatus)

        if op.type == 22:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)

        if op.type == 24:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)

        if op.type == 15:
            if wait3["bcommentOn"] and "bcomment" in wait:
                cl.sendMessage(op.param1,cl.getContact(op.param2).displayName + "\n" + str(wait["bcomment"]))

        if op.type == 19:
            if wait3["ccommentOn"] and "ccomment" in wait:
                cl.sendMessage(op.param1,cl.getContact(op.param2).displayName + "\n" + str(wait["ccomment"]))
#--------------------------------------------------------------------
        if op.type == 26:
            msg = op.message
            msg.from_ = msg._from
            if msg.contentMetadata != {}:
                try:
                    prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                    tagme = False
                    alluids = []
                    for i in range(len(prov)):
                        alluids.append(prov[i]["M"])
                        if prov[i]["M"] == mid:
                            tagme = True
                    alluids = list(set(alluids))
                    if tagme:
                       if len(alluids) <= 4:
                           if msg.to not in mentmedat:
                               mentmedat[msg.to] = []
                               tagfrom = msg._from
                               tagtime = nowS = datetime.strftime(datetime.now(),"%H:%M:%S")
                               tagid = msg.id
                               mentmedat[msg.to].append(
                                   {
                                       "tfrom" : tagfrom,
                                       "ttime" : tagtime,
                                       "tid" : tagid
                                   }
                               )
                       if MasterBeach:
                          msg.contentType = 7
                          msg.text = ''
                          cl.sendMessage(msg.to,"แท็กจังมีอะไรคับ")
                          msg.contentMetadata = {
                                                    'STKPKGID': '1273495',
                                                    'STKTXT': '[Sticker]',
                                                    'STKVER': '1',
                                                    'STKID':'11086195'
                                                }
                          cl.sendMessage(msg)
                except:
                    pass

            if wait["alwayRead"] == True:
                if msg.toType == 26:
                    cl.sendChatChecked(msg.from_,msg.id)
                else:
                    cl.sendChatChecked(msg.to,msg.id)

            if msg.toType == 1:
                if wait["leaveRoom"] == True:
                    cl.leaveRoom(msg.to)

            if msg.contentType == 16:
                if mid is None:
                    mid = cl.proflie.mid
                url = msg.contentMetadata["postEndUrl"]
                cl.pastContect(url[25:58], url[66:], likeType=1002)

        if op.type == 25:
            msg = op.message
            if msg.contentType == 13:
                if wait["contact"] == True:
                    msg.contentType = 0
                    cl.sendMessage(msg.to,msg.contentMetadata["mid"])
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.to,contentMetadata["mid"])
                        try:
                            cu = cl.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[displayName]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))

            elif msg.contentType == 16:
                if wait["timeline"] == True:
                    msg.contentType == 0
                    if wait["lang"] == "JP":
                        msg.text = "" + msg.contentMetadata["postEndUrl"]
                    else:
                        msg.text = "" + msg.contentMetadata["postEndUrl"]
                    cl.sendMessage(msg.to,msg.text)

        if op.type == 25:
            msg = op.message
            msg.from_ = msg._from
            if '.say ' in msg.text.lower():
                red = re.compile(re.escape('.say '),re.IGNORECASE)
                mts = red.sub('',msg.text)
                mtsl = mts.split()
                mtsTimeArg = len(mtsl) - 1
                mtsTime = mtsl[mtsTimeArg]
                del mtsl[mtsTimeArg]
                mtosay = " ".join(mtsl)
                global Rapid1To
                Rapid1To = msg.to
                RapidTime = mtsTime
                rmtosay = []
                for count in range(0,int(RapidTime)):
                    rmtosay.insert(count,mtosay)
                p = Pool(20)
                p.map(Rapid1Say,rmtosay)
                p.close()
            elif msg.text is None:
                return
            elif msg.text.lower() == ".help":
                cl.sendMessage(msg.to,helpuser1)

            elif msg.text.lower() == ".me":
                cl.sendContact(msg.to,mid)

            elif ".myname" == msg.text.lower():
                G = cl.getContact(mid)
                cl.sendMessage(msg.to,G.displayName)

            elif msg.text.lower() == ".cancel":
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.invitee]
                    for i in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[i])

            elif msg.text.lower().startswith("#!selfpython\n"):
                    data = msg.text[len("#!selfpython\n"):]
                    open("selfpython-tmp.py","w").write(data)
                    try:
                        cl.sendMessage(msg.to,subprocess.getoutput("python3 selfpython-tmp.py"))
                    except:
                        pass
                    subprocess.getoutput("rm selfpython-tmp.py")

#--------------------------------------------------------------------
            elif ".comment set:" == msg.text.lower():
                c = msg.text.replace(".comment set:","")
                if c in [""," ","\n",None]:
                    cl.sendMessage(msg.to,"Error")
                else:
                    wait["comment"] = c
                    cl.sendMessage(msg.to,"It was changed。\n\n" + c)

            elif msg.text.lower() == [".commentcheck"]:
                cl.sendMessage(msg.to,"An automatic comment is established as follows at present。\n\n" + str(wait["comment"]))

            elif msg.text.lower() == ".comment on":
                if wait["commentOn"] == True:
                    cl.sendMessage(msg.to,"succes")

            elif msg.text.lower() == ".comment off":
                if wait["commentOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"succes")
            elif msg.text.lower() == ".blockurl on":
                protecturl.append(msg.to)
                cl.sendMessage(msg.to,"succes")

            elif msg.text.lower() == ".blockurl off":
                protecturl.remove(msg.to)
                cl.sendMessage(msg.to,"ᴀʟʟᴏᴡᴇᴅ")

            elif msg.text.lower() == ".blockinvite on":
                if msg.toType == 2:
                    if msg.to not in blockInvite:
                        blockInvite.append(msg.to)
                        cl.sendMessage(msg.to,"ล็อกการเชิญแล้ว (｀・ω・´)")

            elif msg.text.lower() == ".blockinvite off":
                if msg.toType == 2:
                    if msg.to in blockInvite:
                        blockInvite.append(msg.to)
                        cl.sendMessage(msg.to,"ปลดล็อกการเชิญแล้ว (｀・ω・´)")

            elif ".ginfo" == msg.text.lower():
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "(ไม่พบผู้สร้าง)"
                    if wait["lang"] == "JP":
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.perventJoinByTicket == True:
                            u = "ปิดอยู่"
                        else:
                            u = "เปิดอยู่"
                        cl.sendMessage(msg.to,"[ชื่อกลุ่ม]\n" + str(ginfo.name) + "\n\n[ไอดีกลุ่ม]\n" + msg.to + "\n\n[ผู้สร้างกลุ่ม]\n" + gCreator + "\n\n[รูปโปรไฟล์กลุ่ม]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\n\nสมาชิก:" + str(len(ginfo.members)) + " ท่าน\nเชิญ:" + sinvitee + " ท่าน\nURL:" + u + "")
                    else:
                        cl.sendMessage(msg.to,"[名字]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[小组的作成者]\n" + gCreator + "\n[小组图标]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    pass
#------------------------------------------------------------------------------
            elif ".gid" == msg.text.lower():
                if msg.toType == 2:
                    cl.sendMessage(msg.to,msg.to)
                else:
                    cl.sendMessage(msg.to,"คำสั่งนี้ใช้ได้เฉพาะกลุ่ม(｀・ω・´)")

            elif ".myid" == msg.text.lower():
                cl.sendMessage(msg.to,mid)

            elif ".name " in msg.text.lower():
                spl = re.split(".name ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    prof = cl.getProfile()
                    prof.displayName = spl[1]
                    cl.updateProfile(prof)
                    cl.sendMessage(msg.to,"เปลี่ยนชื่อสำเร็จแล้ว(｀・ω・´)")
#------------------------------------------------------------------------------
            elif msg.text.lower() == ".mid on":
                if wait["loop"] == False:
                    cl.sendMessage(msg.to,"ᴄᴏɴᴛᴀᴄᴛ ᴏɴ ᴀʟʀᴇᴀᴅʏ")

            elif msg.text.lower() == ".mid off":
                if wait["loop"] == True:
                    cl.sendMessage(msg.to,"ᴄᴏɴᴛᴀᴄᴛ ᴏᴏғ ᴀʟʀᴇᴀᴅʏ")
#-------------------------------------------------------------------------------
            elif msg.text.lower() == ".contact on":
                if wait["contact"] == True:
                    cl.sendMessage(msg.to,"ᴄᴏɴᴛᴀᴄᴛ ᴏɴ ᴀʟʀᴇᴀᴅʏ")

            elif msg.text.lower() == ".contact off":
                if wait["contact"] == False:
                    cl.sendMessage(msg.to,"ᴄᴏɴᴛᴀᴄᴛ ᴏᴏғ ᴀʟʀᴇᴀᴅʏ")

            elif msg.text.lower() == [".autojoin on"]:
                if wait["autoJoin"] == True:
                    cl.sendMessage(msg.to,"ᴊᴏɪɴ ᴏɴ ᴀʟʀᴇᴀᴅʏ")

            elif msg.text.lower() == [".autojoin off"]:
                if wait["autoJoin"] == False:
                    cl.sendMessage(msg.to,"ᴊᴏɪɴ ᴏғғ ᴀʟʀᴇᴀᴅʏ")

            elif msg.text.lower() == [".autoleave on"]:
                if wait["leaveRoom"] == True:
                    cl.sendMessage(msg.to,"ʟᴇᴀᴠᴇ ᴏɴ ᴀʀᴇᴀᴅʏ")

            elif msg.text.lower() == ".autoleave off":
                if wait["leaveRoom"] == False:
                    cl.sendMessage(msg.to,"ʟᴇᴀᴠᴇ ᴏᴏғ ᴀʀᴇᴀᴅʏ")

            elif msg.text.lower() == ".autoshare on":
                if wait["timeline"] == True:
                    cl.sendMessage(msg.to,"ᴀʟʀᴇᴀᴅʏ ᴏɴ")

            elif msg.text.lower() == ".autoshare off":
                if wait["timeline"] == False:
                    cl.sendMessage(msg.to,"ᴀʟʀᴇᴀᴅʏ ᴏғғ")
#---------------------------------------------------------------------------
            elif ".setting" == msg.text.lower():
               try:
                   md = ""
                   if wait["contact"] == True: md+="✔ ➡Contact → on \n"       
                   else: md+="✖ ➡Contact → off \n"
                   if wait["autoJoin"] == True: md+="✔  ➡Auto join → on \n" 
                   else: md +="✖ ➡Auto join → off \n"
                   if wait["autoCancel"]["on"] == True:md+="✔ ➡Cancel Invite → " + str(wait["autoCancel"]["members"]) + " \n"     
                   else: md+= "✖ ➡Cancel Invite → off \n"  
                   if wait["leaveRoom"] == True: md+="✔ ➡Auto leave → on \n"   
                   else: md+="✖ ➡Auto leave → off \n"
                   if wait["timeline"] == True: md+="✔ ➡Auto Share → on \n"  
                   else:md+="✖ ➡Auto Share → off \n" 
                   if wait["commentOn"] == True: md+="✔ ➡Comment → on \n"   
                   else:md+="✖ ➡Comment → off \n"    
                   if wait["autoAdd"] == True: md+="✔ ➡Auto add → on \n"  
                   else:md+="✖ ➡Auto add → off \n"   
                   if wait["likeOn"] == True: md+="✔ ➡Auto like → on \n"
                   else:md+="✖ ➡Auto like → off \n"
                   if wait["alwayRead"] == True: md+="✔ ➡Read  → on \n"
                   else:md+="✖ ➡Read → off \n"
                   if wait3["Hhx1"] == True: md+="✔ ➡ Hhx1→ on \n"
                   else: md+="✖ ➡Hhx1 → off \n"
                   if wait3["Hhx2"] == True: md+="✔ ➡ Hhx2→ on \n"
                   else: md+="✖ ➡Hhx2 → off \n"
                   if wait3["Hhx3"] == True: md+="✔ ➡ Hhx3→ on \n"
                   else: md+="✖ ➡Hhx3 → off \n"
                   cl.sendMessage(msg.to, str(md))
               except Exception as e:
                   cl.sendMessage(msg.to, str(md))
#--------------------------------------------------------------------
            elif ".rejectall" in msg.text.lower():
                spl = re.split(".rejectall",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    spl[1] = spl[0].strip()
                    ag = cl.getGroupIdsInvited()
                    txt = "กำลังยกเลิกค้างเชิญจำนวน "+str(len(ag))+" กลุ่ม"
                    if spl[1] != "":
                        txt = txt + " ด้วยข้อความ \""+spl[1]+"\""
                    txt = txt + "\nกรุณารอสักครู่.."
                    cl.sendMessage(msg.to,txt)
                    procLock = len(ag)
                    for gr in ag:
                        try:
                            cl.acceptGroupInvitation(gr)
                            if spl[1] != "":
                                cl.sendMessage(gr,spl[1])
                            cl.leaveGroup(gr)
                        except:
                            pass
#------------------------------------------------------------------------------
            elif msg.text.lower() == [".autolike on"]:
                if wait["likeOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"Done。")

            elif msg.text.lower() == [".autolike off"]:
                if wait["likeOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"Done。")

            elif msg.text.lower() == ".autoread on":
                if wait['alwayRead'] == True:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"เปิดโหมดอ่านอัตโนมัติแล้ว")

            elif msg.text.lower() == ".autoread off":
                if wait['alwayRead'] == False:
                    if wait['lang'] == "JP":
                        cl.sendMessage(msg.to,"ปิดโหมดอ่านอัตโนมัติแล้ว")

            elif msg.text.lower() == [".autoadd on"]:
                if wait["autoAdd"] == True:
                    cl.sendMessage(msg.to,"It's on already。")

            elif msg.text.lower() == [".autoadd off"]:
                if wait["autoAdd"] == False:
                    cl.sendMessage(msg.to,"It's off already。")

            elif "Message set:" in msg.text:
                wait["message"] = msg.text.replace("Message add:","")
                cl.sendText(msg.to,"The message was changed。")
            elif "Auto addition→" in msg.text:
                wait["message"] = msg.text.replace("Auto addition→","")
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"The message was changed。")
                else:
                    cl.sendText(msg.to,"was change already。")
            elif msg.text in ["Message check","自動追加問候語確認"]:
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,".automatic message is established as follows。\n\n" + wait["message"])
                else:
                    cl.sendText(msg.to,"One  of weeds on the surface below the self- additional breath image。\n\n" + wait["message"])
            elif msg.text.lower() == ["CHANGE"]:
                if wait["lang"] =="JP":
                    wait["lang"] = "TW"
                    cl.sendText(msg.to,"ƇƠƲƝƬƦƳ ԼƛƝƓƲƛƓЄ ƊƲƦƖƝƓ ƛ ƇHƛƝƓЄ。")
                else:
                    wait["lang"] = "JP"
                    cl.sendText(msg.to,". The language was made English。")
#--------------------------------------------------------
            elif msg.text.lower() == ["url"]:
                if msg.toType == 2:
                    x = cl.getGroup(msg.to)
                    if x.preventJoinByTicket == True:
                        x.preventJoinByTicket = False
                        cl.updateGroup(x)
                    gurl = cl.reissueGroupTicket(msg.to)
                    cl.sendMessage(msg.to,"[Url]\nline://ti/g/" + gurl)

            elif msg.text.lower() == '.mention':
                group = cl.getGroup(msg.to)
                nama = [contact.mid for contact in group.members]
                k = len(nama)//100
                for a in range(k+1):
                    txt = u''
                    s=0
                    b=[]
                    for i in group.members[a*100 : (a+1)*100]:
                        b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                        s += 7
                        txt += u'@Alin \n'
                    cl.sendMessage(msg.to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
#-------------------------------------------------------
            elif msg.text.lower() == (".mentionall"):
                data = msg.text[len(".mentionall"):].strip()
                if data == "":
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members if contact.mid != user1]
                    cb = ""
                    cb2 = ""
                    count = 1
                    strt = len(str(count)) + 2
                    akh = int(0)
                    cnt = 0
                    for md in nama:
                        akh = akh + len(str(count)) + 2 + 5
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + len(str(count+1)) + 2 + 6
                        akh = akh + 1
                        cb2 += str(count)+". @name\n"
                        cnt = cnt + 1
                        if cnt == 50:
                            cb = (cb[:int(len(cb)-1)])
                            cb2 = cb2[:-1]
                            msg.contentType = 0
                            msg.text = cb2
                            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                            try:
                                cl.sendMessage(msg)
                            except:
                                cl.sendMessage(msg.to,"[[NO MENTION]]")
                            cb = ""
                            cb2 = ""
                            strt = len(str(count)) + 2
                            akh = int(0)
                            cnt = 0
                        count += 1
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                        cl.sendMessage(msg)
                    except:
                        cl.sendMessage(msg.to,"[[NO MENTION]]")
                elif data[0] == "<":
                    mentargs = int(data[1:].strip())
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members if contact.mid != user1]
                    cb = ""
                    cb2 = ""
                    count = 1
                    strt = len(str(count)) + 2
                    akh = int(0)
                    cnt = 0
                    for md in nama:
                        if count > mentargs:
                            break
                        akh = akh + len(str(count)) + 2 + 5
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + len(str(count+1)) + 2 + 6
                        akh = akh + 1
                        cb2 += str(count)+". @name\n"
                        cnt = cnt + 1
                        if cnt == 50:
                            cb = (cb[:int(len(cb)-1)])
                            cb2 = cb2[:-1]
                            msg.contentType = 0
                            msg.text = cb2
                            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                            try:
                                cl.sendMessage(msg)
                            except:
                                cl.sendMessage(msg.to,"[[NO MENTION]]")
                            cb = ""
                            cb2 = ""
                            strt = len(str(count)) + 2
                            akh = int(0)
                            cnt = 0
                        count += 1
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                        cl.sendMessage(msg)
                    except:
                        cl.sendMessage(msg.to,"[[NO MENTION]]")
                elif data[0] == ">":
                    mentargs = int(data[1:].strip())
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members if contact.mid != user1]
                    cb = ""
                    cb2 = ""
                    count = 1
                    if mentargs >= 0:
                        strt = len(str(mentargs)) + 2
                    else:
                        strt = len(str(count)) + 2
                    akh = int(0)
                    cnt = 0
                    for md in nama:
                        if count < mentargs:
                            count += 1
                            continue
                        akh = akh + len(str(count)) + 2 + 5
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + len(str(count+1)) + 2 + 6
                        akh = akh + 1
                        cb2 += str(count)+". @name\n"
                        cnt = cnt + 1
                        if cnt == 50:
                            cb = (cb[:int(len(cb)-1)])
                            cb2 = cb2[:-1]
                            msg.contentType = 0
                            msg.text = cb2
                            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                            try:
                                cl.sendMessage(msg)
                            except:
                                cl.sendMessage(msg.to,"[[NO MENTION]]")
                            cb = ""
                            cb2 = ""
                            strt = len(str(count)) + 2
                            akh = int(0)
                            cnt = 0
                        count += 1
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                        cl.sendMessage(msg)
                    except:
                        cl.sendMessage(msg.to,"[[NO MENTION]]")
                elif data[0] == "=":
                    mentargs = int(data[1:].strip())
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members if contact.mid != user1]
                    cb = ""
                    cb2 = ""
                    count = 1
                    akh = int(0)
                    cnt = 0
                    for md in nama:
                        if count != mentargs:
                           count += 1
                           continue
                        akh = akh + len(str(count)) + 2 + 5
                        strt = len(str(count)) + 2
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + len(str(count+1)) + 2 + 6
                        akh = akh + 1
                        cb2 += str(count)+". @name\n"
                        cnt = cnt + 1
                        if cnt == 50:
                            cb = (cb[:int(len(cb)-1)])
                            cb2 = cb2[:-1]
                            msg.contentType = 0
                            msg.text = cb2
                            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                            try:
                                cl.sendMessage(msg)
                            except:
                                cl.sendMessage(msg.to,"[[NO MENTION]]")
                            cb = ""
                            cb2 = ""
                            strt = len(str(count)) + 2
                            akh = int(0)
                            cnt = 0
                        count += 1
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                        cl.sendMessage(msg)
                    except:
                        cl.sendMessage(msg.to,"[[NO MENTION]]")
#--------------------------------------------------------------------
            elif msg.text.lower() == ".checkmention":
                if msg.to in mentmedat and mentmedat[msg.to] != []:
                    text = ""
                    for data in mentmedat[msg.to]:
                        try:
                            conname = cl.getContact(data["tfrom"]).displayName
                        except:
                            conname = "[DELETED]"
                        text += "[%s] %s\nline://nv/chatMsg?chatId=%s&messageId=%s\n\n" % (data["ttime"],conname,msg.to,data["tid"])
                    text = text[:-2]
                    try:
                        cl.sendMessage(msg.to,text)
                    except Exception as e:
                        cl.sendMessage(msg.to,str(e))
                    del mentmedat[msg.to]
                else:
                    cl.sendMessage(msg.to,"ไม่มีการกล่าวถึงก่อนหน้านี้")
            elif msg.text.lower() == ".resetmention":
                dkey = mentmedat.pop(msg.to,None)
                cl.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงเรียบร้อยแล้ว")
#--------------------------------------------------------------------

            elif ".invitetocall" == msg.text.lower():
                cl.inviteIntoGroupCall(msg.to,[uid.mid for uid in cl.getGroup(msg.to).members if uid.mid != cl.getProfile().mid])
                cl.sendMessage(msg.to,"เชิญเข้าร่วมการโทรสำเร็จ(｀・ω・´)")

            elif ".kick" in msg.text.lower():
                if msg.contentMetadata is not None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.kickoutFromGroup(msg.to,[target])
                    else:
                        pass
#-----------------------------------------------------------
            elif ".ban " in msg.text.lower():
                if msg.toType == 2:
                    if msg.from_ in admin:
                       ban0 = msg.text.replace(".ban ","")
                       ban1 = ban0.lstrip()
                       ban2 = ban1.replace("@","")
                       ban3 = ban2.rstrip()
                       _name = ban3
                       gs = cl.getGroup(msg.to)
                       targets = []
                       for s in gs.members:
                           if _name in s.displayName:
                              targets.append(s.mid)
                       if targets == []:
                           cl.sendText(msg.to,"Error")
                           pass
                       else:
                            for target in targets:
                                try:
                                    wait["blacklist"][target] = True
                                    f=codecs.open('st2__b.json','w','utf-8')
                                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"ヽ( ^ω^)ﾉ succes")
                                except:
                                    cl.sendText(msg.to,"ヽ( ^ω^)ﾉ succes")
#--------------------------------------------------------------------
            elif "Hhx1:" in msg.text:
                c = msg.text.replace("Hhx1:","")
                if c in [""," ","\n",None]:
                    cl.sendMessage(msg.to,"เกิดข้อผิดพลาด..!!")
                else:
                    wait["acomment"] = c
                    cl.sendMessage(msg.to,"➠ ตั้งค่าข้อความต้อนรับ👌\n\n" + c)

            elif "Hhx2:" in msg.text:
                c = msg.text.replace("Hhx2:","")
                if c in [""," ","\n",None]:
                    cl.sendMessage(msg.to,"เกิดข้อผิดพลาด..!!")
                else:
                    wait["bcomment"] = c
                    cl.sendMessage(msg.to,"➠ ตั้งค่าข้อความกล่าวถึงคนออกจากกลุ่ม👌\n\n" + c)

            elif "Hhx3:" in msg.text:
                c = msg.text.replace("Hhx3:","")
                if c in [""," ","\n",None]:
                    cl.sendMessage(msg.to,"เกิดข้อผิดพลาด..!!")
                else:
                    wait["ccomment"] = c
                    cl.sendMessage(msg.to,"➠ ตั้งค่าข้อความกล่าวถึงคนลบสมาชิก👌\n\n" + c)

            elif msg.text.lower() == ["hhx1 on"]:
                if wait3["acommentOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ เปิดข้อความต้อนรับเเล้ว👌")
                    else:
                        cl.sendMessage(msg.to,"Already on")
                else:
                    wait3["acommentOn"] = True
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ เปิดข้อความต้อนรับเเล้ว👌")
                    else:
                        cl.sendMessage(msg.to,"Already on")
            elif msg.text in ["Hhx2 on"]:
                if wait3["bcommentOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ เปิดข้อความกล่าวถึงคนออกจากกลุ่ม👌")
                    else:
                        cl.sendMessage(msg.to,"Already on")
                else:
                    wait["bcommentOn"] = True
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ เปิดข้อความกล่าวถึงคนออกจากกลุ่ม👌")
                    else:
                        cl.sendMessage(msg.to,"Already on")

            elif msg.text in ["Hhx3 on"]:
                if wait3["ccommentOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ เปิดข้อความกล่าวถึงคนลบสมาชิก👌")
                    else:
                        cl.sendMessage(msg.to,"Already on")
                else:
                    wait["ccommentOn"] = True
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ เปิดข้อความกล่าวถึงคนลบสมาชิก👌")
                    else:
                        cl.sendMessage(msg.to,"Already on")

            elif msg.text in ["Hhx1 off"]:
                if wait3["acommentOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ ปิดข้อความต้อนรับเเล้ว👌")
                    else:
                        cl.sendMessage(msg.to,"Already off")
                else:
                    wait3["acommentOn"] = False
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ ปิดข้อความต้อนรับเเล้ว👌")
                    else:
                        cl.sendMessage(msg.to,"Already off")
            elif msg.text in ["Hhx2 off"]:
                if wait3["bcommentOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ ปิดข้อความกล่าวถึงคนออกจากกลุ่ม👌")
                    else:
                        cl.sendMessage(msg.to,"Already off")
                else:
                    wait3["bcommentOn"] = False
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ ปิดข้อความกล่าวถึงคนออกจากกลุ่ม👌")
                    else:
                        cl.sendMessage(msg.to,"Already off")
            elif msg.text in ["Hhx3 off"]:
                if wait3["ccommentOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ ปิดข้อความกล่าวถึงคนลบสมาชิก👌")
                    else:
                        cl.sendMessage(msg.to,"Already off")
                else:
                    wait3["ccommentOn"] = False
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"➠ ปิดข้อความกล่าวถึงคนลบสมาชิก👌")
                    else:
                        cl.sendMessage(msg.to,"Already off")
#--------------------------------------------------------------------
            elif msg.text.lower() == ".tagmessage on":
                if wait3["MasterBeach"] == True:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"tag already on")

            elif msg.text.lower() == ".tagmessage off":
                if wait3["MasterBeach"] == False:
                    if wait["lang"] == "JP":
                        cl.sendMessage(msg.to,"tag already off")
#___________________________________________________________
            elif ".uid " in msg.text.lower():
                if msg.toType == 2:
                    red = re.compile(re.escape('.uid '),re.IGNORECASE)
                    namel = red.sub('',msg.text)
                    namel = namel.lstrip()
                    namel = namel.replace(" @","$spliter$")
                    namel = namel.replace("@","")
                    namel = namel.rstrip()
                    namel = namel.split("$spliter$")
                    gmem = cl.getGroup(msg.to).members
                    for targ in gmem:
                        if targ.displayName in namel:
                            cl.sendMessage(msg.to,targ.displayName+": "+targ.mid)
                        else:
                            pass
#___________________________________________________________
            elif "unban " in msg.text.lower():
               if msg.toType == 2:
                  if msg.from_ in admin:
                       unb0 = msg.text.replace("unban ","")
                       unb1 = unb0.lstrip()
                       unb2 = unb1.replace("@","")
                       unb3 = unb2.rstrip()
                       x_name = unb3
                       gs = cl.getGroup(msg.to)
                       targets = []
                       for s in gs.members:
                           if x_name in s.displayName:
                              targets.append(s.mid)
                       if targets == []:
                           cl.sendText(msg.to,"user does not exist")
                           pass
                       else:
                            for target in targets:
                                try:
                                    del wait["blacklist"][target]
                                    f=codecs.open('st2__b.json','w','utf-8')
                                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"succes ヽ( ^ω^)ﾉ")
                                except:
                                    cl.sendText(msg.to,"succes ヽ( ^ω^)ﾉ")
#-----------------------------------------------------------
            elif msg.text.lower() == [".deletechat"]:
                cl.removeAllMessages(op.param2)
                cl.sendText(msg.to,"ทำการลบแชทบอทเรียบร้อย (｀・ω・´)")
#-----------------------------------------------------------
            elif msg.text.lower() == "conban":
                if wait["blacklist"] == {}:
                    cl.sendText(msg.to,"ɴᴏ ᴍᴇᴍʙᴇʀ ʟɪsᴛ")
                else:
                    cl.sendText(msg.to,"ᴍᴇᴍʙᴇʀ ʙʟᴀᴄᴋʟɪsᴛ")
                    h = ""
                    for i in wait["blacklist"]:
                        h = cl.getContact(i)
                        M = Message()
                        M.to = msg.to
                        M.contentType = 13
                        M.text = None
                        M.contentMetadata = {'mid': i}
                        cl.sendMessage(M)
#----------------------------------------------------------
            elif "ban" == msg.text.lower():
                wait["wblacklist"] = True
                cl.sendText(msg.to,"ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴄᴏɴᴛᴀᴄᴛ")
            elif "unban" == msg.text.lower():
                wait["dblacklist"] = True
                cl.sendText(msg.to,"ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴄᴏɴᴛᴀᴄᴛ")

            elif msg.text.lower == "banlist":
                if wait["blacklist"] == {}:
                    cl.sendText(msg.to,"ɴᴏ ᴍᴇᴍʙᴇʀs ʟɪsᴛ")
                else:
                    cl.sendText(msg.to,"ʙᴇʟᴏᴡ ɪs ᴀ ʙʟᴄᴋʟɪsᴛ")
                    mc = ""
                    for mi_d in wait["blacklist"]:
                        mc += "・" +cl.getContact(mi_d).displayName + "\n"
                    cl.sendText(msg.to,mc)
#-------------------------------------------------------------------------------
            elif msg.text.lower() == ["killban"]:
                if msg.toType == 2:
                    group = aa.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in wait["blacklist"]:
                        matched_list+=[str for str in gMembMids if str == tag]
                    if matched_list == []:
                        aa.sendText(msg.to,"There wasn't a blacklist user。")
                        return
                    for jj in matched_list:
                        try:
                            klist=[cl,aa,ab,ac,ad,ae]
                            kicker=random.choice(klist)
                            kicker.kickoutFromGroup(msg.to,[jj])
                            print((msg.to,[jj]))
                        except:
                            pass
#--------------------------------------------------------------------
            elif ".talk " in msg.text.lower():
                data = re.split(".talk ",msg.text,flags=re.IGNORECASE)
                tl = "th-TH"
                if data[0] == "":
                    if msg.toType != 0:
                        cl.sendAudioWithURL(msg.to,"http://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&textlen=32&client=tw-ob&q="+data[1]+"&tl="+tl)
                    else:
                        cl.sendAudioWithURL(msg._from,"http://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&textlen=32&client=tw-ob&q="+data[1]+"&tl="+tl)
#--------------------------------------------------------------------
            elif msg.text.lower() == ".uptime":
                cl.sendMessage(msg.to,str(datetime.now() - start_runtime)[:-7].split(":")[0]+" hour, "+str(datetime.now() - start_runtime)[:-7].split(":")[1]+" minute, "+str(datetime.now() - start_runtime)[:-7].split(":")[2]+" second,")

            elif ".bash " in msg.text.lower():
                    spl = re.split(".bash ",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                        try:
                            cl.sendMessage(msg.to,subprocess.getoutput(spl[1]))
                        except:
                            pass
#--------------------------------------------------------------------
            elif msg.text.lower() == ".virus":
                msg.contentType = 13
                msg.text = None
                msg.contentMetadata = {'mid': msg.to+"',"}
                cl.sendMessage(msg)
#--------------------------------------------------------------------
            elif ".info " in msg.text.lower():
                spl = re.split(".info ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                    for i in range(len(prov)):
                         uid = prov[i]["M"]
                         userData = cl.getContact(uid)
                         try:
                             cl.sendImageWithURL(msg.to,"http://dl.profile.line.naver.jp/"+userData.pictureStatus)
                         except:
                             pass
                         cl.sendMessage(msg.to,"ชื่อที่แสดง: "+userData.displayName)
                         cl.sendMessage(msg.to,"ข้อความสเตตัส:\n"+userData.statusMessage)
                         cl.sendMessage(msg.to,"ไอดีบัญชี: "+userData.mid)
                         cl.sendContact(msg.to,userData.mid)
#-------------------------------------------------------------------
            elif ".url " in msg.text.lower():
                spl = re.split(".url ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    try:
                        cl.sendMessage(msg.to,"http://line.me/R/ti/g/"+str(cl.reissueGroupTicket(spl[1])))
                    except:
                        cl.sendMessage(msg.to,"พบข้อผิดพลาด")
#--------------------------------------------------------------------
            elif ".tx:" in msg.text.lower():
                spl = re.split(".tx:",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    cl.kedapkedip(msg.to,spl[1])
            elif ".time" == msg.text.lower():
                    cl.sendMessage(msg.to,datetime.today().strftime('%H:%M:%S'))
#--------------------------------------------------------------------
            elif ".me " in msg.text.lower():
                spl = re.split(".me ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                    for i in range(len(prov)):
                        uid = prov[i]["M"]
                        userData = cl.getContact(uid)
                        try:
                            cl.sendMessage(msg.to,"กำลังดำเนินการดึงข้อมูลติดต่อ(｀・ω・´)")
                        except:
                            pass
                        cl.sendContact(msg.to,userData.mid)
#--------------------------------------------------------------------
            elif msg.text.lower() == ".gcreator":
                ginfo = cl.getGroup(msg.to)
                gCreator = ginfo.creator.mid
                cl.sendContact(msg.to,gCreator)
#--------------------------------------------------------------------
            elif ".covergroup" == msg.text.lower():
                thisgroup = cl.getGroups([msg.to])
                Mids = [contact.mid for contact in thisgroup[0].members]
                mi_d = Mids[:33]
                cl.createGroup("•─ ͜͡ᴛᴇᴀᴍ ᴛᴇsᴛ ʙᴏᴛ͜͡ ─•", mi_d)
                cl.sendMessage(msg.to,"Succes")
#--------------------------------------------------------------------
            elif ".bye " in msg.text.lower():
                if msg.toType == 2:
                    prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                    allmid = [msg.con]
                    for i in range(len(prov)):
                        cl.kickoutFromGroup(msg.to,[prov[i]["M"]])
                        allmid.append(prov[i]["M"])
                    cl.findAndAddContactByMetaTag(allmid)
                    cl.inviteIntoGroup(msg.to,allmid)
                    cl.cancelGroupInvitation(msg.to,allmid)
#-----------------------------------------------------------
            elif "|" in msg.text.lower():
                    spl = msg.text.split("|")
                    if spl[len(spl)-1] == "":
                        cl.sendMessage(msg.to,"กดที่นี่เพื่อเขย่า:\nline://nv/chatMsg?chatId="+msg.to+"&messageId="+msg.id)
#-----------------------------------------------
            elif ".grouppict" == msg.text.lower():
                 group = cl.getGroup(msg.to)
                 path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                 cl.sendImageWithURL(msg.to,path)

            elif ".speed"  == msg.text.lower():
                start = time.time()
                cl.sendMessage(msg.to, "sᴘᴇᴇᴅʙᴏᴛ....")
                elapsed_time = time.time() - start
                cl.sendMessage(msg.to,str(elapsed_time))
#-------------------------------------------------------------------
            elif msg.text.lower() == ".save":
                me = cl.getProfile()
                save1["displayName"] = me.displayName
                save1["statusMessage"] = me.statusMessage
                save1["pictureStatus"] = me.pictureStatus
                save1["Saved"] = True
                cl.sendMessage(msg.to,"บันทึกสถานะบัญชีเรียบร้อยแล้ว")
 #-------------------------------------------------------------------
            elif msg.text.lower() == ".load":
                if save1["Saved"]:
                    me = cl.getProfile()
                    me.displayName = save1["displayName"]
                    me.statusMessage = save1["statusMessage"]
                    me.pictureStatus = save1["pictureStatus"]
                    cl.updateProfileCoverById(me.pictureStatus)
                    cl.updateProfile(me)
                    cl.sendMessage(msg.to,"โหลดสถานะบัญชีเรียบร้อยแล้ว(｀・ω・´)")
                else:
                    cl.sendMessage(msg.to,"ก่อนหน้านี้ยังไม่ได้มีการบันทึกสถานะบัญชี(｀・ω・´)")
 #-------------------------------------------------------------------
            elif msg.text.lower() == ".copy":
                if msg.toType == 0:
                    targ = cl.getContact(mid)
                    me = cl.getProfile()
                    me.displayName = targ.displayName
                    me.statusMessage = targ.statusMessage
                    me.pictureStatus = targ.pictureStatus
                    cl.getProfileCoverById(me.pictureStatus)
                    cl.updateProfile(me)
                    cl.sendMessage(msg.to,"สำเร็จแล้ว")
                else:
                    cl.sendMessage(msg.to,"คำสั่งนี้ใช้ได้เฉพาะในแชทส่วนตัวเท่านั้น")
#--------------------------------------------------------------------
            elif ".copy " in msg.text.lower():
                if msg.toType == 2:
                    red = re.compile(re.escape('.copy '),re.IGNORECASE)
                    tname = red.sub('',msg.text)
                    tname = tname.lstrip()
                    tname = tname.replace(" @","$spliter$")
                    tname = tname.rstrip()
                    tname = tname.split("$spliter$")
                    tname = tname[0]
                    tname = tname[1:]
                    clist = {
                        "Founded":False,
                        "displayName":"",
                        "statusMessage":"",
                        "pictureStatus":""
                    }
                    mems = cl.getGroup(msg.to).members
                    for targ in mems:
                        if targ.displayName == tname:
                            clist["displayName"] = targ.displayName
                            clist["statusMessage"] = targ.statusMessage
                            clist["pictureStatus"] = targ.pictureStatus
                            clist["Founded"] = True
                    if clist["Founded"]:
                        me = cl.getProfile()
                        me.displayName = clist["displayName"]
                        me.statusMessage = clist["statusMessage"]
                        me.pictureStatus = clist["pictureStatus"]
                        cl.updateProfile(me.pictureStatus)
                        cl.updateProfile(me)
                        cl.sendMessage(msg.to,"สำเร็จแล้ว")
 #-------------------------------------------------------------------
            elif ".pict " in msg.text.lower():
                if msg.toType == 2:
                    red = re.compile(re.escape('.pict '),re.IGNORECASE)
                    namel = red.sub('',msg.text)
                    namel = namel.lstrip()
                    namel = namel.replace(" @","$spliter$")
                    namel = namel[1:]
                    namel = namel.rstrip()
                    namel = namel.split("$spliter$")
                    gmem = cl.getGroup(msg.to).members
                    for targ in gmem:
                        if targ.displayName in namel:
                            if targ.displayName != '':
                                cl.sendMessage(msg.to,targ.displayName)
                            try:
                                cl.sendImageWithURL(msg.to,"http://dl.profile.line.naver.jp/"+targ.pictureStatus)
                            except:
                                pass
 #-------------------------------------------------------------------
            elif ".home " in msg.text.lower():
                if LINE != None:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', msg.text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = cl.getProfileCoverURL(ls)
                            cl.sendImageWithURL(msg.to, str(path))
#--------------------------------------------------------------------
            elif ".set on" == msg.text.lower():
                if msg.to in wait2['readPoint']:
                        try:
                            del wait2['readPoint'][msg.to]
                            del wait2['readMember'][msg.to]
                            del wait2['setTime'][msg.to]
                        except:
                            pass
                        wait2['readPoint'][msg.to] = msg.id
                        wait2['readMember'][msg.to] = ""
                        wait2['setTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        wait2['ROM'][msg.to] = {}
                        with open('sider.json', 'w') as fp:
                         json.dump(wait2, fp, sort_keys=True, indent=4)
                         cl.sendMessage(msg.to,"Reading already on\nเปิดการอ่านอัตโนมัต")
                else:
                    try:
                            del wait2['readPoint'][msg.to]
                            del wait2['readMember'][msg.to]
                            del wait2['setTime'][msg.to]
                    except:
                          pass
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                    wait2['ROM'][msg.to] = {}
                    with open('sider.json', 'w') as fp:
                     json.dump(wait2, fp, sort_keys=True, indent=4)
                     cl.sendMessage(msg.to, "เปิดการอ่านอัตโนมัต\nSet reading point:\n" + datetime.now().strftime('%H:%M:%S'))
#--------------------------------------------------------------------
            elif ".set off" == msg.text.lower():
                if msg.to not in wait2['readPoint']:
                    cl.sendMessage(msg.to,"Reading already off\nปิดการอ่านอัตโนมัต")
                else:
                    try:
                            del wait2['readPoint'][msg.to]
                            del wait2['readMember'][msg.to]
                            del wait2['setTime'][msg.to]
                    except:
                          pass
                    cl.sendMessage(msg.to, "ปิดการอ่านอัตโนมัต\nDelete reading point:\n" + datetime.now().strftime('%H:%M:%S'))
#--------------------------------------------------------------------
            elif ".whoread" == msg.text.lower():
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                             cl.sendText(msg.to, "Reading:\nNone")
                        else:
                            chiya = []
                            for rom in wait2["ROM"][msg.to].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya)
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = 'Lurkers:\n'
                        for x in range(len(cmem)):
                                xname = str(cmem[x].displayName)
                                pesan = ''
                                pesan2 = pesan+"@a\n"
                                xlen = str(len(zxc)+len(xpesan))
                                xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                                zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                                zx2.append(zx)
                                zxc += pesan2
                                msg.contentType = 0

                        msg.text = xpesan+ zxc + "\nReading time: %s\nCurrent time: %s"%(wait2['setTime'][msg.to],datetime.now().strftime('%H:%M:%S'))
                        lol ={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                        msg.contentMetadata = lol
                        try:
                          cl.sendMessage(msg.to, msg.text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except:
                            traceback.print_exc()
                        pass
                    else:
                        cl.sendMessage(msg.to, "Reading has not been set.")
#--------------------------------------------------------------------
        if op.type == 19:
            try:
                if op.param3 == mid:
                    if op.param2 == helper1:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = aa.getGroup(op.param1)

                        aa.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)

                if op.param3 == mid:
                    if op.param2 == helper2:
                        G = ab.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ab.updateGroup(G)
                    else:
                        G = ab.getGroup(op.param1)

                        ab.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)

                if op.param3 == mid:
                    if op.param2 == helper3:
                        G = ac.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                    else:
                        G = ac.getGroup(op.param1)

                        ac.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)

                if op.param3 == mid:
                    if op.param2 == helper4:
                        G = ad.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ad.updateGroup(G)
                    else:
                        G = ad.getGroup(op.param1)

                        ad.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)

                if op.param3 == mid:
                    if op.param2 == helper5:
                        G = ad.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)
                    else:
                        G = ad.getGroup(op.param1)

                        ad.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)

                if op.param3 == helper1:
                    if op.param2 == helper2:
                        G = ab.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ab.getGroup(op.param1)

                        ab.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        aa.updateGroup(G)

                if op.param3 == helper2:
                    if op.param2 == helper1:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = aa.getGroup(op.param1)

                        aa.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ab.updateGroup(G)

                if op.param3 == helper2:
                    if op.param2 == helper3:
                        G = ac.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ac.getGroup(op.param1)

                        ac.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ab.updateGroup(G)

                if op.param3 == helper3:
                    if op.param2 == helper2:
                        G = ab.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ab.getGroup(op.param1)

                        ab.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)

                if op.param3 == helper3:
                    if op.param2 == helper4:
                        G = ad.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ad.updateGroup(G)
                    else:
                        G = ad.getGroup(op.param1)

                        ad.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)

                if op.param3 == helper4:
                    if op.param2 == helper3:
                        G = ac.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                    else:
                        G = ac.getGroup(op.param1)

                        ac.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ad.updateGroup(G)

                if op.param3 == helper4:
                    if op.param2 == helper5:
                        G = ae.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ae.updateGroup(G)
                        Ticket = ae.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)
                    else:
                        G = ae.getGroup(op.param1)

                        ae.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ae.updateGroup(G)
                        Ticket = ae.reissueGroupTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ad.updateGroup(G)

                if op.param3 == helrpe5:
                    if op.param2 == mid:
                        G = cl.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1)
                        aa.acceptGroupInvitationByTicket(op.param1)
                        ab.acceptGroupInvitationByTicket(op.param1)
                        ac.acceptGroupInvitationByTicket(op.param1)
                        ad.acceptGroupInvitationByTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = cl.getGroup(op.param1)

                        cl.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)
            except:
                pass

        if op.type == 19:
            try:
                if op.param3 in mid:
                    if op.param2 in helper1:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = aa.getGroup(op.param1)                        

                        aa.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        aa.updateGroup(G)
                        wait["blacklist"][op.param2] = False

                if op.param3 in mid:
                    if op.param2 in helper2:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ab.getGroup(op.param1)                        

                        ab.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ab.updateGroup(G)
                        wait["blacklist"][op.param2] = False

                if op.param3 in mid:
                    if op.param2 in helper3:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ac.getGroup(op.param1)                        

                        aa.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                        wait["blacklist"][op.param2] = False

                if op.param3 in mid:
                    if op.param2 in helper4:
                        G = ad.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ad.getGroup(op.param1)                        

                        ad.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ad.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ad.updateGroup(G)
                        wait["blacklist"][op.param2] = False

                if op.param3 in mid:
                    if op.param2 in helper5:
                        G = ae.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ae.updateGroup(G)
                        Ticket = ae.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = aa.getGroup(op.param1)                        

                        ae.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ae.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        KAC = [cl,aa,ab,ac,ad,ae]
                        KAC.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)
                        wait["blacklist"][op.param2] = False

                elif op.param3 in op.param3:
                    if op.param1 in protection:
                        bot_01 = [cl,aa,ab,ac,ad,ae]
                    if op.param2 in KAC:
                        bot_01 = [cl,aa,ab,ac,ad,ae]
                        KAC = random.choice(bot_01)
                        G = random.choice(KAC).getGroup(op.param1)
                        G.preventJoinByTicket = False
                        random.choice(KAC).updateGroup(G)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        random.choice(KAC).updateGroup(G)
                    else:
                        G = random.choice(KAC).getGroup(op.param1)

                        random.choice(KAC).kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        random.choice(KAC).updateGroup(G)
                        Ticket = random.choice(KAC).reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        random.choice(KAC).updateGroup(G)

                        wait["blacklist"][op.param2] = True
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)

                elif op.param3 in helper1:
                    if op.param2 in mid:
                        G = cl.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = cl.getGroup(op.param1)


                        cl.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                        wait["blacklist"][op.param2] = False
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)            
            except:
                pass

        if op.type == 19:
            try:
                if op.param3 in helper1:
                    if op.param2 in mid:
                        G = cl.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = cl.getGroup(op.param1)

                        
                        cl.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)


                elif op.param3 in mid:
                    if op.param2 in helper1:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        aa.updateGroup(G)
                    else:
                        G = aa.getGroup(op.param1)

                        
                        aa.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        aa.updateGroup(G)
                        wait["blacklist"][op.param2] = False
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)            
            except:
                pass
                
        if op.type == 19:
            try:
                if op.param3 in helper1:
                    if op.param2 in helper1:
                        G = ks.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ks.updateGroup(G)
                        Ticket = ks.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ks.updateGroup(G)
                    else:
                        G = ks.getGroup(op.param1)

                        
                        ae.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ks.updateGroup(G)
                        Ticket = ks.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)

                        
                elif op.param3 in helper2:
                    if op.param2 in helper2:
                        G = ab.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ab.updateGroup(G)
                    else:
                        G = ab.getGroup(op.param1)

                        ab.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ab.updateGroup(G)
                        Ticket = ab.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ab.updateGroup(G)
                        wait["blacklist"][op.param2] = False
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)            
            except:
                pass
                
        if op.type == 19:
            try:
                if op.param3 in helper1:
                    if op.param2 in helper2:
                        if op.param2 in helper3:
                            if op.param2 in helper4:
                                G = ab.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        cl.updateGroup(G)
                    else:
                        G = ab.getGroup(op.param1)

                        
                        ab.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        cl.updateGroup(G)
                        Ticket = cl.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        cl.updateGroup(G)

                elif op.param3 in helper5:
                    if op.param2 in helper1:
                        G = aa.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        aa.updateGroup(G)
                    else:
                        G = aa.getGroup(op.param1)

                        aa.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        aa.updateGroup(G)
                        Ticket = aa.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        aa.updateGroup(G)
                        
                elif op.param3 in helper4:
                    if op.param2 in helper5:
                        G = ka.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ka.updateGroup(G)
                        Ticket = ka.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)
                    else:
                        G = ae.getGroup(op.param1)

                        
                        ae.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ae.updateGroup(G)
                        Ticket = ae.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ae.updateGroup(G)

                elif op.param3 in helper2:
                    if op.param2 in helper3:
                        G = ac.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                    else:
                        G = ac.getGroup(op.param1)

                        
                        ac.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                        wait["blacklist"][op.param2] = False
                        f=codecs.open('st2__b.json','w','utf-8')
                        json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)            
            except:
                pass

        if op.type == 19:
            try:
                if op.param3 in mid:
                    if op.param2 in helper3:
                        G = ac.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                    else:
                        G = ac.getGroup(op.param1)

                        ac.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ac.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)

                elif op.param3 in helper3:
                    if op.param2 in mid:
                        G = ad.getGroup(op.param1)
                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
                    else:
                        G = ad.getGroup(op.param1)

                        ad.kickoutFromGroup(op.param1,[op.param2])

                        G.preventJoinByTicket = False
                        ac.updateGroup(G)
                        Ticket = ad.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        aa.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ab.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ac.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ad.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ae.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.preventJoinByTicket = True
                        ac.updateGroup(G)
            except KeyboardInterrupt as e:
                raise e
            except:
                traceback.print_exc()
#------------------------------------------------------------------------------------
        if op.type == 55:
            try:
                if op.param1 in wait2 ['readPoint']:
                    if op.param2 in wait2 ['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += op.param2
                    wait2['ROM'][op.param1][op.param2] = op.param2
                    with open('sider.json', 'w') as fp:
                        json.dump(wait2, fp, sort_keys=True, indent=4)
                else:
                    pass
            except:
                pass

#-----------------------------------------------------------
        if op.type == 59:
            print(op)

    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        traceback.print_exc()

try:
    def autoSta():
        count = 1
        while True:
            try:
               for posts in cl.activity(1)["result"]["posts"]:
                 if posts["postInfo"]["liked"] is False:
                    if wait["likeOn"] == True:
                       cl.like(posts["userInfo"]["writerMid"], posts["postInfo"]["postId"], 1001)
                       if wait["commentOn"] == True:
                          if posts["userInfo"]["writerMid"] in wait["commentBlack"]:
                             pass
                          else:
                              cl.comment(posts["userInfo"]["writerMid"],posts["postInfo"]["postId"],wait["comment"])
            except:
                count += 1
                if(count == 50):
                    sys.exit(0)
                else:
                    pass
    thread1 = threading.Thread(target=autoSta)
    thread1.daemon = True
    thread1.start()
except:
    pass

def a2():
    now2 = datetime.datetime.now()
    nowT = datetime.datetime.strftime(now2,"%M")
    if nowT[14:] in ["10","20","30","40","50","00"]:
        return False
    else:
        return True

try:
    while True:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                bot(op)
                oepoll.setRevision(op.revision)
except:
    traceback.print_exc()
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,save1], f)
