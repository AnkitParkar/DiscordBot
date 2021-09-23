import nest_asyncio
nest_asyncio.apply()

from transfer import recieve_from_discord
import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

called=False

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
    embed.add_field(name='.hello', value='Responds to your hello with a hi', inline=False)
    embed.add_field(name='.syncsheets',value='Sync the local csv file to the Google Sheets. Command only to be used after approval.',inline=False)
    embed.add_field(name='.clearfiles',value="Clear the local csv files. Command only to be used after approval.")

    await ctx.send(embed=embed)

@client.command()
async def rollcall(ctx):
    #msg= await client.send_message(ctx.message.channel)
    #await client.add_reaction(msg,":Thumbs UP:")
    response="Attendance for this meeting!\nReact to this message with the thumbs up emoji, if any issues message @Parkar"
    await ctx.send(response)
    #print(f'At {datetime.datetime.now().strftime("%H:%M")} called is {called}')
    @client.event
    async def on_reaction_add(reaction,user):
        channel=reaction.message.channel
        #print(type(channel))
        if status(str(channel)):
            recieve_from_discord(str(channel),str(user.display_name))
            print(f'{user.display_name} responded in {channel}')
        

@client.command()
async def syncsheets(ctx):
    value=send_to_sheet()
    if value:
        response=f"Sheets have been synced at. {datetime.datetime.now()}"
    else:
        response="Error."
    await ctx.send(response)


@client.command()
async def clearfiles(ctx):
    clear_csv()
    embed=discord.Embed(colour=discord.Colour.blue())
    embed.set_author(name='Content in the csv file:')
    with open("count.csv","r") as reading:
        reader=csv.reader(reading)
        for row in reader:
            embed.add_field(name=row[0],value=row,inline=False)

    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Cannot process ({error})\nPlease type .help for commands.')



def send_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds=ServiceAccountCredentials.from_json_keyfile_name("DiscordBotSheet.json", scope)
    client= gspread.authorize(creds)
    wb=client.open_by_url("https://docs.google.com/spreadsheets/d/14Pnrj_bT8sdWrBkobaHLFj9U4P6ILAPklV-s_2fGUCc/edit?usp=sharing")
    temp=[]
    date=datetime.datetime.now().strftime("%d/%m")
    with open("count.csv","r") as file:
        reader=csv.reader(file)
        for row in reader:
            temp=row
            print(row[0],"done")
            sheet=wb.worksheet(row[0])
            temp[0]=date
            sheet.append_row(temp.copy())
            temp.clear()
    return True
    
def clear_csv():
    f=open("count.csv",'w')
    f.truncate()
    f.close()
    with open("base_count.csv","r") as reading:
        reader=csv.reader(reading)
        with open("count.csv","a",newline='') as appending:
            append=csv.writer(appending)
            for row in reader:
                append.writerow(row)

def status(channel):
    approve=False
    time=datetime.datetime.now().strftime("%H:%M")
    print(time)
    with open("times.csv","r") as read:
        reader=csv.reader(read)
        for row in reader:
            #print("Checking ",row[0]," type: ",type(row[0]))
            if channel == row[0]:
                print("Channel found")
                if row[1]<=time and time<=row[2]:
                    approve=True
    return approve



token=open("secret_token.txt","r").readline()
client.run(token)
    
