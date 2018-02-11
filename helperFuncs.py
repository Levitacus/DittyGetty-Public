class timeObject:



	def __init__(self):

		self.hour = 0
		self.minute = 0

	



	def stringToTime(self, stringTime):

		PM = 0

		AM = 0



		stringTime = stringTime.replace(" ", "").strip().lower()



		if 'pm' in stringTime:

			PM = 1

		if 'am' in stringTime:

			AM = 1



		for sub in ['am','pm']:

			if sub in stringTime:

				stringTime = stringTime.replace(sub,"")



		timeTokens = stringTime.split(':')

		if PM:

			self.hour = (int)(timeTokens[0])

			if(self.hour != 12):

				self.hour = self.hour + 12



		else:

			self.hour = (int)(timeTokens[0])

			if AM and (self.hour == 12):

				self.hour = 0



		self.minute = (int)(timeTokens[1])



	@staticmethod

	def afterTime(currentTime, targetTime):

		currentMins = (currentTime.hour * 60) + currentTime.minute

		targetMins = (targetTime.hour * 60) + targetTime.minute



		if(currentMins > targetMins):

			return True

		else:

			return False

	@staticmethod

	def beforeTime(currentTime, targetTime):

		currentMins = (currentTime.hour * 60) + currentTime.minute

		targetMins = (targetTime.hour * 60) + targetTime.minute



		if(currentMins < targetMins):

			return True

		else:

			return False



	def toString(self):

		return ("%02d:%02d" % (self.hour, self.minute))

		

		



#time1 = TimeObject()

#time2 = TimeObject()

#time1.stringToTime('03:33PM')

#time2.stringToTime('3:02PM')

#print(TimeObject.afterTime(time1, time2))

#print(time2.toString())