# Advanced Discord Dmall

## ❗ Required libraries installation
Run in cmd:
```bash
pip install -r requirements.txt
```

## 📝 Config file info
- botConfig:
  - `botToken` -> Discord Bot Token
  - `botStatus` -> Discord Bot Status 
  - `botAccess` -> Discord User's ID's who can use Bot commands
- dmallConfig:
  - onReady -> true / false:
    - If `onReady` is true, The Bot will dmall ALL severs after main.py file is started.
  - onGuildJoin -> true / false:
    - If `onGuildJoin` is true, The Bot will DM the guild it has been added to.
  - onMemberJoin -> true / false:
    - If `onMemberJoin` is true, The Bot will send a DM to new server members.
  - onlineOnly -> true / false:
    - If `onlineOnly` is true, The Bot will send DMs only to users who are online, idle, or in "Do Not Disturb" status.
  - embed -> true / false:
    - If `embed` is true, The Bot will send messages as embedded content.
  - content -> true / false:
    - If `content` is true, The Bot will send plain text messages.
  - button -> true / false:
    - If `button` is true, The Bot will add a button to the DM message.

## ⭐ Dmall Message Parameters
Use the following message parameters to customize your DMall messages:

1. `{member.mention}` -> Mentions the member.
2. `{member.name}` -> Returns the member's name.
3. `{guild}` -> Returns the guild name from which the message was sent.
4. `{guild.id}` -> Returns the guild ID from which the message was sent.

## 🤖 Bot commands:
1. `!message` - Sends dmall message in author's DMs.
2. `!pfp < newBotPfp >` - Changes bot avatar.
3. `!rename < newBotName >` - Changes bot name. 
