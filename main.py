
from solana_class import Solana_worker
from solders.pubkey import Pubkey
import asyncio

secret_key = [159,170,137,105,139,135,245,111,222,244,95,46,201,78,27,167,169,185,127,22,11,94,228,252,16,6,5,86,217,68,227,254,61,172,5,206,192,159,235,208,243,80,48,227,116,221,227,74,93,185,182,69,54,13,244,182,0,44,246,221,106,70,16,106]
    


async def main():
    service_object = Solana_worker(secret_key)
    source_address = service_object.get_address()
    source_wallet_balance = service_object.get_balance()
    print("Source Address:", source_address)
    print("Source Wallet Balance:", source_wallet_balance)


    destination_address = "AHMm3knQvjYYGHoU38rGUe8XChGnWHGxTvtVmrHueXGA"

    #tx = await service_object.send_solana(service_object.pubkey,service_object.keypair,destination_address,0.001)

    #print("Transaction ID:", tx)
    await service_object.close()

asyncio.run(main())