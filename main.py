import discord
import requests
import os
import asyncio
from bs4 import BeautifulSoup
import datetime
import random
from keep_alive import keep_alive

#reads facts.txt and returns a list
def facts():
	my_file = open("facts.txt", "r")
	content = my_file.read()
	content_list = content.split("\n")
	my_file.close()
	
	return random.choice(content_list)


# scrapes the met.ie webpage for todays weather
def getting_weather():
	page = requests.get("https://www.met.ie/forecasts/dublin")
	soup = BeautifulSoup(page.content, "html.parser")

	title = soup.select("h2")[0].text
	description = soup.select("p")[3].text

	return f"**{title}**\n{description}"


def commands():
	commands = ["!commands - brings this up", "!weather - gets current weather of Dublin","!fact - shows a fun weather fact"]
	result = ""
	for command in commands:
		result += command + "\n"

	return result


# --- discord side ---
client = discord.Client()


#send the weather at 7am
@client.event
async def daily_weather():
	while True:
		now = datetime.datetime.now()
		then = now+datetime.timedelta(days=1)
		then = now.replace(hour=7, minute=0, second=0)
		wait_time = (then-now).total_seconds()

		await asyncio.sleep(wait_time)

		if wait_time == 0:
			channel = client.get_channel(944207098043039784)
			await channel.send(getting_weather())
			wait_time = 1


#when bot starts
@client.event
async def on_ready():
	print(f"Logged in as: {client.user}")
	await daily_weather()


#if user does a command
@client.event
async def on_message(message):
	msg = message.content
	if message.author == client.user:
		return

	#send weather
	if msg.startswith("!weather"):
		await message.channel.send(getting_weather())
	
	if msg.startswith("!commands"):
		await message.channel.send(commands())

	if msg.startswith("!fact"):
		await message.channel.send(facts())


bot_token = os.environ["TOKEN"]
keep_alive()
client.run(bot_token)