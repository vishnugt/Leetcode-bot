from discord.ext import tasks
import discord
import LeetcodeHelper
import config
import MongoHelper
import schedule

client = discord.Client()

@client.event
async def on_message(message):
	command = message.content
	if command.startswith("/addLeetCodeUser"):
		user = command.split(" ")[1].strip()
		MongoHelper.addUser(user)
		await message.channel.send("User added")


async def job():

	print("Hey I'm on loop")
	users = MongoHelper.getUsers()
	for user in users:
		submissionsFromLeetcode = LeetcodeHelper.getUserSubmissions(user)
		submissionsFromMongo = MongoHelper.getSubmissionsForUser(user)
		for submission in submissionsFromLeetcode:
			if submission in submissionsFromMongo:
				continue
				
			# add to MongoDB
			# print in channel
			titleSlug = submission["titleSlug"]
			title = submission["title"]
			timestamp = submission["timestamp"]
			url = "https://leetcode.com/problems/" + titleSlug

			MongoHelper.addSubmission(user, titleSlug)
			print("{0} completed {1}, give the problem a shot [here](url)".format(user, title))


schedule.every(20).seconds.do(job)
client.run(config.discordToken)