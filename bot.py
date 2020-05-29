import discord                          # Interacting with the Discord API
import asyncio                          # For creating async loops
import sys                              # For sending error messages to stderr and accessing argv

class Bot(discord.Client):
    def __init__(self, token):
        super().__init__()
        # The reason token is set here is so I can disconnect the bot and reconnect it without restarting the code or carrying the token around as a global
        self.token = token

    async def on_ready(self):
        # Start 
        pass
        
    async def send_embed(self, channel, content=None, title=None, footer=None, fields=None, image=None):
        # TODO: Add code to limit how much content can be sent to avoid exceeding byte limit
        if not title:
            title = self.user.name.capitalize()
        embed = discord.Embed(colour=discord.Colour(0x985F35), description=content, timestamp=datetime.utcnow())
        embed.set_author(name=title, icon_url=self.user.avatar_url)
        if fields:
            for field in fields: # field = [name, value, inline]
                embed.add_field(name=field[0], value=field[1], inline=field[2])
        if image:
            embed.set_image(url=image)
        if not footer:
            footer = f"{self.user.name.capitalize()} running in {channel.guild.name}"
        embed.set_footer(text=footer)
        await channel.send(embed=embed)

    async def start(self):
        print("Logging in...", end="\r")
        try:
            await self.login(self.token, bot=True)
            print("Logged in.   ")
            # check and load servers from screen
            # THIS IS NOT FUNCTIONALITY THAT MR PUKEKO IS INTENDED TO HAVE
            
            print("Connecting...", end="\r")
            await self.connect(reconnect=True)
        except discord.errors.LoginFailure:
            # Invalid token causes LoginFailure
            print("Invalid token provided", file=sys.stderr)
        except discord.errors.HTTPException as e:
            # HTTP error code raised
            print(f"HTTP request operation failed, status code: {e.status}", file=sys.stderr)
        except discord.errors.GatewayNotFound:
            # Unable to reach Discords API, the API being down will probably also mean no one will be online on the client to complain about the bot :^)
            print("Cannot reach Discord gateway, possible Discord API outage", file=sys.stderr)
        except discord.errors.ConnectionClosed:
            # Connection terminated after it was established, probably caused by internet dropping out, reconnect should take care of this
            print("The websocket connection has been terminated", file=sys.stderr)
        finally:
            # After the connection has ended, save the game servers just in case.
            # TODO: add saving as described above
            # THIS IS NOT FUNCTIONALITY THAT MR PUKEKO IS INTENDED TO HAVE
            pass

    async def disconnect(self):
        # Logout
        await self.logout()
        print("Disconnected.")

    def run(self):
        # Create the loop
        loop = asyncio.get_event_loop()
        try:
            # Connect to Discord using the token stored as one of the system's environment variables
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            # If a keyboard interupt is sent to the console log the bot out
            loop.run_until_complete(self.disconnect())
        finally:
            # Close the loop
            loop.close()
