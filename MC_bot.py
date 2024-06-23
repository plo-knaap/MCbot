#MC server helper bot by Alpo van der Knaap
#based on: https://realpython.com/how-to-make-a-discord-bot-python/
#started SEP 2020

import psutil
import subprocess
import socket
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from requests import get
import xml.etree.ElementTree as et
import shitposts


def getPath(tag):
    tree = et.parse('path_list.xml')
    root = tree.getroot()
    path = root.find(tag)
    return path.text


def status():
    global process
    if process != 0:
        st = 'ONLINE'
    else:
        st = 'OFFLINE'
    return st


def control(key):
    global process
    if key == 'START':
        process = subprocess.Popen(['start'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        return 0
    elif key == 'STOP':
        output = process.communicate(input=b'stop\n')[0]
        process = 0
        return output


def main():
    TOKEN = getPath('discord_token')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    local_ip_address = IP

    ip_address = get(getPath('ip_test_url')).content.decode('utf8')
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    r = [-1, -1, -1]    #random start array for the copy pastas
    byt = 1073741824    #used to calculate bit-values of RAM

   
    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game('on {}, use >help for help'.format(ip_address)))
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        #try:
        if '>addr' == message.content.lower() or '>ip' == message.content.lower():
            await message.channel.send('Servu löytyy osotteesta ' + ip_address)

        elif '>local' == message.content.lower():
            await message.channel.send('Servu löytyy sisäisessä verkossa osotteesta ' + local_ip_address)

        elif '>status' == message.content.lower():
            cputemp = psutil.sensors_temperatures()['coretemp']
            await message.channel.send('Servu on salee %s\n\nCPU (freq/temp): %5.2fGHz / %5.1f°C\nRAM (used/total): %5.2fGiB / %5.2fGiB' % ((status(), psutil.cpu_freq().current/1000, (cputemp[1].current + cputemp[2].current)/2, (psutil.virtual_memory().total - psutil.virtual_memory().available)/byt, psutil.virtual_memory().total/byt)))

        elif '>help' == message.content.lower():
            await message.channel.send('käytä ">" komentojen edessä\n\nip, addr, local: antaa ip osotteen\nstatus: antaa tilan (online/offline + muuta)\nstart: käynnistää servun\nskyblock: käynnistää skyblock servun (ei käytössä!!!)\nstop: sammuttaa servun ja tallentaa')

        elif '>start' == message.content.lower() or 'my brother in christ, start' == message.content.lower():
            if status() == 'ONLINE':
                await message.channel.send('Nah, servu taitaa jo olla päällä')
            elif status() == 'OFFLINE':
                await message.channel.send('Servu käynnistyy osoitteessa ' + ip_address + '\nPelattuasi sammuta servu >stop komennolla')
                control('START')
    
        elif '>stop' == message.content.lower():
            if status() == 'ONLINE':
                await message.channel.send('Yritetään sulkea servu, logi:')
                grep_stdout = control('STOP')
                await message.channel.send("\"" + grep_stdout.decode().splitlines()[-1] + "\"")

        elif '>skyblock' == message.content.lower():
            if status() == 'ONLINE':
                await message.channel.send('Nah, servu taitaa jo olla päällä')
            elif status() == 'OFFLINE':
                #await message.channel.send('Skyblock servu käynnistyy osoitteessa ' + ip_address)
                #subprocess.run(['skyblock_bot'])
                await message.channel.send('no')

        elif '>fedoramode' == message.content.lower():
            await message.channel.send(shitposts.pasta(getPath('pasta'), r))
        
        #except:
        #    await message.channel.send('Jotain meni pieleen...')
        #    print('Jotain meni pieleen...')

    client.run(TOKEN)


process = 0         #initialization for the bacground process

main()
