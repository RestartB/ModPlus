import discord
from discord import Color, ButtonStyle
from discord.ext import commands
from discord.ui import View
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
import asyncio
import re

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auth_manager = SpotifyClientCredentials(client_id = self.bot.spotify_id, client_secret = self.bot.spotify_secret)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
    
    # Message Logger - Delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Ignore bots
        if message.author.bot != True:
            embed = discord.Embed(title = "Message Deleted", description = message.content, color = Color.red())
            embed.add_field(name = "User Info", value = f"User: {message.author.mention} ({message.author.name})\nID: {message.author.id}")
            embed.add_field(name = "Message Info", value = f"Channel: {message.channel.name} - {message.channel.mention}\nMessage ID: {message.id}\nTime Created: <t:{round((message.created_at).timestamp())}:t>")
            embed.add_field(name = "Message Content", value = (f"{message.content[:1021]}..." if len(message.content) > 1024 else message.content))
            if message.attachments != []:
                for attachment in message.attachments:
                    attachStr = ""
                    if attachStr == "":
                        attachStr == f"[{attachment.filename}]({attachment.url})"
                    else:
                        attachStr += f", [{attachment.filename}]({attachment.url})"
                    embed.add_field(name = f"Attachments ({len(message.attachments)} attachments)", value = attachStr)
        else:
            pass
    
    # Message Logger - Edit
    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        # Ignore bots
        if message_before.author.bot != True:
            if message_before.content != message_after.content:
                embed = discord.Embed(title = "Message Edited", color = Color.yellow())
                embed.add_field(name = "User Info", value = f"User: {message_before.author.mention} ({message_before.author.name})\nID: {message_before.author.id}", inline = False)
                embed.add_field(name = "Message Info", value = f"Channel: {message_before.channel.name} - {message_before.channel.mention}\nMessage ID: {message_before.id}\nTime Created: <t:{round((message_before.created_at).timestamp())}:t>", inline = False)
                embed.add_field(name = "Before Edit", value = (f"{message_before.content[:1021]}..." if len(message_before.content) > 1024 else message_before.content), inline = True)
                embed.add_field(name = "After Edit", value = (f"{message_after.content[:1021]}..." if len(message_after.content) > 1024 else message_after.content), inline = True)

                view = View()
                jumpButton = discord.ui.Button(style = discord.ButtonStyle.url, url = message_after.jump_url, label = "Jump to Message")
                view.add_item(jumpButton)



            else:
                pass
        else:
            pass
            
async def setup(bot):
    await bot.add_cog(logging(bot))