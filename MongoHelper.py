import pymongo
import config


client = pymongo.MongoClient(config.connectionString)
db = client["leetcode"]
usersCollection = db["users"]
submissionCollection = db["submissions"]


def addUser(user):
	row = {"user" : user}
	usersCollection.insert_one(row)


def getUsers():
	rows = usersCollection.find()
	for row in rows:
		print(row)
	return rows

def getSubmissions():
	submissions = submissionCollection.find()
	for submission in submissions:
		print(submission)
	return submissions

def getSubmissionsForUser(user):
	query = {"user": user}
	submissions = submissionCollection.find(query)
	for submission in submissions:
		print(submission)
	return submissions

def addSubmission(user, titleSlug):
	row = {"user": user, "titleSlug": titleSlug}
	submissionCollection.insert_one(row)
