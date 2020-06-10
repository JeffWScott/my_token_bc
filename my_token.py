
#my_token.py

#Smart Contract State
S = Hash(default_value=0)

#This runs when our contract is created on the blockchain, and never again.
@construct
def seed(vk: str, amount: int):
    S[vk] = amount

#This method will be exported so our users can call it
@export
def transfer(amount: int, receiver: str):
    #ctx.caller is the verified identity of the person who signed this transaction
    #we will keep this reference as the "sender" of the transaction
    sender = ctx.caller

    #get the sender's balance from State
    balance = S[sender]

    #assert the sender has the appropriate balance to send
    #if this assert fails the method will fail here, all values revert and no more code is executed
    assert balance >= amount, "Transfer amount exceeds available token balance"

    #deducte the tokens from the sender's balance
    S[sender] -= amount

    #add tokens to the receiver's balance
    S[receiver] += amount
