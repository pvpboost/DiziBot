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


client = commands.Bot(command_prefix = 'd!')
#client.event===========================================

#Bot Start------------------------------------------------
@client.event
async def on_ready():
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
    embed = discord.Embed(colour=discord.Colour(0x95efcc), description=f"**נכנס לשרת**")

    embed.set_image(url="https://cdn.discordapp.com/attachments/694151021139853312/708688917343240273/Bot_Logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/694151021139853312/708688917343240273/Bot_Logo.png")
    embed.set_author(name=f"{member.name}",icon_url=f'{member.avatar_url}')
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/694151021139853312/708688917343240273/Bot_Logo.png")

    channel = discord.utils.get(member.guild.channels, name="『👥』welcome")
    await channel.send(embed=embed)

#Welcome leave------------------------------------------------
@client.event
async def on_member_remove(member):
    embed = discord.Embed(colour=discord.Colour(0x95efcc), description=f"**יצא מהשרת**")

    embed.set_image(url="https://cdn.discordapp.com/attachments/694151021139853312/708688788762918912/Bot_Logo_black_and_white.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/694151021139853312/708688788762918912/Bot_Logo_black_and_white.png")
    embed.set_author(name=f"{member.name}",icon_url=f'{member.avatar_url}')
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/694151021139853312/708688788762918912/Bot_Logo_black_and_white.png")

    channel = discord.utils.get(member.guild.channels, name="『👥』welcome")
    await channel.send(embed=embed)

#verify------------------------------------------------
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 712019978240655451:
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
                print("Member not found")
        else:
            print("Role not found")

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
async def ban(ctx, member, *, reason='לא נשלחה סיבה'):
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
async def mute(ctx, member : discord.Member, *, reason='לא נשלחה סיבה'):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
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
    await member.remove_roles(role)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Unmute**",
        description=f"**ירד ל{member.mention} המיוט**"
    )
    await ctx.send(embed=embed)

#help------------------------------------------------
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def helps(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"**Staff Help**",
        description=f"**Mute: d!mute (@מי שאתם רוצים לתת לו מיוט) (סיבה)\n פקודה לכל הצוות\n\nUnmute: d!unmute (@מי שאתם רוצים להוריד לו מיוט)\n פקודה לכל הצוות\n\nClear: d!clear (כמות הודעות שרוצים למחוק)\n פקודה לModerator ומעלה\n\nKick: d!kick (@למי רוצים לתת קיק) (סיבה)\nפקודה לAdmin ומעלה\n\nJail: d!jail (@למי רוצים לתת jail ) (סיבה)\nפקודה לStaff Manager ומעלה\n\nUnjaul: d!unjail (@את מי אתם רוצים להוריד מjail) (סיבה)\nפקודה לStaff Manager ומעלה\n\nBan: d!ban (@למי רוצים לתת באן) (סיבה)\nפקודה לManagement ומעלה**"
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/610121204854030379/661669323588370443/white_1.png")
    await ctx.send(embed=embed)

#jail------------------------------------------------    
@client.command()
@commands.has_any_role('【🔱】Staff Manager', '【🎖️】Management', '【👑】Inspector', '【👑】Owner', '【👑】KingDizi')
async def jail(ctx, member : discord.Member, *, reason='לא נשלחה סיבה'):
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


#=================================TOKEN==================================
client.run('NzAwMDcxOTEzODIwNzgyNjk0.XsLatA.W9RuAZMlPUFle90XI3ghKGgyEMI')
