===
FAQ
===

This is a list of frequently asked questions. 
If you have a question that is not answered here, 
feel free to submit one via pull requests or to suggest one.

Slash Commands
==============

Questions regarding slash commands and how they operate in ``discord.py``.

Where Are The Slash Commands?
-----------------------------

Unlike other frameworks, discord.py **does not** automatically sync slash commands
for you (as slash commands need to be synced to Discord and are handled by them).
As a result, you'll need to manually sync your commands using the included 
`sync command <https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html>`_.
It is strongly recommended you read what the different options the command offers.

For example, in order to sync your commands, you would run a command in your Discord client
such as the following:

.. code-block::

    r>sync

To see details information on why the practice of automatically syncing commands is bad,
see `this gist <https://gist.github.com/No767/e65fbfdedc387457b88723595186000f>`_ for more.

.. note::

    If you do not understand what is syncing, 
    please read the `syncing guide <https://gist.github.com/No767/e65fbfdedc387457b88723595186000f#a-primer-on-syncing>`_.