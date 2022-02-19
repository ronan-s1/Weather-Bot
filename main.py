import discord
import requests
import os
import asyncio
from bs4 import BeautifulSoup
import datetime
import random
from keep_alive import keep_alive


#reads facts.txt and returns a list
def facts_and_gif(f):
	my_file = open(f, "r")
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


# gets tomorrow's weather
def tomorrow():
	page = requests.get("https://www.met.ie/forecasts/dublin")
	soup = BeautifulSoup(page.content, "html.parser")

	for count, i in enumerate(soup.select("h2")):
		if "TOMORROW" in i.text:
			title = i.text
			break

	description = soup.select("p")[3 + count].text

	return f"**{title}**\n{description}"


# links to articles
def news():
	# news_string = "**Weather Related News:**\n"
	news_list = []
	page = requests.get("https://www.google.com/search?q=weather+ireland&rlz=1C1ONGR_en-GBIE979IE979&biw=1536&bih=842&tbm=nws&sxsrf=APq-WBsl_-eeWzTn7FGhUDdCzlFHF_pROg%3A1645226936889&ei=uCsQYubSNePA8gLQq7TABg&ved=0ahUKEwjmjpf5s4r2AhVjoFwKHdAVDWgQ4dUDCA0&uact=5&oq=weather+ireland&gs_lcp=Cgxnd3Mtd2l6LW5ld3MQAzIKCAAQsQMQgwEQQzILCAAQsQMQgwEQkQIyCwgAELEDEIMBEJECMgsIABCxAxCDARCRAjILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATIICAAQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDAVAAWMwRYJwTaABwAHgAgAHSAYgBxQiSAQYxNC4wLjGYAQCgAQHAAQE&sclient=gws-wiz-news")

	soup = BeautifulSoup(page.content, "html.parser")

	# finds all classes with kCrYT
	for item in soup.find_all("div", attrs={"class" : "kCrYT"}):
		# gets the links only
		raw_link = (item.find("a", href=True)["href"])

		# removes evrything after &sa=U&, making the link useable
		link = "<" + (raw_link.split("/url?q=")[1]).split("&sa=U&")[0] + ">"

		news_list.append(link)
	
	return news_list


# shows list of commands
def commands():
	commands = ["**!commands** - shows list of commands (this)", "**!weather** - shows the current weather of Dublin", "**!tmr** - shows the weather for tomorrow in Dublin","**!news** - shows weather related articles in Ireland","**!fact** - shows a fun weather fact", "**!gif** - shows a weather gif"]
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
			channel = client.get_channel(893033706107858945)
			daily_message = "**DAILY UPDATE:**\n" + getting_weather()
			await channel.send(daily_message)
			wait_time = 1


#when bot starts
@client.event
async def on_ready():
	print(f"Logged in as: {client.user}")
	await daily_weather()


#if user does a command
@client.event
async def on_message(message):
	msg = message.content.lower()
	if message.author == client.user:
		return

	#send weather
	elif msg.startswith("!weather"):
		await message.channel.send(getting_weather())
	
	#shows list of commands
	elif msg.startswith("!commands"):
		await message.channel.send(commands())

	#shows fact
	elif msg.startswith("!fact"):
		await message.channel.send(facts_and_gif("facts.txt"))
	
	#shows gif
	elif msg.startswith("!gif"):
		await message.channel.send(facts_and_gif("gifs.txt"))
	
	#send tomorrow's weather
	elif msg.startswith("!tmr"):
		await message.channel.send(tomorrow())
	
	#send tomorrow's weather
	elif msg.startswith("!news"):
		#calling news function to get articles
		articles = news()
		articles = [link for i, link in enumerate(articles) if i % 2 == 1]
		count = 0
		await message.channel.send("**Weather Related News Articles: (be patient)**\n")

		#sending links
		for link in articles:
			await message.channel.send(link)

			count += 1

			#sending 2 links per time so channel doesn't get spammed
			if count == 2:
				count = 0
				await message.channel.send("**Enter 'y' for more articles, else enter 'n'**\n")

				#input validation
				def check(msg):
					return msg.author == message.author and msg.channel == message.channel and \
					msg.content.lower() in ["y", "n", "no", "yes"]

				#user input
				try:
					user_msg = await client.wait_for("message", check=check, timeout = 15.0)

				#if user doesnt have any valid reply
				except asyncio.TimeoutError: 
					await message.channel.send(f"**Error: {message.author}, you didn't send a valid reply in 15 seconds!**")
					return

				#send more articles if user wants more else leave then loop
				if user_msg.content.lower() in ["y", "yes"]:
					await message.channel.send("**More Articles:**\n")

				else:
					break

		#when all articles are sent
		await message.channel.send("**No More Articles**\n")


#starting the bot
bot_token = os.environ["TOKEN"]
keep_alive()
client.run(bot_token)
