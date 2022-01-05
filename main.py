import discord
import os
import asyncio 
import random
import database as db
import time
import json
from keep_alive import keep_alive
from datetime import datetime, timedelta
from database import User
from dataclasses import asdict
from dacite import from_dict, Config

t1 = datetime(year=2021,month=11,day=14,hour=16)

defaultvalue = {
  "spankdur":5
}
NUMERALS = "0123456789"
'''intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)'''
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
CD_MATCH = 86400

testDB = {
  "abc":1,
  "def":2
}

ID_GUILD = 814170478121713686
ID_ROLE_ADMIN = 814172905130557443
ID_ROLE_MUTE = 815600544873578526
ID_CHANNEL_GENERAL = 814170478566178879
ID_CHANNEL_SHAME = 899259828562710578
ID_CHANNEL_DATABASE = 907628026743910491
ID_CHANNEL_EVENTLOG = 824175906120663060
ID_CHANNEL_LOOPER = 908073828557672588
ID_CHANNEL_OTHER_HOT = 814172539290648636
ID_CHANNEL_TRASHBIN = 909426261204533328
ID_MSG_TIME = 922600361884270704
ID_ROLE_BOT = 824177027581739060
ID_CHANNELS_SAUCE = [814170813137420338,819067415245357107,814172539290648636,814309698295562240]
ID_CHANNEL_ART = 824153054022205460
ID_CHANNELS_CAH = [919591734495825921,919593810034589706]

USEREXP_PATH = "userexp.json"
MATCH_PATH = "match.json"

members = dict()
memberdict = dict()
periodic_counter = 0

with open('CAH_question.txt', 'r') as f:
    questions = [line.strip() for line in f]

with open('CAH_answer.txt', 'r') as f:
    answers = [line.strip() for line in f]


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
    global otherhotsauceChannel
    global dbMessage
    global ID_ROLE_ADMIN
    global ID_ROLE_MUTE
    global ID_CHANNEL_GENERAL
    global ID_CHANNEL_SHAME
    global ID_CHANNEL_DATABASE
    global ID_CHANNEL_EVENTLOG
    global ID_GUILD
    global ID_CHANNEL_LOOPER
    global ID_CHANNEL_OTHER_HOT
    global general
    global trashbin
    global ID_MSG_TIME
    global weekMessage
    global weeks
    global t1
    global memberdict
    global members
    global matchhash

    start = time.perf_counter()
    random.seed()

    for emote in client.emojis:
        if emote.name == "KissRoxy":
            kroxy = emote
        if emote.name == "KissSylphy":
            ksilp = emote
    
    spankdur = defaultvalue["spankdur"]
    
    targetguild = client.get_guild(ID_GUILD)
    adminrole = targetguild.get_role(ID_ROLE_ADMIN)
    premiumrole = targetguild.premium_subscriber_role
    muterole = targetguild.get_role(ID_ROLE_MUTE)
    general = targetguild.get_channel(ID_CHANNEL_GENERAL)
    hallofshame = targetguild.get_channel(ID_CHANNEL_SHAME)
    eventlog = targetguild.get_channel(ID_CHANNEL_EVENTLOG)
    dbChannel = targetguild.get_channel(ID_CHANNEL_DATABASE)
    channelLooper = targetguild.get_channel(ID_CHANNEL_LOOPER)
    otherhotsauceChannel = targetguild.get_channel(ID_CHANNEL_OTHER_HOT)
    trashbin = targetguild.get_channel(ID_CHANNEL_TRASHBIN)
    weekMessage = await dbChannel.fetch_message(ID_MSG_TIME)
    
    
    '''# read member exp
    file_empty = False
    file_not_integrity = False
    with open(USEREXP_PATH,"r") as f:
      try:
        memberdict = json.loads(f.read())
      except:
        memberdict = None
        file_empty = True
    if memberdict:
      for id in memberdict:
        members[id] = from_dict(data_class=User,data=memberdict[id],config=Config(check_types=False))
      if len(members) != len(memberdict):
        file_not_integrity = True
    else:
      memberdict = dict()
      async for unit in targetguild.fetch_members():
        members[unit.id] = User(unit.id)
        data = asdict(members[unit.id])
        data.pop("last_message")
        data.pop("last_gain")
        memberdict[unit.id] = data
      with open(USEREXP_PATH, "w") as f:
        f.write(json.dumps(memberdict))

    if file_empty:
        send_log("Orsted bot resets and find file empty.")
    elif file_not_integrity:
        send_log("Orsted bot resets and find file corrupted.")
    else:
        send_log("Orsted bot resets and copied file successfully.")'''
    
    # read match
    with open(MATCH_PATH, "r") as f:
      try:
        matchhash = json.loads(f.read())
      except:
        matchhash = {}
    
    # read week time
    weeks = weekMessage.content
    weeks = parse_number(weeks)
    if weeks is None:
      weeks = 0
    if (weeks < 6):
      t1 = t1 + timedelta(weeks=weeks)
      t2 = datetime.utcnow()
      delta = t1 - t2
      while(delta.days <0 or delta.seconds < 0 or delta.microseconds < 0):
        weeks = weeks + 1
        t1 = t1 + timedelta(weeks=1)
        delta = t1 - t2
      
      await weekMessage.edit(content = weeks)

    end = time.perf_counter()
    string = client.user.mention + " has started another loop!"
    print('We have logged in as {0.user}, the process took '.format(client)+ f'{end-start} seconds!')
    await channelLooper.send(string)

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
    global weeks
    global t1
    global answers
    global questions
    global ID_ROLE_BOT
    '''global periodic_counter
    cah_multiplier = 1.3
    sauce_multiplier = 1.5
    art_multiplier = 2'''

    '''periodic_counter += 1

    if periodic_counter >= 500:
      periodic_counter = 0
      with open(USEREXP_PATH,"r") as f:
        dictchecker = len(json.loads(f.read()))
      if dictchecker != len(members):
        send_log("Periodic check finds error on [members].")
      elif dictchecker != len(memberdict):
        send_log("Periodic check finds error on [memberdict].")
      else:
        send_log("Periodic check finds no error yet.")'''


    if message.author == client.user:
        return

    if message.guild.get_role(ID_ROLE_BOT) in message.author.roles:
        return
    
    '''if message.content.startswith('!exp'):
        if message.channel.id != 922829958999597157:
            return
        target = message.author
        if message.mentions:
          target = message.mentions[0]
        send_log(f"{message.author.name} requests exp of {target.name}.")
        for i,data in enumerate(sorted(members.items(), key=lambda m:m[1].exp, reverse=True)):
          if data[0] == str(target.id):
            member = data[1]
            await message.channel.send(f"{target.name}'s EXP is {member.exp}, at {str(i+1)}{add_suffix(i)} place.")
            return
        return

    if message.content.startswith('!lb'):
        if message.channel.id != 922829958999597157:
            return
        string = ""
        for i, data in enumerate(sorted(members.items(), key=lambda m:m[1].exp, reverse=True)):
            if i > 9:
                break
            member = data[1]
            user = message.guild.get_member(int(data[0]))
            if user:
                string += f"{str(i+1)}{add_suffix(i)} place: {user.name} - {member.exp} exp\n"
        await message.channel.send(string)
        return

    if message.content.startswith('!deletelog'):
      if adminrole in message.author.roles:
          index = 1
          while(os.path.exists(f"explog{index}.json")):
              os.remove(f"explog{index}.json") 
              index += 1
      else:
          send_log(f"{message.author.name} tried to delete log!")
      return

    if message.content.startswith('!resetlb'):
      if adminrole in message.author.roles:
          for id in members:
              members[id].reset_exp()
              write_exp_data(int(id))
      else:
          send_log(f"{message.author.name} tried to reset exp!")
      return

    if message.content.startswith('!penalty'):
        if adminrole in message.author.roles:
            if message.mentions:
                s = "List of member got mudded:\n"
                for mention in message.mentions:
                    members[str(mention.id)].penalty()
                    write_exp_data(mention.id)
                    s += f"{mention.mention}\n"
            else:
                s = "No member specified!"
            embedVar = discord.Embed(color=0xFF0000, description=s)
            await message.channel.send(embed=embedVar)
        else:
            send_log(f"{message.author.name} tried to use penalty!")
        return
    
    # check if member exists already (just in case)
    try:
        member = members[str(message.author.id)]
    except:
        members[str(message.author.id)] = User(str(message.author.id))
        data = asdict(members[str(message.author.id)])
        data.pop("last_message")
        data.pop("last_gain")
        memberdict[str(message.author.id)] = data
        member = members[str(message.author.id)]
    
    # exp calculation
    current_time = datetime.utcnow() - member.last_message
    posting_sauce = False
    if(timedelta(seconds=member.last_gain+10)<current_time or ((message.channel.id in ID_CHANNELS_CAH or message.channel.id in ID_CHANNELS_SAUCE or message.channel.id == ID_CHANNEL_SHAME or message.channel.id == ID_CHANNEL_ART)) and (message.attachments or message.embeds)):
        exp_gain = random.randrange(5,13)
        exp_multiplier = 1
        if message.channel.id in ID_CHANNELS_CAH:
          exp_multiplier = cah_multiplier
        elif message.attachments:
          if message.channel.id in ID_CHANNELS_SAUCE:
            posting_sauce = True
            exp_multiplier = sauce_multiplier
            for i in range(len(message.attachments) - 1):
              exp_gain += random.randrange(5,13)
          elif message.channel.id == ID_CHANNEL_SHAME:
            posting_sauce = True
            exp_multiplier = sauce_multiplier
            for i in range(len(message.attachments) - 1):
              exp_gain += random.randrange(5,13)
          elif message.channel.id == ID_CHANNEL_ART:
            exp_multiplier = art_multiplier
            for i in range(len(message.attachments) - 1):
              exp_gain += random.randrange(5,13)
        elif message.embeds:
          if message.channel.id in ID_CHANNELS_SAUCE:
            posting_sauce = True
            exp_multiplier = sauce_multiplier
            for i in range(len(message.embeds) - 1):
              exp_gain += random.randrange(5,13)
          elif message.channel.id == ID_CHANNEL_ART:
            posting_sauce = True
            exp_multiplier = art_multiplier
            for i in range(len(message.embeds) - 1):
              exp_gain += random.randrange(5,13)
        exp_gain *= exp_multiplier
        member.add_exp(exp_gain)
        if posting_sauce:
          member.last_gain = 0
        member.set_last_message()
        write_exp_data(message.author.id)
        EXP_LOG_PATH = "explog.json"
        with open(EXP_LOG_PATH,"r") as f:
          content = f.read()
        if(len(content)>5000):
          check_index = 1
          while(os.path.exists(f"explog{check_index}.json")):
            check_index += 1
          with open(f"explog{check_index}.json","x") as copy:
            copy.write(content)
          with open(EXP_LOG_PATH,"w") as f:
              f.truncate(0)
        temp = member.last_message
        if member.id == str(message.author.id):
          check_id = True
        else:
          check_id = f"{member.id}-{message.author.id}" 
        send_log(f"{check_id} {message.author.name} - {exp_gain}exp{add_exp_multiplier(exp_multiplier)}.",temp)'''


    if message.content.startswith('!prune '):
        if message.author.guild_permissions.manage_messages:
            amount = parse_number(message.content[7:])
            if amount is None:
                general.send(content="Please specify the amount to purge", delete_after = 15)
            else:
                listmsg = await message.channel.purge(limit=amount)
                if len(listmsg) > 1:
                    for msg in listmsg[1:]:
                        content = f"message: '{msg.content}' was deleted in **#{msg.channel}**"
                        embedVar = discord.Embed(color=0x000000, description=content)
                        embedVar.set_author(name=msg.author.display_name,icon_url=msg.author.avatar_url,)
                        await trashbin.send(embed = embedVar)
        else:
            send_log(f"{message.author.name} tried to prune!")
        return

    if message.channel.id == 899259828562710578:
        return

    if message.content.startswith('!cah') or message.content.startswith('!cardsagainsthumanity'):
        s = random.choice(questions)
        list_answers = []
        if "_" in s:
          a = random.choice(answers)
          while("_" in s):
            while (a in list_answers):
              a = random.choice(answers)
            list_answers.append(a)
            s = s.replace('_', a[:-1], 1)
        else:
          s = s + "\n" + random.choice(answers)
        s = s.replace("\\n","\n")
        embedVar = discord.Embed(color=0xFF0000, description=s)
        await message.channel.send(embed=embedVar)
        return

    if message.content.startswith('!mttime'):
      print(datetime.utcnow())
      t2 = t1 - datetime.utcnow()
      while(t2.days <0 or t2.seconds < 0 or t2.microseconds < 0):
        weeks = weeks + 1
        t1 = t1 + timedelta(weeks=1)
        t2 = t1 - datetime.utcnow()

      if(weeks < 6):
        delta = datetime(1,1,1) + t2
        await weekMessage.edit(content = weeks)
        await message.channel.send(f"Episode {18+weeks} of Mushoku Tensei in " + (f"{delta.day-1} day{'s' if (delta.day-1)>=2 else ''}, " if (delta.day>1) else "") + (f"{delta.hour} hour{'s' if (delta.hour-1)>=2 else ''}, " if (delta.hour>0) else "") + (f"{delta.minute} minute{'s' if (delta.minute-1)>=2 else ''}, " if (delta.minute>0) else "") + f"{delta.second} second{'s' if (delta.second-1)>=2 else ''}.")
      else:
        await message.channel.send(f"Season 1 of Mushoku Tensei has ended.")
      return

    if message.content.startswith('!help'):
      await message.channel.send("List of commands: \n**!ship @mention**: Ship somebody with a random character.\n**!ship @mention (multiple)**: Ship multiple members. \n**!match @mention**: Find compatibility of a member with a random character.\n**!match @mention @mention**: Find compatibility between two members. \n**!apostle @mention**: Somebody is a Hitogami's apostle! \n**!spank @mention**: Try to spank a member!\n**!shame post_id**: Put a post in #hall-of-shame! \n\nGif commands: \n**!holyemotes**: Post the holy emotes \n**!axa**: Post the AxA gif \n**!cunny**: Give me your body! \n**!bread**: Breadgasm! \n**!wholesomekiss**: Post a wholesome kiss \n**!roxynom**: Feed Roxy! \n**!lewdroxy**: God is feeling horny today \n**!iloveyou**: God will confess her love! \n\nModerators only: \n**!donut @mention**: Call Papa Orsted to donut somebody.")
      return
    
    if message.content.startswith('!magicno '):
      magicnumber = parse_number(message.content[9:])
      
      if (magicnumber is None):
        await otherhotsauceChannel.send(content="Magic number not found!", delete_after = 15)
      else:
        magicMessage = await otherhotsauceChannel.send(content=f"https://nhentai.net/g/{magicnumber}/")
        embedVar = discord.Embed(color=0xFF0000, description=magicMessage.content)
        embedVar.set_author(name=message.author.display_name,icon_url=message.author.avatar_url,)
        await eventlog.send(embed=embedVar)
      await message.delete()
      return

    if message.content.startswith('!shame '):
      id = int(message.content[7:])
      targetMessage = await message.channel.fetch_message(id)
      targetContent = f"[**Link**]({targetMessage.jump_url}) \n\n{targetMessage.content}"
      embedVar = discord.Embed(color=0xFF0000, description=targetContent)
      embedVar.set_author(name=targetMessage.author.display_name,icon_url=targetMessage.author.avatar_url,)
      await hallofshame.send(embed=embedVar)
      return

    if message.content.startswith('!ship'):
        if len(message.mentions):
            j = random.randrange(10)
            if j:
              j = 1
            if client.user in message.mentions:
              member = message.author
              embedVar = discord.Embed(color=0x000000, description=f"{client.user.mention} has shipped {member.mention} with {random.choice(randname[j])} for trying to ship Orsted!")
            elif len(message.mentions) == 1:
              member = message.mentions[0]
              embedVar = embedShip(message.author.mention,member.mention,random.choice(randname[j]))
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
        return

    if message.content.startswith('!match'):
        if len(message.mentions):
            if len(message.mentions) == 1: # check if matching with a random character
              # get random gender (10% to get female)
              j = random.randrange(10)
              if j:
                j = 1
              # get random name
              name = random.choice(randname[j])
              # reroll if hitting Orsted
              while name == "Orsted":
                name = random.choice(randname[j])
              member = message.mentions[0]
              await send_match(message.channel,member.mention,name)
            elif len(message.mentions) == 2: # check if there are 2 mentions
              await send_match(message.channel,message.mentions[0].mention,message.mentions[1].mention)
            else: # case matching more than 2
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
        return

    if message.content.startswith('!spank'):
        spankurl = oldspank
        while spankurl == oldspank:
            spankurl = random.choice(randspank)
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
                  if messagecontent[k] in NUMERALS:
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
        return

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
                return
            else:
                member = message.author
                await member.add_roles(muterole)
                embedVar = discord.Embed(color=0x000000, description="You want to joke with me?")
                await message.channel.send(embed=embedVar)

                await asyncio.sleep(10)
                await member.remove_roles(muterole)
                embedVar = discord.Embed(color=0x000000, description="%s has revived!" % member.mention)
                await message.channel.send(embed=embedVar) 
                return
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
        return   

    if message.content.startswith('!apostle'):
        if len(message.mentions):
            member = message.mentions[0]
            embedVar = discord.Embed(color=0x000000, description="%s is Hitogami's apostle!" % member.mention)
        else:
            embedVar = discord.Embed(color=0x000000, description="Are you joking with me?")
        await message.channel.send(embed=embedVar)
        return
    
    if message.content.startswith('!holyemotes'):
        await message.channel.send(str(kroxy) + str(ksilp))
        return
    
    if message.content.startswith('!iloveyou'):
        await message.channel.send('https://media.discordapp.net/attachments/824175906120663060/847311210730487848/IMG_20210521_070902.png?width=960&height=408')
        return

    if message.content.startswith('!axa'):
        await message.channel.send('https://images-ext-2.discordapp.net/external/aZqy-7bn2Kjl2QeIEsF_wmXC-ZLlTVDz3R-a_BXcX-Q/https/media.discordapp.net/attachments/558540706302394368/817231396484677673/Comp_1_1.gif?width=894&height=503')
        return
    
    if message.content.startswith('!cunny'):
        await message.channel.send('https://cdn.discordapp.com/attachments/403019763825246209/894328456609939516/1633281014083.webm')
        return
    
    if message.content.startswith('!bread'):
        await message.channel.send('https://www.sakugabooru.com/data/a56fea265f7f85d50f5ef5e9b48c39bf.mp4')
        return

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
        return
    
    if message.content.startswith('!roxynom'):
        await message.channel.send('https://media.discordapp.net/attachments/814309698295562240/838067728711024700/8f68c86.gif')
        return
    
    if message.content.startswith('!lewdroxy'):
        if message.channel.is_nsfw():
            await message.channel.send('https://media.discordapp.net/attachments/814170813137420338/836444509415800873/ohnopoorroxy3.jpg?width=338&height=467')
            return
        else:
            await message.channel.send("Cannot send in SFW channel")
            return

    if message.content.startswith('!resetdb'):
      if adminrole in message.author.roles:
        await dbMessage.edit(content = '')
        return
    
    if message.content.startswith('!setdb'):
      if adminrole in message.author.roles:
        await dbMessage.edit(content = json.dumps(testDB))
        return
    
    if message.content.startswith('!setweek '):
      if adminrole in message.author.roles:
        await weekMessage.edit(content = parse_number(message.content[9:]))
        return
    
    if message.content.startswith('!week++'):
      if adminrole in message.author.roles:
        await weekMessage.edit(content = parse_number(weekMessage.content)+1)
        return

    if message.content.startswith('!setvalue'):
      if adminrole in message.author.roles:
        dB = json.loads(dbMessage.content)
        string = message.content[9:].strip()
        entry = db.parse_line(string)
        if entry is not None:
          dB[entry[0]] = entry[1]
          await dbMessage.edit(content = json.dumps(dB))
        else:
          await eventlog.send("syntax error")
      else:
        await eventlog.send(f"{message.author.mention} tried to use unauthorized command")
      return

    if message.content.startswith('!deletevalue'):
      if adminrole in message.author.roles:
        dB = json.loads(dbMessage.content)
        string = message.content[12:].strip()
        if string is not None:
          if (dB.pop(string)):
            await dbMessage.edit(content = json.dumps(dB))
          else:
            await eventlog.send("can't find value")
        else:
          await eventlog.send("syntax error")
      else:
        await eventlog.send(f"{message.author.mention} tried to use unauthorized command")
      return

@client.event
async def on_message_delete(message):
  if message is None:
    return
  if message.guild is None:
    return
  msg = f"message id<{message.id}> was deleted in **#{message.channel}**:\n{message.content}"
  embedVar = discord.Embed(color=0x000000, description=msg)
  embedVar.set_author(name=message.author.display_name,icon_url=message.author.avatar_url,)
  await trashbin.send(embed = embedVar)
  return

@client.event
async def on_message_edit(before, after):
  if before is None or after is None:
    return
  if before.guild is None or after.guild is None:
    return
  if before.content == after.content:
    return

  content = f"ID:{before.id}\n**Before:**\n{before.content}\n**[After]({after.jump_url}):**\n{after.content}"
  embedVar = discord.Embed(color=0x000000, description=content)
  embedVar.set_author(name=before.author.display_name,icon_url=before.author.avatar_url,)
  await trashbin.send(embed = embedVar)
  return

@client.event
async def on_member_join(member):
  if member.id not in members:
    members[str(member.id)] = User(member.id)
    write_exp_data(member.id)

@client.event
async def on_member_remove(member):
  members[str(member.id)].penalty()
  write_exp_data(member.id)    

def write_exp_data(id:int):
  data = asdict(members[str(id)])
  data.pop("last_message")
  data.pop("last_gain")
  memberdict[str(id)] = data
  with open(USEREXP_PATH, "w") as f:
    f.write(json.dumps(memberdict))

def comment(value):
  if value == 69:
    return "%. Nice!"
  elif value == 0:
    return "%. Do you hate each other that much?"
  elif value < 15:
    return "%. What a failure!"
  elif value < 30:
    return "%. Terrible!"
  elif value < 45:
    return "%. Not really good!"
  elif value < 60:
    return "%. Not bad!"
  elif value < 75:
    return "%. Great!"
  elif value < 90:
    return "%. Excellent!"
  else:
    return "%. Congratulation!"

async def send_match(channel,member1:str,member2:str):
  now = datetime.utcnow()
  # create hash key based on members
  couple = member1 + member2
  couple2 = member2 + member1
  # check if reverse key exists, if yes, use that as key
  if(couple2 in matchhash):
    couple = couple2
  # in case of key exists, treat its data first
  if(couple in matchhash):
    # check time
    data = matchhash[couple][1:]
    delta = datetime(year = data[0], month = data[1], day = data[2], hour = data[3], minute = data[4], second = data[5]) - now
    # if it is still under cooldown, take old value
    if(delta < timedelta(seconds = CD_MATCH)):
      compatibility = matchhash[couple][0]
      embedVar = embedMatch(member1, member2,compatibility)
      await channel.send(embed=embedVar)
      return
  # in case key not exist, or off cooldown, take new values
  compatibility = random.randrange(100)
  embedVar = embedMatch(member1, member2,compatibility)
  await channel.send(embed=embedVar)
  matchhash[couple] = [compatibility,now.year,now.month,now.day,now.hour,now.minute,now.second]
  with open(MATCH_PATH,"w") as f:
    f.write(json.dumps(matchhash))

def embedMatch(person1, person2, matchvalue) -> discord.Embed:
  string = "The compatibility of " + person1 + " and " + person2 + " is " + str(matchvalue) + comment(matchvalue)
  return discord.Embed(color=0x000000, description=string)

def embedShip(author,person1,person2) -> discord.Embed:
  string = author + " has shipped " + person1 + " and " + person2
  return discord.Embed(color=0x000000, description=string)

def parse_number(value):
  try:
    return int(value)
  except:
    return None

def send_log(string:str,now:datetime = datetime.utcnow()):
    EXP_LOG_PATH = "explog.json"
    with open(EXP_LOG_PATH,"a") as f:
        f.write(f"{now.date()} {now.time():%X}: {string}\n")

def add_suffix(number:int) -> str:
  ending = ["st","nd","rd"]
  i = number + 1
  if (i % 100) == 10 or (i % 100) == 12 or (i % 100) == 13 or (i % 10) > 3:
    return "th"
  
  return ending[number % 10]

def add_exp_multiplier(multiplier:float) -> str:
  return f" - {multiplier}x" if multiplier>1 else ""

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))