import requests
from bs4 import BeautifulSoup
import random
import os
import urllib.request
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER

#shows list of commands
def commands():
    f = "src/data/commands.txt"
    my_file = open(f, "r")
    commands = my_file.read()
    commands_list = commands.split("\n")
    my_file.close()
    
    result = ""
    for count, command in enumerate(commands_list):
        if command[2] == "!":
            result += f"**{count})** {command}\n"

        else:
            result += f"\n{command}\n"

    return result

#sends advice
def advice():
    response = requests.get("https://api.adviceslip.com/advice").json()
    return response["slip"]["advice"]


def bored():
    response = requests.get("https://www.boredapi.com/api/activity").json()
    return response["activity"]


def covid(country):
    url = "https://covid19.mathdro.id/api/countries/" + country + "/og"
    urllib.request.urlretrieve(url, "src/data/delete/covid.png")


#gets crypto chart
def crypto(coin, compare):
    api = os.environ["API"]
    url = "https://api.chart-img.com/v1/tradingview/advanced-chart?interval=1d&studies=RSI&studies=MACD&symbol=" + coin + compare + "&key=" + api
    urllib.request.urlretrieve(url, "src/data/delete/chart.png")


#finds ip
def ip(ip):
    #gets infor of ip
    response = requests.get("http://ip-api.com/json/" + ip).json()
    info = PrettyTable()
    info.field_names =["FIELDS", "DATA"]


    data_fields = ["country", "country code", "region name", "city", "zip", "latitude", "longitude", "timezone", "ISP", "AS", "IP"]
    data = ["country", "countryCode", "regionName", "city", "zip", "lat", "lon", "timezone", "isp", "as", "query"]

    #put info into a table if the ip is valid else display an error
    if response["status"] == "success":
        for i in range(len(data)):
            info.add_row([data_fields[i], response[data[i]]])

        info.align = "l"
        info.set_style(SINGLE_BORDER)
        return f"```\n{info}```"
    
    return "**invalid IP**"


#wordle answer
def wordle():
    page = requests.get("https://gamerjournalist.com/wordle-answers/")
    soup = BeautifulSoup(page.text, "html.parser")

    #getting correct string
    string  =  soup.find_all("p")[10].text.split(" ")
    wordle = ""
    for i in range(len(string) - 1):
        wordle += string[i] + " "

    #spoiler
    ans =  wordle + "||" + str(string[-1]) + "||"

    return ans


#displays worldle
def worldle():
    page = requests.get("https://www.gfinityesports.com/worldle/country/")
    soup = BeautifulSoup(page.text, "html.parser")
    
    #getting correct string
    string  =  soup.find_all("p")[6].text.split(" ")
    wordle = ""
    after_is = 0
    
    for i in range(len(string) - 1):
        wordle += string[i] + " "
        after_is += 1

        if string[i] == "is":
            break

    #spoiler
    ans =  wordle + "||" + " ".join(map(str, string[after_is:])) + "||"

    return ans

    
#displays hourly weather
def hourly():
    #pretty table to display a pretty table :)
    table = PrettyTable()
    table.field_names = ["TIME", "WEATHER", "WIND km/h", "HUMID", "RAIN CHANCE"]
    page = requests.get("https://www.timeanddate.com/weather/ireland/dublin/hourly")
    soup = BeautifulSoup(page.text, "html.parser")
    table_scrape = soup.find_all("tr")

    #rows of data
    rows = []

    #getting rows into table into lists
    for data in table_scrape:
        row = []
        for items in data:
            row.append(items.text)

        rows.append(row)
    
    #cleaning up rows
    count = 0
    for i in range(2, len(rows) - 1):               
        rows[i].pop(len(rows[i]) -1)
        rows[i].pop(1)
        rows[i].pop(5)
        rows[i].pop(1)
        rows[i].pop(2)

        rows[i][0] = rows[i][0].split("m")[0] + "m"

        #mph to kph
        rows[i][2] = str(round(int(rows[i][2].split(" ")[0]) / 0.6214))

        table.add_row(rows[i])

        count += 1
        if count >= 15:
            break
    
    #return the table
    table.align = "l"
    table.set_style(SINGLE_BORDER)
    return f"```\n{table}\n```"


#reads facts.txt and returns a list
def facts_and_gif(f):
	my_file = open(f, "r")
	content = my_file.read()
	content_list = content.split("\n")
	my_file.close()
	
	return random.choice(content_list)


#scrapes the met.ie webpage for todays weather
def getting_weather():
	page = requests.get("https://www.met.ie/forecasts/dublin")
	soup = BeautifulSoup(page.content, "html.parser")

	title = soup.select("h2")[0].text
	description = soup.select("p")[3].text

	return f"**{title}**\n{description}"


#gets tomorrow's weather
def tomorrow():
	page = requests.get("https://www.met.ie/forecasts/dublin")
	soup = BeautifulSoup(page.content, "html.parser")

	for count, i in enumerate(soup.select("h2")):
		if "TOMORROW" in i.text:
			title = i.text
			break

	description = soup.select("p")[5 + count].text

	return f"**{title}**\n{description}"


#links to articles
def news():
	news_list = []
	page = requests.get("https://www.google.com/search?q=weather+ireland&rlz=1C1ONGR_en-GBIE979IE979&biw=1536&bih=842&tbm=nws&sxsrf=APq-WBsl_-eeWzTn7FGhUDdCzlFHF_pROg%3A1645226936889&ei=uCsQYubSNePA8gLQq7TABg&ved=0ahUKEwjmjpf5s4r2AhVjoFwKHdAVDWgQ4dUDCA0&uact=5&oq=weather+ireland&gs_lcp=Cgxnd3Mtd2l6LW5ld3MQAzIKCAAQsQMQgwEQQzILCAAQsQMQgwEQkQIyCwgAELEDEIMBEJECMgsIABCxAxCDARCRAjILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATIICAAQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDAVAAWMwRYJwTaABwAHgAgAHSAYgBxQiSAQYxNC4wLjGYAQCgAQHAAQE&sclient=gws-wiz-news")

	soup = BeautifulSoup(page.content, "html.parser")

	#finds all classes with kCrYT
	for item in soup.find_all("div", attrs={"class" : "kCrYT"}):
		#gets the links only
		raw_link = (item.find("a", href=True)["href"])

		#removes evrything after &sa=U&, making the link useable
		link = "<" + (raw_link.split("/url?q=")[1]).split("&sa=U&")[0] + ">"

		news_list.append(link)
	
	return news_list


def jacket():
	page = requests.get("https://doineedajacket.com/weather/dublin")
	soup = BeautifulSoup(page.content, "html.parser")

	#getting data
	jacket_ans = soup.select("h1")[0].text

	if jacket_ans.lower() == "yes":
		return_string = f"**{jacket_ans}!** You should wear a jacket.\n"
	
	else:
		return_string = f"**{jacket_ans}!** You shouldn't wear a jacket.\n"

	hours_later = soup.select("h4")
	for i in range(1, len(hours_later) - 1):
		return_string += hours_later[i].text + "\n"

	return return_string


def random_fact():
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    return response["text"]