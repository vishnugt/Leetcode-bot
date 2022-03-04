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
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    global channel
    channel = client.get_channel(802543833812172814)
    job.start()
    print('------')

@tasks.loop(seconds = 30)
async def job():
	print('loop')
	
	users = MongoHelper.getUsers()
	for user in users:
		submissionsFromLeetcode = LeetcodeHelper.getUserSubmissions(user)
		submissionsFromMongo = MongoHelper.getUserSubmissions(user)
		print(submissionsFromLeetcode)
		print(submissionsFromMongo)
		print("*******************")
		if submissionsFromMongo is None or submissionsFromLeetcode is None:
			continue
		for titleSlug, submission in submissionsFromLeetcode.items():
			if titleSlug in submissionsFromMongo:
				continue
			title = submission["title"]
			timestamp = submission["timestamp"]
			url = "https://leetcode.com/problems/" + titleSlug

			MongoHelper.addSubmission(user, titleSlug)
			line = user + " completed " + title + ", give the problem a shot [here]( " + url + ")"
			await channel.send(line)


client.run(config.discordToken)
