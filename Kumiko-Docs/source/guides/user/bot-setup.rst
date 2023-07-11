Bot Setup
================

This guide provides the steps for setting up a testing bot. This testing bot should only be used for development purposes, or for trying out a self hosted version of Kumiko. **DO NOT RUN THESE BOTS IN PRODUCTION**


1. Create a new application at https://discord.com/developers/applications

    .. figure:: /_static/1-Getting-Bot.png
        :alt: Create a new application

2. Click on the "Bot" tab and click "Add Bot"

    .. figure:: /_static/2-Create-Bot-Page.png
        :alt: Add a bot

3. Click "Yes, do it!". Optionally if you have 2FA enabled, you'll need to enter in your MFA token.

    .. figure:: /_static/3-Auth-Bot-Creation.png
        :alt: Confirm bot creation

4. Ensure that the intents shown in the pink square are enabled. ``message_content`` intents are required for the bot to function.

    .. figure:: /_static/4-Ensure-Intents-Are-Enabled.png
        :alt: Enable intents

5. Copy the bot token

    .. figure:: /_static/5-Copy-Token.png
        :alt: Copy bot token

6. Now paste this token in the ``.env`` file located in ``Bot/.env``. If you are using the Docker image for Kumiko, put it in the ``.env`` file located in the root of the repo.

    .. code-block:: bash
    
        DEV_BOT_TOKEN=YOUR_TOKEN_HERE