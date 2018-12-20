import discord
from royalroadlapi import *

client = discord.Client()

@client.event
async def on_message(message):
    global final_location
    #don't reply to own messages
    if message.author == client.user:
        return

    if message.content.startswith('!req'):
        print(str(message.author)+":",message.content)
        flag_upload = False
        flag_error = False
        try:
            fiction_term = " ".join(message.content.split(" ")[1:])
            try:
                msg = '{0.author.mention} Retrieving now!'.format(message)
                await client.send_message(message.channel, msg)
                final_location = get_fiction(fiction_term,directory="Fiction - Epubs/")
                if final_location != None:
                    msg = '{0.author.mention} Downloaded Successfully!'.format(message)
                    await client.send_message(message.channel, msg)
                    print("Uploading File")
                    print(final_location)
                    await client.send_file(message.channel, final_location)
                    flag_upload = True
                else:
                    print("Error")
                    flag_error = True
                    msg = '{0.author.mention} There was no chapters!'.format(message)
                    await client.send_message(message.channel, msg)
            except:
                print("Error")
                flag_error = True
                msg = '{0.author.mention} There was an error! (No Fiction?)'.format(message)
                await client.send_message(message.channel, msg)
        except:
            flag_error = True
            msg = '{0.author.mention} There was an error!'.format(message)
            await client.send_message(message.channel, msg)
        print(msg,flag_error,flag_upload)
        #await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as',client.user.name,'({})'.format(client.user.id))
    print('------')

client.run('bot token')
