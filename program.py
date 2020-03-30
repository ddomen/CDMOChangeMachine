from change_machine import ChangeMachine

# Sum the values of a coin dictionary (change or storage)
def coinSum(storage):
    return sum(( c * v for c, v in storage.items() ))

# Machine Storage
COINS = { 1: 23, 2: 32, 5: 12, 10: 7, 20: 23, 50: 11, 100: 12, 200: 5 }

# Array of test changes (data) (Generated once randomly)
inputs = [
    2,      117,    134,
    49,     312,    1234,
    412,    87,     257,
    313,    67,     242,
    112,    77,     28,
    12,     114
]

# Digest input
for inp in inputs:

    request = int(inp)
    print('CHANGE REQUEST:\t{}'.format(request))

    # Calculate the actual change from the request
    ch = ChangeMachine(COINS, request)

    if ch is None:
        print('CHANGE:\t\tUNAVAILABLE! ({} / {})\n'.format(request, coinSum(COINS)))

    else:
        print('CHANGE:\t\t{} ({} / {})\n'.format(ch, coinSum(ch), request))
        # Update the current Machine Storage, removing the change
        for s, v in ch.items():
            COINS[s] = int(COINS[s] - v)

    print('AVAILABLE:\t{} ({})\n'.format(COINS, coinSum(COINS)))
        

