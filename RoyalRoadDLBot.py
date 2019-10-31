import discord
from royalroadlapi import *
import os
from gtts import gTTS
import simpleaudio as sa
from pydub import AudioSegment
from random import randint
import logging
import asyncio

# remove old dependencies
# change discord.py ti new version

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = discord.Client()

async def download_fiction_async(message,fiction_term,start_chapter="start",end_chapter="end"):
    final_location = get_fiction(fiction_term,directory="Fiction - Epubs/",start_chapter=start_chapter,end_chapter=end_chapter)
    if final_location != None:
        title_name = final_location.split("/")[-1].replace(".epub","")
        msg = '{0.author.mention}'.format(message) + str(' Downloaded ***{}*** Successfully!'.format(title_name))
        await client.send_message(message.channel, msg)
        print("Uploading File {}".format(final_location))
        await client.send_file(message.channel, final_location)
        flag_upload = True
    else:
        print("Error")
        flag_error = True
        msg = '{0.author.mention} There are no chapters for that fiction (or maybe in that range)!'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_message(message):
    global final_location
    #don't reply to own messages
    if message.author == client.user:
        return
    if message.content.startswith('!cached'):
        print(str(message.author)+":",message.content)
        flag_upload = False
        flag_error = False
        try:
            fiction_term = " ".join(message.content.split(" ")[1:])
            try:
                chapters = " ".join(message.content.split(" ")[-1:]) #don't include the other stuff
                try:
                    temp = " ".join(message.content.split(" ")[-2:-1])
                    if temp == "!req":
                        end_chapter = "end"
                        start_chapter = "start"
                        end_chapter_flag = False
                        start_chapter_flag = False
                    else:    
                        chapters = chapters.split("-")
                        try:
                            end_chapter = int(chapters[1])
                            end_chapter_flag = True
                        except:
                            end_chapter_flag = False
                            end_chapter = "end"
                        try:
                            start_chapter = int(chapters[0])
                            start_chapter_flag = True
                        except:
                            start_chapter = "start"
                            start_chapter_flag = False
                        if end_chapter_flag or start_chapter_flag:
                            fiction_term = " ".join(fiction_term.split(" ")[:-1])
                except:
                    end_chapter = "end"
                    start_chapter = "start"
            except:
                print("oops")
            try:
                msg = '{0.author.mention} Searching now!'.format(message)
                await client.send_message(message.channel, msg)
                final_location = get_fiction_location(fiction_term,directory="Fiction - Epubs/",start_chapter=start_chapter,end_chapter=end_chapter)
                if final_location != None:
                    print(final_location)
                    if os.path.exists(final_location):
                        print("It exists!")
                        title_name = final_location.split("/")[-1].replace(".epub","")
                        msg = '{0.author.mention}'.format(message) + str(' Located ***{}*** Successfully!'.format(title_name))
                        await client.send_message(message.channel, msg)
                        print("Uploading File {}".format(final_location))
                        await client.send_file(message.channel, final_location)
                        flag_upload = True
                    else:
                        print("It doesn't exist!")
                        msg = '{0.author.mention} That isn\'t cached!'.format(message)
                        await client.send_message(message.channel, msg)
                    
                else:
                    print("Error")
                    flag_error = True
                    msg = '{0.author.mention} There are no chapters for that fiction!'.format(message)
                    await client.send_message(message.channel, msg)
            except:
                print("Error")
                flag_error = True
                msg = '{0.author.mention} There was an error! (No Fiction?)'.format(message)
                await client.send_message(message.channel, msg)
        except:
            print("Error with fiction name")
            flag_error = True
            msg = '{0.author.mention} There was an error with the fiction name!'.format(message)
            await client.send_message(message.channel, msg)
        print(msg,flag_error,flag_upload)
        #await client.send_message(message.channel, msg)
    elif message.content.startswith('!req'):
        print(str(message.author)+":",message.content)
        flag_upload = False
        flag_error = False
        try:
            fiction_term = " ".join(message.content.split(" ")[1:])
            try:
                chapters = " ".join(message.content.split(" ")[-1:]) #don't include the other stuff
                try:
                    temp = " ".join(message.content.split(" ")[-2:-1])
                    if temp == "!req":
                        end_chapter = "end"
                        start_chapter = "start"
                        end_chapter_flag = False
                        start_chapter_flag = False
                    else:
                        if chapters == "-": #when someone tries to use an empty range for some reason
                            chapters = "1"
                        chapters = chapters.split("-")
                        try:
                            end_chapter = int(chapters[1])
                            end_chapter_flag = True
                        except:
                            end_chapter_flag = False
                            end_chapter = "end"
                        try:
                            start_chapter = int(chapters[0])
                            start_chapter_flag = True
                        except:
                            start_chapter = "start"
                            start_chapter_flag = False
                        if end_chapter_flag or start_chapter_flag:
                            fiction_term = " ".join(fiction_term.split(" ")[:-1]) #remove chapter range from search term
                except:
                    end_chapter = "end"
                    start_chapter = "start"
            except:
                print("oops")
            try:
                msg = '{0.author.mention} Searching now!'.format(message)
                await client.send_message(message.channel, msg)
                #here
                loop = asyncio.get_event_loop()
                task = loop.create_task(download_fiction_async(message,fiction_term,start_chapter,end_chapter))
                await task
            except Exception as e:
                print("Error",e)
                flag_error = True
                msg = '{0.author.mention} There was an error! (No Fiction?)'.format(message)
                await client.send_message(message.channel, msg)
        except:
            print("Error with fiction name")
            flag_error = True
            msg = '{0.author.mention} There was an error with the fiction name!'.format(message)
            await client.send_message(message.channel, msg)
        print(msg,flag_error,flag_upload)
        #await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('RoyalRoadEpubCreator logged in as',client.user.name,'({})'.format(client.user.id))
    print('------')

client.run("bot token")
