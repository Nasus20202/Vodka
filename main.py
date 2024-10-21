import discord
from config import *
from list_manager import ListManager
from datetime import timedelta
import persistence

intents = discord.Intents.default()
client = discord.Client(intents=intents)
command_tree = discord.app_commands.CommandTree(client=client)
list_manager = persistence.load_user_metadata(ListManager())


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await command_tree.sync()
    await client.change_presence(activity=discord.CustomActivity(name="/pomoc"))


@command_tree.command(name="pomoc", description="Wyświetla pomoc")
async def attending(interaction: discord.Interaction):
    help = """**Pomoc**
    `/pomoc` - wyświetla pomoc
    `/wpiszcie` - prośba o wpisanie na listę
    `/wpisze` - zapisuje inną osobę na wykład
    `/zapisani` - lista osób zapisanych na wykład
    `/drzemka` - zapisuje się na drzemkę
    `/lista` - lista osób do wpisania
    `/reset` - resetuje listę
    `/metadane` - ustawia imie i indeks użytkownika
    `/indeksy` - wyświetla indeksy użytkowników"""
    await interaction.response.send_message(help, ephemeral=True)


@command_tree.command(name="metadane", description="Ustawia metadane użytkownika")
async def metadane(interaction: discord.Interaction, name: str, index_number: int):
    list_manager.set_user_metadata(interaction.user, name, index_number)
    await interaction.response.send_message("Ustawiono metadane", ephemeral=True)

    persistence.backup_user_metadata(list_manager)


@command_tree.command(name="indeksy", description="Wyświetla indeksy użytkowników")
async def indeksy(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Indeksy użytkowników",
        description="Lista indeksów użytkowników",
        color=0x0000FF,
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

    for user in sorted(list_manager.get_all_users(), key=lambda x: str(x)):
        embed.add_field(
            name=str(user),
            value=str(
                user.metadata.index_number if user.metadata.index_number else "N/A"
            ),
            inline=False,
        )
    embed.set_footer(text="Miłego wykładu!")

    await interaction.response.send_message("Indeksy", embed=embed)


@command_tree.command(name="wpiszcie", description="Prośba o wpisanie na liste")
async def not_attending(interaction: discord.Interaction):
    list_manager.set_user_attending(interaction.user, False)
    list_user = list_manager.users[interaction.user.id]
    await interaction.response.send_message(
        f"{list_user} ({list_user.metadata.index_number if list_user.metadata.index_number else 'N/A'}) prosi o wpisanie na listę"
    )


@command_tree.command(name="wpisze", description="Zapisuje inną osobę na wykład")
async def enlist(interaction: discord.Interaction, user: discord.User):
    list_manager.enlist_user(user, interaction.user)
    list_user = list_manager.users[user.id]
    await interaction.response.send_message(
        f"{interaction.user.name} zapisze {list_user} ({list_user.metadata.index_number if list_user.metadata.index_number else "N/A"}) na listę"
    )


@command_tree.command(name="zapisani", description="Lista osób zapisanych na wykład")
async def print_enlisted(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Lista osób wpisanych",
        description="Osoby na tej liście zostały wpisane na listę",
        color=0xFF0000,
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    for user in list_manager.get_enlisted():
        user_enlister = list_manager.users[user.enlister.id]
        embed.add_field(
            name=f"{user} ({user.metadata.index_number if user.metadata.index_number else 'N/A'})",
            value=f"wpisany przez {user_enlister} ({user_enlister.metadata.index_number if user_enlister.metadata.index_number else 'N/A'})",
            inline=False,
        )
    embed.set_footer(text="Miłego wykładu!")

    await interaction.response.send_message("Lista", embed=embed)


@command_tree.command(name="drzemka", description="Zapisuje się na drzemkę")
async def sleep(interaction: discord.Interaction, time: int = 8):
    if time > 12:
        await interaction.response.send_message(
            "Nie możesz spać tyle godzin!", ephemeral=True
        )
        return
    if time < 1:
        await interaction.response.send_message(
            "Troche nie zdrowo tak krótko spać", ephemeral=True
        )
        return
    sleep_time = timedelta(hours=time)
    list_manager.sleep_user(interaction.user, sleep_time)
    await interaction.response.send_message(
        f"Zapisano na drzemkę na {time} godzin, smacznego", ephemeral=True
    )


@command_tree.command(name="lista", description="Lista osób do wpisania")
async def print_list(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Lista osób do wpisania",
        description="Osoby na tej liście zadeklarowały, że nie będzie ich na wykładzie",
        color=0x00FF00,
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    for user in list_manager.get_not_attending():
        embed.add_field(
            name=str(user),
            value=str(
                user.metadata.index_number if user.metadata.index_number else "N/A"
            ),
            inline=False,
        )
    embed.set_footer(text="Miłego wykładu!")

    await interaction.response.send_message("Lista", embed=embed)


@command_tree.command(name="reset", description="Resetuje listę")
async def reset_list(interaction: discord.Interaction):
    list_manager.reset_list()
    await interaction.response.send_message("Zresetowano listę")


client.run(token)
