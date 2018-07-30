class Account:
	#User.
	user = ""
	#Amount
	coins = 0
	def Load(self, user, coins):
		self.user = user
		self.coins = coins
	def Create(self, user, coins):
		self.user = user 
		self.coins = coins 
		accounts.append(self)
		UpdateAccounts()
	def Create(self, user):
		self.user = user 
		accounts.append(self)
		UpdateAccounts()
	def Deposit(self, amount):
		self.coins += amount
		UpdateAccounts()
	def Withdraw(self, amount):
		temp = self.coins - amount
		if temp < 0:
			return False
		else:
			self.coins = temp
			UpdateAccounts()
accounts = []
def CheckAccount(user):
	for account in accounts:
		if account.user == user:
			return True
	return False
def FindAccount(user):
	for account in accounts:
		if account.user.lower() == user.lower():
			return account
	return False
def LoadAccounts():
	#accounts = []
	accountRecords = open("accountRecords.txt","r")
	line = accountRecords.readline()
	while line:
		if line != '\n' and line != "":
			data = line.split(",")
			a = Account()
			a.Load(data[0], int(data[1]))
			accounts.append(a)
		line = accountRecords.readline()
	accountRecords.close()
def UpdateAccounts():
	file = open("accountRecords.txt","w")
	for account in accounts:
		file.write(account.user+","+str(account.coins)+"\r\n")
	file.close()
LoadAccounts()