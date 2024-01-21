import rpyc

# Test 1 passes (all details ok)
test1 = {"card_num": "8002 1235 5687 9898",
         "expiry": "12/24",
         "cvv": "994",
         "amount": 29.99,
         }

# Test 2 : Transaction declined by Bisa (card expired)
test2 = {"card_num": "8002 6543 3456 7634",
         "expiry": "02/23",
         "cvv": "456",
         "amount": 15.99,
         }

# Test 3 : Transaction declined by Bisa (incorrect CCV)
test3 = {"card_num": "8002 8945 2356 8345",
         "expiry": "02/25",
         "cvv": "654",
         "amount": 31.99,
         }

# Test 4 : Transaction declined by Bisa (not enough balance)
test4 = {"card_num": "8002 6354 2345 8765",
         "expiry": "06/26",
         "cvv": "134",
         "amount": 49.99,
         }

# Test 5 : Transaction declined by payment processor. (Not Bisa card)
test5 = {"card_num": "1200 6537 9864 3425",
         "expiry": "04/24",
         "cvv": "231",
         "amount": 12.99,
         }

rpyc_config = {
    'allow_pickle': True
}

conn = rpyc.connect('34.242.46.121', 18080, config=rpyc_config)

print(conn.root.processor(test1))
print(conn.root.processor(test2))
print(conn.root.processor(test3))
print(conn.root.processor(test4))
print(conn.root.processor(test5))
