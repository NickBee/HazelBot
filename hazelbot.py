#hazelbot.py
import os
import discord
import random
import praw
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN', default=None)
DABEMOJI = os.getenv("DAB_EMOJI", default=None)
CLIENT_ID = os.getenv("CLIENT_ID", default=None)
CLIENT_SECRET = os.getenv("CLIENT_SECRET", default=None)
USER_AGENT = os.getenv("USER_AGENT", default=None)

client = commands.Bot(command_prefix = '!')
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

testqueue = []

##aiohttp
##TODO read up on calling sync functions from async ones, this might not be a good thing to do
async def load_random_reddit_image(subreddit_title):
	subredditlist = list(reddit.subreddit(subreddit_title).hot(limit=100))
	for submission in subredditlist:
		if submission.stickied or submission.is_self or submission.over_18:
			subredditlist.remove(submission)
			print (f'{submission.url} removed')
	if(len(subredditlist) > 0):
		return random.choice(subredditlist).url
	else:
		return "No images found."

@client.event
async def on_ready():
	print(f'{client.user} is alive.')

@client.command()
async def test(ctx):
	await ctx.send("Testing")

@client.command()
async def helpme(ctx):
	await ctx.send("`Commands: \n !marshal : Display a heartfelt message from Marshal to Hazel \n !hazel : See Hazel in all her beauty \n !dab : yeah \n !funny : Say a bad word \n !hegdog : Random image/post from r/hedgehog \n !raccoon : Random image/post from r/raccoons \n !hammo : Random image/post from r/hamsters \n !ratto : Random image/post from r/rats \n !bat : Random image/post from r/batty`")

@client.command()
async def marshal(ctx):
	await ctx.send(file=discord.File('Marshal_NH.png'))
	await ctx.send("My face was chiseled by the gods themselves, Hazel. My body was sculpted to the proportions of Michelangelo's David. You on the other hand, well... you're a pit of despair. Hazel, you disgust me. You disgust everyone. And you will never, *ever* be anyone's fave.")

@client.command()
async def hazel(ctx):
	hazelimages = ['ugly1.png', 'ugly2.png', 'ugly3.png', 'ugly4.png', 'ugly5.png', 'ugly6.png', 'ugly7.png']
	await ctx.send(file=discord.File(random.choice(hazelimages)))

@client.command()
async def dab(ctx):
	await ctx.send(f'{DABEMOJI}')

@client.command()
async def funny(ctx):
	funnyresponses = ["STOP TALKING THAT!!!", "STOP THE BAD WORD!!!", "IF YOU KEEP SAYING BAD WORD'S LEAVE THE CHAT!!!"]
	await ctx.send(random.choice(funnyresponses))

@client.command(aliases = ['hedgehog', 'hedgehogs'])
async def hegdog(ctx):
	await ctx.send(await load_random_reddit_image("hedgehog+hedgehogs"))

@client.command(aliases = ['trashpanda', 'trashpandas', 'tonto'])
async def raccoon(ctx):
	await ctx.send(await load_random_reddit_image("raccoons+trashpandas+raccoongifs"))

@client.command(aliases = ['hamster', 'hamsters'])
async def hammo(ctx):
	await ctx.send(await load_random_reddit_image("hamster+hamsters"))

@client.command(aliases = ['rat', 'rats'])
async def ratto(ctx):
	await ctx.send(await load_random_reddit_image("rat+rats"))

@client.command(aliases = ['battos', 'skydoggos'])
async def bat(ctx):
	await ctx.send(await load_random_reddit_image("batty+babybats"))

@client.command(aliases = ['wholesome', 'pure'])
async def cursed(ctx):
	await ctx.send(await load_random_reddit_image("cursedimages"))

@client.command()
async def que(ctx, *arg):
	name = (ctx.author, ' '.join([str(element) for element in arg]))[len(arg) > 0]
	testqueue.append(name)
	await ctx.send(f'{name} added to queue. There are now {len(testqueue)} items in queue.')

@client.command()
async def quenext(ctx):
	try:
		await ctx.send(f'Next item in queue: {testqueue.pop(0)}. There are now {len(testqueue)} items in queue.')
	except IndexError:
		await ctx.send('No items in queue.')

async def on_message(message):
	if message.author == client.user:
		return
	await client.process_commands(message)

client.run(TOKEN)