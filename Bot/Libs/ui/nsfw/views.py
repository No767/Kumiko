import discord


# Probably will remove this anyways
class R34DownloadView(discord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="Download", url=link))
