import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
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
    githubUser = github.create_subgroup("user", "GitHub user commands")
    githubSearch = github.create_subgroup("search", "Search for repositories on GitHub")
    githubIssuesGroup = github.create_subgroup("issues", "Search for issues on GitHub")
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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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
                        embedNoItemsError.description = f"Sorry, there seems to be no users named {user}. Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, but something went wrong. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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
                    if r.status == 404:
                        raise HTTPException
                    else:
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
                        await ctx.respond(embed=embedMain)
                except HTTPException:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="It seems like that there isn't a commit with that hash or repo. Please try again"
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @githubIssuesGroup.command(name="all")
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
                        try:
                            if len(dataMain) == 0:
                                raise NoItemsError
                            elif r.status == 404:
                                raise HTTPException
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
                                        .set_thumbnail(
                                            url=mainItem3["user"]["avatar_url"]
                                        )
                                        for mainItem3 in dataMain
                                    ],
                                    loop_pages=True,
                                )
                                await mainPages.respond(
                                    ctx.interaction, ephemeral=False
                                )
                        except HTTPException:
                            await ctx.respond(
                                embed=discord.Embed(
                                    description="It seems like that there isn't a repo with that name. Please try again"
                                )
                            )
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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @githubIssuesGroup.command(name="one")
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
                f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}",
                headers=headers,
            ) as r:
                try:
                    if r.status == 404:
                        raise HTTPException
                    else:
                        data = await r.content.read()
                        dataMain = parser.parse(data, recursive=True)
                        embed = discord.Embed()
                        filter54 = [
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
                            "assignees",
                            "reactions",
                        ]
                        for k, v in dict(dataMain).items():
                            if k not in filter54:
                                embed.add_field(name=k, value=v, inline=True)
                        for itemMain in dataMain["labels"]:
                            for k, v in itemMain.items():
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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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
                    try:
                        if r.status == 404:
                            raise HTTPException
                        elif len(dataMain) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=dictItem5["name"],
                                        description=dictItem5["body"],
                                    )
                                    .add_field(
                                        name="URL",
                                        value=dictItem5["html_url"],
                                        inline=True,
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
                                        name="Zipball URL",
                                        value=dictItem5["zipball_url"],
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
                                    .set_thumbnail(
                                        url=dictItem5["author"]["avatar_url"]
                                    )
                                    for dictItem5 in dataMain
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        await ctx.respond(
                            embed=discord.Embed(
                                description="It seems like that there isn't a release for that repo. Please try again"
                            )
                        )
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, there seems to be no releases in that repo. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @githubReleases.command(name="latest")
    async def githubLatestRelease(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The repo's name"),
    ):
        """Gets the latest published full release for any repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                mainFilter = ["author", "assets", "body", "name"]
                embed = discord.Embed()
                try:
                    if r.status == 404:
                        raise HTTPException
                    else:
                        for keys, value in dataMain.items():
                            if keys not in mainFilter:
                                embed.add_field(name=keys, value=value, inline=True)
                        for mainItem in dataMain["assets"]:
                            for k, v in mainItem.items():
                                if k not in "uploader":
                                    embed.add_field(name=k, value=v, inline=True)
                        embed.add_field(
                            name="author", value=dataMain["author"]["login"]
                        )
                        embed.title = dataMain["name"]
                        embed.description = dataMain["body"]
                        embed.set_thumbnail(url=dataMain["author"]["avatar_url"])
                        await ctx.respond(embed=embed)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, but it seems like either there was no release or the repo doesn't exist. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @github.command(name="repo")
    async def githubReposInfo(
        self,
        ctx,
        *,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
    ):
        """Returns info about any repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}", headers=headers
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embedMain = discord.Embed()
                embedFilter = [
                    "permissions",
                    "owner",
                    "template_repository",
                    "organization",
                    "source",
                    "parent",
                    "license",
                    "url",
                    "archive_url",
                    "assignees_url",
                    "blobs_url",
                    "branches_url",
                    "collaborators_url",
                    "commits_url",
                    "comments_url",
                    "compare_url",
                    "contributors_url",
                    "deployments_url",
                    "downloads_url",
                    "events_url",
                    "forks_url",
                    "git_commits_url",
                    "git_refs_url",
                    "git_tags_url",
                    "git_url",
                    "issue_comment_url",
                    "issue_events_url",
                    "issues_url",
                    "keys_url",
                    "labels_url",
                    "languages_url",
                    "merges_url",
                    "milestones_url",
                    "notifications_url",
                    "pulls_url",
                    "releases_url",
                    "stargazers_urls",
                    "statuses_url",
                    "subscribers_url",
                    "subscription_url",
                    "tags_url",
                    "teams_url",
                    "trees_url",
                    "clone_url",
                    "mirror_url",
                    "hooks_url",
                    "svn_url",
                    "contents_url",
                    "description",
                ]
                licenseFilter = ["key, url", "spdx_id", "node_id", "html_url"]
                try:
                    if r.status == 404:
                        raise HTTPException
                    else:
                        for keys, value in dataMain.items():
                            if keys not in embedFilter:
                                embedMain.add_field(
                                    name=keys, value=f"[{value}]", inline=True
                                )
                        for k, v in dataMain["license"].items():
                            if k not in licenseFilter:
                                embedMain.add_field(
                                    name=f"License {k}", value=f"[{v}]", inline=True
                                )
                        for k1, v1 in dataMain["permissions"].items():
                            embedMain.add_field(
                                name=f"Permissions {k1}", value=f"[{v1}]", inline=True
                            )
                        embedMain.title = dataMain["name"]
                        embedMain.description = dataMain["description"]
                        embedMain.set_thumbnail(url=dataMain["owner"]["avatar_url"])
                        await ctx.respond(embed=embedMain)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, it seems like there is no repo named like that. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @githubUser.command(name="one")
    async def githubUserSearch(
        self, ctx, *, username: Option(str, "The username to search")
    ):
        """Returns info on a user in GitHub"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {githubAPIKey}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/users/{username}", headers=headers
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embedMain = discord.Embed()
                mainFilterEmbed = [
                    "url",
                    "followers_url",
                    "following_url",
                    "gists_url",
                    "starred_url",
                    "subscriptions_url",
                    "organizations_url",
                    "repos_url",
                    "events_url",
                    "received_events_url",
                    "name",
                    "bio",
                    "login",
                    "gravatar_id",
                    "avatar_url",
                    "plan",
                ]
                try:
                    if r.status == 404:
                        raise HTTPException
                    else:
                        for keys, value in dataMain.items():
                            if keys not in mainFilterEmbed:
                                embedMain.add_field(
                                    name=keys, value=f"[{value}]", inline=True
                                )
                        embedMain.title = f"{dataMain['login']} - {dataMain['name']}"
                        embedMain.description = dataMain["bio"]
                        embedMain.set_thumbnail(url=dataMain["avatar_url"])
                        await ctx.respond(embed=embedMain)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, it seems like there is no org named like that. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(GitHubV1(bot))
