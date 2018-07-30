import discord

async def KickUser(client, userName: discord.User):
	try:
		await client.kick(userName)
	except Exception as e:
		print(e)