
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from spl.token.async_client import AsyncToken
from spl.token.client import Token
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.keypair import Keypair
from solders.bankrun import BanksClient
import base58



class Solana_worker():
    def __init__(self, secret_key_json):
        self.client = Client("https://api.devnet.solana.com")
        self.async_client = AsyncClient("https://api.devnet.solana.com")
        self.keypair = Keypair.from_bytes(secret_key_json)
        self.pubkey = self.keypair.pubkey()
    
    def get_address(self):
        return self.pubkey
    
    def get_balance(self):
        balance = self.client.get_balance(self.pubkey).value
        return balance


    def create_wallets(self, wallets_amount):
        keypair_list = []
        data_object = {}
        for _ in range(wallets_amount):
            keypair = Keypair()
            data_object = {
                "keypair_json" : keypair.to_json(),
                "public_key" : keypair.pubkey(),
                "secret_key" : base58.b58encode(bytes(keypair)).decode(),
            }
            
            keypair_list.append(data_object)
        return keypair_list
    
    async def send_solana(self, source_address, source_keypair, destination_address, amount):
        txn = Transaction().add(transfer(TransferParams(
            from_pubkey=source_address, to_pubkey=Pubkey.from_string(destination_address), lamports=int(amount*1000000000))))
        transaction_signature = await self.async_client.send_transaction(txn, source_keypair)
        return str(transaction_signature.value)

    async def send_spl_token(self, spl_client: AsyncToken, source_token_address: Pubkey, destination_token_address: Pubkey, owner_keypair: Keypair, amount: float):
        txn = Transaction().add(
            spl_client.transfer(
                source=source_token_address,
                dest=destination_token_address,
                owner=owner_keypair.pubkey(),
                amount=int(amount * 1000000000)
            )
        )
        response = await self.client.send_transaction(txn, owner_keypair)
        transaction_signature = response['result']
        return str(transaction_signature)
    
    # своп; принимает: адрес токена А, адрес токена Б, в каком токене ведется расчет, , сумму/ы, пару/ы ключей; возвращает: хеш(сигнатуру/ы) 
    async def swap_tokens(self, source_token: AsyncToken, destination_token: AsyncToken, sender_keypair: Keypair, recipient_address: Pubkey, source_amount: float, destination_amount: float):
        # Создание транзакции для отправки исходного токена
        txn = Transaction().add(
            source_token.transfer(
                source=await source_token.get_account_info(sender_keypair.pubkey()),
                dest=recipient_address,
                owner=sender_keypair.pubkey(),
                amount=int(source_amount * 1000000000)
            )
        )
        # Добавление транзакции для получения целевого токена
        txn.add(
            destination_token.transfer(
                source=await destination_token.get_account_info(recipient_address),
                dest=sender_keypair.pubkey(),
                owner=recipient_address,
                amount=int(destination_amount * 1000000000)
            )
        )
        # Подписание и отправка транзакции
        response = await self.client.send_transaction(txn, sender_keypair)
        transaction_signature = response['result']
        return str(transaction_signature)

    async def close(self):
        await self.async_client.close()


