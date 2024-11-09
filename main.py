import random
from datetime import datetime, timezone

def generate_lt_address():
    lt_address = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return lt_address

class MT103:
    content = ""
    
    def __init__(self):
        pass
    
    def add_header(self, type_message, bic_bank_sender):
        lt = generate_lt_address()
        self.content += '{1:' + f'{type_message}{bic_bank_sender}{lt}' + '}:'
    
    def add_header_app(self, bic_bank_destiny, priority="N"):
        current_time = datetime.now(timezone.utc)
        date_entry = current_time.strftime('%d%m%y')
        time_entry = current_time.strftime('%H%M')
        date_send = current_time.strftime('%d%m%y')
        time_send = current_time.strftime('%H%M')
        self.content += '{2:O' + f'103{time_entry}{date_entry}{bic_bank_destiny}{generate_lt_address()}{date_send}{time_send}{priority}' + '}'
    
    def add_user_header(self, id_transaction):
        self.content += '{3:{108:' + f'{id_transaction}' + '}}'
    
    def add_transaction_details(self, reference, amount_date, currency, amount, sender_account, receiver_account, charges):
        self.content += '{4:\n'
        self.content += f':20:{reference}\n'
        self.content += ':23B:CRED\n'
        self.content += f':32A:{amount_date}{currency}{amount}\n'
        self.content += f':50A:/{sender_account}\n'
        self.content += f':59:/{receiver_account}\n'
        self.content += f':71A:{charges}\n'
        self.content += '-}'

def generate_mt103(type_message, bic_bank_sender, bic_bank_destiny, id_transaction, reference, amount_date, currency, amount, sender_account, receiver_account, charges="SHA"):
    message = MT103()
    message.add_header(
        type_message=type_message,
        bic_bank_sender=bic_bank_sender
    )
    message.add_header_app(
        bic_bank_destiny=bic_bank_destiny,
        priority="N"
    )
    message.add_user_header(id_transaction=id_transaction)
    message.add_transaction_details(
        reference=reference,
        amount_date=amount_date,
        currency=currency,
        amount=amount,
        sender_account=sender_account,
        receiver_account=receiver_account,
        charges=charges
    )
    return message.content

mt103_message = generate_mt103(
    type_message="F01",
    bic_bank_sender="BANKBEBBAXXX",
    bic_bank_destiny="BANKDEFFXXX",
    id_transaction="MT103",
    reference="REFERENCE12345",
    amount_date="230501",
    currency="EUR",
    amount="123456,78",
    sender_account="12345678901234567890",
    receiver_account="23456789012345678901",
    charges="SHA"
)

print(mt103_message)