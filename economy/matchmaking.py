from economy.coins import *
users = []

def AddUser(user):
	users.append(user)
	print(users)
	ProcessMatches()
def ProcessMatches():
	users.sort(key=lambda Account: Account.coins, reverse=True)
	
		
