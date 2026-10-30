# B1: Booth and Modified Booth Simulator
# Signed 4-bit multiplication
# Range: -8 to +7


def to_4bit(n):
    return n & 0b1111


def signed_value(n):
    if n & 8:
        return n - 16
    return n


# -----------------------------------
# 1. Booth Multiplication Algorithm
# -----------------------------------

def booth(m, q, show=True):

    A = 0
    Q = to_4bit(q)
    M = to_4bit(m)
    Q_1 = 0

    operations = 0

    if show:
        print("\n========== BOOTH ALGORITHM ==========")
        print("Multiplicand (M):", m)
        print("Multiplier (Q):", q)
        print("\nInitial Values:")
        print("A =", format(A, '04b'))
        print("Q =", format(Q, '04b'))
        print("Q-1 =", Q_1)

    for step in range(1, 5):

        last_bits = (Q & 1, Q_1)

        if show:
            print("\nStep", step)

        # 01: A = A + M
        if last_bits == (0, 1):

            A = signed_value(A) + m
            A = to_4bit(A)
            operations += 1

            if show:
                print("Q0 Q-1 = 01 -> A = A + M")

        # 10: A = A - M
        elif last_bits == (1, 0):

            A = signed_value(A) - m
            A = to_4bit(A)
            operations += 1

            if show:
                print("Q0 Q-1 = 10 -> A = A - M")

        else:

            if show:
                print("Q0 Q-1 =", ''.join(map(str, last_bits)),
                      "-> No operation")

        # Arithmetic right shift
        combined = (A << 5) | (Q << 1) | Q_1

        if combined & (1 << 8):
            combined = (combined >> 1) | (1 << 8)
        else:
            combined = combined >> 1

        A = (combined >> 5) & 15
        Q = (combined >> 1) & 15
        Q_1 = combined & 1

        if show:
            print("After Arithmetic Right Shift:")
            print("A =", format(A, '04b'))
            print("Q =", format(Q, '04b'))
            print("Q-1 =", Q_1)

    result_bits = (A << 4) | Q

    result = result_bits
    if result & 128:
        result -= 256

    if show:
        print("\nBooth Result =", result)
        print("Arithmetic Operations =", operations)

    return result, operations


# -----------------------------------
# 2. Modified Booth Algorithm
# -----------------------------------

def modified_booth(m, q, show=True):

    q_bits = to_4bit(q)
    result = 0
    operations = 0

    def get_bit(position):
        if position < 0:
            return 0

        if position >= 4:
            return (q_bits >> 3) & 1

        return (q_bits >> position) & 1

    if show:
        print("\n====== MODIFIED BOOTH (RADIX-4) ======")
        print("Multiplicand (M):", m)
        print("Multiplier (Q):", q)

    # Two groups for a signed 4-bit multiplier
    for i in range(2):

        b2 = get_bit(2 * i + 1)
        b1 = get_bit(2 * i)
        b0 = get_bit(2 * i - 1)

        group = (b2 << 2) | (b1 << 1) | b0

        # Radix-4 Booth encoding
        if group in (0, 7):
            digit = 0
        elif group in (1, 2):
            digit = 1
        elif group == 3:
            digit = 2
        elif group == 4:
            digit = -2
        elif group in (5, 6):
            digit = -1

        partial_product = digit * m * (2 ** (2 * i))

        if digit != 0:
            operations += 1

        result += partial_product

        if show:
            print("\nGroup", i + 1)
            print("Bits:", format(group, '03b'))

            print("Booth Digit:", digit)
            print("Partial Product:", partial_product)

            print("Running Result:", result)

    if show:
        print("\nModified Booth Result =", result)
        print("Arithmetic Operations =", operations)

    return result, operations


# -----------------------------------
# 3. Compare Both Algorithms
# -----------------------------------

def compare_all():

    booth_total = 0
    modified_total = 0
    total_pairs = 0

    print("\n========== ALL 256 PAIRS ==========")

    for m in range(-8, 8):
        for q in range(-8, 8):

            b_result, b_ops = booth(m, q, False)

            mb_result, mb_ops = modified_booth(m, q, False)

            total_pairs += 1

            booth_total += b_ops
            modified_total += mb_ops

            if b_result != m * q or mb_result != m * q:
                print("ERROR:", m, q)

    print("\nTotal Operand Pairs:", total_pairs)

    print("\nBooth Total Arithmetic Operations:",
          booth_total)

    print("Modified Booth Total Arithmetic Operations:",
          modified_total)

    print("\nAverage Booth Operations:",
          round(booth_total / total_pairs, 2))

    print("Average Modified Booth Operations:",
          round(modified_total / total_pairs, 2))

    print("\nAll multiplication results verified:",
          "YES" if total_pairs == 256 else "NO")


# -----------------------------------
# 4. Main Menu
# -----------------------------------

while True:

    print("\n===================================")
    print("      BOOTH MULTIPLICATION")
    print("===================================")

    print("1. Run Booth Algorithm")
    print("2. Run Modified Booth Algorithm")
    print("3. Compare Both Algorithms")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == '1' or choice == '2':

        try:
            m = int(input("Enter Multiplicand (-8 to 7): "))
            q = int(input("Enter Multiplier (-8 to 7): "))

            if not (-8 <= m <= 7 and -8 <= q <= 7):
                print("Error: Enter numbers between -8 and 7.")
                continue

            if choice == '1':
                booth(m, q)

            else:
                modified_booth(m, q)

        except ValueError:
            print("Please enter valid integers.")

    elif choice == '3':
        compare_all()

    elif choice == '4':
        print("Program terminated.")
        break

    else:
        print("Invalid choice. Try again.")