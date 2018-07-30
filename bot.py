import discord
import os
import random
from management.warning import *
from management.kicking import *
from economy.coins import *
from economy.matchmaking import *
from games.purge import *
from games.roulette import *
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='$')
blDict = open("blDictionary.txt","r").read().split()
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    elif message.content != "" and message.content.lower() in blDict:
    	w = Warning()
    	if w.Create(str(message.author), "Bad Language"):
    		msg = '{0.author.mention} has been issued a warning for bad language'.format(message)
    		await client.send_message(message.channel, msg)
    	else:
    		msg = '{0.author.mention} has recieved too many warnings, and now will be kicked'.format(message)
    		await client.send_message(message.channel, msg)
    		await KickUser(client,message.author)
    await bot.process_commands(message)
@bot.command(pass_context=True)
async def commands(ctx):
	embed=discord.Embed(title="Commands",color=0x45a5d3)
	embed.add_field(name="$kick", value="Kick a user from the server", inline=False)
	embed.add_field(name="$clear", value="Clear a number of messages from the channel", inline=False)
	embed.add_field(name="$joinmatchmaking", value="Join the matchmaking queue", inline=False)
	embed.add_field(name="$startpurge", value="Start a purge event", inline=False)
	embed.add_field(name="$purgelist", value="See users who have joined the purge", inline=False)
	embed.add_field(name="$endpurge", value="End the purge and view the results", inline=False)
	embed.add_field(name="$givecoins", value="Give a user X amount of coins", inline=False)
	embed.add_field(name="$takecoins", value="Take X amount of coins from a user", inline=False)
	embed.add_field(name="$balance", value="Check how many coins you have", inline=False)
	embed.add_field(name="$balanceof", value="Check how many coins a user has", inline=False)
	embed.add_field(name="$leaderboard", value="View the coin leaderboard", inline=False)
	await client.send_message(ctx.message.channel,embed=embed)
@bot.command(pass_context=True)
async def leaderboard(ctx):
	temp = accounts
	temp.sort(key=lambda Account: Account.coins, reverse=True)
	embed=discord.Embed(title="Leaderboard",color=0x45a5d3)
	for user in temp:
		embed.add_field(name=user.user, value="{} coins".format(user.coins), inline=False)
	await client.send_message(ctx.message.channel,embed=embed)
@bot.command(pass_context=True)
async def addrole(ctx, arg1, arg2):
	if ctx.message.channel.permissions_for(ctx.message.author).manage_server:
		role = discord.utils.get(ctx.message.server.roles, name=arg1)
		if role != None:
			user = GetUser(ctx.message.server.members, arg2)
			if user != False:
				await client.add_roles(user, role)
				await client.send_message(ctx.message.channel,"{} is now {}".format(user.name, role))
			else:
				await client.send_message(ctx.message.channel,"Unable to find the user given")
		else:
			await client.send_message(ctx.message.channel,"Unable to find the role given")
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")   
@bot.command(pass_context=True)
async def kick(ctx, arg):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		server = client.get_server(id="388460730996752385")
		user = GetUser(server.members, arg)
		if user != False:	
			await client.send_message(ctx.message.channel,"Successfully kicked user '{}'".format(arg))
			await KickUser(client, user)
		else:
			await client.send_message(ctx.message.channel,"Unable to find user '{}'".format(arg))
@bot.command(pass_context = True)
async def clear(ctx, number):
	if ctx.message.channel.permissions_for(ctx.message.author).manage_channels:
	    mgs = [] #Empty list to put all the messages in the log
	    number = int(number) #Converting the amount of messages to delete to an integer
	    if number > 100:
	    	number = 100
	    async for x in client.logs_from(ctx.message.channel, limit = number):
	        mgs.append(x)
	    await client.delete_messages(mgs)
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def joinmatchmaking(ctx):
	user = FindAccount(ctx.message.author.name)
	AddUser(user)
@bot.command(pass_context=True)
async def startpurge(ctx):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		#If start purge failed
		if StartPurge() == False:
			await client.send_message(ctx.message.channel,"Please wait for the current purge to finish before starting a new one")
		else:
			await client.send_message(ctx.message.channel,"A new purge has started... use $joinpurge for the chance to win big!")
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def purgelist(ctx):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		if users != []:
			temp = ""
			for u in users:
				temp+=u.name+", "
			await client.send_message(ctx.message.channel,temp)
		else:
			await client.send_message(ctx.message.channel,"There are no users in the purge")
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def joinpurge(ctx):
	server = ctx.message.server
	user = GetUser(server.members, ctx.message.author.name)
	if AddPurgeUser(user) == False:
		await client.send_message(ctx.message.channel,"There isn't a purge at the moment")
	else:
		await client.send_message(ctx.message.channel,"You have joined the purge")
@bot.command(pass_context=True)
async def endpurge(ctx):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		#Gets all users not kicked from the purge and rewards them.
		survivers = await EndPurge(client)
		for u in survivers:
			reward = random.randint(20,200)
			FindAccount(u.name).Deposit(reward)
			await client.send_message(ctx.message.channel,"{} has been awarded {} coins for survivng the purge!".format(u.name,reward))
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def givecoins(ctx, arg1, arg2):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		account = FindAccount(arg1)
		try:
			amount = int(arg2)
			if account != False:
				account.Deposit(amount)
				server = client.get_server(id="388460730996752385")
				user = GetUser(server.members, arg1)
				return await client.send_message(ctx.message.channel,"{} has been given {} coins".format(user, arg2))
			else:
				return await client.send_message(ctx.message.channel,"Unable to find user '{}'".format(arg1))	
		except ValueError:
			await client.send_message(ctx.message.channel,"Second argument must be an integer (number)")	
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def takecoins(ctx, arg1, arg2):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		account = FindAccount(arg1)
		try:
			amount = int(arg2)
			if account != False:
				if account.Withdraw(amount) != False:
					server = client.get_server(id="388460730996752385")
					user = GetUser(server.members, arg1)
					return await client.send_message(ctx.message.channel,"{} coins were taken from {}".format(arg2,user))
				else:
					return await client.send_message(ctx.message.channel,"Not enough coins are available")
			else:
				return await client.send_message(ctx.message.channel,"Unable to find user '{}'".format(arg1))
		except ValueError:
			await client.send_message(ctx.message.channel,"Second argument must be an integer (number)")	
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def balance(ctx):
	await client.send_message(ctx.message.channel,"You currently have {} coins".format(FindAccount(ctx.message.author.name).coins))
@bot.command(pass_context=True)
async def balanceof(ctx, arg):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		account = FindAccount(arg)
		if account != False:
			await client.send_message(ctx.message.channel,"{} currently has {} coins".format(arg,account.coins))
		else:
			await client.send_message(ctx.message.channel,"Unable to find user '{}'".format(arg))
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command")
@bot.command(pass_context=True)
async def startroulette(ctx):
	if StartRoulette() == False:
		await client.send_message(ctx.message.channel,"Please wait for the current Roulette Game to finish before starting a new one!")
	else:
		await client.send_message(ctx.message.channel,"A new Roulette Game has started. Use $joinroulette for your chance of winning!")
		

@bot.command(pass_context=True)
async def rouletteplayers(ctx):
	if users != []:
		temp = ""
		for u in users:
			temp+=u.name+", "
		await client.send_message(ctx.message.channel,temp)
	else:
		await client.send_message(ctx.message.channge,"There are no players in the Roulette Game!")

@bot.command(pass_context=True)
async def joinroulette(ctx):
	server = ctx.message.server
	user = GetUser(server.members, ctx.message.author.name)
	if AddRoulettePlayer(user) == False:
		await client.send_message(ctx.message.channel,"There isn't a Roulette Game active currently!")
	elif insufficientFunds == True:
		await client.send_message(ctx.message.channel,"You have insufficient funds!")
	else:
		await client.send_message(ctx.message.channel,"You have joined the Roulette Game!")

@bot.command(pass_context=True)
async def spinroulette(ctx):
	if ctx.message.channel.permissions_for(ctx.message.author).kick_members:
		FindAccount(winner).deposit(pot)
		await client.send_message(ctx.message.channel,"{} has been awarded {} coins for winning the Roulette Game!".format(winner,pot))
		
	else:
		await client.send_message(ctx.message.channel,"You do not have the required permissions for this command!")
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	CheckServerForAccounts()
@client.event
async def on_member_join(member):
	if not CheckAccount(member.name):
		a = Account()
		a.Create(member.name)
	
def GetUser(data, user):
	for i in data:
		if str(i.name).lower() == user.lower():
			return i
	return False
def CheckServerForAccounts():
	#Connected steves
	server = client.get_server(id="388460730996752385")
	for user in server.members:
		if CheckAccount(user.name) == False:
			a = Account()
			a.Create(user.name)
client.run('NDY5MTcwOTk3NTAxNjI0MzMw.DjD1IA.NtakvdszP945tmDTrSLXSJSFrsM')
