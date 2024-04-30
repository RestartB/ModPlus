import discord
from discord import app_commands, Color
import discord.ext
from discord.ui import View
from discord.ext import commands
import sqlite3

import discord.ext.tasks

class leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect(f"{self.bot.path}{self.bot.pathtype}content{self.bot.pathtype}sql{self.bot.pathtype}logging.db")
        self.cursor = self.connection.cursor()
    
    # # Enable LB command
    # @app_commands.command(name = "logging-config", description = "Control logging features.")
    # @app_commands.default_permissions(administrator = True)
    # async def enable_lb(self, interaction: discord.Interaction):
    #     await interaction.response.defer(ephemeral = True)
        
    #     embed = discord.Embed(title = "Loading...", color = Color.orange())
    #     await interaction.edit_original_response(embed = embed)

    #     try:
    #         if self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{str(interaction.guild.id)}_logging';").fetchone() != None:
    #             pass
    #         else:
    #             self.cursor.execute(f"CREATE TABLE '{interaction.guild.id}_logging' (messageCreateLogging text, messageDeleteLogging text, messageEditLogging text)")
    #     except Exception:
    #         embed = discord.Embed(title = "Unexpected Error", description = "Please try again later or message <@563372552643149825> for assistance.", color = Color.red())
    #         await interaction.edit_original_response(embed = embed, view = None)
    #         return
            
    #     embed = discord.Embed(title = "Logging Config", description = "Enable or disable logging for events.\n\nChanging Logging Channels\nTo change the channel for a logging type, disable the logging type and enable it again.")
    #     embed.add_field(name = "Logging Channels")
    #     view = View()

    #     messageCreateLogging = self.cursor.execute(f"SELECT messageCreateLogging FROM '{str(interaction.guild.id)}_logging';").fetchone()
    #     messageDeleteLogging = self.cursor.execute(f"SELECT messageDeleteLogging FROM '{str(interaction.guild.id)}_logging';").fetchone()
    #     messageEditLogging = self.cursor.execute(f"SELECT messageEditLogging FROM '{str(interaction.guild.id)}_logging';").fetchone()

    #     if messageCreateLogging == "True":
    #         createLogButton = discord.ui.Button(label='Message Created (enabled)', style=discord.ButtonStyle.green)
    #     if messageCreateLogging == "False":
    #         createLogButton = discord.ui.Button(label='Message Created (disabled)', style=discord.ButtonStyle.red)
        
    #     if messageDeleteLogging == "True":
    #         createLogButton = discord.ui.Button(label='Message Deleted (enabled)', style=discord.ButtonStyle.green)
    #     if messageDeleteLogging == "False":
    #         createLogButton = discord.ui.Button(label='Message Deleted (disabled)', style=discord.ButtonStyle.red)

    #     if messageEditLogging == "True":
    #         createLogButton = discord.ui.Button(label='Message Edited (enabled)', style=discord.ButtonStyle.green)
    #     if messageEditLogging == "False":
    #         createLogButton = discord.ui.Button(label='Message Edited (disabled)', style=discord.ButtonStyle.red)

    # Enable Logging command
    @app_commands.command(name = "enable-logging", description = "Enable a logging category.")
    @app_commands.default_permissions(administrator = True)
    @app_commands.choices(log_type=[
        app_commands.Choice(name="Message Create", value="messageCreateLogging"),
        app_commands.Choice(name="Message Delete", value="messageDeleteLogging"),
        app_commands.Choice(name="Message Edit", value="messageEditLogging"),
        ])
    async def enable_logging(self, interaction: discord.Interaction, log_type: app_commands.Choice[str], logging_channel: discord.TextChannel):
        await interaction.response.defer(ephemeral = True)

        embed = discord.Embed(title = "Enabling...", color = Color.orange())
        await interaction.followup.send(embed = embed, ephemeral = True)

        # try:
        if self.cursor.execute(f"SELECT server_id FROM 'loggingToggle' WHERE server_id = {interaction.guild.id}").fetchone() != None:
            if self.cursor.execute(f"SELECT {log_type.value} FROM 'loggingToggle' WHERE server_id = {interaction.guild.id}").fetchone() == "False":
                self.cursor.execute(f"UPDATE 'loggingChannel' SET {log_type.value} = {logging_channel.id} WHERE server_id = {interaction.guild.id}")
                self.cursor.execute(f"UPDATE 'loggingToggle' SET {log_type.value} = 'True' WHERE server_id = {interaction.guild.id}")

                self.connection.commit()

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
            
            embed = discord.Embed(title = "Enabled.", color = Color.green())
            await interaction.edit_original_response(embed = embed)
            return
        # except Exception:
        #     embed = discord.Embed(title = "Unexpected Error", description = "Please try again later or message <@563372552643149825> for assistance.", color = Color.red())
        #     await interaction.edit_original_response(embed = embed, view = None)
    
    # Disable Logging command
    # Broken
    @app_commands.command(name = "disable-logging", description = "Disable a logging category.")
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
    await bot.add_cog(leaderboard(bot))