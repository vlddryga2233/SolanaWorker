
from solana_class import Solana_worker
from solders.pubkey import Pubkey
from spl.token.async_client import AsyncToken
import asyncio

secret_key = [159,170,137,105,139,135,245,111,222,244,95,46,201,78,27,167,169,185,127,22,11,94,228,252,16,6,5,86,217,68,227,254,61,172,5,206,192,159,235,208,243,80,48,227,116,221,227,74,93,185,182,69,54,13,244,182,0,44,246,221,106,70,16,106]
    


async def main():
    service_object = Solana_worker(secret_key)
    source_address = service_object.get_address()
    source_wallet_balance = await service_object.get_balance()
    print("Source Address:", source_address)
    print("Source Wallet Balance:", source_wallet_balance)


    destination_address = Pubkey.from_string("AHMm3knQvjYYGHoU38rGUe8XChGnWHGxTvtVmrHueXGA")
    TOKEN_PROGRAM_ID = service_object.find_token_program_id("FTT/USDT")
    source_token_address ="AGFEad2et2ZJif9jaGpdMixQqvW5i81aBdvKe7PHNfz3"
    source_token = AsyncToken(service_object.client, Pubkey.from_string(source_token_address), Pubkey.from_string(TOKEN_PROGRAM_ID), service_object.keypair)
    print(f"Program ID: {TOKEN_PROGRAM_ID}")
    #tx = await service_object.send_solana(service_object.pubkey,service_object.keypair,destination_address,0.001)
    tx_send_spl = await service_object.send_spl_token(source_token,Pubkey.from_string(source_token_address), destination_address, service_object.keypair, 1)
    #print("Transaction ID:", tx)
    print("Transaction ID:", tx_send_spl)
    
    
    #source_token = AsyncToken(service_object.client, Pubkey(source_token_address), TOKEN_PROGRAM_ID, service_object.keypair)
    #destination_token = AsyncToken(service_object.client, Pubkey(destination_token_address), TOKEN_PROGRAM_ID, service_object.keypair)

    #print(f"Source token: {source_token}")
    #print(f"Destination token: {destination_token}")
    #txn_signature = await service_object.swap_tokens(source_token, destination_token, service_object.keypair, recipient_address, source_amount, destination_amount)
    #print(f"Swap signature: {txn_signature}")

    await service_object.close()

asyncio.run(main())