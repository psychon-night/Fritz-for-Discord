"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

from characterai import aiocai

from resources.shared import CAI_TOKEN, AI_BLACKLIST, NoneType, SIXUSERS, GIT_URL

from scripts.tools.advanced_logging import log2f

CHARACTERS = {
	"assistant":"YntB_ZeqRq2l_aVf2gWDCZl4oBttQzDvhj9cXafWcF8",
	"bryce the bear":"GXGDvaTDHSF77mgVh2e8HOz4b_LC76bp9qYAePOLquo",
	"caine": "99iPJ7tzD_HoaJyNi3lRDq3diOJZ7EI90vtUu-XkjW4",
	"childe":"qUyZhAJhbQ9UQWLv-zwrUibvhAT3uV6iJPWRPmPao-Y",
	"connor": "32s_oiKKRLR2D-7a4otjvRa0UEpIFUUVtIVssD2ez64",
	"cyno":"DCKUsZ-oNCKOe2nUcDIpk3hBcCNjhR1UsnoIHF-G4Nk",
	"daddy": "75TOU_oL1QLib1XP8MpdGHRiu78DmjpBCHDcGRW0KIg",
	"goose":"Nvt8JStFgrJJ0ssEhk2bato1tjiTm8MFw0z5SNjhPIU",
	"ii dottore":"qUyZhAJhbQ9UQWLv-zwrUibvhAT3uV6iJPWRPmPao-Y", 
	"kaeya":"1-hkfvky9mPLhz2SN5rReTe3VJOblHId2Wfw8UgjfH8",
	"lyney":"_52oONdEiPJyVxNRBoTTrAVL3mlaXTZhsPNBQiQdot0",
	"markiplier":"4CvFRPck3FDXNv2Aa23gJ17BHMmiRCQugbR_gI5AyRk",
	"neuvillette":"WhXlEtl2VOaT5wRyqEdtkXGXit42moQIy6KuR-KM-hA",
	"neuvillette_punisher":"g7STZs-qe82O665S7FpZzBZ_q_j2vvw4FcWFXebMKhY",
	"proto": "Vohv3F4oEjVKaDmD5quQYYQtcST0VqKGIfXAcewuZ-o",
	"ralsei": "YLualttErjbl_BgjnlG1gntDXTJWY-EFtkuOJGEnG5s",
	"scaramouche":"ZciLSmnkMriz3RtRcvKgafqiWqRlgRULdwzykCyH_pM",
	"scaramouche_dommy":"NaG9__a7jQ89cgJcgH2ueTyaBlskQ_zgbQRwAZui-4w",
	"taylor": "faymYHmsei0EsPH0cDlhrnMXg2cQz8pqLC83eQSvtzo",
	"tighnari":"29YAp_A1WIskNgycOorSd6erabVcUnGqsX23Rxr-E1I",
	"vsauce/michael":"nCFbTLQNVZssDULCaIyYG85kPDtERk7ke17zap6KABo",
	"wanderer":"qUyZhAJhbQ9UQWLv-zwrUibvhAT3uV6iJPWRPmPao-Y",
	"xiao":"PsEGZOFC_kWx8rOqayWx1xWBI7RfRYJ3rqZKlk2NHJk",
	"zhongli":"yXx1xCuVxFPb8zLdTGRQmwL4zezxgGILs2yfu8YN5sQ",
}

async def characterPrompt(ctx, prompt, character, reset):
	if not isinstance(ctx.guild, NoneType):
		if ctx.guild.id in AI_BLACKLIST: await ctx.respond("That command is disabled on this server"); return -1

	await ctx.defer()

	try:
		client = aiocai.Client(CAI_TOKEN)
		user = await client.get_me()

		bot = CHARACTERS[character] if character in str(CHARACTERS.keys()) else CHARACTERS["assistant"]

		async with await client.connect() as chat:
			match reset:
				case True:
					log2f("cai", f"Requesting new chat for {bot}")

					chatID, null = await chat.new_chat(char=bot, creator_id=user.id)
					response = await chat.send_message(bot, chatID.chat_id, prompt)

					await ctx.respond(f"*{response.name}*: " + response.text)

				case False: 
					log2f("cai", f"Connecting to most recent chat for {bot}")

					chatID = await client.get_chat(char=bot)
					response = await chat.send_message(char=bot, chat_id=chatID.chat_id, text=prompt)

					await ctx.respond(f"*{response.name}*: " + response.text)

	except Exception as err: await crashHandler(ctx, err, character)

async def sixPrompt(ctx, prompt, reset):
	if not isinstance(ctx.guild, NoneType):
		if ctx.guild.id in AI_BLACKLIST: await ctx.respond("That command is disabled on this server"); return -1

	if not ctx.author.id in SIXUSERS:
		await ctx.respond("err/403: You are not allowed to use Six")

		log2f("caiSix", f"Access violation! {ctx.author} is not allowed to use Six")

		return 403

	await ctx.defer()

	try:
		client = aiocai.Client(CAI_TOKEN)
		user = await client.get_me()

		bot = "Vohv3F4oEjVKaDmD5quQYYQtcST0VqKGIfXAcewuZ-o"

		async with await client.connect() as chat:
			match reset:
				case True:
					log2f("caiSix", f"Requesting new chat for {bot}")

					chatID, null = await chat.new_chat(char=bot, creator_id=user.id)
					response = await chat.send_message(bot, chatID.chat_id, prompt)

					await ctx.respond(f"*{response.name}*: " + response.text)

				case False: 
					log2f("caiSix", f"Connecting to most recent chat for {bot}")

					chatID = await client.get_chat(char=bot)
					response = await chat.send_message(char=bot, chat_id=chatID.chat_id, text=prompt)

					await ctx.respond(f"*{response.name}*: " + response.text)

	except Exception as err: await crashHandler(ctx, err, "Vohv3F4oEjVKaDmD5quQYYQtcST0VqKGIfXAcewuZ-o")

async def crashHandler(ctx, err, character):
	log2f("cai", "ERROR: " + str(err))

	if "validation error for BotAnswer" in str(err):
		await ctx.respond("Character AI returned a malformed response. Cannot proceed")

		return -1

	elif "'chats'" in str(err):
			try: bot = CHARACTERS[character] if character in str(CHARACTERS.keys()) else CHARACTERS["assistant"]
			except: bot = character

			await ctx.respond(f"Missing Character! \nCouldn't find the character. Please report this on [the bug tracker](<{GIT_URL}/issues/new?assignees=&labels=missing+character&projects=&template=missing-bot.yml&title=Missing+Character>). \n### **CID: {bot}**")

			return 404

	await ctx.respond("Something went wrong while communicating with CharacterAI's servers")