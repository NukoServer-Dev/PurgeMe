from discord.ext import commands
import discord
import os
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.none()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.tree.command(name="help", description="このBotの使い方")
@discord.app_commands.default_permissions(manage_channels=True)
async def help_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=discord.Embed(title="このBotの使い方", description="`/purge`で自分のメッセージを削除できます。\nチャンネルの管理権限が必要です。", color=discord.Color.blue()))

@bot.tree.command(name="purge", description="自分のメッセージを削除します。")
@discord.app_commands.describe(count="削除する数")
@discord.app_commands.default_permissions(manage_channels=True)
async def purge_me(interaction: discord.Interaction, count: int):
    if count > 100:
        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description="一回で100件まで削除できます。", color=discord.Color.red()))
        return
    if count < 1:
        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description="1件以上を指定してください。", color=discord.Color.red()))
        return

    await interaction.response.defer()

    def check(message: discord.Message):
        if message.author.bot:
            if message.author.display_avatar == interaction.user.display_name:
                return True

        if message.author.id == interaction.user.id:
            return True

        return False

    try:
        deleted = await interaction.channel.purge(limit=count + 1, check=check)
    except:
        await interaction.channel.send(embed=discord.Embed(description="削除に失敗しました。", color=discord.Color.red()))

    await interaction.followup.send(embed=discord.Embed(description=f"<:trash:1574976390682378300> あなたのメッセージが{len(deleted)}件削除されました。", color=discord.Color.blue()))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("起動完了！")

    await bot.change_presence(activity=discord.CustomActivity(name="/purge"))

    await bot.get_channel(1572070912964956272).send(content="<:trash:1574976390682378300> 起動しました。")

bot.run(os.environ.get('DISCORD_TOKEN'))