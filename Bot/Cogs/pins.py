import asyncio
import datetime
from io import BytesIO
from typing import Dict, Optional

import orjson
from discord import File, Member, PartialEmoji, User, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.pins import (
    createPin,
    editPin,
    formatOptions,
    getAllPins,
    getOwnedPins,
    getPinInfo,
    getPinText,
)
from Libs.ui.pins import CreatePin, DeletePinView, PinEditModal, PinPages, PurgePinView
from Libs.utils import ConfirmEmbed, Embed, PinName, get_or_fetch_member
from typing_extensions import Annotated


class Pins(commands.Cog):
    """Pin text for later retrieval"""

    def __init__(self, bot: KumikoCore):
        self.bot = bot
        self.pool = self.bot.pool
        self._reserved_tags_being_made: Dict[int, set[str]] = {}

    def is_tag_being_made(self, guild_id: int, name: str) -> bool:
        try:
            being_made = self._reserved_tags_being_made[guild_id]
        except KeyError:
            return False
        else:
            return name.lower() in being_made

    def add_in_progress_tag(self, guild_id: int, name: str) -> None:
        tags = self._reserved_tags_being_made.setdefault(guild_id, set())
        tags.add(name.lower())

    def remove_in_progress_tag(self, guild_id: int, name: str) -> None:
        try:
            being_made = self._reserved_tags_being_made[guild_id]
        except KeyError:
            return

        being_made.discard(name.lower())
        if len(being_made) == 0:
            del self._reserved_tags_being_made[guild_id]

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f4cc")

    @commands.guild_only()
    @commands.hybrid_group(name="pins", fallback="get")
    @app_commands.describe(name="Pin to get")
    async def pins(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ):
        """Pin text for later retrieval"""
        pinText = await getPinText(ctx.guild.id, name, self.bot.pool)  # type: ignore
        if isinstance(pinText, list):
            await ctx.send(formatOptions(pinText) or ".")
            return
        await ctx.send(pinText or ".")

    @commands.guild_only()
    @pins.command(name="create")
    async def createPin(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        content: Annotated[str, commands.clean_content],
    ) -> None:
        """Create a pin"""

        if len(content) > 2000:
            await ctx.send("The pin content is too long. The max is 2000 characters")
            return

        await createPin(ctx, self.pool, name, content)

    @commands.guild_only()
    @pins.command(name="make", aliases=["add"])
    async def makePin(self, ctx: commands.Context) -> None:
        """Interactively creates a tag for you"""
        if ctx.interaction is not None:
            createPinModal = CreatePin(self.pool)
            await ctx.interaction.response.send_modal(createPinModal)
            return

        await ctx.send("What would you like the pin's name to be?")

        converter = PinName()
        original = ctx.message

        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel

        try:
            name = await self.bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took long. Goodbye.")
            return

        try:
            ctx.message = name
            name = await converter.convert(ctx, name.content)
        except commands.BadArgument as e:
            await ctx.send(f'{e}. Redo the command "{ctx.prefix}pins make" to retry.')
            return
        finally:
            ctx.message = original

        if self.is_tag_being_made(ctx.guild.id, name):  # type: ignore
            await ctx.send(
                "Sorry. This pins is currently being made by someone. "
                f'Redo the command "{ctx.prefix}pins make" to retry.'
            )
            return

        query = """SELECT 1 FROM pin WHERE guild_id=$1 AND LOWER(name)=$2;"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, ctx.guild.id, name.lower())  # type: ignore
            if row is not None:
                await ctx.send(
                    "Sorry. A pins with that name already exists. "
                    f'Redo the command "{ctx.prefix}pins make" to retry.'
                )
                return None

        self.add_in_progress_tag(ctx.guild.id, name)  # type: ignore
        await ctx.send(
            f"Neat. So the name is {name}. What about the pin's content? "
            f"**You can type {ctx.prefix}abort to abort the pin make process.**"
        )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=300.0)
        except asyncio.TimeoutError:
            self.remove_in_progress_tag(ctx.guild.id, name)  # type: ignore
            await ctx.send("You took too long. Goodbye.")
            return

        if msg.content == f"{ctx.prefix}abort":
            self.remove_in_progress_tag(ctx.guild.id, name)  # type: ignore
            await ctx.send("Aborting.")
            return
        elif msg.content:
            clean_content = await commands.clean_content().convert(ctx, msg.content)
        else:
            # fast path I guess?
            clean_content = msg.content

        if msg.attachments:
            clean_content = f"{clean_content}\n{msg.attachments[0].url}"

        if len(clean_content) > 2000:
            await ctx.send("Pin content is a maximum of 2000 characters.")
            return

        try:
            await createPin(ctx, self.pool, name, clean_content)
        finally:
            self.remove_in_progress_tag(ctx.guild.id, name)  # type: ignore

    @commands.guild_only()
    @pins.command(name="info")
    @app_commands.describe(name="Pin name to search")
    async def pinInfo(
        self, ctx: commands.Context, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Provides info about a pin"""
        pinInfo = await getPinInfo(ctx.guild.id, name, self.pool)  # type: ignore
        if pinInfo is None:
            await ctx.send("Pin not found.")
            return
        embed = Embed()
        embed.title = pinInfo["name"]
        embed.timestamp = pinInfo["created_at"].replace(tzinfo=datetime.timezone.utc)
        embed.set_footer(text="Pin created at")
        embed.add_field(name="Owner", value=f"<@{pinInfo['author_id']}>")
        embed.add_field(
            name="Aliases", value=",".join(pinInfo["aliases"]).rstrip(",") or "None"
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @pins.command(name="delete")
    @app_commands.describe(name="Pin name to delete")
    async def deletePin(
        self, ctx: commands.Context, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Deletes a pin. You can only delete your own."""
        view = DeletePinView(self.pool, name)
        embed = ConfirmEmbed()
        embed.description = f"Do you want to delete the pin: {name}?"
        await ctx.send(embed=embed, view=view)

    @commands.guild_only()
    @pins.command(name="alias")
    @app_commands.describe(name="Pin name to alias", alias="The new name to alias")
    async def aliasPin(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        alias: Annotated[str, commands.clean_content],
    ) -> None:
        """Alias a pin. You can only alias your own pins

        Pin aliases are not checked for others. You have to provide with the exact spelling (case insensitive) as what the alias is
        """
        # later we need to validate the max that the aliases can have
        insertQuery = """
        UPDATE pin_lookup SET aliases = ARRAY_APPEND(aliases, $2)
        WHERE guild_id=$3 AND id=(SELECT id FROM pin WHERE LOWER(pin.name)=$1)
        AND (NOT $2 = ANY(aliases) OR aliases IS NULL);
        """
        async with self.pool.acquire() as conn:
            status = await conn.execute(insertQuery, name, alias, ctx.guild.id)  # type: ignore
            if status[-1] == "0":
                await ctx.send(
                    f"A pin with the name of `{name}` does not exist or there is an aliases with the name `{alias}` set already."
                )
                return
            else:
                await ctx.send(f"Successfully aliased `{name}` to `{alias}`")

    @commands.guild_only()
    @pins.command(name="unalias")
    @app_commands.describe(name="Pin name to unalias", alias="The alias to remove")
    async def unalias(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        alias: Annotated[str, commands.clean_content],
    ) -> None:
        """Unalias a pin. You can only unalias your own pins"""
        # later we need to validate the max that the aliases can have
        insertQuery = """
        UPDATE pin_lookup SET aliases = ARRAY_REMOVE(aliases, $2)
        WHERE guild_id=$3 AND id=(SELECT id FROM pin WHERE LOWER(pin.name)=$1)
        AND $2 = ANY(aliases);
        """
        async with self.pool.acquire() as conn:
            status = await conn.execute(insertQuery, name, alias, ctx.guild.id)  # type: ignore
            if status[-1] == "0":
                await ctx.send(
                    f"A pin with the name of `{name}` does not exist or there are no aliases set."
                )
                return
            else:
                await ctx.send(f"Successfully removed alias `{alias}` from `{name}`")

    @commands.guild_only()
    @pins.command(name="search")
    @app_commands.describe(name="Pin name to search")
    async def search(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ):
        """Searches for a tag.

        Aliases are not counted towards searches (meaning that they will not show up in the search results). The query must be at least 3 characters.
        """
        if len(name) < 3:
            await ctx.send("The query must be at least 3 characters.")
            return

        sql = """SELECT name, id
                 FROM pin_lookup
                 WHERE guild_id=$1 AND name % $2
                 ORDER BY similarity(name, $2) DESC
                 LIMIT 100;
              """
        async with self.pool.acquire() as conn:
            records = await conn.fetch(sql, ctx.guild.id, name)  # type: ignore

        # The reason why this is outside of the scope is that since the session can be long, we want to release the conn back into the pool once done
        # This will essentially prevent the conn from being stalled by a bunch of searches
        if records:
            pages = PinPages(entries=records, per_page=20, ctx=ctx)
            await pages.start()
        else:
            await ctx.send("No pins found")

    @commands.guild_only()
    @pins.command(name="edit")
    @app_commands.describe(
        name="Pin to edit", content="The new content to edit the pin with"
    )
    async def edit(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        content: Annotated[Optional[str], commands.clean_content] = None,
    ) -> None:
        """Edits a pin. Aliases cannot be used as the name to search."""
        if content is None:
            if ctx.interaction is None:
                raise commands.BadArgument("Missing content to edit tag with")
            else:
                query = "SELECT content FROM pin WHERE LOWER(name)=$1 AND guild_id=$2 AND author_id=$3"
                async with self.pool.acquire() as conn:
                    row: Optional[tuple[str]] = await conn.fetchrow(query, name, ctx.guild.id, ctx.author.id)  # type: ignore
                    if row is None:
                        await ctx.send(
                            "Could not find a tag with that name, are you sure it exists or you own it?",
                            ephemeral=True,
                        )
                        return
                modal = PinEditModal(self.pool, row[0])
                await ctx.interaction.response.send_modal(modal)
                return

        if len(content) > 2000:
            await ctx.send("Ping content can only be up to 2000 characters")
            return

        sqlRes = await editPin(ctx.guild.id, ctx.author.id, self.pool, name, content)  # type: ignore
        if sqlRes[-1] == "0":
            await ctx.send("Could not edit the pin. Are you sure you own it?")
        else:
            await ctx.send("Successfully edited pin")

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @pins.command(name="dumps")
    async def dumps(self, ctx: commands.Context) -> None:
        """Dumps all tags in your guild into a JSON file"""
        await ctx.defer()
        result = await getAllPins(ctx.guild.id, self.pool)  # type: ignore
        buffer = BytesIO(
            orjson.dumps([dict(row) for row in result], option=orjson.OPT_INDENT_2)
        )
        await ctx.send(
            content="Finished exporting all pins in your guild!",
            file=File(fp=buffer, filename="export.json"),
        )

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @pins.command(name="all")
    async def all(self, ctx: commands.Context) -> None:
        """Lists all pins in your guild"""
        rows = await getAllPins(ctx.guild.id, self.pool)  # type: ignore
        if rows:
            pages = PinPages(entries=rows, per_page=20, ctx=ctx)
            await pages.start()
        else:
            await ctx.send("The server does not have any pins")

    @commands.guild_only()
    @pins.command(name="list")
    @app_commands.describe(member="The member or yourself to list pins from")
    async def list(self, ctx: commands.Context, member: User = commands.Author) -> None:
        """Lists all pins from a member or yourself"""
        rows = await getOwnedPins(member.id, ctx.guild.id, self.pool)  # type: ignore
        if len(rows) == 0:
            await ctx.send("The member does not have any pins")
            return
        else:
            pages = PinPages(entries=rows, per_page=20, ctx=ctx)
            await pages.start()

    @commands.guild_only()
    @pins.command(name="purge")
    async def purge(self, ctx: commands.Context) -> None:
        """Purges all pins that you own in the server"""
        view = PurgePinView(self.pool)
        embed = ConfirmEmbed()
        embed.description = (
            "Are you sure you want to delete all pins that you own in the server?"
        )
        await ctx.send(embed=embed, view=view)

    @commands.guild_only()
    @pins.command(name="claim")
    @app_commands.describe(name="Name of the pin. Aliases are supported")
    async def claim(
        self, ctx: commands.Context, *, name: Annotated[PinName, commands.clean_content]
    ) -> None:
        """Claims a pin that you do not own. Aliases will be retained"""
        query = """
        SELECT pin.id, pin.author_id
        FROM pin_lookup
        INNER JOIN pin ON pin.id = pin_lookup.pin_id
        WHERE pin_lookup.guild_id = $1 AND LOWER(pin.name) = $2;
        """
        row = await self.pool.fetchrow(query, ctx.guild.id, name)  # type: ignore
        if row is None:
            await ctx.send("Could not find a pin with that name or alias")
            return

        member = await get_or_fetch_member(ctx.guild, dict(row)["author_id"])  # type: ignore

        if member is not None:
            await ctx.send("The pin is already owned by someone else")
            return

        query = """
        WITH pin_update AS (
        UPDATE pin_lookup
        SET owner_id = $3
        WHERE pin_lookup.guild_id = $1 AND LOWER(pin_lookup.name) = $2
        RETURNING pin_id
        )
        UPDATE pin
        SET author_id = $3
        WHERE pin.guild_id = $1 AND id = (SELECT id FROM pin_update);
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, ctx.guild.id, name, ctx.author.id)  # type: ignore

        await ctx.send("Successfully claimed the pin")

    @commands.guild_only()
    @pins.command(name="transfer")
    @app_commands.describe(
        member="The member to transfer the pin to", pin="The pin's name to transfer"
    )
    async def transfer(
        self, ctx: commands.Context, member: Member, *, pin: Annotated[str, PinName]
    ) -> None:
        """Transfers a pin to another member. Once transferred, you can't get it back."""
        if member.bot:
            await ctx.send("You can't transfer a pin to a bot")
            return
        query = """
        SELECT pin.id, pin.author_id
        FROM pin_lookup
        INNER JOIN pin ON pin.id = pin_lookup.pin_id
        WHERE pin_lookup.guild_id = $1 AND LOWER(pin.name) = $2;
        """
        row = await self.pool.fetchrow(query, ctx.guild.id, pin)  # type: ignore
        if row is None:
            await ctx.send("Could not find a pin with that name or alias")
            return

        # This can be removed later if we want to allow transferring to yourself
        if dict(row)["author_id"] == ctx.author.id:
            await ctx.send("You can't transfer the pin back to yourself")
            return

        query = """
        UPDATE pin
        SET author_id = $3
        WHERE pin.guild_id = $1 AND pin.name = $2;
        """
        lookupQuery = """
        UPDATE pin_lookup
        SET owner_id = $3
        WHERE pin_lookup.guild_id = $1 AND pin_lookup.name = $2;
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, ctx.guild.id, pin.lower(), member.id)  # type: ignore
                await conn.execute(lookupQuery, ctx.guild.id, pin.lower(), member.id)  # type: ignore

        await ctx.send(
            f"Successfully transfer the pin `{pin.lower()}` to {member.mention}"
        )


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Pins(bot))
