import discord
import random

running = False
insufficientFunds = False
users = []
pot = 0

def StartRoulette():
	users = []
	global running
	if not running:
		running = True
	else:
		return False

def AddRoulettePlayer(user):
	global insufficientFunds
	global pot
	global running
	if running:
		exists = False
		for u in users:
			if u.name == user.name:
				exists = True
		if not exists:
			player = FindAccount(user)
			fee = 10
				if player != False
					if account.Withdraw(fee) != False:
						pot += fee
						users.append(user)
						return pot
					else:
						insufficientFunds = True
						return insufficientFunds
	else:
		return False
		
async def SpinRoulette():
	running = False
	winner = randrange(0,len(users))
	return winner