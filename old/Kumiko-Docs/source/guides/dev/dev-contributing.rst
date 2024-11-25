Dev Contributing Guide
======================

We are glad that you're willing to contribute to this project. 
We are usually very lenient and relaxed with the submissions of PRs, and Issues reports. 
But there are some stuff that you need to know before contributing.

Note to new contributors
---------------------------

When you contribute to this project, you are subject to the `Code of Conduct <https://github.com/No767/Kumiko/blob/dev/CODE_OF_CONDUCT.md>`_. 
Any violations of the Code Of Conduct will be handled as stated. Read the contributing guide. 
**Support is not given if you didn't bother reading the documentation for setting up any of the requirements, or if you didn't bother to read the contributing guide.**

Before Starting
----------------

Make suer to read these guides listed below (read them in order):

- :doc:`requirements`
- :doc:`setup`

Coding Style
-------------

Variables
^^^^^^^^^^

.. note::

    If these standards are not met, more than likely the PR will not get merged and be rejected.

Kumiko follows PEP8 naming conventions and standards. There is no question about it. 
The only exception is with the naming of some of the project directories, which is kept that way in order not to break the project.

Ruff is used to lint and check whether the code meets PEP8 standards or not. In order to learn more about PEP8, see `this <https://realpython.com/python-pep8/>`_ guide.

Static Typing (aka Type Hinting)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the most part, Kumiko's codebase is fully typed. Pyright in this case is used to check whether the code is typed and meets standards or not. 
If you are using VS Code, then you can enable this on VSC by clicking on the ``{}`` icon in your status bar.

Formatting
^^^^^^^^^^^

Kumiko uses pre-commit hooks to format all of the code. 
The formatters used are Black, AutoFlake, and isort. 
Make sure run ``git add --all`` before committing to add all of the files. 
More than likely you'll need to commit twice due to the formatting that pre-commit does afterwards.

Docstrings
^^^^^^^^^^^

Just like how major programs are documented, the libraries that are custom made for Kumiko also have to be documented. 
The current standard for this project is to use `Google's Docstring Guide <https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings>`_. 
A handy VS Code extension that should be used is the `autoDocstring <https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring>`_ extension. 
By default it will generate the docstring in the Google format. Docstrings should be used on all coroutines and methods (excluding cogs), and on classes as well. 

Google, Numpy, and Sphinx docstrings are also supported for commands. Kumiko is documented w/ Google docstrings, so please make sure to use that format.

Example Cog:

.. code-block:: python

    import discord
    from discord.ext import commands
    from discord.ext.commands import Context, Bot

    class MyCog(commands.Cog):
        """An example cog for demo purposes"""
        def __init__(self, bot: Bot):
            self.bot = bot

        @commands.hybrid_command(name="hello")
        async def my_command(self, ctx: Context):
            """This is an example of a description for a slash command"""
            await ctx.send(f"Hello {ctx.user.name}!")

    async def setup(bot: Bot):
        await bot.add_cog(MyCog(bot))

Python Version Support
----------------------

Kumiko's codebase is written to keep compatibility for Python versions 3.8 - 3.11. 
Generally speaking, a Python version is supported until it's EOL (when the security support ends).

When a new version of Python releases, support for that version cannot be added 
**until the next patch version of that release** or until all packages and codebase internally support that new release. 
This means support for Python 3.12 for example, will not be included until Python 3.12.1 releases.

When writing code for this project, you must keep in mind to ensure that your code is compatible for versions 3.8 - 3.11. 
If said code is not compatible, then it will not be merged.

GitHub Contributing Guidelines
-----------------------------------

Issue and Feature Requests Reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If there is an issue or a feature you want to be added, use the built-in GitHub issue tracker. 
Though a system like Jira could be used, it would be more efficient to just use the issue tracker that GitHub provides. 

- If submitting a issue report, follow the template. Duplicates will not receive support
- If submitting a feature request, follow the template as well. As with issue reports, duplicate requests will not receive support

Git Commit Styleguides
^^^^^^^^^^^^^^^^^^^^^^^

- If updating any other files that aren't project files or not important (stuff like README.md, contributing.md, etc), add the [skip ci] label in the front
- With each new commit, the message should be more or less describing the changes. Please don't write useless commit messages...
- If releasing tags, have it in this style. ``Release: v[version number]``, ``Update: v[version number]``, and ``Fix: v[version number]``. Release is a major release. This means it bumps from 1.0.0 to 2.0.0. Minor means it bumps up the version from 1.4 to 1.5 for example. And fix just applies a patch, which would be 1.4.1 to 1.4.2.

Source Control Branching Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: /_static/gitflow.svg
   :align: center
   :width: 800

The source control branching model used in this project is the standard `Gitflow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`_ workflow. 
An example of what the Gitflow model looks like can be seen on the example above. 
In this case, the stable branch that has production code is the ``master`` branch, and only I (Noelle) will make PRs to that branch for production releases. 
The ``dev`` branch serves to host unstable or in-development code, where the code may be subject to breakage.

If you want to contribute to this project, then you will need to fork the ``dev`` branch, and add your contributions there. 
Once you feel like your code is ready to be merged, you can make a PR to the current dev branch and 
I will review the code in order to give feedback and to judge if the code meets standards or not. 
If the code meets the standards and is approved by me, then either within 24 hours or less, 
I will merge the code into the dev branch, and thus your code has now become a part of the project and future releases.

Releasing Tags
^^^^^^^^^^^^^^^

In order to automate the release system, you have to make sure that in order to use it, the git commit message must be done correctly. 
Only use this if there is a new update that is ready to be released. 
Kumiko uses `SemVer <https://semver.org/>`_  as the standard for versioning. Here's a table that should help with explaining this:

 =============================================================== ===================== 
                Type of Release, Update, or Patch                       Example        
 =============================================================== ===================== 
  Major Release (For updates that are not backwards compatible)   ``Release: v2.0.0``  
    Minor Release (For updates that are backwards compatible)     ``Update: v2.5.0``   
   Patch Release (For critical security patches and bug fixes)      ``Fix: v2.5.1``    
 =============================================================== ===================== 
