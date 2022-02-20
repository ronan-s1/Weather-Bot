import requests
from bs4 import BeautifulSoup
import random


# shows list of commands
def commands():
	commands = ["**!commands** - shows list of commands (this)", "**!weather** - shows the current weather of Dublin", "**!tmr** - shows the weather for tomorrow in Dublin","**!news** - shows weather related articles in Ireland","**!fact** - shows a fun weather fact", "**!gif** - shows a weather gif", "**!jacket** - says if you should wear a jacket or not"]
	result = ""
	for count, command in enumerate(commands):
		result += f"**{count + 1})** {command}\n"

	return result


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


def jacket():
	page = requests.get("https://doineedajacket.com/weather/dublin")
	soup = BeautifulSoup(page.content, "html.parser")

	# getting data
	jacket_ans = soup.select("h1")[0].text

	if jacket_ans.lower() == "yes":
		return_string = f"**{jacket_ans}!** You should wear a jacket.\n"
	
	else:
		return_string = f"**{jacket_ans}!** You shouldn't wear a jacket.\n"

	hours_later = soup.select("h4")
	for i in range(1, len(hours_later) - 1):
		return_string += hours_later[i].text + "\n"

	return return_string
	
