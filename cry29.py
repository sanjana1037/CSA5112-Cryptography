# keccak_pi_sim.py
# Simulate Keccak π lane permutation on 5x5 lanes (0..24).
# Initial nonzero lanes: 0..15 (from P0).
# Capacity lanes: 16..24 (initially zero).
# Apply π repeatedly, track which lanes have ever been nonzero.

def pi_map(idx):
    x = idx % 5
    y = idx // 5
    nx = y
    ny = (2 * x + 3 * y) % 5
    return 5 * ny + nx

def simulate(max_steps=50, verbose=True):
    N = 25
    current = [False] * N   # occupancy this step
    seen = [False] * N      # ever seen nonzero
    capacity_indices = list(range(16, 25))

    # initial nonzero lanes from P0
    for i in range(16):
        current[i] = True
        seen[i] = True

    if verbose:
        print("Initial nonzero lanes (from P0):", [i for i,v in enumerate(current) if v])
        print("Capacity lanes (initially zero):", capacity_indices)
        print()

    if all(seen[i] for i in capacity_indices):
        print("All capacity lanes already nonzero at t = 0")
        return 0, seen

    for t in range(1, max_steps + 1):
        next_state = [False] * N
        # apply pi: lane i -> pi_map(i)
        for i in range(N):
            if current[i]:
                j = pi_map(i)
                next_state[j] = True

        # update seen
        for i in range(N):
            if next_state[i]:
                seen[i] = True

        if verbose:
            print(f"After {t:2d} permutation(s), nonzero lanes:",
                  [i for i,v in enumerate(next_state) if v])

        if all(seen[i] for i in capacity_indices):
            if verbose:
                print(f"\nAll capacity lanes {capacity_indices} have been nonzero by t = {t} π-permutations.")
            return t, seen

        current = next_state

    if verbose:
        print(f"\nDid not cover all capacity lanes within {max_steps} iterations.")
    return None, seen

if __name__ == "__main__":
    t, seen = simulate(max_steps=10, verbose=True)
