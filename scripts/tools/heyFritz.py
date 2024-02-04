import g4f, asyncio, textwrap, threading, sys, os

from concurrent.futures import ThreadPoolExecutor


async def onHeyFritz(ctx, loop):

	sentMessage = await ctx.channel.send("Working....")

	textPrompt = str(ctx.content).split(",", 1)[1]

	try:
		response = await loop.run_in_executor(
			ThreadPoolExecutor(), 
			lambda: g4f.ChatCompletion.create(
			model=g4f.models.gpt_35_long, 
			messages=[{"role": "user", "content": textPrompt }], 
		))
	
	except: response = "My LLM failed to respond correctly"

	await sentMessage.delete()
		
	match [len(str(response)) > 0, len(str(response)) > 2000]:
		case [False, _]: await ctx.channel.send("Sorry, it looks like none of my LLMs are responding. Maybe try using the `chatgpt` with `use_legacy` set?")
		case [True, True]:  
			for message in textwrap.wrap(response, 1900): await ctx.channel.send(message)
		case [True, False]: await ctx.channel.send(str(response))

async def lyricLoader(ctx):
	# print(sys.path[0] + "/resources/docs/lyrics/%s"%str(ctx.content))
	# print(str(ctx.content), ": ", str(ctx.content).lower() in os.listdir(sys.path[0] + "/resources/docs/lyrics/"))

	for line in open(sys.path[0] + "/resources/docs/lyrics/%s"%str(ctx.content).lower(), "r").read().splitlines():
		await ctx.channel.send(line, silent=True)
		await asyncio.sleep(1)