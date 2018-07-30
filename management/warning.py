class Warning:
	#User.
	user = ""
	#Reason.
	reason = ""
	def Load(self, user, reason):
		self.user = user
		self.reason = reason
	def Create(self, user, reason):
		self.user = user 
		self.reason = reason 
		#If warning count is equal to max amount of warnings.
		UpdateWarnings()
		if GetWarningCount(user) >= 3:
			return False
		else:
			file = open("warningDictionary.txt","a")
			file.write(user+","+reason+"\r\n")
			file.close()
			warnings.append(self)
			return True
warnings = []
def FindWarnings(user):
	w = ""
	for warning in warnings:
		if warning.user == user:
			w += warning.reason
	return w
def GetWarningCount(user):
	count = 0
	for warning in warnings:
		if warning.user == user:
			count+=1
	print(count)
	return count
def UpdateWarnings():
	warnings = []
	warningDictionary = open("warningDictionary.txt","r")
	line = warningDictionary.readline()
	while line:
		if line != '\n' and line != "":
			data = line.split(",")
			w = Warning()
			w.Load(data[0], data[1])
			warnings.append(w)
		line = warningDictionary.readline()
UpdateWarnings()

