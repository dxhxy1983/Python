def shuffle_deck(K, order):
    # Initial deck configuration
    deck = [
        "S" + str(i) for i in range(1, 14)
    ] + [
        "H" + str(i) for i in range(1, 14)
    ] + [
        "C" + str(i) for i in range(1, 14)
    ] + [
        "D" + str(i) for i in range(1, 14)
    ] + ["J1", "J2"]

    # Perform the shuffle K times
    for _ in range(K):
        new_deck = [None] * 54  # Create an empty new deck
        for i in range(54):
            new_deck[order[i] - 1] = deck[i]  # Move card to its new position
        deck = new_deck  # Update the deck to the new deck

    # Output the final deck configuration
    print(" ".join(deck))

# Input
K = int(input())
order = list(map(int, input().split()))

# Call the function to shuffle the deck
shuffle_deck(K, order)
