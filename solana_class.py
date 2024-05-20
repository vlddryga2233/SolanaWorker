
from solana.rpc.async_api import AsyncClient
from spl.token.async_client import AsyncToken
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.keypair import Keypair
from spl.token.constants import TOKEN_PROGRAM_ID
#from pyserum.connection import conn
#from pyserum.market import Market
import base58
import json


class Solana_worker():
    def __init__(self, secret_key_json):
        self.client = AsyncClient("https://api.devnet.solana.com")
        self.keypair = Keypair.from_bytes(secret_key_json)
        self.pubkey = self.keypair.pubkey()
    
    def get_address(self):
        return self.pubkey
    
    async def get_balance(self):
        balance =  await self.client.get_balance(self.pubkey)
        return balance.value

    async def create_token_account(self, client, token_mint_address, owner_keypair):
        token_client = AsyncToken(client, token_mint_address, TOKEN_PROGRAM_ID, owner_keypair)
        new_account_pubkey = await token_client.create_account(owner_keypair.pubkey())
        return new_account_pubkey
    
    async def get_existing_token_account(self, owner_pubkey, token_mint_address):
        opts = {
            "encoding" : "base58"
        }
        resp = await self.client.get_token_accounts_by_owner(owner_pubkey, opts)
        accounts = resp['result']['value']
        if len(accounts) > 0:
            return Pubkey.from_string(accounts[0]['pubkey'])
        else:
            raise ValueError("Token account not found.")


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
        transaction_signature = await self.client.send_transaction(txn, source_keypair)
        return str(transaction_signature.value)

    async def send_spl_token(self, spl_client: AsyncToken, source_token_address: Pubkey, destination_token_address: Pubkey, owner_keypair: Keypair, amount: float):
        transaction = await spl_client.transfer(
            source=source_token_address,
            dest=destination_token_address,
            owner=owner_keypair,
            amount=int(amount * 1000000000),  # Количество в минимальных единицах (например, 1 токен с 9 десятичными знаками = 1000000000)
            multi_signers=None
        )
        return str(transaction.value)
    
    # Функция для поиска маркета в JSON-файле
    def find_market_address(self, pair_name):
        with open('markets.json', 'r') as f:
            markets = json.load(f)
        for market in markets:
            if market['name'] == pair_name:
                return market['address']
        raise ValueError(f"Market for pair {pair_name} not found.")
    
    def find_token_program_id(self, pair_name):
        with open('markets.json', 'r') as f:
            programs = json.load(f)
        for program in programs:
            if program['name'] == pair_name:
                return program['programId']
        raise ValueError(f"Program ID for pair {pair_name} not found.")
    
    async def close(self):
        await self.client.close()

    # своп; принимает: адрес токена А, адрес токена Б, в каком токене ведется расчет, , сумму/ы, пару/ы ключей; возвращает: хеш(сигнатуру/ы) 
    async def swap_tokens(self, pair_name: str, base_token: AsyncToken, quote_token: AsyncToken, sender_keypair: Keypair, source_amount: float):
        # Подключение к рынку
        serum_conn = conn("https://api.devnet.solana.com")
        market_address = self.find_market_address(pair_name)
        market = await Market.load(serum_conn, market_address)

        # Получение ордербука
        bids = await market.load_bids()
        asks = await market.load_asks()

        # Поиск лучшего предложения
        best_bid = max(bids, key=lambda order: order.info.price)
        best_ask = min(asks, key=lambda order: order.info.price)

        # Логика свапа на основе лучшего предложения
        best_price = best_bid.info.price if best_bid.info.price > best_ask.info.price else best_ask.info.price

        # Создание транзакции для свапа токенов
        txn = Transaction()

        # Добавление инструкции для продажи base_token
        txn.add(
            base_token.transfer(
                source=await base_token.get_account_info(sender_keypair.pubkey()),
                dest=best_bid.order_id,
                owner=sender_keypair.pubkey(),
                amount=int(source_amount * 1000000000)
            )
        )

        # Добавление инструкции для покупки quote_token
        txn.add(
            quote_token.transfer(
                source=best_ask.order_id,
                dest=sender_keypair.pubkey(),
                owner=sender_keypair.pubkey(),
                amount=int(source_amount * best_price * 1000000000)
            )
        )

        # Подписание и отправка транзакции
        response = await self.client.send_transaction(txn, sender_keypair)
        transaction_signature = response['result']
        return str(transaction_signature)
    



