import discord
import asyncio
import json
import re
import bs4
from discord.ext import commands
from discord.ext.commands import Bot
from discord import File

with open('ticket/ticket.json', 'r') as f:
    count = json.load(f)


class ticket:
    def __init__(self, client):
        self.client = client

    async def on_guild_channel_update(self, before, after):
        if after.category_id in [473652853354004480]:
            if "are" in after.name[0:4]:
                areCategory = discord.utils.get(after.guild.categories, id=533147428715495434)
                await after.edit(category=areCategory, topic="ARK PvE Ticket")
                print("Ticket moved to PvE with ID: " + str(areCategory.id))
            elif "arp" in after.name[0:4]:
                arpCategory = discord.utils.get(after.guild.categories, id=533752291853860864)
                await after.edit(category=arpCategory, topic="ARK PvP Ticket")
                print("Ticket moved to PvP with ID: " + str(arpCategory.id))
            elif "ar6" in after.name[0:4]:
                ar6Category = discord.utils.get(after.guild.categories, id=561726806554574848)
                await after.edit(category=arpCategory, topic="ARK 6 Man Ticket")
                print("Ticket moved to 6 Man with ID: " + str(ar6Category.id))

    # new command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator', 'Tribe Reps', '6 Man Tribe Reps', 'VIP - Donators')
    async def new(self, ctx, *string):
        await ctx.message.delete()
        string = ' '.join(string)
        guild = ctx.message.guild
        newTickets = discord.utils.get(ctx.guild.categories, id=473652853354004480)
        ticketLogs = discord.utils.get(ctx.guild.channels, id=472494364241690644)

        if string is '':
            fail = discord.Embed(description=f"❌ You must include a ticket subject.", color=0xFF0000)
            message = await ctx.channel.send(embed=fail, delete_after=20)
        else:
            ticketID = int(count['ticket'])
            ticketID = ticketID + 1
            count['ticket'] = str(ticketID)
            with open('ticket/ticket.json', 'w') as f:
                json.dump(count, f)
            ticketName = str(ticketID).zfill(4)

            channel = await guild.create_text_channel(name=f'ticket {ticketName}', category=newTickets, reason='Ticket')

            m = re.search(r'\d{15}$', string)
            if m is None:
                await channel.set_permissions(ctx.message.author, read_messages=True, send_messages=True)
                message = await channel.send(f"{ctx.author.mention}")
            else:
                member = guild.get_member(int(string))
                await channel.set_permissions(member, read_messages=True, send_messages=True)
                message = await channel.send(f"{member.mention}")

            embed = discord.Embed(description=f"{ctx.author.mention} opened ticket {channel.mention}", color=0x00FF00)
            embed.add_field(name="Name", value=f"{channel.name.replace('_', '-')}")
            embed.add_field(name="Subject", value=f"{string}")
            try:
                message = await ticketLogs.send(embed=embed)
            except:
                print("Couldn't log ticket.")

            success = discord.Embed(description=f"✅ Success! Your new ticket can be found here: {channel.mention}", color=0x00FF00)
            message = await ctx.channel.send(embed=success, delete_after=20)

            embed = discord.Embed(description=f"Thank you, {ctx.author.mention}, for contacting the ARKADE team!\n\nWe will be with you as soon as possible, in the mean time please provide any information you can regarding your issue.", color=0xFF00FF)
            embed.add_field(name="Subject", value=string)
            message = await channel.send(embed=embed)

    # close command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def close(self, ctx, *string):
        await ctx.message.delete()
        m = re.search(r'\d{4}$', ctx.channel.name)
        if m is not None:
            string = ' '.join(string)
            guild = ctx.message.guild
            ticketLogs = discord.utils.get(ctx.guild.channels, id=472494364241690644)

            if string is '':
                fail = discord.Embed(description=f"❌ You must include a reason.", color=0xFF0000)
                message = await ctx.channel.send(embed=fail, delete_after=10)
            else:
                embed = discord.Embed(description=f"{ctx.author.mention} closed ticket {ctx.channel.mention}", color=0xFF0000)
                embed.add_field(name="Name", value=f"{ctx.channel.name.replace('_', '-')}")
                embed.add_field(name="Reason", value=f"{string}")
                transcript = await ctx.channel.history(limit=5000).flatten()
                transcript.reverse()
                ticketOwner = transcript[:1]
                for line in ticketOwner:
                    ownerID = line.content
                try:
                    owner = guild.get_member(int(''.join(c for c in ownerID if c.isdigit())))
                except:
                    owner = guild.get_member(147901548167430144)
                transcript = transcript[2:-1]

                with open('transcriptTemplate.html') as inf:
                    txt = inf.read()
                    soup = bs4.BeautifulSoup(txt, "html.parser")
                    messageBody = soup.find("div", {"class": "messages"})
                    for message in transcript:
                        header = soup.new_tag('h3')
                        timestr = str(message.created_at)
                        header.string = f"{message.author} - {timestr[0:19]}"
                        messageBody.append(header)
                        tempMessage = f"{message.content}"
                        tempMessage = tempMessage.split("\n")
                        for line in tempMessage:
                            messageBody.append(line)
                            br = soup.new_tag('br')
                            messageBody.append(br)

                with open("ticket/transcript.html", "w") as outf:
                    outf.write(str(soup))
                try:
                    message = await ticketLogs.send(embed=embed)
                    message = await ticketLogs.send(file=File('ticket/transcript.html'))
                except:
                    print("Couldn't log ticket")
                await ctx.channel.delete()

                message = await owner.send(embed=embed)
                message = await owner.send(file=File('ticket/transcript.html'))

                ticketName = ctx.channel.name
                try:
                    ticketCategory = str(ticketName[:3])
                    print(f"...{ticketCategory}...")
                    ticketName = ticketName[4:-5].replace('_', '-')
                    ticketList = ticketName.split('-')
                except:
                    print('Category not found.')

                for item in count[ticketCategory]:
                    for word in ticketList:
                        try:
                            if item['value'] == word:
                                try:
                                    item['count'] = str(int(item['count']) + 1)
                                    print(item['count'])
                                except:
                                    print("Unknown Error")
                        except:
                            print(word)
                with open('ticket/ticket.json', 'w') as f:
                    json.dump(count, f, indent=4)

        else:
            fail = discord.Embed(description=f"❌ This only works in a ticket!", color=0xFF0000)
            message = await ctx.channel.send(embed=fail)

    # rename command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def rename(self, ctx, *string):
        await ctx.message.delete()
        m = re.search(r'\d{4}$', ctx.channel.name)
        if m is not None:
            string = ' '.join(string)
            if string is '':
                fail = discord.Embed(description=f"❌ Name can't be empty.", color=0xFF0000)
                message = await ctx.channel.send(embed=fail, delete_after=10)
            else:
                await ctx.channel.edit(name=f'{string}-{ctx.channel.name[-4:]}')
                success = discord.Embed(description=f"✅ Success! New name is {ctx.channel.mention}", color=0x00FF00)
                message = await ctx.channel.send(embed=success, delete_after=10)
        else:
            fail = discord.Embed(description=f"❌ This only works in a ticket!", color=0xFF0000)
            message = await ctx.channel.send(embed=fail, delete_after=10)

    # add command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def add(self, ctx, string):
        await ctx.message.delete()
        m = re.search(r'\d{4}$', ctx.channel.name)
        if m is not None:
            guild = ctx.message.guild
            try:
                member = guild.get_member(int(string))
            except:
                fail = discord.Embed(description=f"❌ Invalid user ID.", color=0xFF0000)
                message = await ctx.channel.send(embed=fail, delete_after=10)
            if string is '':
                fail = discord.Embed(description=f"❌ Must specify a user ID.", color=0xFF0000)
                message = await ctx.channel.send(embed=fail, delete_after=10)
            else:
                await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
                message = await ctx.channel.send(f"{member.mention}")
                success = discord.Embed(description=f"✅ {member.mention} has been added.", color=0x00FF00)
                message = await ctx.channel.send(embed=success, delete_after=10)
        else:
            fail = discord.Embed(description=f"❌ This only works in a ticket!", color=0xFF0000)
            message = await ctx.channel.send(embed=fail, delete_after=10)

    # ticket commands
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def ticket(self, ctx, string=None):
        await ctx.message.delete()
        embed = discord.Embed(title="Ticket Stats", description=f"Lifetime tickets: {count['ticket']}", color=0x00FF00)

        if string in "arp":
            arpString = ''

            list = count['arp']
            sortedList = sorted(list, key = lambda i: i['count'], reverse=True)
            for entry in sortedList:
                if int(entry['count']) > 0:
                    arpString = arpString + f"{entry['value']} - `{entry['count']} tickets`\n"
            if not arpString:
                arpString = '-'
            embed.add_field(name="ARP", value=f"{arpString}\n")

        elif string in "are":
            areString = ''

            list = count['are']
            sortedList = sorted(list, key = lambda i: i['count'], reverse=True)
            for entry in count['are']:
                if int(entry['count']) > 0:
                    areString = areString + f"{entry['value']} - `{entry['count']} tickets`\n"
            if not areString:
                areString = '-'
            embed.add_field(name="ARE", value=f"{areString}\n")

        elif string in "ar6":
            ar6String = ''

            list = count['ar6']
            sortedList = sorted(list, key = lambda i: i['count'], reverse=True)
            for entry in count['ar6']:
                if int(entry['count']) > 0:
                    ar6String = ar6String + f"{entry['value']} - `{entry['count']} tickets`\n"
            if not ar6String:
                ar6String = '-'
            embed.add_field(name="AR6", value=f"{ar6String}\n")

        else:
            embed.add_field(name="Error", value="No Valid Category Specified")
        message = await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(ticket(client))
