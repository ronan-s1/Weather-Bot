import discord
import os
import asyncio
import datetime
import commands
from keep_alive import keep_alive

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
			daily_message = "**DAILY UPDATE:**\n" + commands.getting_weather()
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
	facts_file = "other/facts.txt"
	gifs_file = "other/gifs.txt"
	msg = message.content.lower()
	if message.author == client.user:
		return

	#send weather
	elif msg.startswith("!weather"):
		await message.channel.send(commands.getting_weather())
	
	#shows list of commands
	elif msg.startswith("!commands"):
		await message.channel.send(commands.commands())

	#shows fact
	elif msg.startswith("!fact"):
		await message.channel.send(commands.facts_and_gif(facts_file))
	
	#shows gif
	elif msg.startswith("!gif"):
		await message.channel.send(commands.facts_and_gif(gifs_file))
	
	#send tomorrow's weather
	elif msg.startswith("!tmr"):
		await message.channel.send(commands.tomorrow())
	
	#send tomorrow's weather
	elif msg.startswith("!jacket"):
		await message.channel.send(commands.jacket())
	
	#send tomorrow's weather
	elif msg.startswith("!news"):
		#calling news function to get articles
		articles = commands.news()
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
