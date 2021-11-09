import discord
import os
import asyncio 
import random
import database as db
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
matchhash = {}
matchcd = 86400

dB = {}

testDB = {
  'abc':1,
  'def':2
}

id_guild = 814170478121713686
id_adminrole = 814172905130557443
id_muterole = 815600544873578526
id_channelGeneral = 814170478566178879
id_channelShame = 899259828562710578
id_channelDB = 907628026743910491
id_messageDB = 907628138656317450
id_eventlog = 824175906120663060


@client.event
async def on_ready():
    global kroxy
    global ksilp
    global adminrole
    global premiumrole
    global muterole
    global hallofshame
    global eventlog
    global dbChannel
    global dbMessage
    global dB
    global msgDB
    global id_adminrole
    global id_muterole
    global id_channelGeneral
    global id_channelShame
    global id_channelDB
    global id_messageDB
    global id_eventlog
    global id_guild

    print('We have logged in as {0.user}'.format(client))
    for emote in client.emojis:
        if emote.name == "KissRoxy":
            kroxy = emote
        if emote.name == "KissSylphy":
            ksilp = emote
    
    spankdur = defaultvalue["spankdur"]
    
    for targetguild in client.guilds:
      if targetguild.id == id_guild:
        adminrole = targetguild.get_role(id_adminrole)
        premiumrole = targetguild.premium_subscriber_role
        muterole = targetguild.get_role(id_muterole)
        general = targetguild.get_channel(id_channelGeneral)
        hallofshame = targetguild.get_channel(id_channelShame)
        eventlog = targetguild.get_channel(id_eventlog)
        dbChannel = targetguild.get_channel(id_channelDB)
        dbMessage = await dbChannel.fetch_message(id_messageDB)
        break
    
    msgDB = dbMessage.content
    
    for i in range(len(msgDB)):
      tab,i = db.parse_database(msgDB,i)
      entry = db.parse_line(tab)
      if entry is not None:
        dB[entry[0]] = entry[1]

    string = client.user.mention + " has started another loop!"
    await eventlog.send(string)

@client.event
async def on_message(message):
    global oldspank
    global spankcount
    global oldname
    global namecount
    global oldkiss
    global kisscount
    global spankdur
    global matchhash
    global matchcd
    global testDB

    if message.author == client.user:
        return
    
    if message.channel.id == 899259828562710578:
      return

    if message.content.startswith('!help'):
      await message.channel.send("List of commands: \n**!ship @mention**: Ship somebody with a random character.\n**!ship @mention (multiple)**: Ship multiple members. \n**!match @mention**: Find compatibility of a member with a random character.\n**!match @mention @mention**: Find compatibility between two members. \n**!apostle @mention**: Somebody is a Hitogami's apostle! \n**!spank @mention**: Try to spank a member!\n**!shame post_id**: Put a post in #hall-of-shame! \n\nGif commands: \n**!holyemotes**: Post the holy emotes \n**!axa**: Post the AxA gif \n**!cunny**: Give me your body! \n**!bread**: Breadgasm! \n**!wholesomekiss**: Post a wholesome kiss \n**!roxynom**: Feed Roxy! \n**!lewdroxy**: God is feeling horny today \n**!iloveyou**: God will confess her love! \n\nModerators only: \n**!donut @mention**: Call Papa Orsted to donut somebody.")

    if message.content.startswith('!shame '):
      id = int(message.content[7:])
      targetMessage = await message.channel.fetch_message(id)
      targetContent = f"[**Link**]({targetMessage.jump_url}) \n\n{targetMessage.content}"
      embedVar = discord.Embed(color=0xFF0000, description=targetContent)
      embedVar.set_author(name=targetMessage.author.display_name,icon_url=targetMessage.author.avatar_url,)
      await hallofshame.send(embed=embedVar)


    if message.content.startswith('!ship'):
        if len(message.mentions):
            j = random.randrange(10)
            if j:
              j = 1
            i = random.randrange(len(randname[j]))
            if client.user in message.mentions:
              member = message.author
              embedVar = discord.Embed(color=0x000000, description=f"{client.user.mention} has shipped {member.mention} with {randname[j][i]} for trying to ship Orsted!")
            elif len(message.mentions) == 1:
              member = message.mentions[0]
              embedVar = embedShip(message.author.mention,member.mention,randname[j][i])
            elif len(message.mentions) == 2:
              member1 = message.mentions[0]
              member2 = message.mentions[1]
              embedVar = embedShip(message.author.mention,member1.mention,member2.mention)
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

    if message.content.startswith('!match'):
        if len(message.mentions):
            j = random.randrange(10)
            compatibility = random.randrange(100)
            if j:
              j = 1
            i = random.randrange(len(randname[j]))
            while randname[j][i] == "Orsted":
              i = random.randrange(len(randname[j]))
            if len(message.mentions) == 1:
              member = message.mentions[0]
              couple = member.mention + randname[j][i]
              if(couple in matchhash):
                compatibility = matchhash[couple]
                embedVar = embedMatch(member.mention, randname[j][i],compatibility)
                await message.channel.send(embed=embedVar)
              else:
                embedVar = embedMatch(member.mention, randname[j][i],compatibility)
                await message.channel.send(embed=embedVar)
                matchhash[couple] = compatibility

                await asyncio.sleep(matchcd)
                matchhash.pop(couple)
            elif len(message.mentions) == 2:
              member1 = message.mentions[0]
              member2 = message.mentions[1]
              couple1 = member1.mention + member2.mention
              couple2 = member2.mention + member1.mention
              if(couple1 in matchhash):
                compatibility = matchhash[couple1]
                embedVar = embedMatch(member1.mention, member2.mention,compatibility)
                await message.channel.send(embed=embedVar)
              elif (couple2 in matchhash):
                compatibility = matchhash[couple2]
                embedVar = embedMatch(member1.mention, member2.mention,compatibility)
                await message.channel.send(embed=embedVar)
              else:
                embedVar = embedMatch(member1.mention, member2.mention,compatibility)
                await message.channel.send(embed=embedVar)
                matchhash[couple1] = compatibility

                await asyncio.sleep(matchcd)
                matchhash.pop(couple1)
            else:
              string = message.author.mention + " has tried to match "
              for i in range(len(message.mentions)-1):
                member = message.mentions[i]
                string = string + member.mention + ", "
              member = message.mentions[len(message.mentions)-1]
              string = string + member.mention + ". How lewd!"
              embedVar = discord.Embed(color=0x000000, description=string)
              await message.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(color=0x000000, description="%s has matched no one." % (message.author.mention))
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
                '''
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
                    durationstr = durationstr + "s"'''
                embedVar = discord.Embed(color=0x000000, description="%s has spanked %s!" % (message.author.mention,target.mention))
                if target == message.author:
                  '''durationstr = spankdur'''
                  embedVar = discord.Embed(color=0x000000, description="%s has spanked him/herself!" % (message.author.mention))
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
            embedVar = discord.Embed(color=0x000000, description="%s has been spanked!" % (target.mention))
            if len(message.mentions):
                for checkmember in message.mentions:
                    if checkmember == target:
                        embedVar = discord.Embed(color=0x000000, description="%s has spanked him/herself!" % (target.mention))
                        break
                    if (premiumrole in checkmember.roles or checkmember.guild_permissions.kick_members):
                        embedVar = discord.Embed(color=0x000000, description="%s tried to spank %s. %s got spanked instead!" % (target.mention,checkmember.mention,target.mention))
                        break
            embedVar.set_image(url=spankurl)
        
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
    
    if message.content.startswith('!cunny'):
        await message.channel.send('https://cdn.discordapp.com/attachments/403019763825246209/894328456609939516/1633281014083.webm')
    
    if message.content.startswith('!bread'):
        await message.channel.send('https://www.sakugabooru.com/data/a56fea265f7f85d50f5ef5e9b48c39bf.mp4')

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
            await message.channel.send("Cannot send in SFW channel")


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
    
    if message.content.startswith('!resetdb'):
      if adminrole in message.author.roles:
        await dbMessage.edit(content = '')
    
    
    if message.content.startswith('!setdb'):
      if adminrole in message.author.roles:
        await dbMessage.edit(content = testDB)        
    
    if message.content.startswith('!setvalue'):
      if adminrole in message.author.roles:
        string = message.content[9:].strip()
        entry = db.parse_line(string)
        if entry is not None:
          dB[entry[0]] = entry[1]
          await dbMessage.edit(content = dB)

def comment(value):
  if value == 69:
    return "%. Nice!"
  elif value < 20:
    return "%. What a failure!"
  elif value < 40:
    return "%. Terrible!"
  elif value < 60:
    return "%. Not bad!"
  elif value < 80:
    return "%. Great!"
  else:
    return "%. Congratulation!"
  
def embedMatch(person1, person2, matchvalue):
  string = "The compatibility of " + person1 + " and " + person2 + " is " + str(matchvalue) + comment(matchvalue)
  return discord.Embed(color=0x000000, description=string)

def embedShip(author,person1,person2):
  string = author + " has shipped " + person1 + " and " + person2
  return discord.Embed(color=0x000000, description=string)



keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))