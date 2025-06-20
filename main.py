"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import scripts.hooks.firstRun
import scripts.hooks.createConfigs # NOQA

import asyncio
import nest_asyncio
import discord

from resources.shared import CONTEXTS, CONTEXTS_SERVER_ONLY, INTEGRATION_TYPES, INTEGRATION_TYPES_SERVER_ONLY
from resources.shared import BLACKLISTED_USERS, DISALLOW_SYSINF_LEAKS, DISALLOW_PLATFORM_LEAKS, GIT_URL, IS_ANDROID
from resources.shared import IS_DEBUGGING, version, TOKEN, REGISTERED_DEVELOPERS, INVITE_URL
from resources.responses import help_messages

from resources.colour import RED, DRIVES, YELLOW, SPECIALDRIVE, BLUE, RESET, MAGENTA, SEAFOAM

import scripts.api.ptk_reactions      as ptk_reactions
import scripts.api.qrTools            as qrTools
import scripts.api.fun                as oneOff
import scripts.api.animal_images      as animals
import scripts.api.discord            as discord_fancy
import scripts.api.lumos_status       as lumos_status
import scripts.api.starboard          as starboard
import scripts.errors.commandCheck    as commandCheck

import scripts.tools.journal          as journal

from scripts.tools.utility import isDeveloper, bannedUser, loadString

bot = discord.Bot()
loop = asyncio.get_event_loop()

# Some minor fixes for asyncio
nest_asyncio.apply(loop)

### COMMAND GROUPS ###
fritz = bot.create_group("f",          "Fritz's generic commands",           contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)
inDev = bot.create_group("f_unstable", "Unstable and under development",     contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)
qr    = bot.create_group("qr",         "Tools relating to QR codes",         contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)
zdev  = bot.create_group("f_dev",      "Developer-only utilities",           contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)

### SERVER-ONLY COMMANDS ###
sonly = bot.create_group("fs",         "Fritz's server-only commands",   contexts=CONTEXTS_SERVER_ONLY, integration_types=INTEGRATION_TYPES_SERVER_ONLY)

### GLOBAL CHECKS ###
@bot.check
async def global_isbanned_check(ctx):
	if ctx.author.id in BLACKLISTED_USERS:
		raise bannedUser("You are banned from using Fritz")

	return True

### ===================================== ###
### EVENTS ###
# Listen for reactions. Used for starboard features
@bot.event
async def on_raw_reaction_add(reactionContext:discord.RawReactionActionEvent): await starboard.reactionAdded(reactionContext, bot)

# Listen for "All stay strong"
@bot.event
async def on_message(message):
	if str(message.content).lower() == "all stay strong":
		await message.channel.send("We live eternally")

#  Listen for command errors
@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException): await commandCheck.on_command_error(ctx, error)

# Wait for the bot to be ready
@bot.event
async def on_ready():
	print(MAGENTA + "Connected to Discord!" + RESET)
	journal.log("Fritz is connected to Discord")

	if len(BLACKLISTED_USERS) != 0:
		print(YELLOW + f"{len(BLACKLISTED_USERS)} users in blacklist" + RESET)

### ===================================== ###
### RIGHT-CLICK COMMANDS ###
@bot.message_command(name="Quotebook", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
async def quotebookContext(ctx:discord.ApplicationCommand, message:discord.Message):
	authorName = message.author.display_name
	author     = message.author.id
	text       = message.content
	avat       = message.author.display_avatar.url

	await oneOff.quotebookMessage(ctx, text, author, authorName, avat)

# Theoretically, I don't need this anymore?
# @bot.message_command(name="Quotebook (Mutts)", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
# async def quotebookContextMutts(ctx, message:discord.Message):
# 	authorName = message.author.display_name
# 	author     = message.author.id
# 	text       = message.content
# 	avat       = message.author.display_avatar.url

# 	await oneOff.quotebookMessage(ctx, text, author, authorName, avat, True)

@bot.message_command(name="Quotebook (via Forward)", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
async def forwardToQuotebook(ctx, message:discord.Message):
	await oneOff.forwardToQuotebook(ctx, message, bot)

@bot.message_command(name="Snepify", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
async def snepify(ctx, message:discord.Message):
	await animals.add_file_to_snep_folder(ctx, message)

### ===================================== ###
### API COMMANDS ###

# CHECK IF THE CONFIGURED MINECRAFT SERVER IS ONLINE #
@fritz.command(name="mcstatus", description="Check if the Minecraft server is online")
async def mcstatus(ctx, sendplayerlist:bool=False): await lumos_status.getServerStatus(ctx, sendplayerlist)

### ===================================== ###
### QR CODES ###

# SCAN A QR CODE #
@qr.command(name="scan", description="Scan a QR code", pass_context=True)
async def scanQR(ctx, qr_code_image: discord.Attachment):
	await qrTools.read_cv(ctx, qr_code_image.url)

# CREATE A QR CODE #
@qr.command(name="create", description="Make a QR code", pass_context=True)
async def makeQR(ctx, qr_data, style_mode:discord.Option(str, choices=qrTools.designTypes, description='QR style')="stylized (default)"): #type:ignore
	await qrTools.createQR(ctx, qr_data, style_mode)

### ===================================== ###
### BECOME FURRIFIED (yeah i'm a furry if you didn't realize that) ###
@fritz.command(name="artemis_reaction", description="The funny bird man")
async def artemisReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.ARTEMIS)): #type:ignore
	await ptk_reactions.reaction_image(ctx, "artemis", sprite)

@fritz.command(name="rofi_reaction", description="The depressed dog")
async def rofiReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.ROFI)): #type:ignore
	await ptk_reactions.reaction_image(ctx, "rofi", sprite)

@fritz.command(name="theo_reaction", description="Father figure we all need")
async def theoReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.THEO)): #type:ignore
	await ptk_reactions.reaction_image(ctx, "theo", sprite)

@fritz.command(name="hunter_reaction", description="Daddy? Sorry. Daddy? Sorry. Daddy? Sorry-")
async def hunterReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.HUNTER)): #type:ignore
	await ptk_reactions.reaction_image(ctx, "hunter", sprite)

@fritz.command(name="friend_reaction", description="Why so angy tho")
async def friendReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.FRIEND)): #type:ignore
	await ptk_reactions.reaction_image(ctx, "friend", sprite)

@fritz.command(name="ollie_reaction", description="AUTISTIC")
async def ollieReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.OLLIE)): #type:ignore
	await ptk_reactions.reaction_image(ctx, "ollie", sprite)

### ===================================== ###
### ANIMAL CONTENT ###

# PICTURES #
# CAT PICTURE #
@fritz.command(name="givecat", description="Get a random cat photo")
async def givecat(ctx): await animals.giveCat(ctx)

# LYNX PICTURE #
@fritz.command(name="givelynx", description="Get a random lynx photo")
async def givelynx(ctx): await animals.giveLynx(ctx)

# FOX PICTURE #
@fritz.command(name="givefox", description="Get a random fox photo")
async def givefox(ctx): await animals.giveFox(ctx)

# RACOON PICTURE #
@fritz.command(name="giveracc", description="Get a random raccoon photo (or video)")
async def trashpanda(ctx, video:bool=False): await animals.giveTrashPanda(ctx, video)

# WAH IMAGE #
@fritz.command(name="givewah", description="Get a random red panda photo")
async def wahimage(ctx): await animals.giveWah(ctx)

# SNEP IMAGE #
@fritz.command(name="givesnep", description="Get a random snep photo")
async def snepimage(ctx): await animals.giveSnep(ctx)

# FACTS #
# RACOON FACTS #
@fritz.command(name="raccfacc", description="Get a random raccoon fact")
async def raccfacc(ctx): await animals.giveRaccFacc(ctx)

# WAH FACT #
@fritz.command(name="wahfact", description="Get a random red panda fact")
async def wahfact(ctx): await animals.giveWahFact(ctx)

### ===================================== ###
### SERVER-ONLY COMMANDS ###

### ===================================== ###
### USER MANAGEMENT ###

### ===================================== ###
### BOT UTILITIES ###
@fritz.command(name='bug', description='Report a bug')
async def bugreport(ctx):
	await ctx.respond(loadString("/bug_report").format(GITHUB_BASE=GIT_URL), ephemeral=True)

@fritz.command(name='ping', description='Get Fritz\'s current ping')
async def ping(ctx):
	latency = round(bot.latency * 1000); await ctx.respond('Current latency: ' + str(latency) + "ms")

### ===================================== ###
### INFORMATION COMMANDS ###
@fritz.command(name="help", description="Stop and RTFM", pass_context=True)
async def help(ctx):
	await ctx.respond(loadString("/commands"), ephemeral=True)

@fritz.command(name="changelog", description="See past changes to Fritz", pass_context=True)
async def changelog(ctx): await ctx.respond(file=help_messages.changelog, ephemeral=True)

## Get info about Fritz ##
@fritz.command(name="system", description="Advanced system info", pass_context=True)
async def help(ctx):
	if DISALLOW_SYSINF_LEAKS and not (str(ctx.author.id) in REGISTERED_DEVELOPERS): await ctx.respond("You are not allowed to run this command"); return

	response = help_messages.about_system # Base text

	if not DISALLOW_PLATFORM_LEAKS:
		if IS_ANDROID  : response = response + "\n" + loadString("/android/command_flare")
		if IS_DEBUGGING: response = response + "\n" + loadString("/debug/command_flare")

	await ctx.respond(response, ephemeral=True)

@fritz.command(name="about", description="Learn more about Fritz")
async def help(ctx):
	await ctx.respond(help_messages.about_fritz)

@fritz.command(name='invite', description='Get Fritz\'s invite URL', pass_context=True)
async def getInvite(ctx):
	await ctx.respond("NOTE: This link is to add Fritz to a SERVER. To add it to an account, you need to click \"Add App\" in Fritz's profile\n" + INVITE_URL, ephemeral=True)

@fritz.command(name='git_url', description='Get Fritz\'s Git URL')
async def getGit(ctx): await ctx.respond(GIT_URL)

### ===================================== ###
### DEVELOPER ONLY ###
@zdev.command(name='shutdown', description='DEV: Shuts down Fritz, if possible. Does not work on Android', pass_context=True)
@isDeveloper()
async def initiateShutdown(ctx):
	await ctx.respond(":saluting_face:")

	os.system("sudo systemctl stop fritz")

@zdev.command(name='download_messages', description='Prints the last 50 messages in a channel. Use `id` to set the channel')
@isDeveloper()
async def downloadMessages(ctx, id):
	await ctx.defer(ephemeral="True")

	messageList = await discord_fancy.query_messages(id)

	authorList  = await discord_fancy.parse_tools.messages.authors(messageList)
	contentList = await discord_fancy.parse_tools.messages.content(messageList)

	index = 0

	for author in authorList:
		print(f"{RED}CACHED: {str(id)}{YELLOW} {str(author)}: {DRIVES}{str(contentList[index])}{RESET}")
		index += 1

	await ctx.respond("Dumped to console")

### ===================================== ###

try:
	match [IS_DEBUGGING, IS_ANDROID]:
		case [False, False]: print(MAGENTA + f"Fritz {version}" + RESET)
		case [True, False] : print(MAGENTA + f"Fritz {version}" + RED + " (debug mode)" + RESET)
		case [False, True] : print(MAGENTA + f"Fritz {version}" + RED + " (experimental)" + RESET)
		case [True, True]  : print(MAGENTA + f"Fritz {version}" + RED + " (debug, experimental)" + RESET)

	print("")

	bot.run(TOKEN)

except Exception as err:
	print(MAGENTA + "FATAL: " + RED + "Failed to start Fritz")
	print("   -> " + str(err) + RESET)

	journal.log_fatal("Failed to start: " + str(err))
