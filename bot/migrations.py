import asyncio
import os
import re
import traceback
from functools import wraps
from pathlib import Path
from types import TracebackType
from typing import Optional, TypeVar

import asyncpg
import click
from discord.utils import utcnow
from libs.utils.config import KumikoConfig
from typing_extensions import Self

# If we can't load the configuration, then let's look for the environment variable
try:
    path = Path(__file__).parent / "config.yml"
    config = KumikoConfig(path)
    POSTGRES_URI = config["postgres_uri"]
except KeyError:
    POSTGRES_URI = os.environ["POSTGRES_URI"]


BE = TypeVar("BE", bound=BaseException)

REVISION_FILE = re.compile(r"(?P<kind>V)(?P<version>\d+)__(?P<description>.+).sql")

CREATE_MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS migrations (
    id SERIAL PRIMARY KEY,
    description TEXT,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc')
);
"""

GET_LATEST_VERSION = """
SELECT id FROM migrations
ORDER BY id DESC
LIMIT 1;
"""

INSERT_VERSION = """
INSERT INTO migrations (id, description)
VALUES ($1, $2);
"""


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


class Revision:
    __slots__ = ("kind", "version", "description", "file")

    def __init__(
        self, *, kind: str, version: int, description: str, file: Path
    ) -> None:
        self.kind: str = kind
        self.version: int = version
        self.description: str = description
        self.file: Path = file

    @classmethod
    def from_match(cls, match: re.Match[str], file: Path):
        return cls(
            kind=match.group("kind"),
            version=int(match.group("version")),
            description=match.group("description"),
            file=file,
        )


class Migrations:
    def __init__(self, *, no_conn: bool = False, migrations_path: str = "migrations"):
        self.no_conn = no_conn
        self.migrations_path = migrations_path
        self.root: Path = Path(__file__).parent
        self.revisions: dict[int, Revision] = self.get_revisions()
        self.ensure_path()

    async def __aenter__(self) -> Self:
        if self.no_conn is False:
            self.conn = await asyncpg.connect(POSTGRES_URI)
            self.version = await self.get_latest_version()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.conn.close()

    async def get_latest_version(self):
        record_version = await self.conn.fetchval(GET_LATEST_VERSION)
        if record_version is None:
            return 0
        return record_version

    def ensure_path(self) -> None:
        migrations_path = self.root / self.migrations_path
        migrations_path.mkdir(exist_ok=True)

    def get_revisions(self) -> dict[int, Revision]:
        result: dict[int, Revision] = {}
        for file in self.root.glob("migrations/*.sql"):
            match = REVISION_FILE.match(file.name)
            if match is not None:
                rev = Revision.from_match(match, file)
                result[rev.version] = rev

        return result

    def is_next_revision_taken(self) -> bool:
        return self.version + 1 in self.revisions

    @property
    def ordered_revisions(self) -> list[Revision]:
        return sorted(self.revisions.values(), key=lambda r: r.version)

    def create_revision(self, reason: str, *, kind: str = "V") -> Revision:
        cleaned = re.sub(r"\s", "_", reason)
        filename = f"{kind}{self.version + 1}__{cleaned}.sql"
        path = self.root / self.migrations_path / filename

        stub = (
            f"-- Revision Version: V{self.version + 1}\n"
            f"-- Revises: V{self.version}\n"
            f"-- Creation Date: {utcnow()} UTC\n"
            f"-- Reason: {reason}\n\n"
        )

        with open(path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(stub)

        return Revision(
            kind=kind, description=reason, version=self.version + 1, file=path
        )

    async def upgrade(self) -> int:
        ordered = self.ordered_revisions
        successes = 0
        async with self.conn.transaction():
            for revision in ordered:
                if revision.version > self.version:
                    sql = revision.file.read_text("utf-8")
                    await self.conn.execute(sql)
                    await self.conn.execute(
                        INSERT_VERSION, revision.version, revision.description
                    )
                    successes += 1

        self.version += successes
        return successes

    def display(self) -> None:
        ordered = self.ordered_revisions
        for revision in ordered:
            if revision.version > self.version:
                sql = revision.file.read_text("utf-8")
                click.echo(sql)


async def create_migrations_table() -> None:
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute(CREATE_MIGRATIONS_TABLE)
    await conn.close()


@click.group(short_help="database migrations util", options_metavar="[options]")
def main():
    # grouped database commands
    pass


@main.command()
@coro
async def init():
    """Initializes the database and runs all the current migrations"""
    await create_migrations_table()
    async with Migrations() as mg:
        try:
            applied = await mg.upgrade()
            click.secho(
                f"Successfully initialized and applied {applied} revisions(s)",
                fg="green",
            )
        except Exception:
            traceback.print_exc()
            click.secho(
                "failed to initialize and apply migrations due to error", fg="red"
            )


@main.command()
@click.option("--reason", "-r", help="The reason for this revision.", required=True)
@coro
async def migrate(reason: str):
    """Creates a new revision for you to edit"""
    async with Migrations() as mg:
        if mg.is_next_revision_taken():
            click.echo(
                "an unapplied migration already exists for the next version, exiting"
            )
            click.secho(
                "hint: apply pending migrations with the `upgrade` command", bold=True
            )
            return
        revision = mg.create_revision(reason)
        click.echo(f"Created revision V{revision.version!r}")


@main.command()
@coro
async def current():
    """Shows the current version"""
    async with Migrations() as mg:
        click.echo(f"Version {mg.version}")


@main.command()
@click.option("--sql", help="Print the SQL instead of executing it", is_flag=True)
@coro
async def upgrade(sql):
    """Upgrade to the latest version"""
    async with Migrations() as mg:
        if sql:
            mg.display()
            return

        try:
            applied = await mg.upgrade()
            click.secho(
                f"Applied {applied} revisions(s) (Current: V{mg.version})", fg="green"
            )
        except Exception:
            traceback.print_exc()
            click.secho("failed to apply migrations due to error", fg="red")


@main.command()
@click.option("--reverse", help="Print in reverse order (oldest first).", is_flag=True)
@coro
async def log(reverse):
    """Displays the revision history"""
    # We don't need to make an connection in ths case
    migrations = Migrations(no_conn=True)

    # Revisions is oldest first already
    revs = (
        reversed(migrations.ordered_revisions)
        if not reverse
        else migrations.ordered_revisions
    )
    for rev in revs:
        as_yellow = click.style(f"V{rev.version:>03}", fg="yellow")
        click.echo(f'{as_yellow} {rev.description.replace("_", " ")}')


if __name__ == "__main__":
    main()
