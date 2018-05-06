# -*- coding: utf-8 -*-

from linepy import *
from akad import *
import traceback
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, urllib, urllib,pickle
from datetime import datetime
from random import randint

print("""

\033["""+str(randint(0,1))+""";"""+str(randint(31,36))+"""mplay free\nby beach noxtian\033[0m

""")

with open('tval.pkl', 'rb') as f:
    [cltoken,wait] = pickle.load(f,encoding='latin1')

if len(sys.argv) == 2 and sys.argv[1] == "reset":
    cltoken = ""
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,wait], f)
    os._exit(0)

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


user1 = cl.profile.mid
admin = OEPoll(cl)

start_runtime = datetime.now()

wait = {
    'alwayread':False,
    'autoBlock':False,
    'welcomepic':False,
    'welcomemessage':False,
    'autoadd':False,
    'messageadd':"",
    'autotag':False,
    'tagmessage':"",
}

userhelp = """╠✪➥〘THAILAND BoT LiNE〙
╠✪〘 รายการทั้งหมด〙✪══
╠➥menu
╠➥mid
╠➥me
╠➥myname
╠➥speed
╠➥name
╠➥.kick (@)
╠➥uid (@)
╠➥danyall [text]
╠➥mentionall
╠➥invitetocall
╠➥uptime
╠➥remember [1:2]
╠➥forget [1]
╠➥forgetall
╠➥autodeny off
╠➥autodeny [numbers]
╠➥autoread on/off
╠➥autoblock on/off
╠➥welmes on/off
╠➥welcomeset:[text]
╠➥setmessageadd:[text]
╠➥tagmessage:
╠➥checkmention
╠➥autoadd on/off
╠✪════════
╠✪➥〘THAILAND BoT LiNE〙"""

procLock = 0
mentmedat = {}
respRemember = {}

def user1scipt(op):
    global startruntime
    global user1
    global wait
    global alwayread
    global autoBlock
    global welcomepic
    global welcomemessage
    global autoadd
    global messageadd
    global autotag
    global tagmessage
    global autoDeny
    global procLock
    global mentmedat
    global respRemember
    try:
        if op.type == 0:
            return

        if op.type == 5:
            if wait['autoBlock'] == True:
                cl.blockContact(op.param1)

            if wait['autoadd'] == True:
                cl.findAndAddContactsByMid(op.param1)
                if (wait["messageadd"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendMessage(op.param1,str(wait["messageadd"]))

        if op.type ==13:
            invitor = op.param2
            gotinvite = []
            if "\x1e" in op.param3:
                gotinvite = op.param3.split("\x1e")
            else:
                gotinvite.append(op.param3)
            if invitor in user1 in gotinvite:
                cl.acceptGroupInvitation(op.param1)
            else:
                group = cl.getGroup(op.param1)
                if len(group.members) <= autoDeny:
                    procLock += 1
                    cl.acceptGroupInvitation(op.param1)
                    cl.leaveGroup(op.param1)

        if op.type == 17:
            if wait['welcomemessage'] and "welcomemessage" in wait:
               cnt = cl.getContact(op.param2)
               cl.sendMessage(op.param1,cnt.displayName + "\n" + str(wait["welcomemessage"]))

            if wait['welcomepic'] and "welcomepic" in wait:
                cnt = cl.getContact(op.param2)
                cl.sendImageWithURL(op.param1,"http://dl.profile.line.naver.jp/" + cnt.pictureStatus)

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
                                tagfrom = msg.from_
                                tagtime = nowS = datetime.strftime(datetime.now(),"%H:%M:%S")
                                tagid = msg.id
                                mentmedat[msg.to].append(
                                    {
                                        "tfrom" : tagfrom,
                                        "ttime" : tagtime,
                                        "tid" : tagid
                                    }
                                )
                 except:
                     pass

             if wait["alwayread"]:
                 cl.sendChatChecked(msg.from_,msg.id)
             else:
                 cl.sendChatChecked(msg.to,msg.id)

             if msg.to in respRemember and msg.text in respRemember[msg.to]:
                 if msg.toType != 0:
                     cl.sendMessage(msg.to,respRemember[msg.to][msg.text])
                 else:
                     cl.sendMessage(msg.from_,respRemember[msg.to][msg.text])

             if wait["tagmessage"] == True:
                 cl.sendMessage(msg.to)
                 if (wait["tagmessage"] in [""," ","\n",None]):
                     pass
                 else:
                     cl.sendMessage(msg.to,str(wait["tagmessage"]))

        if op.type == 25:
            msg = op.message
            if msg.text is None:
               return

            elif msg.text.lower() == "menu":
                cl.sendMessage(msg.to,userhelp)

            elif msg.text.lower() == "mid":
                cl.sendMessage(msg.to,user1)

            elif msg.text.lower() == "me":
                beach = user1
                cl.sendContact(msg.to,beach)

            elif msg.text.lower() == "myname":
                G = cl.getContact(user1)
                cl.sendMessage(msg.to,G.displayName)

            elif msg.text.lower() == "speed":
                start = time.time()
                cl.sendMessage(msg.to,"กำลังทดสอบ(｀・ω・´)")
                cl.sendMessage(msg.to,str(int(round((time.time() - start) * 1000)))+" ms")

            elif "name " in msg.text.lower():
                spl = re.split("name ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    prof = cl.getProfile()
                    prof.displayName = spl[1]
                    cl.updateProfile(prof)
                    cl.sendMessage(msg.to,"เปลี่ยนชื่อสำเร็จแล้ว(｀・ω・´)")

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

            elif "uid " in msg.text.lower():
                if msg.toType == 2:
                    red = re.compile(re.escape('uid '),re.IGNORECASE)
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

            elif "denyall" in msg.text.lower():
                 spl = re.split("denyall",msg.text,flags=re.IGNORECASE)
                 if spl[0] == "":
                     spl[1] = spl[1].strip()
                     ag = cl.getGroupIdsInvited()
                     txt = "กำลังยกเลิกค้างเชิญจำนวน "+str(len(ag))+"กลุ่ม"
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
                     cl.sendMessage(msg.to,"สำเร็จแล้ว(｀・ω・´)")

            elif "setmessageadd:" in msg.text.lower():
                wait['messageadd'] = msg.text.replace("setmessageadd:","")
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จ(｀・ω・´)")

            elif "tagmessage:" in msg.text.lower():
                wait['tagmessage'] = msg.text.replace("tagmessage:","")
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จ(｀・ω・´)")

            elif msg.text.lower().startswith("mentionall"):
                data = msg.text[len("mentionall"):].strip()
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
                       cl.sendMessage(msg.to, text=cb2,contentMetadata={u'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'},contentType=0)
                    except:
                       cl.sendMessage(msg.to,"[[NO MENTION]]")

            elif msg.text.lower() == "checkmention":
                if msg.to in mentmedat and mentmedat[msg.to] != []:
                    text = ""
                    for data in mentmedat[msg.to]:
                        print("555")
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
                    cl.sendMessage(msg.to,"ไม่มีการกล่าวถึงก่อนหน้านี้(｀・ω・´)")

            elif msg.text.lower() == "resetmention":
                dkey = mentmedat.pop(msg.to,None)
                cl.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงเรียบร้อยแล้ว")


            elif msg.text.lower() == "resetallmention":
                mentmedat = {}
                cl.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงทั้งหมดแล้ว")
                
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
                        if ginfo.preventedJoinByTicket == True:
                            u = "ปิดอยู่"
                        else:
                            u = "เปิดอยู่"
                        cl.sendMessage(msg.to,"[ชื่อกลุ่ม]\n" + str(ginfo.name) + "\n\n[ไอดีกลุ่ม]\n" + msg.to + "\n\n[ผู้สร้างกลุ่ม]\n" + gCreator + "\n\n[รูปโปรไฟล์กลุ่ม]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\n\nสมาชิก:" + str(len(ginfo.members)) + " ท่าน\nเชิญ:" + sinvitee + " ท่าน\nURL:" + u + "")
                    else:
                        cl.sendMessage(msg.to,"[名字]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[小组的作成者]\n" + gCreator + "\n[小组图标]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    pass

            elif ".gid" == msg.text.lower():
                if msg.toType == 2:
                    cl.sendMessage(msg.to,msg.to)
                else:
                    cl.sendMessage(msg.to,"คำสั่งนี้ใช้ได้เฉพาะกลุ่ม(｀・ω・´)") 
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
                   if wait["autoBlock"] == True: md+="✔ ➡autoBlock  → on \n"
                   else:md+="✖ ➡autoBlock → off \n"
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
                cl.sendMessage(msg.to,"The message was changed。")
            elif "Auto addition→" in msg.text:
                wait["message"] = msg.text.replace("Auto addition→","")
                if wait["lang"] == "JP":
                    cl.sendMessage(msg.to,"The message was changed。")
                else:
                    cl.sendMessage(msg.to,"was change already。")
            elif msg.text in ["Message check","自動追加問候語確認"]:
                if wait["lang"] == "JP":
                    cl.sendMesaage(msg.to,".automatic message is established as follows。\n\n" + wait["message"])
                else:
                    cl.sendMessage(msg.to,"One  of weeds on the surface below the self- additional breath image。\n\n" + wait["message"])
            elif msg.text.lower() == ["CHANGE"]:
                if wait["lang"] =="JP":
                    wait["lang"] = "TW"
                    cl.sendMesaage(msg.to,"ƇƠƲƝƬƦƳ ԼƛƝƓƲƛƓЄ ƊƲƦƖƝƓ ƛ ƇHƛƝƓЄ。")
                else:
                    wait["lang"] = "JP"
                    cl.sendMessage(msg.to,". The language was made English。")
#--------------------------------------------------------
            elif msg.text.lower() == [".url"]:
                if msg.toType == 2:
                    x = cl.getGroup(msg.to)
                    if x.preventedJoinByTicket == True:
                        x.preventedJoinByTicket == False
                        cl.updateGroup(x)
                    gurl = reissueGroupTicket(msg.to)
                    cl.sendMessage(msg.to,"[Url]\nline://ti/g/" + gurl)
 #--------------------------------------------------------------------
            elif msg.text.lower() == ".uptime":
                cl.sendMessage(msg.to,str(datetime.now() - start_runtime)[:-7].split(":")[0]+" hour, "+str(datetime.now() - start_runtime)[:-7].split(":")[1]+" minute, "+str(datetime.now() - start_runtime)[:-7].split(":")[2]+" second,")
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
            elif msg.text.lower() == ".virus":
                msg.contentType = 13
                msg.text = None
                msg.contentMetadata = {'mid': msg.to+"',"}
                cl.sendMessage(msg)
#__________________________________________________________
            elif msg.text.startswith(".picturetext"):
                sep = msg.text.split(" ")
                textnya = msg.text.replace(sep[0] + " ","")
                picture = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                cl.sendImageWithURL(msg.to,picture)                

            elif "!sh " in msg.text.lower():
                spl = re.split("!sh ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    try:
                        cl.sendMessage(msg.to,subprocess.getoutput(spl[1]))
                    except:
                        pass

            elif msg.text.lower() == "invitetocall":
                exc = cl.getGroup(msg.to).members
                zxc = cl.getProfile().mid
                cl.inviteIntoGroupCall(msg.to,[uid.mid for uid in exc if uid.mid != zxc])
                cl.sendMessage(msg.to,"เชิญเข้าร่วมการคอลเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "uptime":
                cl.sendMessage(msg.to,str(datetime.now() - start_runtime)[:-7].split(":")[0]+" hour, "+str(datetime.now() - start_runtime)[:-7].split(":")[1]+" minute, "+str(datetime.now() - start_runtime)[:-7].split(":")[2]+" second,")

            elif msg.text.lower().startswith("remember "):
                data = msg.text[len("remember "):]
                keyword = data.split(":",1)[0]
                if keyword.lower().startswith("remember") or keyword.lower().startswith("!forget") or keyword in ["",None]:
                    raise ValueError
                response = data.split(":",1)[1]
                if response in ["",None]:
                    raise ValueError
                if msg.to not in respRemember:
                    respRemember[msg.to] = {}
                respRemember[msg.to][keyword] = response
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"%H")
                nowM = datetime.strftime(now2,"%M")
                nowS = datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                if msg.toType != 0:
                    cl.sendMessage(msg.to,"จำแล้ว (｀・ω・´)"+tm)
                else:
                    cl.sendMessage(msg._from,"จำแล้ว (｀・ω・´)"+tm)

            elif msg.text.lower().startswith("forget "):
                keyword = msg.text[len("forget "):]
                if keyword in ["",None]:
                    raise ValueError
                if msg.to in respRemember and keyword in respRemember[msg.to]:
                    dkey = respRemember[msg.to].pop(keyword,None)
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"%H")
                    nowM = datetime.strftime(now2,"%M")
                    nowS = datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    if msg.toType != 0:
                        cl.sendMessage(msg.to,"ลืมแล้ว (｀・ω・´)"+tm)
                    else:
                        cl.sendMessage(msg._from,"ลืมแล้ว (｀・ω・´)"+tm)
                else:
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"%H")
                    nowM = datetime.strftime(now2,"%M")
                    nowS = datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    if msg.toType != 0:
                        cl.sendMessage(msg.to,"ไม่สามารถลืมได้ (｀・ω・´)"+tm)
                    else:
                        cl.sendMessage(msg._from,"ไม่สามารถลืมได้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "forgetall":
                dkey = respRemember.pop(msg.to,None)
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"%H")
                nowM = datetime.strftime(now2,"%M")
                nowS = datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                if msg.toType != 0:
                    cl.sendMessage(msg.to,"ลืมทุกอย่างแล้ว (｀・ω・´)"+tm)
                else:
                    cl.sendMessage(msg.from_,"ลืมทุกอย่างแล้ว (｀・ω・´)"+tm)

            elif "welcomeset:" in msg.text.lower():
                 c = msg.text.replace("welcomemessage:","")
                 if c in [""," ","\n",None]:
                     cl.sendMessage(msg.to,"เกิดข้อผิดพลาด!!(｀・ω・´)")
                 else:
                     wait['welcomemessage'] = c
                     cl.sendMessage(msg.to,"ตั้งค่าข้อความสำเร็จแล้ว(｀・ω・´)")

            elif msg.text.lower() == "autodeny off":
                autoDeny = -1
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จแล้ว(｀・ω・´)")

            elif msg.text.lower().startswith("autodeny "):
               try:
                   autoDeny = int(msg.text[len(".autodeny "):])
                   cl.sendMessage(msg.to,"ตั้งค่าสำเร็จแล้ว(｀・ω・´)")
               except:
                   cl.sendMessage(msg.to,"พบข้อผิดพลาด(｀・ω・´)")

            elif msg.text.lower() == "autoread on":
                if wait["alwayread"] == True:
                    cl.sendMessage(msg.to,"เปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")
                    wait["alwayread"] = False
                else:
                    if wait["alwayread"] == False:
                        cl.sendMessage(msg.to,"เปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")

            elif msg.text.lower() == "autoread off":
                if wait["alwayread"] == False:
                    cl.sendMessage(msg.to,"ปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")
                    wait["alwayread"] = True
                else:
                    if wait["alwayread"] == True:
                        cl.sendMessage(msg.to,"ปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")

            elif msg.text.lower() == "autoblock on":
                if wait['autoBlock'] == True:
                    cl.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัตื(｀・ω・´)")
                    wait['autoBlock'] = False
                else:
                    if wait['autoBlock'] == False:
                        cl.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัตื(｀・ω・´)")

            elif msg.text.lower() == "autoblock off":
                if wait['autoBlock'] == False:
                    cl.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัตื(｀・ω・´)")
                    wait['autoBlock'] = True
                else:
                    if wait['autoBlock'] == True:
                        cl.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัตื(｀・ω・´)")

            elif msg.text.lower() == "welpic on":
                if wait['welcomepic'] == False:
                    cl.sendMessage(msg.to,"เปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")
                    wait['welcomepic'] = True
                else:
                    if wait['welcomepic'] == True:
                        cl.sendMessage(msg.to,"เปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "welpic off":
                if wait['welcomepic'] == True:
                    cl.sendMessage(msg.to,"ปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")
                    wait['welcomepic'] = False
                else:
                    if wait['welcomepic'] == False:
                        cl.sendMessage(msg.to,"ปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "welmes on":
                if wait['welcomemessage'] == False:
                    cl.sendMessage(msg.to,"เปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")
                    wait['welcomemessage'] = True
                else:
                    if wait['welcomemessage'] == True:
                        cl.sendMessage(msg.to,"เปิดระบบข้อความต้อนรับเรียบร้อยสำเร็จ...")

            elif msg.text.lower() == "welmes off":
                if wait['welcomemessage'] == True:
                    cl.sendMessage(msg.to,"ปิดระบบข้อความต้อนรับสำเร็จ..")
                    wait['welcomemessage'] = False
                else:
                    if wait['welcomemessage'] == False:
                        cl.sendMessage(msg.to,"ปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "autoadd on":
                if wait['autoadd'] == False:
                    cl.sendMessage(msg.to,"เปิดการรับเพื่อนอัตโนมัติสำเร็จ...")
                    wait['autoadd'] = True
                else:
                    if wait['autoadd'] == True:
                        cl.sendMessage(msg.to,"เปิดการรับเพื่อนอัตโนมัติสำเร็จ...")

            elif msg.text.lower() == "autoadd off":
                if wait['autoadd'] == True:
                    cl.sendMessage(msg.to,"ปิดการรับเพื่อนอัตโนมัติสำเร็จ...")
                    wait['auto'] = False
                else:
                    if wait['autoadd'] == False:
                        cl.sendMessage(msg.text,"ปิดการรับเพื่อนอัตโนมัติสำเร็จ...")

            elif msg.text.lower() == "autotag on":
                if wait['autotag'] == False:
                    cl.sendMessage(msg.to,"เปิดระบบตอบกลับเรียบร้อย...")
                    wait['autotag'] = True
                else:
                    if wait['autotag'] == True:
                        cl.sendMessage(msg.to,"เปิดระบบตอบกลับเรียบร้อย...")

            elif msg.text.lower() == "autotag off":
                if wait['autotag'] == True:
                    cl.sendMessage(msg.to,"ปิดระบบตอบกลับเรียบร้อย...")
                    wait['autotag'] = False
                else:
                    if wait['autotag'] == False:
                        cl.sendMessage(msg.to,"ปิดระบบตอบกลับเรียบร้อย...")
    except:
        traceback.print_exc()

try:
    while True:
        ops = admin.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                user1scipt(op)
                admin.setRevision(op.revision)
except:
    traceback.print_exc()
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,wait], f)
