import discord
import json
import requests
import colorama
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
from colorama import init, Fore, Style
colorama.init()

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
client.remove_command("help")

class console():
    def success(text):
        print(f'[{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Fore.RESET}] {Fore.LIGHTWHITE_EX}[{Fore.RESET} {Fore.MAGENTA}SUCCESS{Fore.RESET} {Fore.LIGHTWHITE_EX}]{Fore.RESET} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{text}{Fore.RESET}')
    def error(text):
        print(f'[{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Fore.RESET}] {Fore.LIGHTWHITE_EX}[{Fore.RESET} {Fore.MAGENTA}ERROR{Fore.RESET} {Fore.LIGHTWHITE_EX}]{Fore.RESET} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{text}{Fore.RESET}')
    def info(text):
        print(f'[{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Fore.RESET}] {Fore.LIGHTWHITE_EX}[{Fore.RESET} {Fore.MAGENTA}INFO{Fore.RESET} {Fore.LIGHTWHITE_EX}]{Fore.RESET} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{text}{Fore.RESET}')

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

botToken = config_data["botConfig"]["botToken"]
botStatus = config_data["botConfig"]["botStatus"]
botAccess = config_data["botConfig"]["botAccess"]

embedEnabled = config_data["dmallConfig"]["embed"]
embedTitle = config_data["dmallConfig"]["embedConfig"]["emdedTitle"]
embedDescription = config_data["dmallConfig"]["embedConfig"]["embedDescription"]
embedFooter_text = config_data["dmallConfig"]["embedConfig"]["embedFooterText"]
embedFooter_icon_url = config_data["dmallConfig"]["embedConfig"]["embedFooterIconURL"]
embedImage_url = config_data["dmallConfig"]["embedConfig"]["embedImageURL"]
embedThumbnail_url = config_data["dmallConfig"]["embedConfig"]["embedThumbnailURL"]

contentEnabled = config_data["dmallConfig"]["content"]
contentText = config_data["dmallConfig"]["contentConfig"]["contentText"]

buttonEnabled = config_data["dmallConfig"]["button"]
buttonLabel = config_data["dmallConfig"]["buttonConfig"]["buttonLabel"]
buttonEmoji = config_data["dmallConfig"]["buttonConfig"]["buttonEmoji"]
buttonURL = config_data["dmallConfig"]["buttonConfig"]["buttonURL"]

onMemberJoin = config_data["dmallConfig"]["onMemberJoin"]
onGuildJoin = config_data["dmallConfig"]["onGuildJoin"]
onReady = config_data["dmallConfig"]["onReady"]
onlineOnly = config_data["dmallConfig"]["onlineOnly"]

def configureBot(botToken):
    headers = {
        "Authorization": f"Bot {botToken}",
        "Content-Type": "application/json"
    }

    payload = {
        "description": "*Dmall by https://github.com/notxVirus/advanced-discord-dmall*",
        "flags": 565248
    }

    bot = requests.get("https://discord.com/api/v9/users/@me", headers = headers)
    if bot.status_code == 200:
        bot = bot.json()

        old_intents = requests.get("https://discord.com/api/v9/oauth2/applications/@me", headers = headers)
        intents = old_intents.json()

        response = requests.patch(f"https://discord.com/api/v9/applications/{bot['id']}", headers = headers, json = payload)
        app = response.json()
    else:
        return console.error("Invalid token provided.")

    config = requests.get(f"https://discord.com/api/v9/applications/{bot['id']}", headers = headers)
    if config.status_code == 200:
        config = config.json()
        if intents['flags'] != config['flags']:
            console.info(f"{Fore.LIGHTBLACK_EX}Turned on Bot Intents: {intents['flags']} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{config['flags']}{Fore.RESET}")
            return console.info(f"Please, run script again.")
    else:
        console.error("Invalid token provided.")

def checkToken(botToken):
    headers = {
        "Authorization": f"Bot {botToken}",
        "Content-Type": "application/json"
    }

    bot = requests.get("https://discord.com/api/v9/users/@me", headers = headers)
    if bot.status_code == 200:
        configureBot(botToken)
        pass
    else:        
        console.error(f"It seems that the botToken in the {Fore.MAGENTA}config.json{Fore.RESET} {Fore.LIGHTBLACK_EX}file is invalid.")
        newBotToken = input("Please provide a valid Discord Bot token: ")

        config_data["botConfig"]["botToken"] = newBotToken
        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent = 4)
        console.success(f"Updated bot token in config.json with: {Fore.MAGENTA}{newBotToken}{Fore.RESET}")
        configureBot(newBotToken)

@client.event
async def on_ready():
    try:
        await client.change_presence(status = discord.Status.online, activity = discord.Game(botStatus))
    except Exception as e:
        pass
    console.success(f"Logged in as {Fore.MAGENTA}{client.user}{Fore.LIGHTBLACK_EX} | {Fore.MAGENTA}{client.user.id}{Fore.RESET}")
    console.info(f"DISCORD BOT INVITE URL: {Fore.MAGENTA}https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=0&scope=bot%20applications.commands")
    console.info(f"The Discord Bot {Fore.MAGENTA}{client.user}{Fore.LIGHTBLACK_EX} is in {Fore.MAGENTA}{len(client.guilds)}{Fore.LIGHTBLACK_EX} server(s) and has {Fore.MAGENTA}{sum([g.member_count for g in client.guilds])}{Fore.LIGHTBLACK_EX} user(s).")
    if onReady is True:
        for guild in client.guilds:
            for member in guild.members:
                if not member.bot:
                    embed = discord.Embed(title = embedTitle.format(member = member, guild = guild), description = embedDescription.format(member = member, guild = guild))
                    if embedFooter_text:
                        embed.set_footer(text = embedFooter_text.format(member = member, guild = guild))
                    if embedFooter_icon_url:
                        embed.set_footer(icon_url = embedFooter_icon_url.format(member = member, guild = guild))
                    if embedFooter_text and embedFooter_icon_url:
                        embed.set_footer(text = embedFooter_text.format(member = member, guild = guild), icon_url = embedFooter_icon_url)
                    if embedImage_url:
                        try:
                            embed.set_image(url = embedImage_url)
                        except Exception as e:
                            console.error(f"Failed to set embed image: {Fore.MAGENTA}{e}{Fore.RESET}")
                    if embedThumbnail_url:
                        try:
                            embed.set_thumbnail(url = embedThumbnail_url)
                        except Exception as e:
                            console.error(f"Failed to set embed thumbnail: {Fore.MAGENTA}{e}{Fore.RESET}")
                    if buttonEnabled is True:
                        if buttonEmoji:
                            button = Button(label = buttonLabel.format(member = member, guild = guild), url = buttonURL, emoji = str(buttonEmoji))
                        else:
                            button = Button(label = buttonLabel.format(member = member, guild = guild), url = buttonURL)
                        view = View()
                        view.add_item(button)

                    if onlineOnly is True:
                        if member.status != discord.Status.offline:
                            if contentEnabled and embedEnabled and buttonEnabled is True:
                                try:
                                    await member.send(content = contentText.format(member = member, guild = guild), embed = embed, view = view)
                                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                                except Exception as e:
                                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                            elif embedEnabled and buttonEnabled is True:
                                try:
                                    await member.send(embed = embed, view = view)
                                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                                except Exception as e:
                                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                            elif contentEnabled and buttonEnabled is True:
                                try:
                                    await member.send(content = contentText.format(member = member, guild = guild), view = view)
                                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                                except Exception as e:
                                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                            elif contentEnabled and embedEnabled is True:
                                try:
                                    await member.send(content = contentText.format(member = member, guild = guild), embed = embed)
                                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                                except Exception as e:
                                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                            elif contentEnabled is True:
                                try:
                                    await member.send(content = contentText.format(member = member, guild = guild))
                                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                                except Exception as e:
                                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                            elif embedEnabled is True:
                                try:
                                    await member.send(embed = embed)
                                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                                except Exception as e:
                                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                    else:
                        if contentEnabled and embedEnabled and buttonEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild), embed = embed, view = view)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif embedEnabled and buttonEnabled is True:
                            try:
                                await member.send(embed = embed, view = view)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif contentEnabled and buttonEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild), view = view)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif contentEnabled and embedEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild), embed = embed)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif contentEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild))
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif embedEnabled is True:
                            try:
                                await member.send(embed = embed)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")


@client.event
async def on_member_join(member):
    if onMemberJoin is True:
        if not member.bot:
            guild = member.guild
            embed = discord.Embed(title = embedTitle.format(member = member, guild = guild), description = embedDescription.format(member = member, guild = guild))
            if embedFooter_text:
                embed.set_footer(text = embedFooter_text.format(member = member, guild = guild))
            if embedFooter_icon_url:
                embed.set_footer(icon_url = embedFooter_icon_url.format(member = member, guild = guild))
            if embedFooter_text and embedFooter_icon_url:
                embed.set_footer(text = embedFooter_text.format(member = member, guild = guild), icon_url = embedFooter_icon_url)
            if embedImage_url:
                try:
                    embed.set_image(url = embedImage_url)
                except Exception as e:
                    console.error(f"Failed to set embed image: {Fore.MAGENTA}{e}{Fore.RESET}")
            if embedThumbnail_url:
                try:
                    embed.set_thumbnail(url = embedThumbnail_url)
                except Exception as e:
                    console.error(f"Failed to set embed thumbnail: {Fore.MAGENTA}{e}{Fore.RESET}")
            if buttonEnabled is True:
                if buttonEmoji:
                    button = Button(label = buttonLabel.format(member = member, guild = guild), url = buttonURL, emoji = str(buttonEmoji))
                else:
                    button = Button(label = buttonLabel.format(member = member, guild = guild), url = buttonURL)
                view = View()
                view.add_item(button)

            if contentEnabled and embedEnabled and buttonEnabled is True:
                try:
                    await member.send(content = contentText.format(member = member, guild = guild), embed = embed, view = view)
                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                except Exception as e:
                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
            elif embedEnabled and buttonEnabled is True:
                try:
                    await member.send(embed = embed, view = view)
                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                except Exception as e:
                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
            elif contentEnabled and buttonEnabled is True:
                try:
                    await member.send(content = contentText.format(member = member, guild = guild), view = view)
                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                except Exception as e:
                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
            elif contentEnabled and embedEnabled is True:
                try:
                    await member.send(content = contentText.format(member = member, guild = guild), embed = embed)
                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                except Exception as e:
                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
            elif contentEnabled is True:
                try:
                    await member.send(content = contentText.format(member = member, guild = guild))
                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                except Exception as e:
                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
            elif embedEnabled is True:
                try:
                    await member.send(embed = embed)
                    console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                except Exception as e:
                    console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")



@client.event
async def on_guild_join(guild):
    if onGuildJoin is True:
        for member in guild.members:
            if not member.bot:
                embed = discord.Embed(title = embedTitle.format(member = member, guild = guild), description = embedDescription.format(member = member, guild = guild))
                if embedFooter_text:
                    embed.set_footer(text = embedFooter_text.format(member = member, guild = guild))
                if embedFooter_icon_url:
                    embed.set_footer(icon_url = embedFooter_icon_url.format(member = member, guild = guild))
                if embedFooter_text and embedFooter_icon_url:
                    embed.set_footer(text = embedFooter_text.format(member = member, guild = guild), icon_url = embedFooter_icon_url)
                if embedImage_url:
                    try:
                        embed.set_image(url = embedImage_url)
                    except Exception as e:
                        console.error(f"Failed to set embed image: {Fore.MAGENTA}{e}{Fore.RESET}")
                if embedThumbnail_url:
                    try:
                        embed.set_thumbnail(url = embedThumbnail_url)
                    except Exception as e:
                        console.error(f"Failed to set embed thumbnail: {Fore.MAGENTA}{e}{Fore.RESET}")
                if buttonEnabled is True:
                    if buttonEmoji:
                        button = Button(label = buttonLabel.format(member = member, guild = guild), url = buttonURL, emoji = str(buttonEmoji))
                    else:
                        button = Button(label = buttonLabel.format(member = member, guild = guild), url = buttonURL)
                    view = View()
                    view.add_item(button)

                if onlineOnly is True:
                    if member.status != discord.Status.offline:
                        if contentEnabled and embedEnabled and buttonEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild), embed = embed, view = view)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif embedEnabled and buttonEnabled is True:
                            try:
                                await member.send(embed = embed, view = view)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif contentEnabled and buttonEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild), view = view)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif contentEnabled and embedEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild), embed = embed)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif contentEnabled is True:
                            try:
                                await member.send(content = contentText.format(member = member, guild = guild))
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                        elif embedEnabled is True:
                            try:
                                await member.send(embed = embed)
                                console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                            except Exception as e:
                                console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                else:
                    if contentEnabled and embedEnabled and buttonEnabled is True:
                        try:
                            await member.send(content = contentText.format(member = member, guild = guild), embed = embed, view = view)
                            console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                        except Exception as e:
                            console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                    elif embedEnabled and buttonEnabled is True:
                        try:
                            await member.send(embed = embed, view = view)
                            console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                        except Exception as e:
                            console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                    elif contentEnabled and buttonEnabled is True:
                        try:
                            await member.send(content = contentText.format(member = member, guild = guild), view = view)
                            console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                        except Exception as e:
                            console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                    elif contentEnabled and embedEnabled is True:
                        try:
                            await member.send(content = contentText.format(member = member, guild = guild), embed = embed)
                            console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                        except Exception as e:
                            console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                    elif contentEnabled is True:
                        try:
                            await member.send(content = contentText.format(member = member, guild = guild))
                            console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                        except Exception as e:
                            console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")
                    elif embedEnabled is True:
                        try:
                            await member.send(embed = embed)
                            console.success(f"Sent message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX})")
                        except Exception as e:
                            console.error(f"Failed to send message to: {Fore.MAGENTA}{member}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{member.id}{Fore.LIGHTBLACK_EX}) {e}")

@client.command()
async def message(ctx):
    if ctx.author.id in botAccess:
        embed = discord.Embed(title = embedTitle.format(member = ctx.author, guild = ctx.guild), description = embedDescription.format(member = ctx.author, guild = ctx.guild))
        if embedFooter_text:
            embed.set_footer(text = embedFooter_text.format(member = ctx.author, guild = ctx.guild))
        if embedFooter_icon_url:
            embed.set_footer(icon_url = embedFooter_icon_url.format(member = ctx.author, guild = ctx.guild))
        if embedFooter_text and embedFooter_icon_url:
            embed.set_footer(text = embedFooter_text.format(member = ctx.author, guild = ctx.guild), icon_url = embedFooter_icon_url)
        if embedImage_url:
            try:
                embed.set_image(url = embedImage_url)
            except Exception as e:
                console.error(f"Failed to set embed image: {Fore.MAGENTA}{e}{Fore.RESET}")
        if embedThumbnail_url:
            try:
                embed.set_thumbnail(url = embedThumbnail_url)
            except Exception as e:
                console.error(f"Failed to set embed thumbnail: {Fore.MAGENTA}{e}{Fore.RESET}")
        if buttonEnabled is True:
            if buttonEmoji:
                button = Button(label = buttonLabel.format(member = ctx.author, guild = ctx.guild), url = buttonURL, emoji = str(buttonEmoji))
            else:
                button = Button(label = buttonLabel.format(member = ctx.author, guild = ctx.guild), url = buttonURL)
            view = View()
            view.add_item(button)

        if contentEnabled and embedEnabled and buttonEnabled is True:
            try:
                await ctx.author.send(content = contentText.format(member = ctx.author, guild = ctx.guild), embed = embed, view = view)
                console.success(f"Sent message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX})")
                await ctx.send(f"Sent dmall message in {ctx.author.mention}'s DMs", delete_after = 5)
            except Exception as e:
                console.error(f"Failed to send message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX}) {e}")
        elif embedEnabled and buttonEnabled is True:
            try:
                await ctx.author.send(embed = embed, view = view)
                console.success(f"Sent message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX})")
                await ctx.send(f"Sent dmall message in {ctx.author.mention}'s DMs", delete_after = 5)
            except Exception as e:
                console.error(f"Failed to send message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX}) {e}")
        elif contentEnabled and buttonEnabled is True:
            try:
                await ctx.author.send(content = contentText.format(member = ctx.author, guild = ctx.guild), view = view)
                console.success(f"Sent message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX})")
                await ctx.send(f"Sent dmall message in {ctx.author.mention}'s DMs", delete_after = 5)
            except Exception as e:
                console.error(f"Failed to send message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX}) {e}")
        elif contentEnabled and embedEnabled is True:
            try:
                await ctx.author.send(content = contentText.format(member = ctx.author, guild = ctx.guild), embed = embed)
                console.success(f"Sent message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX})")
                await ctx.send(f"Sent dmall message in {ctx.author.mention}'s DMs", delete_after = 5)
            except Exception as e:
                console.error(f"Failed to send message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX}) {e}")
        elif contentEnabled is True:
            try:
                await ctx.author.send(content = contentText.format(member = ctx.author, guild = ctx.guild))
                console.success(f"Sent message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX})")
                await ctx.send(f"Sent dmall message in {ctx.author.mention}'s DMs", delete_after = 5)
            except Exception as e:
                console.error(f"Failed to send message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX}) {e}")
        elif embedEnabled is True:
            try:
                await ctx.author.send(embed = embed)
                console.success(f"Sent message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX})")
                await ctx.send(f"Sent dmall message in {ctx.author.mention}'s DMs", delete_after = 5)
            except Exception as e:
                console.error(f"Failed to send message to: {Fore.MAGENTA}{ctx.author}{Fore.LIGHTBLACK_EX} ({Fore.MAGENTA}{ctx.author.id}{Fore.LIGHTBLACK_EX}) {e}")
    else:
        await ctx.send(f"Sorry, but you can't use this command.", delete_after = 5)

@client.command()
async def rename(ctx, *, name = None):
    if ctx.author.id in botAccess:
        oldName = client.user.name
        if name is None:
            return await ctx.send("Wrong usage. `rename < newBotName >`", delete_after = 5)
        try:
            await client.user.edit(username = name)
            await ctx.send(f"Success. Changed Discord Bot name.\n`{oldName}` ---> `{client.user.name}`", delete_after = 5)
        except Exception as e:
            await ctx.send(f"```{e}```", delete_after = 5)
    else:
        await ctx.send(f"Sorry, but you can't use this command.", delete_after = 5)

@client.command(aliases = ['avatar'])
async def pfp(ctx, url = None):
    if ctx.author.id in botAccess:
        oldPfp = client.user.avatar
        if url is None:
            return await ctx.send("Wrong usage. `pfp < url >`", delete_after = 5)
        try:
            newPfp = requests.get(url)
            if newPfp.status_code == 200:
                await client.user.edit(avatar = newPfp.content)
                await ctx.send(f"Success. Changed Discord Bot pfp.\n`{oldPfp}` ---> `{client.user.avatar}`", delete_after = 5)
        except Exception as e:
            await ctx.send(f"```{e}```", delete_after = 5)
    else:
        await ctx.send(f"Sorry, but you can't use this command.", delete_after = 5)

try:
    configureBot(botToken)
    client.run(botToken)
except Exception as e:
    console.error(f"Failed to log in with {Fore.MAGENTA}{botToken[:26]}{Fore.RESET}{Fore.LIGHTBLACK_EX} token...")
    console.info(f"Error: {Fore.MAGENTA}{e}{Fore.RESET}")
    checkToken(botToken)
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    botToken = config_data["botConfig"]["botToken"]
    if not botToken:
        console.error(f"It seems that the botToken in the {Fore.MAGENTA}config.json{Fore.RESET}{Fore.LIGHTBLACK_EX} file is empty.")
        newBotToken = input("Please provide a valid Discord Bot token: ")

        config_data["botConfig"]["botToken"] = newBotToken
        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent = 4)
        console.success(f"Updated bot token in config.json with: {Fore.MAGENTA}{newBotToken}{Fore.RESET}")
