import discord
import os
import asyncio 
import random
from keep_alive import keep_alive


defaultvalue = {
  "spankdur":5
}
numerals = "0123456789"
client = discord.Client()

randspank = ["https://c.tenor.com/4RIbgFCLRrUAAAAC/rikka-takanashi-bad-girl.gif", "https://c.tenor.com/WNnO4lxUMVQAAAAC/anime-school-girl.gif", "https://c.tenor.com/5ropePOLZV4AAAAC/bad-beat.gif", "https://c.tenor.com/gScnebhgJn4AAAAC/taritari-anime-spank.gif"]
oldspank = ""
spankcount = 0


randname  = [["Ariel","Atofe","Miko","Kishirika Kishirisu"],["Perugius","Sieg","Pax","Darius","Nokopara","Hitogami","Dark King Vita", "Gal Farion", "Luke", "Somal", "Philemon","Orsted"]]
oldname = ""
namecount = 0

wholesomekiss = ["https://media.discordapp.net/attachments/824175906120663060/843483983080849418/E0ndCMxVoAAeSy3.png?width=804&height=504","https://media.discordapp.net/attachments/824175906120663060/843465128644313108/20210511_104844.png?width=952&height=504"]
oldkiss = 0
kisscount = 0

@client.event
async def on_ready():
    global kroxy
    global ksilp
    global adminrole
    global premiumrole
    global muterole
    global spankdur

    print('We have logged in as {0.user}'.format(client))
    for emote in client.emojis:
        if emote.name == "KissRoxy":
            kroxy = emote
        if emote.name == "KissSylphy":
            ksilp = emote
    
    spankdur = defaultvalue["spankdur"]
    
    for targetguild in client.guilds:
        adminrole = targetguild.get_role(814172905130557443)
        premiumrole = targetguild.premium_subscriber_role
        muterole = targetguild.get_role(815600544873578526)

@client.event
async def on_message(message):
    global oldspank
    global spankcount
    global oldname
    global namecount
    global oldkiss
    global kisscount
    global spankdur

    if message.author == client.user:
        return

    if message.content.startswith('!help'):
      await message.channel.send("List of commands: \n**!ship @mention**: Ship somebody with a random character.\n**!ship @mention (multiple)**: Ship multiple members. \n**!apostle @mention**: Somebody is a Hitogami's apostle! \n**!holyemotes**: Post the holy emotes \n**!axa**: Post the AxA gif \n**!wholesomekiss**: Post a wholesome kiss \n**!roxynom**: Feed Roxy! \n**!lewdroxy**: God is feeling horny today \n\nModerators only: \n**!donut @mention**: Call Papa Orsted to donut somebody.")

    if message.content.startswith('!ship'):
        if len(message.mentions):
            j = random.randrange(10)
            if j:
              j = 1
            i = random.randrange(len(randname[j]))
            if client.user in message.mentions:
              member = message.author
              embedVar = discord.Embed(color=0x000000, description="%s has shipped %s with %s for trying to ship Orsted!" % (client.user.mention,member.mention,randname[j][i]))
            elif len(message.mentions) == 1:
              member = message.mentions[0]
              embedVar = discord.Embed(color=0x000000, description="%s has shipped %s with %s" % (message.author.mention,member.mention,randname[j][i]))
            elif len(message.mentions) == 2:
              string = message.author.mention + " has shipped "
              member = message.mentions[0]
              string = string + member.mention + " and "
              member = message.mentions[1]
              string = string + member.mention
              embedVar = discord.Embed(color=0x000000, description=string)
            else:
              string = message.author.mention + " has shipped "
              for i in range(len(message.mentions)-1):
                member = message.mentions[i]
                string = string + member.mention + ", "
              member = message.mentions[len(message.mentions)-1]
              string = string + member.mention + ". How lewd!"
              embedVar = discord.Embed(color=0x000000, description=string)
        else:
            embedVar = discord.Embed(color=0x000000, description="%s has shipped no one, the ship has sunk" % (message.author.mention))
        await message.channel.send(embed=embedVar)

    if message.content.startswith('!spank'):
        spankurl = oldspank
        while spankurl == oldspank:
            i = random.randrange(len(randspank))
            spankurl = randspank[i]
            if (spankurl == oldspank):
                if spankcount < 2:
                    spankcount = spankcount + 1
                    break
                else:
                    print("redo")
            else:
                spankcount = 0
        oldspank = spankurl
          
        if ((premiumrole in message.author.roles) or (message.author.guild_permissions.kick_members)):
            if len(message.mentions) == 1: 
                target = message.mentions[0]
                duration = 0
                durationstr = ''
                duree = ''
                messagecontent = message.content
                if message.author.guild_permissions.kick_members:
                  k = messagecontent.rfind(">")
                else:
                  k = len(messagecontent)
                while k < len(messagecontent):
                  if messagecontent[k] in numerals:
                    duree = duree + str(messagecontent[k])
                  else:
                    if len(duree):
                      print(duree)
                      if messagecontent[k] == 'd':
                        duration = duration + int(duree) * 3600 * 24
                      elif messagecontent[k] == 'h':
                        duration = duration + int(duree) * 3600
                      elif messagecontent[k] == 'm':
                        duration = duration + int(duree) * 60
                      elif messagecontent[k] == 's':
                        duration = duration + int(duree)
                      duree = ''
                  if duration > 172800:
                    duration = 172800
                    k = len(messagecontent)
                  k = k + 1
                if duration == 0:
                  duration = spankdur
                i = int(duration)
                if (i // 86400):
                  durationstr = str(i // 86400) + " day"
                  if (i // 86400 - 1):
                    durationstr = durationstr + "s"
                  i = i % 86400
                if (i // 3600):
                  if len(durationstr):
                    durationstr = durationstr + ", "
                  durationstr = durationstr + str(i // 3600) + " hour"
                  if (i // 3600 - 1):
                    durationstr = durationstr + "s"
                  i = i % 3600
                if (i // 60):
                  if len(durationstr):
                    durationstr = durationstr + ", "
                  durationstr = durationstr + str(i // 60) + " minute"
                  if (i // 60 - 1):
                    durationstr = durationstr + "s"
                  i = i % 60
                if i:
                  if len(durationstr):
                    durationstr = durationstr + " and "
                  durationstr = durationstr + str(i) + " second"
                  if (i - 1):
                    durationstr = durationstr + "s"
                embedVar = discord.Embed(color=0x000000, description="%s has spanked %s for %s!" % (message.author.mention,target.mention,durationstr))
                if target == message.author:
                  durationstr = spankdur
                  embedVar = discord.Embed(color=0x000000, description="%s has spanked him/herself for %ss!" % (message.author.mention,durationstr))
                embedVar.set_image(url=spankurl)
            elif len(message.mentions) > 1:
                target = 0
                embedVar = discord.Embed(color=0x000000, description="You cannot spank more than one at a time. You only have one hand to hold their ass and another to do the spanking.")
                embedVar.set_image(url="https://c.tenor.com/4hQUTxADAT8AAAAC/kiznaiber-hand.gif")
            else:
                target = 0
                embedVar = discord.Embed(color=0x000000, description="Your hands feel empty, no ass to spank.")
                embedVar.set_image(url="https://c.tenor.com/4hQUTxADAT8AAAAC/kiznaiber-hand.gif")
        else:
            target = message.author
            embedVar = discord.Embed(color=0x000000, description="%s has been spanked for %ss!" % (target.mention,str(spankdur)))
            if len(message.mentions):
                for checkmember in message.mentions:
                    if checkmember == target:
                        embedVar = discord.Embed(color=0x000000, description="%s has spanked him/herself for %ss!" % (target.mention, str(spankdur)))
                        break
                    if (premiumrole in checkmember.roles or checkmember.guild_permissions.kick_members):
                        embedVar = discord.Embed(color=0x000000, description="%s tried to spank %s. %s got spanked instead for %ss!" % (target.mention,checkmember.mention,target.mention,str(spankdur)))
                        break
            embedVar.set_image(url=spankurl)
        
        await message.channel.send(embed=embedVar)

    if message.content.startswith('!setvar'):
        if adminrole in message.author.roles:
            setmessage = ""
            if "$spankdur=" in message.content:
                value = ""
                k = message.content.find("$spankdur=") + 10
                if k < len(message.content):
                    while(message.content[k] in numerals):
                        value = value + message.content[k]
                        k = k + 1
                        if k >= len(message.content):
                            break
                if len(value):
                    setmessage = setmessage + "Value for spankdur has been set!\n"
                    spankdur = int(value)
                else:
                    setmessage = setmessage + "Cannot find value for spankdur!\n"
            
            if len(setmessage):
                embedVar = discord.Embed(color=0x000000, description=setmessage)
            else:
                embedVar = discord.Embed(color=0x000000, description="Nothing has been set!")
        else:
            embedVar = discord.Embed(color=0x000000, description="You are not authorized for this command!")
        await message.channel.send(embed=embedVar)

    if message.content.startswith('!resetvar'):
        if adminrole in message.author.roles:
            setmessage = ""
            if "$spankdur" in message.content:
                setmessage = setmessage + "Value for spankdur has been reset to default!\n"
                spankdur = defaultvalue["spankdur"]
            if len(setmessage):
                embedVar = discord.Embed(color=0x000000, description=setmessage)
            else:
                embedVar = discord.Embed(color=0x000000, description="Nothing has been reset!")
        else:
            embedVar = discord.Embed(color=0x000000, description="You are not authorized for this command!")
        await message.channel.send(embed=embedVar)

    if message.content.startswith('!donut'):
        if random.randrange(10):
            if message.author.guild_permissions.kick_members:
                if not message.mentions:
                    embedVar = discord.Embed(color=0x000000, description="Who do you want me to make into a donut?")
                    await message.channel.send(embed=embedVar)
                    return
                member = message.mentions[0]
                await member.add_roles(muterole)
                embedVar = discord.Embed(color=0x000000, description="%s has become donut!" % member.mention)
                await message.channel.send(embed=embedVar)

                await asyncio.sleep(10)
                await member.remove_roles(muterole)
                embedVar = discord.Embed(color=0x000000, description="%s has revived!" % member.mention)
                await message.channel.send(embed=embedVar)
            else:
                member = message.author
                await member.add_roles(muterole)
                embedVar = discord.Embed(color=0x000000, description="You want to joke with me?")
                await message.channel.send(embed=embedVar)

                await asyncio.sleep(10)
                await member.remove_roles(muterole)
                embedVar = discord.Embed(color=0x000000, description="%s has revived!" % member.mention)
                await message.channel.send(embed=embedVar) 
        else:
            await message.channel.send('https://media.discordapp.net/attachments/814170478566178879/832430180676272148/latest.png?width=352&height=503')
            return

    if message.content.startswith('!listmention'):
        if len(message.mentions):
          string = "There are " + str(len(message.mentions)) + " in the list: "
          for i in range(len(message.mentions)):
            member = message.mentions[i]
            string = string + member.mention
          embedVar = discord.Embed(color=0x000000, description=string)
        else:
          embedVar = discord.Embed(color=0x000000, description="List is empty.")
        await message.channel.send(embed=embedVar)          


    if message.content.startswith('!apostle'):
        if len(message.mentions):
            member = message.mentions[0]
            embedVar = discord.Embed(color=0x000000, description="%s is Hitogami's apostle!" % member.mention)
        else:
            embedVar = discord.Embed(color=0x000000, description="Are you joking with me?")
        await message.channel.send(embed=embedVar)
    
    if message.content.startswith('!holyemotes'):
        await message.channel.send(str(kroxy) + str(ksilp))
    
    if message.content.startswith('!iloveyou'):
        await message.channel.send('https://media.discordapp.net/attachments/824175906120663060/847311210730487848/IMG_20210521_070902.png?width=960&height=408')

    if message.content.startswith('!axa'):
        await message.channel.send('https://images-ext-2.discordapp.net/external/aZqy-7bn2Kjl2QeIEsF_wmXC-ZLlTVDz3R-a_BXcX-Q/https/media.discordapp.net/attachments/558540706302394368/817231396484677673/Comp_1_1.gif?width=894&height=503')
    
    if message.content.startswith('!wholesomekiss'):
        j = oldkiss
        while j == oldkiss:
            j = random.randrange(len(wholesomekiss))
            if (j == oldkiss):
                if kisscount < 2:
                    kisscount = kisscount + 1
                    break
                else:
                    print("redo")
            else:
                kisscount = 0
        oldkiss = j
        await message.channel.send(wholesomekiss[j])
    
    if message.content.startswith('!roxynom'):
        await message.channel.send('https://media.discordapp.net/attachments/814309698295562240/838067728711024700/8f68c86.gif')
    
    if message.content.startswith('!lewdroxy'):
        if message.channel.is_nsfw():
            await message.channel.send('https://media.discordapp.net/attachments/814170813137420338/836444509415800873/ohnopoorroxy3.jpg?width=338&height=467')
        else:
            return        

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))