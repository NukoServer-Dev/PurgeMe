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
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(
        embed=discord.Embed(title="このBotの使い方", description="`/purge`で自分のメッセージを削除できます。", color=discord.Color.blue())
    )

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
            if not message.webhook_id:
                return False
            if message.author.display_name == interaction.user.display_name:
                return True

        if message.author.id == interaction.user.id:
            return True

        return False

    try:
        deleted = await interaction.channel.purge(limit=count + 1, check=check)
    except:
        await interaction.channel.send(embed=discord.Embed(description="削除に失敗しました。", color=discord.Color.red()))

    await interaction.followup.send(embed=discord.Embed(description=f"<:trash:1574976390682378300> あなたのメッセージが{len(deleted)}件削除されました。", color=discord.Color.blue()))

@bot.tree.context_menu(name="メッセージを削除")
@discord.app_commands.default_permissions(manage_messages=True)
async def delete_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True)

    async def process():
        if message.author.id == interaction.user.id:
            await message.delete()
            return True
        if message.author.bot:
            if not message.webhook_id:
                return False
            if message.author.display_name == interaction.user.display_name:
                await message.delete()
                return True

        return False

    check = await process()
    if check:
        await interaction.followup.send(ephemeral=True, content="<:trash:1574976390682378300> あなたのメッセージを削除しました。")
    else:
        await interaction.followup.send(ephemeral=True, content="削除できるのはあなたのメッセージだけです。")

@bot.tree.context_menu(name="ここから下を削除")
@discord.app_commands.default_permissions(manage_messages=True)
async def delete_under_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()

    def check(message: discord.Message):
        if message.author.bot:
            if not message.webhook_id:
                return False
            if message.author.display_name == interaction.user.display_name:
                return True

        if message.author.id == interaction.user.id:
            return True

        return False

    try:
        deleted = await interaction.channel.purge(limit=100, check=check, after=message.created_at)
    except:
        await interaction.channel.send(embed=discord.Embed(description="削除に失敗しました。", color=discord.Color.red()))

    await interaction.followup.send(embed=discord.Embed(description=f"<:trash:1574976390682378300> あなたのメッセージが{len(deleted)}件削除されました。", color=discord.Color.blue()))

class ReadyButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="通知ON")
    async def start_notify_on(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        await interaction.user.add_roles(discord.Object(1575471165454024869), reason="起動通知ON")

        await interaction.followup.send(content="起動通知をOnにしました。", ephemeral=True)

    @discord.ui.button(label="通知OFF")
    async def start_notify_off(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        await interaction.user.remove_roles(discord.Object(1575471165454024869), reason="起動通知OFF")
        
        await interaction.followup.send(content="起動通知をOffにしました。", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("起動完了！")

    await bot.change_presence(activity=discord.CustomActivity(name="/purge"))

    await bot.get_channel(1575470427034357811).send(
        content="<@&1575471165454024869>",
        embed=discord.Embed(title="PurgeMeは起動しました！", description="以下のボタンで通知を切り替えられます↓", color=discord.Color.random()),
        view=ReadyButtonView()
    )

bot.run(os.environ.get('DISCORD_TOKEN'))