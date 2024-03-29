import discord

from resources.shared import intents


class activities():
	halloween = discord.Activity(name = "Halloween", 
		state = "HAPPY SPOOKY DAY", 
		type=discord.ActivityType.competing, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	christmas = discord.Activity(name = "Yiffmas", 
		state = "Merry Yiffmas!", 
		type=discord.ActivityType.competing, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	frc = discord.Activity(name = "FRC", 
		state = "GOOD LUCK <3", 
		type=discord.ActivityType.watching, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	standard = discord.Activity(name = "the world burn", 
		state = "The flames bring me joy...", 
		type=discord.ActivityType.watching, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	screamingChildren = discord.Activity(
		name = "screaming children", 
		state = "Their screams make me happy...", 
		type=discord.ActivityType.listening, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)

	generic = discord.Activity(
		name = " ", 
		state = "", 
		type=discord.ActivityType.listening, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)


class Holiday:
	halloween = [
		discord.Client(activity=activities.halloween, intents=intents, log_level=None, log_handler=None), 
		"SPOOKY SEASON"
	]


	christmas = [
		discord.Client(activity=activities.christmas, intents=intents, log_level=None, log_handler=None), 
		"Christmas"
	]

class Events:
	frc = [
		discord.Client(activity=activities.frc, intents=intents, log_level=None, log_handler=None), 
		"FRC Motivation"
	]


class Default:
	none = [
		discord.Client(activity=activities.generic, intents=intents, log_level=None, log_handler=None), 
		"none"
	]

	standard = [
		discord.Client(activity=activities.standard, intents=intents, log_level=None, log_handler=None), 
		"Default"
	]

	screamingChildren = [
		discord.Client(activity=activities.screamingChildren, intents=intents, log_level=None, log_handler=None), 
		"Screaming Children"
	]