import traceback
import sys
from discord.ext import tasks
import discord
import LeetcodeHelper
import config
import MongoHelper
import schedule

client = discord.Client()
channel = None

@client.event
async def on_message(message):
	command = message.content
	if command.startswith("/addLeetCodeUser"):
		user = command.split(" ")[1].strip()
		MongoHelper.addUser(user)
		await message.channel.send("User added")


@client.event
async def on_ready():
    print('Logged in')
    global channel
    channel = client.get_channel(config.channelId)
    job.start()

@tasks.loop(seconds = 300)
async def job():
	#print('loop')
	users = MongoHelper.getUsers()
	for user in users:
		submissionsFromLeetcode = LeetcodeHelper.getUserSubmissions(user)
		submissionsFromMongo = MongoHelper.getUserSubmissions(user)
		# print(submissionsFromLeetcode)
		# print(submissionsFromMongo)
		# print("*******************")
		if submissionsFromMongo is None or submissionsFromLeetcode is None:
			continue
		for titleSlug, submission in submissionsFromLeetcode.items():
			if titleSlug in submissionsFromMongo:
				continue
			title = submission["title"]
			timestamp = submission["timestamp"]
			url = "https://leetcode.com/problems/" + titleSlug

			MongoHelper.addSubmission(user, titleSlug)
			line = user + " completed the problem in " + submission["lang"]
			embed=discord.Embed(title=title, url=url, description=line, color=0xFF5733)
			await channel.send(embed=embed)
			#await channel.send(line)


client.run(config.discordToken)
