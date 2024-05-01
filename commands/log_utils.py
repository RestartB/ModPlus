import discord
from discord import app_commands, Color
import discord.ext
from discord.ui import View
from discord.ext import commands
import sqlite3
#import log_utils
import asyncio

import discord.ext.tasks

class log_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect(f"{self.bot.path}{self.bot.pathtype}content{self.bot.pathtype}sql{self.bot.pathtype}logging.db")
        self.cursor = self.connection.cursor()
        self.bot.loggingToggle = self.cursor.execute(f"SELECT * FROM 'loggingToggle'").fetchall()
        self.bot.loggingChannel = self.cursor.execute(f"SELECT * FROM 'loggingChannel'").fetchall()
        print("[LOG] Refreshed logging vars.")

    async def refreshLoggingVars(self):
        self.bot.loggingToggle = self.cursor.execute(f"SELECT * FROM 'loggingToggle'").fetchall()
        self.bot.loggingChannel = self.cursor.execute(f"SELECT * FROM 'loggingChannel'").fetchall()
    
    loggingControlGroup = app_commands.Group(name="logging", description="Control logging features.")
    
    # Enable Logging command
    @loggingControlGroup.command(name = "enable", description = "Enable a logging category.")
    @app_commands.default_permissions(administrator = True)
    @app_commands.choices(log_type=[
        app_commands.Choice(name="Message Create", value="messageCreateLogging"),
        app_commands.Choice(name="Message Delete", value="messageDeleteLogging"),
        app_commands.Choice(name="Message Edit", value="messageEditLogging"),
        ])
    async def enable_logging(self, interaction: discord.Interaction, log_type: app_commands.Choice[str], logging_channel: discord.TextChannel):
        await interaction.response.defer(ephemeral = True)

        try:
            embed = discord.Embed(title = "Enabling...", color = Color.orange())
            await interaction.followup.send(embed = embed, ephemeral = True)

            if self.cursor.execute(f"SELECT server_id FROM 'loggingToggle' WHERE server_id = {interaction.guild.id}").fetchone() != None:
                if (self.cursor.execute(f"SELECT {log_type.value} FROM 'loggingToggle' WHERE server_id = {interaction.guild.id}").fetchone())[0] == "False":
                    self.cursor.execute(f"UPDATE 'loggingChannel' SET {log_type.value} = {logging_channel.id} WHERE server_id = {interaction.guild.id}")
                    self.cursor.execute(f"UPDATE 'loggingToggle' SET {log_type.value} = 'True' WHERE server_id = {interaction.guild.id}")

                    self.connection.commit()

                    await log_utils.refreshLoggingVars()

                    embed = discord.Embed(title = "Enabled.", color = Color.green())
                    await interaction.edit_original_response(embed = embed)
                else:
                    embed = discord.Embed(title = "Already enabled.", color = Color.green())
                    await interaction.edit_original_response(embed = embed)
            else:
                self.cursor.execute(f"INSERT INTO 'loggingToggle' (server_id, messageCreateLogging, messageDeleteLogging, messageEditLogging) VALUES ({interaction.guild.id}, 'False', 'False', 'False')")
                self.cursor.execute(f"INSERT INTO 'loggingChannel' (server_id) VALUES ({interaction.guild.id})")

                self.cursor.execute(f"UPDATE 'loggingChannel' SET {log_type.value} = {logging_channel.id} WHERE server_id = {interaction.guild.id}")
                self.cursor.execute(f"UPDATE 'loggingToggle' SET {log_type.value} = 'True' WHERE server_id = {interaction.guild.id}")
                
                self.connection.commit()
                
                await log_utils.refreshLoggingVars()
                
                embed = discord.Embed(title = "Enabled.", color = Color.green())
                await interaction.edit_original_response(embed = embed)
        except Exception:
            embed = discord.Embed(title = "Unexpected Error", description = "Please try again later or message <@563372552643149825> for assistance.", color = Color.red())
            await interaction.edit_original_response(embed = embed)
    
    # Disable Logging command
    # Broken
    @loggingControlGroup.command(name = "disable", description = "Disable a logging category.")
    @app_commands.default_permissions(administrator = True)
    @app_commands.choices(log_type=[
        app_commands.Choice(name="Message Create", value="messageCreateLogging"),
        app_commands.Choice(name="Message Delete", value="messageDeleteLogging"),
        app_commands.Choice(name="Message Edit", value="messageEditLogging"),
        ])
    async def disable_logging(self, interaction: discord.Interaction, log_type: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral = True)

        embed = discord.Embed(title = "Disabling...", color = Color.orange())
        await interaction.followup.send(embed = embed, ephemeral = True)

        try:
            if self.cursor.execute(f"SELECT server_id FROM 'loggingToggle' WHERE server_id = {interaction.guild.id}").fetchone() != None:
                if self.cursor.execute(f"SELECT {log_type.value} FROM 'loggingToggle' WHERE server_id = {interaction.guild.id}").fetchone() == "True":
                    self.cursor.execute(f"UPDATE 'loggingChannel' SET {log_type.value} = {None} WHERE server_id = {interaction.guild.id}")
                    self.cursor.execute(f"UPDATE 'loggingToggle' SET {log_type.value} = 'False' WHERE server_id = {interaction.guild.id}")

                    self.connection.commit()

                    await log_utils.refreshLoggingVars()
                    
                    embed = discord.Embed(title = "Disabled.", color = Color.green())
                    await interaction.edit_original_response(embed = embed)
                else:
                    embed = discord.Embed(title = "Already disabled.", color = Color.green())
                    await interaction.edit_original_response(embed = embed)
            else:
                embed = discord.Embed(title = "Already disabled.", color = Color.green())
                await interaction.edit_original_response(embed = embed)
        except Exception:
            embed = discord.Embed(title = "Unexpected Error", description = "Please try again later or message <@563372552643149825> for assistance.", color = Color.red())
            await interaction.edit_original_response(embed = embed, view = None)
        
async def setup(bot):
    await bot.add_cog(log_utils(bot))