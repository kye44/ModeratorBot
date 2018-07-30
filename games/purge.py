import discord
import random
from management.kicking import *
started = False
users = []
def StartPurge():
	users = []
	global started
	if not started:
		started = True
	else:
		return False
def AddPurgeUser(user):
	global started
	if started:
		exists = False
		for u in users:
			if u.name == user.name:
				exists = True
		if not exists:
			users.append(user)
	else:
		return False
async def EndPurge(client):
	started = False
	for u in users:
		if random.randrange(0,2) == 1:
			await KickUser(client, u)
			users.remove(u)
	return users

