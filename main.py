import discord
from discord.ext import commands
import json
from discord.ext.commands import Bot
from keep_alive import keep_alive
from discord.ext import tasks
print("Started")
import asyncio

intents = discord.Intents().all()
intents.members = True
intents.guilds = True

prefix = "!"

help_command = commands.DefaultHelpCommand(no_category='Commands')

bot = commands.Bot(command_prefix=(prefix),
                   help_command=help_command,
                   intents=intents)
bot.remove_command("help")


@bot.event
async def on_member_join(member):
    with open('guilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    channel_id = guilds_dict[str(member.guild.id)]
    await bot.get_channel(int(channel_id)).send(f"{member.mention}")
    embed = discord.Embed(
        title=f"Info",
        description=f"Welcome {member.mention}, please verify using !verify",
        colour=discord.Colour.dark_blue())
    await bot.get_channel(int(channel_id)).send(embed=embed)


@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name="test")
    await channel.edit(name = "Member Count: " + str(guild.member_count) )


@commands.has_permissions(administrator=True)
@bot.command(name='setverify')
async def set_verify_channel(ctx, channel: discord.TextChannel):
    with open('guilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict[str(ctx.guild.id)] = str(channel.id)
    with open('guilds.json', 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)

    await ctx.send(
        f'Set verification channel for {ctx.message.guild.name} to {channel.name}')


@bot.command()
async def verify(ctx):
  role = "Verified"
  role2 = "Member"
  member = ctx.author
  rank = discord.utils.get(member.guild.roles, name=role)
  rank2 = discord.utils.get(member.guild.roles, name=role2)
  await member.add_roles(rank)
  await member.add_roles(rank2)
  await member.send(f"Thank you for verifying in {ctx.guild.name}")
  print(f"{member.mention} Verified!")


@bot.command()
@commands.is_owner()
async def doit(ctx, role: discord.Role):
  therole = "Verified"
  guild = ctx.guild
  channels = ctx.guild.channels
  for channel in channels:
      if isinstance(channel, discord.TextChannel):
          await channel.set_permissions(role, view_channel=True)


keep_alive()
print("Started")
bot.run("ODcyNjU3MzY3NzIzMDQwODQ4.YQtDgQ.8HQ6E6r5ZAIlttyc7Rmvxd23TFE")