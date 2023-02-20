# Ref
# https://thesadru.github.io/genshin.py


import asyncio
import genshin
import platform
from prettytable import PrettyTable

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

accounts = [
    {"label": "Akun 1", "genshin_daily": True, "honkai_daily": True,  
        "ltuid": 999999999, "ltoken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
    {"label": "Akun 2", "genshin_daily": True, "honkai_daily": False, 
        "ltuid": 999999999, "ltoken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
]

async def claim_daily(client):
    result = ""
    try:
        reward = await client.claim_daily_reward()
    except genshin.AlreadyClaimed:
        result = "Today:Claimed"
    else:
        result = f"Today:Claim {reward.amount}x \n{reward.name}"

    signed_in, claimed_rewards = await client.get_reward_info()
    return signed_in, claimed_rewards, result


async def main():

    for account in accounts:
        client = genshin.Client(account)
        data = await client.get_notes()
        
        honkai_daily = {}
        genshin_daily = {}
        expedition = ""

        for exped in data.expeditions:
            expedition += f"{exped.character.name[:10]} ({exped.remaining_time})"
            if exped.character.name != data.expeditions[-1].character.name:
                expedition += "\n"

        # Uhmmm.. i can explain this.. >///<
        headers = [
            "  Label  ", 
            "   Resin   ", 
            "       Teapot       ", 
            "Parametic Transf", 
            " Weekly ", 
            " Daily Comm ", 
            "     Expedition     "
        ]

        if (account['genshin_daily']):
            client.default_game = genshin.Game.GENSHIN
            genshin_daily = await claim_daily(client)
            headers.append("Genshin Daily Reward")

        if (account['honkai_daily']):
            client.default_game = genshin.Game.HONKAI
            honkai_daily = await claim_daily(client)
            headers.append("Honkai Daily Reward")

        table = PrettyTable()
        table.align["Expedition"] = "l"
        table.field_names = headers
        row = [
            # Label
            account['label'], 

            # Resin
            f"{data.current_resin}/{data.max_resin} \n"
            + f"({data.remaining_resin_recovery_time})",

            # Teapot
            f"{data.current_realm_currency}/"
            + f"{data.max_realm_currency} \n"
            + f"({data.remaining_realm_currency_recovery_time})",

            # Parametic Transformer
            f"{data.remaining_transformer_recovery_time}",

            # Weekly
            f"{data.remaining_resin_discounts}/"
            + f"{data.max_resin_discounts}",

            # Daily Commision
            f"{data.completed_commissions}/"
            + f"{data.max_commissions}/"
            + f"{data.claimed_commission_reward}",

            # Expedition
            expedition,
        ]

        # Daily Reward
        if (account['genshin_daily']):
            row.append(f"{genshin_daily[1]} Days Claimed\n{genshin_daily[2]}")
        if (account['honkai_daily']):
            row.append(f"{honkai_daily[1]} Days Claimed\n{honkai_daily[2]}")

        table.add_row(row)
        print(table)

        # Old View
        # print ("===========================================")
        # print (f"{account['label']}")
        # print ("===========================================")
        # print (f"Resin           "
        #     + f"{data.current_resin}/"
        #     + f"{data.max_resin} "
        #     + f"({data.remaining_resin_recovery_time})")
        # print (f"Teapot Currency {data.current_realm_currency}/{data.max_realm_currency} ({data.remaining_realm_currency_recovery_time})")
        # print (f"Transformer     {data.remaining_transformer_recovery_time}")
        # print (f"Weekly Discount {data.remaining_resin_discounts}/{data.max_resin_discounts}")
        # print (f"Daily Commision {data.completed_commissions}/{data.max_commissions}/{data.claimed_commission_reward}")
        
        # print ("-------------------------------------------")
        # print (f"Expeditions     {len(data.expeditions)}/{data.max_expeditions}")
        # for expedition in data.expeditions:
        #     print (f"    {expedition.character.name}-{expedition.status} ({expedition.remaining_time})")

        # if (account['genshin_daily']):
        #     print ("-------------------------------------------")
        #     print ("Genshin Daily Reward")
        #     print (genshin_daily[2])
        # if (account['honkai_daily']):
        #     print ("-------------------------------------------")
        #     print ("Honkai Daily Reward")
        #     print (honkai_daily[2])

        # print ("===========================================")

asyncio.run(main())