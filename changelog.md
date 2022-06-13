# ✨ Rin V2.1.0 ✨

This update mainly focuses on properly handling exceptions (eg when a user puts in random data), and includes new services as well. 

## Changes

- Use Pysimdjson for handling JSON processing instead of Orjson
- Finished Blue Alliance API support
- Swap from Python docker images to process management with PM2 within an Ubuntu docker image
- Organize all commands into groups and subgroups
- Changed Jisho and other cogs to use a paginated embed instead
- Switched Pyenv to use 3.10.5 instead of 3.10.4
- Make Rin's logo trans (in support of pride month)
- Actually use pre-commit hooks instead of format workflow
- Update Help Command
- Actually specify which exceptions to handle 

## Additions
- GitHub API Support
- Full Blue Alliance API Support
- Full AniList API Support
- MangaDex Reader
- Custom exceptions package  
- /reddit egg_irl command (just feeds u with posts from r/egg_irl)
- Use Makefile for easier and faster setup + development
- Proper exception handling for all service cogs
- Guides for setup + development for Rin
- Task template 
- Actually use pre-commit hooks instead of format workflow

## Removals

- OpenAI API Support + Cog
- Format workflow (replaced with pre-commit hooks)
- Arch-Docker Dockerfile (Use Ubuntu-Docker instead)
- DeviantArt-Token-Refresher Cog
- All of the old patches (they apparently never worked...)

## Dependency Updates

- Bump py-cord from 2.0.0b5 to 2.0.0b7 (@dependabot[bot])
- Bump actions/setup-node from 3.1.0 to 3.1.1  (@dependabot[bot])
- Bump github/codeql-action from 1 to 2  (@dependabot[bot])
- Bump sqlalchemy from 1.4.35 to 1.4.36  (@dependabot[bot])
- Bump py-cord from 2.0.0b7 to 2.0.0rc1  (@dependabot[bot])
- Bump ujson from 5.2.0 to 5.3.0  (@dependabot[bot])
- Bump pysimdjson from 4.0.3 to 5.0.1  (@dependabot[bot])
- Bump lxml from 4.8.0 to 4.9.0  (@dependabot[bot])
- Bump sqlalchemy from 1.4.36 to 1.4.37  (@dependabot[bot])
- Bump orjson from 3.6.8 to 3.6.9  (@dependabot[bot])
- Bump orjson from 3.6.9 to 3.7.0  (@dependabot[bot])
- Bump orjson from 3.7.0 to 3.7.1   (@dependabot[bot])
- Bump actions/setup-node from 3.2.0 to 3.3.0  (@dependabot[bot])
- Bump orjson from 3.7.1 to 3.7.2  (@dependabot[bot])
- Bump actions/setup-python from 3 to 4 (@dependabot[bot])
