import rpyc


def test_transaction(conn, card_number, cvv, expiry_date, amount):
    print("\n======================================================================================")
    print(f"Testing transaction:")
    print(f"  Card Number: {card_number}")
    print(f"  CVV: {cvv}")
    print(f"  Expiry Date: {expiry_date}")
    print(f"  Amount: {amount}")
    print("-------------------------------------------------------------------------------------")

    authentication_response = conn.root.authenticate_transaction(card_number, cvv, expiry_date)
    print("Authentication Service Response:")
    print("  ", authentication_response)

    # Use dictionary access
    if authentication_response['status'] == "failure":
        print("FAILED - Failure at Authentication Stage")
        print("======================================================================================\n")
        return

    print("-------------------------------------------------------------------------------------")
    authorisation_response = conn.root.authorise_transaction(card_number, amount)
    print("Authorisation Service Response:")
    print("  ", authorisation_response)

    # Use dictionary access
    if authorisation_response['status'] == "failure":
        print("FAILED - Failure at Authorisation Stage")
        print("======================================================================================\n")
        return

    print("-------------------------------------------------------------------------------------")
    settlement_response = conn.root.settle_transaction(card_number, amount)
    print("Settlement Service Response:")
    print("  ", settlement_response)

    # Use dictionary access
    if settlement_response['status'] == "failure":
        print("FAILED - Failure at Settlement Stage")
        print("======================================================================================\n")
        return

    print("-------------------------------------------------------------------------------------")
    print("SUCCESS - Transaction completed successfully")
    print("======================================================================================\n")


def main():
    conn = rpyc.connect("3.255.225.193", 18080)  # Replace with the actual host and port

    # Success scenario
    test_transaction(conn, "8002 8945 2356 8345", "546", "02/25", 2.00)

    # Test cases for different failure scenarios
    # Invalid card number
    test_transaction(conn, "9999 9999 9999 9999", "546", "02/25", 2.00)

    # Incorrect CVV
    test_transaction(conn, "8002 8945 2356 8345", "123", "02/25", 2.00)

    # Expired card
    test_transaction(conn, "8002 8945 2356 8345", "546", "02/20", 2.00)

    # Insufficient funds
    test_transaction(conn, "8002 8945 2356 8345", "546", "02/25", 10000.00)

    conn.close()


if __name__ == "__main__":
    main()
