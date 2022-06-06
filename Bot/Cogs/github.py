import os

import aiohttp
import discord
import orjson
import simdjson
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from exceptions import HTTPException, NoItemsError

parser = simdjson.Parser()

load_dotenv()

githubAPIKey = os.getenv("GitHub_API_Access_Token")


class GitHubV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    github = SlashCommandGroup("github", "GitHub commands")
    githubSearch = github.create_subgroup("search", "Search for repositories on GitHub")
    githubIssues = github.create_subgroup("issues", "Search for issues on GitHub")
    githubReleases = github.create_subgroup("releases", "Search for releases on GitHub")

    @githubSearch.command(name="repos")
    async def githubRepos(self, ctx, *, repo: Option(str, "The name of the repo")):
        """Searches for repositories on GitHub"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {"q": repo, "sort": "stars", "order": "desc", "per_page": 25}
            async with session.get(
                "https://api.github.com/search/repositories",
                headers=headers,
                params=params,
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    try:
                        if len(dataMain["items"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=mainItem["name"],
                                        description=mainItem["description"],
                                    )
                                    .add_field(
                                        name="URL",
                                        value=mainItem["html_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Private",
                                        value=mainItem["private"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Fork", value=mainItem["fork"], inline=True
                                    )
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
                                        name="Language",
                                        value=mainItem["language"],
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
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = f"Sorry, there seems to be no repos named {repo}. Please try again"
                        await ctx.respond(embed=embedNoItemsError)

                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, but something went wrong. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    @githubSearch.command(name="users")
    async def githubSearchUsers(
        self, ctx, *, user: Option(str, "The user on GitHub to search")
    ):
        """Searches for users on GitHub"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {"q": user, "sort": "stars", "order": "desc", "per_page": 25}
            async with session.get(
                "https://api.github.com/search/users", headers=headers, params=params
            ) as response:
                try:
                    try:
                        data = await response.content.read()
                        dataMain = parser.parse(data, recursive=True)
                        if len(dataMain["items"]) == 0:
                            raise NoItemsError
                        else:
                            mainFilters = [
                                "login",
                                "id",
                                "node_id",
                                "avatar_url",
                                "html_url",
                                "gravatar_id",
                                "type",
                                "site_admin",
                                "score",
                            ]
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(title=dictItem["login"])
                                    .add_field(
                                        name="Type", value=dictItem["type"], inline=True
                                    )
                                    .add_field(
                                        name="URL",
                                        value=dictItem["html_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="User URLS",
                                        value=str(
                                            [
                                                v
                                                for k, v in dictItem.items()
                                                if k not in mainFilters
                                            ]
                                        ).replace("'", ""),
                                        inline=True,
                                    )
                                    .set_thumbnail(url=dictItem["avatar_url"])
                                    for dictItem in dataMain["items"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = f"Sorry, there seems to be no repos from {user}. Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, but something went wrong. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    # Remake tokens with correct scopes
    @githubSearch.command(name="commits")
    async def githubSearchCommits(
        self,
        ctx,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
        search: Option(str, "The search term you wish to search for"),
    ):
        """Searches for commits in any GitHub repo based on the given search term"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {
                "q": f"repo:{owner}/{repo}+{search}",
                "sort": "stars",
                "order": "desc",
                "per_page": 25,
            }
            async with session.get(
                "https://api.github.com/search/commits", headers=headers, params=params
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    print(dataMain)
                    try:
                        if len(dataMain["items"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=mainItem2["commit"]["author"]["name"],
                                        description=mainItem2["commit"]["message"],
                                    )
                                    .add_field(
                                        name="Commit Hash",
                                        value=mainItem2["sha"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="URL",
                                        value=mainItem2["html_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Commit Date",
                                        value=mainItem2["commit"]["date"],
                                        inline=True,
                                    )
                                    .set_thumbnail(
                                        url=mainItem2["author"]["avatar_url"]
                                    )
                                    for mainItem2 in dataMain["items"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = f"Sorry, there seems to be no commits that has any relationship with the term {search}. Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, but something went wrong. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    @github.command(name="commit")
    async def githubCommit(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
        commit_sha: Option(str, "The commit's SHA hash"),
    ):
        """Gets info about a commit based on hash"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/git/commits/{commit_sha}",
                headers=headers,
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    embedMain = discord.Embed()
                    mainFilters = [
                        "url",
                        "author",
                        "committer",
                        "tree",
                        "parents",
                        "verification",
                        "message",
                    ]
                    for k, v in dataMain.items():
                        if k not in mainFilters:
                            embedMain.add_field(name=k, value=v, inline=True)
                    for keys, value in dataMain["verification"].items():
                        embedMain.add_field(name=keys, value=value, inline=True)
                    embedMain.title = dataMain["author"]["name"]
                    embedMain.description = dataMain["message"]
                    embedMain.set_thumbnail(url=dataMain["author"]["avatar_url"])
                    await ctx.respond(embed=embedMain)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = "It seems like that there isn't a commit with that hash or repo. Please try again"
                    await ctx.respond(embed=embedError)

    @githubIssues.command(name="all")
    async def githubIssuesRepo(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
        state: Option(
            str,
            "Whether an issue has been open or closed (or all)",
            choices=["Open", "Closed", "All"],
        ),
    ):
        """Gets all issues from a repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {
                "state": str(state).lower(),
                "sort": "created",
                "per_page": 25,
                "direction": "desc",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/issues",
                headers=headers,
                params=params,
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    try:
                        if len(dataMain) == 0:
                            raise NoItemsError
                        else:

                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=mainItem3["title"],
                                        description=mainItem3["body"],
                                    )
                                    .add_field(
                                        name="URL",
                                        value=mainItem3["html_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Issue State",
                                        value=mainItem3["state"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Issue Number",
                                        value=mainItem3["number"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Issue Created",
                                        value=mainItem3["created_at"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Issue Updated",
                                        value=mainItem3["updated_at"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Label",
                                        value=[
                                            labelItemMain["name"]
                                            for labelItemMain in mainItem3["labels"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Comments", value=mainItem3["comments"]
                                    )
                                    .add_field(
                                        name="Assigness",
                                        value=[
                                            item4["login"]
                                            for item4 in mainItem3["assignees"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Reporter",
                                        value=mainItem3["user"]["login"],
                                        inline=True,
                                    )
                                    .set_thumbnail(url=mainItem3["user"]["avatar_url"])
                                    for mainItem3 in dataMain
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = f"Sorry, there seems to be no issues in that repo. Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "It seems like there was a error. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    @githubIssues.command(name="one")
    async def githhubIssuesRepoOne(
        self,
        ctx,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
        issue_number: Option(str, "The number for the issue on GitHub"),
    ):
        """Gets info about one issue on any repo on GitHub"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/issues{issue_number}",
                headers=headers,
            ) as r:
                try:
                    if r.status == 404:
                        raise HTTPException
                    else:
                        data = await r.content.read()
                        dataMain = parser.parse(data, recursive=True)
                        embed = discord.Embed()
                        filter = [
                            "user",
                            "labels",
                            "assignee",
                            "assignee",
                            "milestone",
                            "pull_request",
                            "closed_by",
                            "title",
                            "body",
                            "url",
                            "repository_url",
                            "labels_url",
                            "comments_url",
                            "events_url",
                        ]
                        for k, v in dataMain.items():
                            if k not in filter:
                                embed.add_field(name=k, value=v, inline=True)
                        for itemMain in dataMain["labels"]:
                            for k, v in itemMain["labels"]:
                                embed.add_field(
                                    name=f"{k} (Labels)", value=v, inline=True
                                )
                        embed.add_field(
                            name="Assignees",
                            value=[
                                itemMain5["login"]
                                for itemMain5 in dataMain["assignees"]
                            ],
                            inline=True,
                        )
                        embed.add_field(
                            name="Reporter",
                            value=dataMain["user"]["login"],
                            inline=True,
                        )
                        embed.title = dataMain["title"]
                        embed.description = dataMain["body"]
                        await ctx.respond(embed=embed)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "It seems like that there isn't an issue with that number. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    @githubIssues.command(name="comments")
    async def githubIssuesRepoComments(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
    ):
        """Gets up to 25 of the comments from the repo's issues"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {"sort", "created", "direction", "desc", "per_page", 25}
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/issues/comments",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    try:
                        if len(dataMain) == 0:
                            raise NoItemsError
                        elif r.status == 404:
                            raise HTTPException
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=dictItem4["user"]["login"],
                                        description=dictItem4["body"],
                                    )
                                    .add_field(
                                        name="URL",
                                        value=dictItem4["html_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Created At",
                                        value=dictItem4["created_at"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Updated At",
                                        value=dictItem4["updated_at"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Author Association",
                                        value=f"[{dictItem4['author_association']}]",
                                        inline=True,
                                    )
                                    .set_thumbnail(url=dictItem4["user"]["avatar_url"])
                                    for dictItem4 in dataMain
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = "Sorry, there seems to be no comments in that repo. Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, there seems to be no comments in that repo. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    @github.command(name="license")
    async def githubLicenses(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
    ):
        """Returns the license used in the repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/license", headers=headers
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    if r.status == 404:
                        raise HTTPException
                    else:
                        embed = discord.Embed()
                        filterV2 = [
                            "git_url",
                            "url",
                            "_links",
                            "license",
                            "content",
                            "encoding",
                        ]
                        for keys, value in dataMain.items():
                            if keys not in filterV2:
                                embed.add_field(name=keys, value=value, inline=True)
                        for k, v in dataMain["_links"].items():
                            embed.add_field(name=k, value=v, inline=True)
                        embed.title = dataMain["license"]["name"]
                        await ctx.respond(embed=embed)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, there seems to be no license in that repo. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    @githubReleases.command(name="list")
    async def githubReleasesList(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
    ):
        """Lists out up to 25 releases of any repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {"per_page": 25}
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases",
                headers=headers,
                params=params,
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    if r.status == 404:
                        raise HTTPException
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=dictItem5["name"],
                                    description=dictItem5["body"],
                                )
                                .add_field(
                                    name="URL", value=dictItem5["html_url"], inline=True
                                )
                                .add_field(
                                    name="Created At",
                                    value=dictItem5["created_at"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Published At",
                                    value=dictItem5["published_at"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Tarball URL",
                                    value=dictItem5["tarball_url"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Zipball URL", value=dictItem5["zipball_url"]
                                )
                                .add_field(
                                    name="Author",
                                    value=dictItem5["author"]["login"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Download URL",
                                    value=str(
                                        [
                                            items5["browser_download_url"]
                                            for items5 in dictItem5["assets"]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="Download Count",
                                    value=str(
                                        [
                                            items6["download_count"]
                                            for items6 in dictItem5["assets"]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .set_thumbnail(url=dictItem5["author"]["avatar_url"])
                                for dictItem5 in dataMain
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, there seems to be no releases in that repo. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)


def setup(bot):
    bot.add_cog(GitHubV1(bot))
