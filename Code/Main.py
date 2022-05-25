import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext  
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
import asyncio
  
  
bot = commands.Bot(command_prefix=['?'], intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
  

@bot.event
async def on_ready():
  print('로딩완료')
  await bot.change_presence(activity=discord.Game("관리하는중..."))
  
#docs
@slash.slash(name="티켓생성",description="티켓 임베드 생성(관리자만 보입니다)",guild_ids=[975739201721073734], default_permission = False)
async def ticket(ctx):
  chan = bot.get_channel(978546439443587092)
  embed = discord.Embed(title=f"차스공 문의", description = "버튼을 눌러 티켓을 생성할 수 있습니다.", color = 0xFF73FA)
  buttons = [
    create_button(style=ButtonStyle.green, label="티켓생성", custom_id = 'ticket', emoji="📪")
  ]
  action_row = create_actionrow(*buttons)
  await chan.send(embed = embed,components=[action_row])
  await ctx.send('생성완료', hidden = True)
  
  
@bot.event
async def on_component(ctx):
  id = ctx.custom_id
    
  if id == "ticket":
    category = discord.utils.get(ctx.guild.categories, name="📡ㆍ문의 공간 ───────────")
    guild = ctx.guild
    msg = await guild.create_text_channel(f"{ctx.author.name}님의 문의채널", category = category)
    await msg.set_permissions(ctx.author,speak=True,send_messages=True,read_message_history=True,read_messages=True)   
    await ctx.send(f"문의채널이 생성되었습니다! <#{msg.id}>", hidden = True)
  
    chan = bot.get_channel(msg.id)
    buttons = [
      create_button(style=ButtonStyle.green, label="티켓닫기", custom_id = "close", emoji="🔒")
    ]
    action_row = create_actionrow(*buttons)
    await chan.send('티켓이 생성이 되었습니다!\n \n> 티켓닫기는 관리자만 가능합니다.',components=[action_row])
    
  if id == "close":
    if ctx.author.guild_permissions.administrator:
      await ctx.send('3초후에 채널이 삭제됩니다...')
      await asyncio.sleep(3)
      channel = bot.get_channel(ctx.channel.id)
      await channel.delete()
  
    else:
      await ctx.send("티켓닫기는 관리자만 가능합니다.", hidden = True)

bot.run('Token')
