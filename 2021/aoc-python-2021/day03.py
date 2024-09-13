import numpy as np

with open("data-day03.txt") as f:
    rows = f.readlines()
    bitmap = np.array([[int(c) for c in r.strip()] for r in rows])

most_common_bits = (bitmap.mean(axis=0) > 0.5).astype(int)

pows_of_two = np.array([2**i for i in range(len(most_common_bits))][::-1])

def bitmap_to_int(bits):
    return (bits * pows_of_two).sum()

gamma_rate = bitmap_to_int(most_common_bits)
epsilon_rate = 2**(len(most_common_bits))-1 - gamma_rate

print("Power Consumption: ", gamma_rate * epsilon_rate)

# part 2

# oxygen
rows_to_keep = np.arange(bitmap.shape[0])

for bit_col in range(bitmap.shape[1]):
    most_common_bit = 1 if bitmap[rows_to_keep,bit_col].mean() >= 0.5 else 0
    rows_to_keep = [x for x in np.where(bitmap[:,bit_col]==most_common_bit)[0] if x in rows_to_keep]

    if len(rows_to_keep) == 1:
        break

oxygen_rate = bitmap_to_int(bitmap[rows_to_keep])

# co2
rows_to_keep = np.arange(bitmap.shape[0])

for bit_col in range(bitmap.shape[1]):
    least_common_bit = 1 if bitmap[rows_to_keep,bit_col].mean() < 0.5 else 0
    rows_to_keep = [x for x in np.where(bitmap[:,bit_col]==least_common_bit)[0] if x in rows_to_keep]

    if len(rows_to_keep) == 1:
        break

co2_rate = bitmap_to_int(bitmap[rows_to_keep])

print("Life Support Rating: ", oxygen_rate * co2_rate)
