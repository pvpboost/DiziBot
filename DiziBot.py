#import===========================================
import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import json
from pathlib import Path
import datetime
import platform
import logging
import sqlite3
import random
from discord.ext import tasks
from itertools import cycle
from datetime import datetime

#Roles:
#Staff Role: @commands.has_any_role('――――――● Staff ●――――――')
#Staff: @commands.has_any_role('【♻️】Trade Manager','【💠】Helper','【【🔰】Moderator')
#HighStaff Role: @commands.has_any_role('―――――● High Staff ●―――――')
#High Staff: @commands.has_any_role('【🔱】Admin','【🔱】Staff Manager','【🎖️】Management','【👑】Inspector','【👑】Owner','【👑】KingDizi')


client = commands.Bot(command_prefix = '!')
client.remove_command("help")
#client.event===========================================

#Bot Start------------------------------------------------
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="My commands !help"))
    print('The bot is start')
    

#Command not found------------------------------------------------
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f'**שגיאה**',
            description=f'**הפקודה לא נמצאה**'
        )
        await ctx.send(embed=embed)

#No permissions------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour=discord.Colour.default(),
            title=f'**שגיאה**',
            description=f'**אין לך גישה לפקודה**'
        )
        await ctx.send(embed=embed)

#Welcome join------------------------------------------------
@client.event
async def on_member_join(member):
    embed = discord.Embed(colour=discord.Colour(0x95efcc), description=f"**נכנס לשרת**", timestamp=datetime.utcnow())
    embed.set_image(url="https://cdn.discordapp.com/attachments/694151021139853312/708688917343240273/Bot_Logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/694151021139853312/708688917343240273/Bot_Logo.png")
    embed.set_author(name=f"{member.name}",icon_url=f'{member.avatar_url}')
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/694151021139853312/708688917343240273/Bot_Logo.png")
    channel = discord.utils.get(member.guild.channels, name="『👥』welcome-bye")
    await channel.send(embed=embed)

#Welcome leave------------------------------------------------
@client.event
async def on_member_remove(member):
    embed = discord.Embed(colour=discord.Colour(0x95efcc), description=f"**יצא מהשרת**", timestamp=datetime.utcnow())
    embed.set_image(url="https://cdn.discordapp.com/attachments/694151021139853312/708688788762918912/Bot_Logo_black_and_white.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/694151021139853312/708688788762918912/Bot_Logo_black_and_white.png")
    embed.set_author(name=f"{member.name}",icon_url=f'{member.avatar_url}')
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/694151021139853312/708688788762918912/Bot_Logo_black_and_white.png")
    channel = discord.utils.get(member.guild.channels, name="『👥』welcome-bye")
    await channel.send(embed=embed)

#verify------------------------------------------------
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 717053310573740052:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'KingDizi':
            role = discord.utils.get(guild.roles, name='【👥】Member')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                print("הממבר לא נמצא")
        else:
            print("הרול לא נמצא")

#client.command===========================================

#clear------------------------------------------------
@client.command(pass_context=True)
@commands.has_any_role('【🔰】Moderator','【🔱】Admin','【🔱】Staff Manager', '【🎖️】Management', '【👑】Inspector', '【👑】Owner', '【👑】KingDizi')
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f'**Clear**',
        description=f'**{amount} הודעות נמחקו**'
    )

    await ctx.send(embed=embed)
    await ctx.channel.purge(limit=1)

#clear error------------------------------------------------
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f'**Clear**',
            description=f'**תרשום כמה הודעות אתה רוצה למחוק**'
        )
        await ctx.send(embed=embed)
#kick------------------------------------------------
@client.command()
@commands.has_any_role('【🔱】Admin','【🔱】Staff Manager', '【🎖️】Management', '【👑】Inspector', '【👑】Owner', '【👑】KingDizi')
async def kick(ctx, member: discord.Member, *, reason='לא נשלחה סיבה'):
    await member.kick(reason=reason)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f'**Kick**',
        description=f'**{member.mention} קיבל קיק\n סיבה: {reason}**'
    )
    await ctx.send(embed=embed)

#ban------------------------------------------------
@client.command()
@commands.has_any_role('【🎖️】Management', '【👑】Inspector', '【👑】Owner', '【👑】KingDizi')
async def ban(ctx, member, *, reason=':no_entry_sign:לא נשלחה סיבה:no_entry_sign:'):
    await member.ban(reason=reason)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Ban**",
        description=f"**{member.mention} קיבל באן\n סיבה: {reason}**"
    )
    await ctx.send(embed=embed)

#send message in the server------------------------------------------------
@client.command()
@commands.has_permissions(administrator=True)
async def msg(ctx, *, msg=None):
    await ctx.send(f'**{msg}**')

#send message to all------------------------------------------------
@client.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'" + args + "' נשלח אל:" + member.name)

            except:
                print("לא יכול היה לשלוח'" + args + "' ל" + member.name)
    else:
        await ctx.channel.send("ההודעה נשלחה")

#mute------------------------------------------------
@client.command()
@commands.has_any_role('――――――● Staff ●――――――')
async def mute(ctx, member : discord.Member, *, reason=':no_entry_sign:לא נשלחה סיבה:no_entry_sign:'):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    role2 = discord.utils.get(ctx.guild.roles, name="【👥】Member")
    await member.add_roles(role)
    await member.remove_roles(role2)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Mute**",
        description=f"**{member.mention} קיבל מיוט\n סיבה: {reason}**"
    )
    await ctx.send(embed=embed)
   

#unmute------------------------------------------------
@client.command()
@commands.has_any_role('――――――● Staff ●――――――')
async def unmute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    role2 = discord.utils.get(ctx.guild.roles, name="【👥】Member")
    await member.remove_roles(role)
    await member.add_roles(role2)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Unmute**",
        description=f"**ירד ל{member.mention} המיוט**"
    )
    await ctx.send(embed=embed)

#help staff------------------------------------------------
@client.command(pass_context=True)
@commands.has_any_role('――――――● Staff ●――――――')
async def helpstaff(ctx):
    role = discord.utils.get(ctx.guild.roles, name="――――――● Staff ●――――――")
    channel = ctx.message.channel
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Staff Help 🔱**",
        description=f"**Mute: !mute (@מי שאתם רוצים לתת לו מיוט) (סיבה)\n פקודה לכל הצוות\n\nUnmute: !unmute (@מי שאתם רוצים להוריד לו מיוט)\n פקודה לכל הצוות\n\nWarn: !warn (@מי שאתם רוצים ללת לו אזהרה) (סיבה)\nפקודה לכל הצוות\n\nUnwarn: !unwarn (@מי שאתם רוצים להוריד לו אזהרות) (כמות האזהרות שרוצים להוריד)\nפקודה לכל הצוות\n\nClear: !clear (כמות הודעות שרוצים למחוק)\n פקודה לModerator ומעלה\n\nKick: !kick (@למי רוצים לתת קיק) (סיבה)\nפקודה לAdmin ומעלה\n\nJail: !jail (@למי רוצים לתת jail ) (סיבה)\nפקודה לStaff Manager ומעלה\n\nUnjaul: !unjail (@את מי אתם רוצים להוריד מjail) (סיבה)\nפקודה לStaff Manager ומעלה\n\nBan:!ban (@למי רוצים לתת באן) (סיבה)\nפקודה לManagement ומעלה**"
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/610121204854030379/661669323588370443/white_1.png")
    embed.set_footer(text=f' הפרפיקס של הבוט השתנה מd! ל!')
    await ctx.send(embed=embed)

#jail------------------------------------------------    
@client.command()
@commands.has_any_role('【🔱】Staff Manager', '【🎖️】Management', '【👑】Inspector', '【👑】Owner', '【👑】KingDizi')
async def jail(ctx, member : discord.Member, *, reason=':no_entry_sign:לא נשלחה סיבה:no_entry_sign:'):
    role = discord.utils.get(ctx.guild.roles, name="jail")
    role2 = discord.utils.get(ctx.guild.roles, name="【👥】Member")
    await member.add_roles(role)
    await member.remove_roles(role2)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Jail**",
        description=f"**{member.mention} נכנס לjail\n סיבה: {reason}**"
    )
    await ctx.send(embed=embed)

#unjail------------------------------------------------    
@client.command()
@commands.has_any_role('【🔱】Staff Manager', '【🎖️】Management', '【👑】Inspector', '【👑】Owner', '【👑】KingDizi')
async def unjail(ctx, member : discord.Member):
    role2 = discord.utils.get(ctx.guild.roles, name="jail")
    role = discord.utils.get(ctx.guild.roles, name="【👥】Member")
    await member.add_roles(role)
    await member.remove_roles(role2)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Unjail**",
        description=f"**{member.mention} יצא מהjail**"
    )
    await ctx.send(embed=embed)

#warn------------------------------------------------    
@client.command()
@commands.has_any_role('――――――● Staff ●――――――')
async def warn(ctx, member : discord.Member, *, reason=':no_entry_sign:לא נשלחה סיבה:no_entry_sign:'):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Warn**",
        description=f"**{member.mention} קיבל warn\n סיבה: {reason}**"
    )
    await ctx.send(embed=embed)

#unwarn------------------------------------------------    
@client.command()
@commands.has_any_role('――――――● Staff ●――――――')
async def unwarn(ctx, member : discord.Member, *, num=1):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Unwarn**",
        description=f"**ירד ל{member.mention} הwarns\n מספר הwarns שמורידים: {num}**"
    )
    await ctx.send(embed=embed)

#helpme-commands------------------------------------------------    
@commands.cooldown(1, 20, commands.BucketType.member)
@client.command()
async def helpme(ctx, reason=':no_entry_sign:לא נשלחה סיבה:no_entry_sign:'):
    staffRole = discord.utils.get(ctx.guild.roles, name="――――――● Staff ●――――――")
    if ctx.author.voice:
        await ctx.send(f"**{ctx.author.mention} צריך את עזרתכם {staffRole.mention}\n סיבה: {reason}\nהוא נמצא בחדר: {ctx.author.voice.channel.name}**")
    else:
        await ctx.send(f"**{ctx.author.mention} צריך את עזרתכם {staffRole.mention}\n סיבה: {reason}\n:no_entry_sign:המשתמש לא נמצא בשום חדר:no_entry_sign:**")

#------------------------------------------------    
@commands.cooldown(1, 20, commands.BucketType.member)
@client.command()
async def h(ctx, reason=':no_entry_sign:לא נשלחה סיבה:no_entry_sign:'):
    staffRole = discord.utils.get(ctx.guild.roles, name="――――――● Staff ●――――――")
    if ctx.author.voice:
        await ctx.send(f"**{ctx.author.mention} צריך את עזרתכם {staffRole.mention}\n סיבה: {reason}\nהוא נמצא בחדר: {ctx.author.voice.channel.name}**")
    else:
        await ctx.send(f"**{ctx.author.mention} צריך את עזרתכם {staffRole.mention}\n סיבה: {reason}\n:no_entry_sign:המשתמש לא נמצא בשום חדר:no_entry_sign:**")

#dev------------------------------------------------    
@client.command()
@commands.has_any_role('――――――● Staff ●――――――')
async def dev(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Dev**",
        description=f"**Developer: <@306829958595215360>**"
    )
    await ctx.send(embed=embed)

#members------------------------------------------------    
@client.command()
@commands.has_any_role('――――――● Staff ●――――――')
async def members(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Members**",
        description=f"**מספר האנשים בשרת: {ctx.guild.member_count}**"
    )
    await ctx.send(embed=embed)

#server-info------------------------------------------------    
@client.command()
async def serverinfo(ctx):
    embed = discord.Embed(
        colour=discord.Colour.green(),
        title=f"**ServerInfo**"
    )
    embed.add_field(name=f"**Server Name**", value=f"**{ctx.guild.name}**", inline=False)
    embed.add_field(name=f"**Server Id**", value=f"**506176154844135437**", inline=False)
    embed.add_field(name=f"**Server Owner Ship**", value=f"**{ctx.guild.owner}**", inline=False)
    embed.add_field(name=f"**Server Region**", value=f"**Europe**", inline=False)
    embed.add_field(name=f"**Users Count**", value=f"**Members: {ctx.guild.member_count} | Bots: 17**", inline=False)
    embed.add_field(name=f"**AFK Time**", value=f"**1 hour**", inline=True)
    embed.add_field(name=f"**AFK Room**", value=f"**『💤』AFK**", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/610121204854030379/661669323588370443/white_1.png")
    await ctx.send(embed=embed)
#help------------------------------------------------    
@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Commands**"
    )
    embed.add_field(name=f"**General Commands :question:**", value="**!helpgeneral**", inline=True)
    embed.add_field(name=f"**Staff Commands 🔱**", value="**!helpstaff**", inline=True)
    embed.add_field(name=f"**Info Commands :notebook_with_decorative_cover:**", value="**!helpinfo**", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def helpgeneral(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**General Commands :question:**"
    )
    embed.add_field(name=f"**!helpme, !h**", value="**Request help from staff**", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def helpinfo(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Server Info :notebook_with_decorative_cover:**"
    )
    embed.add_field(name=f"**!serverinfo**", value="**Send the server information**", inline=False)
    embed.add_field(name=f"**!userinfo**", value="**Send the user information**", inline=False)
    embed.add_field(name=f"**!members**", value="**Send the member count on the server**", inline=False)
    embed.add_field(name=f"**!avatar member.mention**", value="**Send the avater of the member**", inline=False)
    embed.add_field(name=f"**!dev**", value="**Shows who development the bot**", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx):
    member = ctx.author
    embed = discord.Embed(
        colour=discord.Colour.green(),
        title=f"**UserInfo**",
        timestamp=datetime.utcnow()
    )
    embed.add_field(name=f"**User Name**", value=f"**{member.name}**", inline=True)
    embed.add_field(name=f"**User ID**", value=f"**{member.id}**", inline=True)
    embed.add_field(name=f"**NickName**", value=f"**{member.nick}**", inline=True)
    embed.add_field(name=f"**Status**", value=f"**{member.status}**", inline=True) 
    embed.add_field(name=f"**Playing**", value=f"**{member.activity}**", inline=True)
    embed.add_field(name=f"**Highest Role**", value=f"**{member.top_role}**", inline=True)
    embed.add_field(name=f"**Join To Discord**", value=f"**{member.created_at}**", inline=False)
    embed.add_field(name=f"**Join The Server**", value=f"**{member.joined_at}**", inline=False)
    embed.set_footer(text=f'Info of {member.name}')
    embed.set_thumbnail(url=f"{member.avatar_url}")
    await ctx.send(embed=embed) 

@client.command()
async def avatar(ctx, member : discord.Member):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_image(url=f"{member.avatar_url}")
    await ctx.send(embed=embed) 

#=================================TOKEN==================================
client.run('NzAwMDcxOTEzODIwNzgyNjk0.XsfCLQ.KQ2CpFMeUtUcpbDRwYMhNktDI-Y')
