import os

import aiohttp
import discord
import orjson
import simdjson
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv

parser = simdjson.Parser()

load_dotenv()

githubAPIKey = os.getenv("GitHub_API_Access_Token")


class GitHubV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    github = SlashCommandGroup("github", "GitHub commands")
    githubSearch = github.create_subgroup("search", "Search for repositories on GitHub")

    @githubSearch.command(name="repos")
    async def githubRepos(self, ctx, *, repo: Option(str, "The name of the repo")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {"q": repo, "sort": "stars", "order": "desc", "per_page": 50}
            async with session.get(
                "https://api.github.com/search/repositories",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=mainItem["name"], description=mainItem["description"]
                        )
                        .add_field(name="URL", value=mainItem["html_url"], inline=True)
                        .add_field(
                            name="Private", value=mainItem["private"], inline=True
                        )
                        .add_field(name="Fork", value=mainItem["fork"], inline=True)
                        .add_field(
                            name="Creation Date",
                            value=mainItem["created_at"],
                            inline=True,
                        )
                        .add_field(
                            name="Homepage",
                            value=f"[{mainItem['homepage']}]",
                            inline=True,
                        )
                        .add_field(
                            name="Stars",
                            value=mainItem["stargazers_count"],
                            inline=True,
                        )
                        .add_field(
                            name="Language", value=mainItem["language"], inline=True
                        )
                        .add_field(
                            name="License",
                            value=[
                                dictItem["name"]
                                for dictItem in mainItem["license"]
                                if dictItem["name"] is None
                            ],
                            inline=True,
                        )
                        .add_field(
                            name="Forks Count",
                            value=mainItem["forks_count"],
                            inline=True,
                        )
                        .set_thumbnail(url=mainItem["owner"]["avatar_url"])
                        for mainItem in dataMain["items"]
                    ]
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(GitHubV1(bot))
