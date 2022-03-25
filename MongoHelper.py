import traceback
import sys
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
	userIds = []
	for row in rows:
		userIds.append(row["user"])
	return userIds

def getSubmissions():
	submissions = submissionCollection.find()
	subList = []
	for submission in submissions:
		subList.append(submission["titleSlug"])
	return subList

def getUserSubmissions(user):
	query = {"user": user}
	submissions = submissionCollection.find(query)
	subList = []
	for submission in submissions:
		subList.append(submission["titleSlug"])
	return subList

def addSubmission(user, titleSlug):
	row = {"user": user, "titleSlug": titleSlug}
	submissionCollection.insert_one(row)
