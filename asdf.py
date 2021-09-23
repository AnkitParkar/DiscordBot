import nest_asyncio
nest_asyncio.apply()

from transfer import recieve_from_discord

import discord
from discord.ext import commands
from discord.ext.commands import Bot

client= commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def hello(ctx):
    print("Hello called")
    await ctx.send("Hi")

@client.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms')


client.remove_command('help')

@client.command(pass_context=True)
async def help(ctx):
    embed=discord.Embed(colour=discord.Colour.blue())
    embed.set_author(name='Help : list of commands available ')
    embed.add_field(name='.rollcall',value='Used for attendance, respond to the following message',inline =False)
    embed.add_field(name='.ping', value='Returns the response time of the bot', inline=False)
    embed.add_field(name=".hello", value='Responds to your hello with a hi', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def rollcall(ctx):
    response="Attendance for this meeting!\nReact to this message with the thumbs up emoji, if any issues message @Parkar"
    await ctx.send(response)
    
    @client.event
    async def on_reaction_add(reaction,user):
        channel=reaction.message.channel
        #print(type(channel))
        recieve_from_discord(str(channel),str(user.display_name))
        print(f'{user.display_name} responded in {channel}')
        

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Try .Cannot process ({error})\nPlease type .help for commands.')



#def send_to_csv(channel,name,time):
    
    
token=open("secret_token.txt","r").readline()
client.run(token)
    
