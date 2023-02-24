# Getting the Discord Bot

First things first, you'll more than likely need a dev bot to run Kumiko. Luckily you'll find the steps below to help you on that

1. Create the app that will be needed for the bot. Once done, you should see the page as shown above

    ![images](../assets/getting-started-assets/create-app.png)


2. Now head done to the bot section, and click on the button that says "Add Bot". 
    
    ![yesyes](../assets/getting-started-assets/create-bot.png)

3. You'll see a pop-up that asks you if you want to create the bot. 
    
    ![ewom](../assets/getting-started-assets/allow-bot.png)

4. Make sure to have all 3 of the buttons enabled. Kumiko will need all 3 of them to work.
    
    ![intents](../assets/getting-started-assets/allow-intents.png)


5. You'll see a page just like the one above. We'll need access the the token for the bot, and the only way to do it is to reset the token.
    
    ![whyyy](../assets/getting-started-assets/reset-token.png)

6. Allow for the token to be reset. Note that if your account is hooked up with 2FA, it will ask you to enter your 2FA code. Go to your authenticator app and enter the code from the app.
    
    ![confirm](../assets/getting-started-assets/allow-reset-token.png)


7. Now click on the copy button and copy the token
    
    ![copytoken](../assets/getting-started-assets/copy-token.png)
    

8. Head back to the `Bot` directory, where the `.env` file is stored. Update the variable `Dev_Bot_Token` with the token you just copied. An example would look like this:

    ```bash
    Dev_Bot_Token = "my-discord-bot-token"
    ```
