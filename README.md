Методы класса для транзакций:
- создание кошельков; принимает: кол-во; возвращает: пары ключей
- трансфер токена; принимает: получателя/ей, сумму/ы; возвращает: хеш(сигнатуру/ы) транзакции/ий
- своп; принимает: адрес токена А, адрес токена Б, в каком токене ведется расчет, , сумму/ы, пару/ы ключей; возвращает: хеш(сигнатуру/ы) транзакции/ий

python3 -m venv env
aource env/bin/activate

deactivate

Address 1: 59k1RZ8L882PopU677T9oBAEU2c6MRc6cy7ZuWfBhG7K
           

[159,170,137,105,139,135,245,111,222,244,95,46,201,78,27,167,169,185,127,22,11,94,228,252,16,6,5,86,217,68,227,254,61,172,5,206,192,159,235,208,243,80,48,227,116,221,227,74,93,185,182,69,54,13,244,182,0,44,246,221,106,70,16,106]

connect icon lumber ribbon sweet miracle whisper uniform notice unfold essence nation



GetBalanceResp { context: RpcResponseContext { slot: 298453903, api_version: Some("1.18.12") }, value: 4000000000 }

keypair 2 address: AHMm3knQvjYYGHoU38rGUe8XChGnWHGxTvtVmrHueXGA
[147,86,13,225,199,13,122,11,223,126,61,101,21,73,137,251,201,237,142,20,150,87,176,19,9,123,208,24,43,185,94,238,137,233,242,179,197,70,219,32,215,164,197,98,79,72,169,32,226,235,110,143,5,18,41,42,167,203,168,238,67,238,20,239]


Transaction ID: 2WQdsXEetnbP7278XV5P1BLoMVCpkSZMYZqh2CWM5Dkd1cS9hLHV4szZn3X5DbK4s8AhWZ2J9jYhj1ANuu42GMXg



pl-token create-token
Creating token AQU19TGzgAf1KRAdgDUowuLiKA33Boi1ep6XWxdzuGwM under program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA

Address:  AQU19TGzgAf1KRAdgDUowuLiKA33Boi1ep6XWxdzuGwM
Decimals:  9

Creating account 7KknKbUFERvkcuttadfDtMyCybe3LC36fmqT1VUXXWFt

Minting 1000 tokens
  Token: AQU19TGzgAf1KRAdgDUowuLiKA33Boi1ep6XWxdzuGwM
  Recipient: 7KknKbUFERvkcuttadfDtMyCybe3LC36fmqT1VUXXWFt


  New Token Account Address: 6uQW6FcJQoox5mjhd1sFmajfhSR69wmVBZuAzpirpwLW



solana.rpc.core.RPCException: SendTransactionPreflightFailureMessage { message: "Transaction simulation failed: Transaction results in an account (1) with insufficient funds for rent", data: RpcSimulateTransactionResult(RpcSimulateTransactionResult { err: Some(InsufficientFundsForRent { account_index: 1 }), logs: Some(["Program 11111111111111111111111111111111 invoke [1]", "Program 11111111111111111111111111111111 success"]), accounts: None, units_consumed: Some(150), return_data: None, inner_instructions: None }) }