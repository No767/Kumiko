# Contributing

We are glad that you're willing to contribute to this project. We are usually very lenient and relaxed with the submissions of PRs, and Issues reports. But there are some stuff that you need to know before contributing.

## Note to new contributors

When you contribute to this project, you are subject to the [Code of Conduct](./CODE_OF_CONDUCT.md). Any violations of the Code Of Conduct will be handled as stated. Read the contributing guide. **Support is not given if you didn't bother reading the documentation for setting up any of the requirements, or if you didn't bother to read the contributing guide.**

## Before Starting

Make sure to read these guides listed below (read them in order):

- [Installing-Requirements](./installing-requirements.md)
- [Getting the Discord Bot](./getting-discord-bot.md)
- [Database Setup](./database-setup.md)

## Getting Started
### Developing Kumiko

Once you have the discord bot up, there's a few things that needs to be done before development can begin. 

1. Follow the steps in [Installing Dependencies](#installing-dependencies) to get all of the dependencies installed.
2. Now create a shell that poetry needs. Run the following command:

    ```sh
    poetry shell
    ```

3. To run Kumiko, run the following command:

   ```sh
   make
   ```

   You could also run this command, which does the same thing:

   ```sh
   make run
   ```

   To stop Kumiko, hit Ctrl + C to kill the process. 

### Things to keep in mind

Make sure to always keep this in mind: Always add exception handling for Kumiko. And make sure it is done correctly. A poor example would be this:

   ```py
   try:
      async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
         async with session.get(url) as resp:
            data = await resp.content.read()
            dataMain = parser.parse(data, recursive=True)
            print(dataMain["data"]["children"][0]["data"]["title"]) # Doesn't exist within JSON data
   except Exception as e:
      await ctx.respond(e)
   ```
   But rather actually specify the exception that you want to handle.

   ```py

   try:
      async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
         async with session.get(url) as resp:
            data = await resp.content.read()
            dataMain = parser.parse(data, recursive=True)
            print(dataMain["data"]["children"][0]["data"]["title"]) # Doesn't exist within JSON data
   except ValueError:
      await ctx.respond("That item doesn't exist! Please try again")
   ```

## API Keys

Kumiko is built on top of Rin, and Kumiko requires some API keys. Here's a list of current services that require API keys:

- [GitHub](https://docs.github.com/en/rest/guides/basics-of-authentication)
- [Reddit](https://www.reddit.com/prefs/apps) (Get both the ID and Secret)
- [Tenor](https://developers.google.com/tenor/guides/quickstart#setup)
- [Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api) (Get the Bearer Token that supports both API v2 and v1.1)
- [YouTube](https://developers.google.com/youtube/registering_an_application)

## Docker Build System
All commits on the `dev` branch will be tagged with `edge` on Docker Hub and GHCR. These builds are dev builds, which means they are unstable and should be not used in an production environment. If you are interested in just testing out Kumiko, and are willing to deal with the instability, you can use the dev builds. Kumiko is built using Debian 11 as a base.

In short:

- If you want to use Kumiko in a production environment, use a versioned tag.
- If you want to test out Kumiko, use the `edge` tag.

## Coding Style
### Variables

Most of the code written uses camelCasing for variables, `PascalCasing` for classes, and `snake_casing` for args. To sum it up:

- `camelCasing` for variables
- `PascalCasing` for classes
- `snake_casing` for args
- `ALL_CAPS` for constants
- `kebab-casing` for files

### Formatting

Kumiko uses pre-commit hooks to format all of the code. Make sure run `git add --all` before committing to add all of the files. More than likely you'll need to commit twice due to the formatting that pre-commit does afterwards.

### Docstrings

Just like how major programs are documented, the libraries that are custom made for Kumiko also have to be documented. The current standard for this project is to use [Google's Docstring format](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings). A handy VS Code extension that should be used is the [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) extension. By default it will generate the docstring in the Google format. Docstrings should be used on all coroutines and methods (excluding cogs), and on classes as well. 

For Cogs, docstrings formats are not needed. All you need to do is to add a basic docstring and Pycord will pick it up.

Example Cog:

```py 
import discord
from discord.commands import slash_command
from discord.ext import commands

class MyCog(commands.Cog):
    """An example cog for demo purposes"""
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="hello")
    async def myCommand(self, ctx: discord.ApplicationContext):
        """This is an example of a description for a slash command"""
        await ctx.respond(f"Hello {ctx.user.name}!")

def setup(bot):
    bot.add_cog(MyCog(bot))
```
## GitHub Contributing Guidelines
### Issue and Feature Requests Reports

If there is an issue or a feature you want to be added, use the built-in GitHub issue tracker. Though a system like Jira could be used, it would be more efficient to just use the issue tracker that GitHub provides. 

- If submitting a issue report, follow the template. Duplicates will not receive support
- If submitting a feature request, follow the template as well. As with issue reports, duplicate requests will not receive support

### Git Commit Styleguides

- If updating any other files that aren't project files or not important (stuff like README.md, contributing.md, etc), add the [skip ci] label in the front
- With each new commit, the message should be more or less describing the changes. Please don't write useless commit messages...
- If releasing tags, have it in this style. `Release: v[version number]`, `Update: v[version number]`, and `Fix: v[version number]`. Release is a major release. This means it bumps from 1.0.0 to 2.0.0. Minor means it bumps up the version from 1.4 to 1.5 for example. And fix just applies a patch, which would be 1.4.1 to 1.4.2.

### Releasing Tags
In order to automate the release system, you have to make sure that in order to use it, the git commit message must be done correctly. Only use this if there is a new update that is ready to be released. Kumiko uses [SemVer](https://semver.org/) as the standard for versioning. Here's a table that should help with explaining this:

| Type of Release, Update, or Patch | Example |
|              :--:                 | :--:    | 
| Major Release (For updates that are not backwards compatible) | `Release: v2.0.0` | 
| Minor Release (For updates that are backwards compatible) | `Update: v2.5.0`|
| Patch Release (For critical security patches and bug fixes) | `Fix: v2.5.1` |

### Deploying a Production Release

All production releases of Kumiko are located in the `master` branch. To deploy a full production release, there has to be a few things:

- A full audit of the release needs to be done (every command, and tons of edge cases will be needed to be tested)
- Changelogs need to be written 
- Tests by the owner (Noelle should be the one who does this) to make sure it meets quality control and standards