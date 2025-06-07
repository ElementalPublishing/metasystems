import fastmath
import random
import sys

def random_prime(lower, upper, max_attempts=100000):
    attempts = 0
    while attempts < max_attempts:
        n = random.randint(lower, upper)
        if fastmath.is_prime(n):
            return n
        attempts += 1
    return None

def generate_primes(count, lower, upper):
    primes = set()
    while len(primes) < count:
        p = random_prime(lower, upper)
        if p is not None:
            primes.add(p)
        else:
            print(f"Could not find enough primes in range {lower}-{upper}.")
            break
    return list(primes)

def generate_256bit_prime():
    lower = 2**255
    upper = 2**256 - 1
    print("Generating a random 256-bit prime (this may take a moment)...")
    p = random_prime(lower, upper, max_attempts=5000000)
    if p is None:
        print("Failed to find a 256-bit prime. Try increasing max_attempts or check your fastmath.is_prime implementation.")
        sys.exit(1)
    return p

def main():
    print("Randomer - Fast random prime/number generator using fastmath")
    print("Choose a mode:")
    print("  primes   - Generate random primes in a range")
    print("  prime256 - Generate a random 256-bit prime")
    print("  seeded   - Generate primes with a specific random seed")
    print("  quit     - Exit the program")
    mode = input("Enter mode: ").strip().lower()

    if mode == "primes":
        count = int(input("How many primes? [default 5]: ") or "5")
        lower = int(input("Lower bound? [default 10000]: ") or "10000")
        upper = int(input("Upper bound? [default 100000]: ") or "100000")
        print(f"Generating {count} random primes between {lower} and {upper}...")
        primes = generate_primes(count, lower, upper)
        for i, p in enumerate(primes, 1):
            print(f"Prime {i}: {p}")
        print("All primes:", primes)
    elif mode == "prime256":
        p = generate_256bit_prime()
        print(f"Random 256-bit prime:\n{p}")
    elif mode == "seeded":
        seed = int(input("Enter seed (integer): "))
        random.seed(seed)
        count = int(input("How many primes? [default 5]: ") or "5")
        lower = int(input("Lower bound? [default 10000]: ") or "10000")
        upper = int(input("Upper bound? [default 100000]: ") or "100000")
        print(f"Generating {count} random primes between {lower} and {upper} with seed {seed}...")
        primes = generate_primes(count, lower, upper)
        for i, p in enumerate(primes, 1):
            print(f"Prime {i}: {p}")
        print("All primes:", primes)
    elif mode == "quit":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Unknown mode. Please run the program again and choose a valid option.")

if __name__ == "__main__":
    main()