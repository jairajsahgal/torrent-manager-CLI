from tabulate import tabulate
import requests
import subprocess
import sys


def main():
	results=user_input() #takes user input and returns list of dictioary of every magnet link with details
	results=sfw(results) #clears up nsfw tags
	display(results)
	var=choose(results)
	temp=movie_or_not(var[0],results)
	if temp==True:
		t=input("It's a movie. Do you want to stream it? Y or N ->")
		if t=="Y":
			stream(var[1])
		elif t=="N":
			download(var[1])
	else:
		download(var[1])




def sfw(results):
	safe_results=[]
	for result in results:
		if result["nsfw"]==True:
			continue
		if result["nsfw"]==False:
			safe_results.append(result)
	return safe_results

def display(results):
	data=[]
	index=[i+1 for i in range(len(results))]
	for result in range(len(results)):
		data.append([index[result],results[result]["name"],results[result]["size"],results[result]["seeder"],results[result]["leecher"],results[result]["site"]])
	print(tabulate(data, headers=["Name", "Size", "Seeder", "Leecher","Site"]))
	

def user_input():
	name=input("Enter the search term\t")
	url="https://api.sumanjay.cf/torrent/?query={name}".format(name=name)
	results=requests.get(url).json()
	return results

def choose(results):
	index=int(input("Enter index to choose torrent  -> "))
	
	magnet_link=[]
	for i in results:
		magnet_link.append(i["magnet"])
	return [index-1,magnet_link[index-1]]

def movie_or_not(index,results):
	if "movie" in results[index]["type"].lower():
		return True
	else:
		return False


def stream(magnet_link):
	cmd=[]
	cmd.append("webtorrent")
	cmd.append(magnet_link)
	cmd.append("--vlc")
	subprocess.call(cmd)


def download(magnet_link):
	cmd=[]
	cmd.append("webtorrent")
	cmd.append(magnet_link)
	subprocess.call(cmd)


main()