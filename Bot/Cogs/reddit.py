from tkinter import *
from discord.ext import commands
import discord
import random
import sqlite3
import praw


# reddit login script
def redditkey():
    # saving information to database
    def save_information(redditid, redditsecret):
        conn = sqlite3.connect("reddit.db")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS saved_information (
            redditid text,
            redditsecret text);
            """
        )
        conn.commit()
        conn.execute(
            """INSERT INTO saved_information (redditid, redditsecret)
            VALUES (?, ?)""",
            (redditid, redditsecret),
        )
        conn.commit()
        conn.close()
        return (redditid, redditsecret)

    conn = sqlite3.connect("reddit.db")
    try:
        # attempt login discord
        cur = conn.cursor()
        cur.execute("SELECT redditid, redditsecret FROM saved_information;")
        saved_information_tuple = cur.fetchone()
        conn.close()
        return (saved_information_tuple[0], saved_information_tuple[1])
    except sqlite3.Error:
        # upon error start ui
        # window
        tkWindow = Tk()
        tkWindow.geometry("400x150")
        tkWindow.title("reddit.py by Chisaki-Dev")
        # redditid label and text entry box
        redditidLabel = Label(tkWindow, text="redditid").grid(row=0, column=0)
        redditid = StringVar()
        redditidEntry = Entry(tkWindow, textvariable=redditid).grid(row=0, column=1)

        # redditsecret label and text entry box
        redditsecretLabel = Label(tkWindow, text="redditsecret").grid(row=1, column=0)
        redditsecret = StringVar()
        redditsecretEntry = Entry(tkWindow, textvariable=redditsecret).grid(
            row=1, column=1
        )

        # startup button
        startupButton = Button(
            tkWindow,
            text="start reddit.py",
            command=lambda: [
                tkWindow.withdraw(),
                save_information(redditid.get(), redditsecret.get()),
            ],
        ).grid(row=6, column=1)

        tkWindow.mainloop()


cred = redditkey()
redditapi = praw.Reddit(
    client_id=cred[0],
    client_secret=cred[1],
    # the user_agent just identifies to reddit what browser it's connecting from.
    user_agent="Discord",
    # asyncpraw is causing issues and will be worked upon
    check_for_async=False,
)


class reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme", help="finds a meme")
    async def meme(self, ctx):
        searchtopics = [
            " ",
            "dank",
            "anime",
            "christian",
            "tech ",
            "funny ",
            "coding ",
            "reddit ",
            "music ",
            "manga ",
            "school ",
            "relatable ",
        ]
        searchterm = random.choice(searchtopics) + "memes"
        await ctx.invoke(self.bot.get_command("reddit"), search=searchterm)

    @commands.command(name="transmeme", help="finds a trans related meme")
    async def transmeme(self, ctx):
        # Tried to watch onetopic in order to figure out the different subs
        searchtopics = [
            " ",
            " trans ",
            " egg_irl ",
            " traaaaaaannnnnnnnnns ",
            " GaySoundsShitposts ",
            " Bisexual ",
            " Bi_IRL ",
            " ActualLesbians ",
            " SapphoAndherFriend",
        ]
        searchterm = random.choice(searchtopics)
        await ctx.invoke(self.bot.get_command("reddit"), search=searchterm)

    @commands.command(name="reddit", help="browses on reddit")
    async def reddit(self, ctx, *, search: str):
        original_search = search
        try:
            if "r/" in search:
                # treat as subreddit
                search = search.split("/")
                sub = search[1]
                search = "all"
            else:
                # treat as general search
                sub = "all"
            # query reddit for posts
            redditquery = redditapi.subreddit(sub).search(search)
            # looks for a suitable posts
            posts = [
                post
                for post in redditquery
                if ".jpg" in post.url
                or ".png" in post.url
                or ".gif" in post.url
                and not post.over_18
            ]
            # ensuring random post
            post = random.choice(posts)
            # finding a suitable post
            submission = post
            # discord embed setup
            reddit_embed = discord.Embed()
            reddit_embed.description = f"{self.bot.user.name} found this post in r/{submission.subreddit.display_name} by {submission.author.name} when searching {original_search}"
            reddit_embed.set_image(url=submission.url)
            await ctx.send(embed=reddit_embed)
            return
        except:
            await ctx.send(
                f"There was an error, this is likely caused by a lack of posts found in the query {original_search}. Please try again."
            )


def setup(bot):
    bot.add_cog(reddit(bot))
