import discord
from discord import Color, ButtonStyle
from discord.ext import commands
from discord.ui import View
import sqlite3
import datetime

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect(f"{self.bot.path}{self.bot.pathtype}content{self.bot.pathtype}sql{self.bot.pathtype}logging.db")
        self.cursor = self.connection.cursor()

    # Message Logger - Delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Look through logging toggle list
        for val in self.bot.loggingToggle:
            # If we find our server in the list...
            if val[0] == message.guild.id:
                # And message delete logging is enabled...
                if val[2] == "True":
                    # Ignore bots
                    if message.author.bot != True:
                        # Create embed
                        embed = discord.Embed(title = "Message Deleted", description = message.content, color = Color.red())
                        embed.add_field(name = "User Info", value = f"**User:** {message.author.mention} *(@{message.author.name})*\n**ID:** {message.author.id}", inline = False)
                        embed.add_field(name = "Message Info", value = f"**Channel:** {message.channel.name} - {message.channel.mention}\n**Message ID:** {message.id}\n**Time Created:** <t:{round((message.created_at).timestamp())}:t>", inline = False)
                        embed.timestamp = datetime.datetime.now()
                        
                        # Add attachments to embed
                        if message.attachments != []:
                            for attachment in message.attachments:
                                attachStr = ""
                                if attachStr == "":
                                    attachStr == f"[{attachment.filename}]({attachment.url})"
                                else:
                                    attachStr += f", [{attachment.filename}]({attachment.url})"
                                embed.add_field(name = f"Attachments ({len(message.attachments)} attachments)", value = attachStr)
                        
                        # Find logging channel
                        for val in self.bot.loggingChannel:
                            if val[0] == message.guild.id:
                                channel_id = val[2]
                        
                        channel = self.bot.get_channel(int(channel_id))
                        await channel.send(embed = embed)
                        break
                else:
                    pass
            else:
                pass
    
    # # Message Logger - Delete
    # @commands.Cog.listener()
    # async def on_raw_message_delete(self, payload):
    #     print("RAW TRIGGER")
    #     print(payload.channel_id)
    #     channel = self.bot.get_channel(1213954609299853365)
    #     await channel.send("Hello world!")
    #     message = channel.get_message(1235657890220474468)
    #     print(message)
    #     print(message.content)
    
    # Message Logger - Edit
    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        # Look through logging toggle list
        for val in self.bot.loggingToggle:
            # If we find our server in the list...
            if val[0] == message_before.guild.id:
                # And message edit logging is enabled...
                if val[3] == "True":
                    # Ignore bots
                    if message_before.author.bot != True:
                        if message_before.content != message_after.content:
                            embed = discord.Embed(title = "Message Edited", color = Color.yellow())
                            embed.add_field(name = "User Info", value = f"**User:** {message_before.author.mention} *({message_before.author.name})*\n**ID:** {message_before.author.id}", inline = False)
                            embed.add_field(name = "Message Info", value = f"**Channel:** {message_before.channel.name} - {message_before.channel.mention}\n**Message ID:** {message_before.id}\n**Time Created:** <t:{round((message_before.created_at).timestamp())}:t>", inline = False)
                            embed.add_field(name = "Before Edit", value = (f"{message_before.content[:1021]}..." if len(message_before.content) > 1024 else message_before.content), inline = True)
                            embed.add_field(name = "After Edit", value = (f"{message_after.content[:1021]}..." if len(message_after.content) > 1024 else message_after.content), inline = True)
                            embed.timestamp = datetime.datetime.now()

                            view = View()
                            jumpButton = discord.ui.Button(style = ButtonStyle.url, url = message_after.jump_url, label = "Jump to Message")
                            view.add_item(jumpButton)

                            # Find logging channel
                            for val in self.bot.loggingChannel:
                                if val[0] == message_before.guild.id:
                                    channel_id = val[3]
                            
                            channel = self.bot.get_channel(int(channel_id))
                            await channel.send(embed = embed)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
            
async def setup(bot):
    await bot.add_cog(logging(bot))