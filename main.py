import discord
import os
import bot_data
import requests
from io import BytesIO
import sqlite3
import urllib.parse
import re

client = discord.Client()
conn = sqlite3.connect('legends.db')
c = conn.cursor()

print('legends.db connected..')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
        """
        Whenever bot receives a message, it uses this method to perform an action

        ACTIONS
        - Greeting -> Respond with `Hello` when user enters $hello or $hi
        - Help -> Repond with a message that lists all commands when user enters $help or $commands
        - Theorems -> Repond with a list of all theorems in the system when user enters $theorems or something
        - Theorem -> Repond with a theorem solution image when user enters $theorem number
        """
        # HOUSE KEEPING
        # ===========================================================================================================
        # ignore messages from the bot
        if message.author == client.user:
                return
       
        if message.content.startswith('%%admin%%'):
            
            command = message.content.lower().split('\"')
            print(command)

            if 'add'in command[0]:

                if len(command) < 5:
                    return await message.channel.send('Failed! Command format: %%admin%% add \"Question text\" \"Link to Question Answer\"')

                try: 
                    ques = command[1]
                    link = command[3]

                    query = c.execute('INSERT INTO theorems(q, l) VALUES (?, ?)', (ques, link))
                    conn.commit()

                    return await message.channel.send('Success!')

                except:
                    return await message.channel.send("Some error occured! Try again, or contact @ghoul")

            return

        # Messages should start with $
        if not message.content.startswith('$') and not message.content.startswith('='):
                
                author = message.author

                query = c.execute('SELECT msgs FROM legends WHERE uid=?', (author.id, ))
                messages_sent = query.fetchone()
                
                if messages_sent is None:
                        c.execute('INSERT INTO legends VALUES(?, ? , ?)', (author.id, author.display_name, 1))
                        conn.commit()
                else:
                        c.execute('UPDATE legends SET msgs = ? WHERE uid = ?', (int(messages_sent[0]) + 1, author.id))
                        conn.commit()
                return
        
        # Greetings people
        if message.content.lower().startswith('$hello') or message.content.lower().startswith('$hi'):
                return await message.channel.send('Hello!')
        # ===========================================================================================================

        
        # Help 
        # ===========================================================================================================
        if message.content.lower().startswith('$help') or message.content.lower().startswith('$commands') :
                return await message.channel.send(bot_data.help)
        # ===========================================================================================================
        
        
        # THEOREMS 
        # ===========================================================================================================
        if message.content.lower().startswith('$theorems') or message.content.lower().startswith('$def') or message.content.lower().startswith('$definitions') or message.content.lower().startswith('$proofs'):
                all_theorems = ""

                query = c.execute('SELECT * FROM theorems')

                result = query.fetchall()

                for i in range(1, len(result) + 1):
                        all_theorems += f"{result[i - 1][0]}- {result[i - 1][1]}\n"

                all_theorems += "\nTo see solution of a theorem, use command `$theorem 1`, where `1` is the theorem number as listed above. Dont see a theorem listed above? Contact @Ghoul to add it!`"

                return await message.channel.send(all_theorems)

        if message.content.lower().startswith('$theorem') or message.content.lower().startswith('$th') or message.content.lower().startswith('$proof'):
                try: 
                        th_number = int(message.content.lower().split(' ')[1])

                        query = c.execute('SELECT * FROM theorems WHERE id=' + str(th_number))

                        result = query.fetchone()

                        response = requests.get(result[2])
                        img = BytesIO(response.content)

                        return await message.channel.send(file=discord.File(img, f'th_solution_{th_number + 1}.jpg'))
                
                except Exception:
                        return await message.channel.send('I can understand calc but I cannot understand you :disappointed_relieved:\nThere is either no question associated with `' + message.content + '` or the link expired. Contact `@Ghoul` if the link is expired')
        # ===========================================================================================================


        # Anime 
        # ===========================================================================================================
        if message.content.lower().startswith('$anime'):
                parts = re.split(' +', message.content.lower())
                
                if len(parts) == 1:
                    return await message.channel.send('Need anime advice? Go look for `@Allie`.Nah! I cannot defeat someone that great.') 

                search_type = parts[1]
                search_query = " ".join(parts[2:])

                url = f'https://api.jikan.moe/v3/search/{search_type}?q={urllib.parse.quote_plus(search_query)}'
                
                res = requests.get(url)
                json = res.json()

                if 'error' in json:
                        return await message.channel.send('Not found! retry :(')
                else:
                        url = json['results'][0]['url']
                        img = json['results'][0]['image_url'].split('?')[0]
                        name = ""

                        if search_type == 'character':
                                name = json['results'][0]['name']
                        else:
                                name = json['results'][0]['title']

                        return await message.channel.send(f"{name} -> {url}")
        # ===========================================================================================================


        # MATHS
        # ===========================================================================================================
        if message.content.lower().startswith('$maths') or message.content.lower().startswith('$mathshelp') or message.content.lower().startswith('=maths') or message.content.lower().startswith('=mathshelp'):
                result = "Any command that starts with `=` is treated as a maths solving command. Expressions should be in brackets and there should be no spaces in the entire expression. A command of the form `=operation expression` will give you the result of applying `operation` to the `expression`\n\n\n**Some Examples:**\n\n"
                result += "**Command**\t\t\t\t\t\t\t**Result**\n"
                for x, y in bot_data.maths:
                        result += x + "\t\t\t" + y + "\n"

                result += '\n\n`To find the area under a function, send the request as c:d|f(x) where c is the starting x value, d is the ending x value, and f(x) is the function under which you want the curve between the two x values.`\n\n'

                return await message.channel.send(result)

        if message.content.lower().startswith('='):
                operation = message.content.lower().split(' ')[0][1:]
                expression = re.split(' +', message.content.lower())[1]

                url = f'https://newton.now.sh/api/v2/{operation}/{urllib.parse.quote_plus(expression)}'
                res = requests.get(url)

                json = res.json()
                
                if 'error' in json:
                        result = json['error'] + '. Try adding brackets around all expressions and removing all spaces'
                else:
                        result = json['result']

                return await message.channel.send(result)
        # ===========================================================================================================


        # LEGENDS
        # ===========================================================================================================
        if message.content.lower().startswith('$legends'):
                query = c.execute('SELECT * FROM legends WHERE msgs > ? ORDER BY msgs DESC', (bot_data.LEGEND_BREAKPOINT, ))
                result = query.fetchall()
                
                legends = "*Name*\t\t\t*Messages*\n"
                for id, name, msgs in result:
                        legends += name + "\t\t\t" + str(msgs) + "\n"

                return await message.channel.send(f'**List of LEGENDS of the server:**\n\n{legends}\n\nHow to become a legend? Thats a secret!')
        # ==========================================================================================================
        
        if message.content.lower().startswith('$who') or message.content.lower().startswith('$admin'):
            return await message.channel.send('Looking for server admin? `@averykeen`. That\'s her! LEGEND!!')

        if message.content.lower().startswith('$ultralegend') or message.content.lower().startswith('anime sugges'):
            return await message.channel.send('Looking for anime advice? Looking for a LEGEND? Go find: `@Allie`')

        if message.content.lower().startswith('$feedback'):
            return await message.channel.send('Want to update the bot? Have a suggestion or bug? Feedback? Find `@Ghoul`')
        
client.run(os.environ['BOT_TOKEN'])
