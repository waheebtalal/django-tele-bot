from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.helper import *
import asyncio
from pyrogram.errors import FloodWait

##django
import os, django

from bot.helper.ffmpeg_utils import get_thumbnail, get_width_height, get_duration, encode

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db.settings")
#os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "True")
from db import settings

django.setup()
from TgUser.models import TgUser

q = []


async def FProgress(current, total, chatid, mesgid):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    # proc = "downloading \n" + (
    #        "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total)))
    #  if str(msg.text) != str(proc):
    try:
        await app.edit_message_text(chat_id=chatid, message_id=mesgid, text="جاري التنزيل ... \n" + (
                "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))
    except FloodWait as e:
        print("error download progress")
        await asyncio.sleep(e.value)


async def stats(out: str):
    try:
        ot = os.path.getsize("encode/" + out.split("-")[0] + "/" + out + '.HEVC' + '.mp4')
        oos = hbs(ot)
        ans = "جاري الضغط:" + " \n " + str(oos)
        return ans
    except:
        return "خطأ !!"


def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def UProgress(current: int, total, chatid, mesgid):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    #  progress = "uploading \n" + (
    #    "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total)))

    try:
        await app.edit_message_text(chat_id=chatid, message_id=mesgid, text="جاري الرفع ... \n" + (
                "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))
    except FloodWait as e:
        print("error upload progress")
        await asyncio.sleep(e.value)


async def add_queue(msg: []):
    print("add_queue")
    q.append(msg)
    print(msg)
    if len(q) == 1:
        await  enc(msg)


async def add_queue_admin(msg: []):
    print("add_queue_admin")
    print(msg)
    if len(q) != 0:
        q.insert(1, msg)
    else:
        q.append(msg)
    if len(q) == 1:
        await  enc(msg)


async def enc(ls: []):
    chatid = ls[0]
    msg_file = ls[1]
    msg_rep = ls[2]
    msg: Message = await app.get_messages(chatid, message_ids=msg_rep)
    file: Message = await app.get_messages(chatid, message_ids=msg_file)

    video_file = ""
    try:
        video_file = await file.download(file_name=str(file.chat.id) + "-" + str(file.id), progress=FProgress,
                                         progress_args=(msg.chat.id, msg.id))
        print(video_file)
        ttl = get_duration(video_file)
        print("ttl  :" + str(ttl))
        width_high = get_width_height(video_file)
        print("width_high :" + str(width_high))
        thumb = get_thumbnail(video_file, "thumbs//" + str(file.chat.id), 1)
        print("thumb :" + str(thumb))

        enpa = "encode/" + str(file.chat.id)
        os.makedirs(enpa, exist_ok=True)
        basefilepath, extension = os.path.splitext(video_file)
        print("basefilepath : " + basefilepath + " | extension : " + extension)
        output_filepath = basefilepath + '.HEVC' + '.mp4'
        output_filepath = str(output_filepath).replace("downloads", enpa)
        await msg.edit(text="جاري الضغط...", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="الحالة", callback_data=str(file.chat.id) + "-" + str(file.id))],
                 [InlineKeyboardButton(text="الغاء", callback_data="c:" + str(file.id))]]))

        # await msg.reply_text(text="Encoding", reply_markup=InlineKeyboardMarkup(
        #   [[InlineKeyboardButton(text="state", callback_data=output_filepath)]]))
        print("start enc")
        print(video_file)
        print(output_filepath)
        outfile = await encode(video_file, output_filepath)
        before = hbs(os.path.getsize(video_file))
        after = hbs(os.path.getsize(outfile))
        try:
            message = await app.send_video(msg.chat.id, outfile,
                                           progress=UProgress,
                                           progress_args=(msg.chat.id, msg.id)
                                           , duration=ttl
                                           , width=width_high[0]
                                           , height=width_high[1]
                                           , thumb=thumb
                                           , supports_streaming=True
                                           )
            if group != "":
                msg_forward = await  message.forward(chat_id=int(group))
                await msg_forward.reply(text=f"قبل: {before} \n بعد: {after}\n{msg.chat.id}\n{msg.chat.first_name}"
                                        ,
                                        quote=True
                                        )
        except FloodWait as e:
            print("send error")
            await asyncio.sleep(e.value)
            try:
                message = await app.send_video(msg.chat.id, outfile
                                               # , progress=UProgress
                                               # , progress_args=(msg)
                                               , duration=ttl
                                               , width=width_high[0]
                                               , height=width_high[1]
                                               , thumb=thumb
                                               , supports_streaming=True)
                if group != "":
                    msg_forward = await  message.forward(chat_id=int(group))
                    await msg_forward.reply(text=f"قبل: {before} \n بعد: {after}\n{msg.chat.id}\n{msg.chat.first_name}"
                                            ,
                                            quote=True
                                            )
            except FloodWait as ex:
                print("error send no progress")
                await asyncio.sleep(ex.value)

        try:
            await msg.edit(text=f"قبل: {before} \n بعد: {after}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await msg.reply_text(text=f"قبل: {before} \n بعد: {after}")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                print("error reply done")
            print("error edit done")
        os.remove(video_file)
        os.remove(outfile)
        os.remove(thumb)

    except Exception as en:
        print(str(en))

    pop()
    if len(q) > 0:
        await enc(q[0])


def pop():
    if len(q) != 0:
        q.pop(0)


def empty():
    q = []


def appen(nu, owner):
    if q.__contains__(nu):
        return "موجود بالفعل"
    else:
        if owner & len(q) != 0:
            q.insert(1, nu)
        else:
            q.append(nu)


def pop_index(index):
    q.pop(index)


def inde(msg):
    if q.__contains__(msg):
        return q.index(msg)
    else:
        return None


def kill_user(msg):
    ind = inde(msg)
    if not ind:
        return
    if ind == 0:
        kill()
    else:
        q.pop(ind)


def kill():
    os.system("kill $(pidof /usr/bin/ffmpeg)")

def Run_Server():
    os.system("gunicorn 'db.wsgi'")
def find(m):
    for a in q:
        if a[0] == m:
            return a

    return False


# django
async def ck_user(m: Message):
    if not TgUser.objects.filter(id=m.from_user.id).exists():
        tg_id = m.from_user.id
        username = m.from_user.username if m.from_user.username else " "
        name = ((m.from_user.first_name if m.from_user.first_name else " ") + (
            m.from_user.last_name if m.from_user.last_name else " "))
        phone = m.from_user.phone_number if m.from_user.phone_number else " "
        TgUser(id=tg_id, username=username,
                     name=name, phone=phone).save()


async def ck_block(m: Message):
    await ck_user(m)
    return TgUser.objects.filter(id=m.from_user.id).values('block').get()['block']


async def ck_admin(m: Message):
    await ck_user(m)
    return TgUser.objects.filter(id=m.from_user.id).values('admin').get()['admin']


async def ck_lim(m: Message):
    await ck_user(m)
    return m.video.duration > TgUser.objects.filter(id=m.from_user.id).values('long_lim').get()['long_lim']


async def gt_lim(m: Message):
    await ck_user(m)
    return TgUser.objects.filter(id=m.from_user.id).values('long_lim').get()['long_lim']


async def min_lim(m: Message):
    await ck_user(m)
    TgUser.objects.filter(id=m.from_user.id).update(
        long_lim=TgUser.objects.filter(id=m.from_user.id).values('long_lim').get()['long_lim'] - m.video.duration)


async def add_lim(id, lim):
    TgUser.objects.filter(id=id).update(
        long_lim=TgUser.objects.filter(id=id).values('long_lim').get()['long_lim'] + int(lim))
