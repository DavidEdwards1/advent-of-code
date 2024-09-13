from typing import Dict, List, Set, Tuple


def input_to_display(input_string: str) -> Tuple[List[Set[str]]]:
    digit_codes, displayed_digits = input_string.strip().split("|")
    digit_codes = [frozenset(d) for d in digit_codes.strip().split()]
    displayed_digits = [frozenset(d) for d in displayed_digits.strip().split()]

    return (digit_codes, displayed_digits)

def map_signal_codes(digit_codes: List[Set[str]]) -> Dict[Set[str], str]:
    codes_to_digits = {dc: "Unknown" for dc in digit_codes}

    # first run over the unique length codes so that we build them up
    # that covers 1, 4, 7 and 8
    for dc in digit_codes:
        if len(dc) == 2:
            codes_to_digits[dc] = "1"
        elif len(dc) == 3:
            codes_to_digits[dc] = "7"
        elif len(dc) == 4:
            codes_to_digits[dc] = "4"
        elif len(dc) == 7:
            codes_to_digits[dc] = "8"

    digits_to_codes = {d: code for code, d in codes_to_digits.items() if d != "Unknown"}

    # now we can tackle separating the 0, 6 or 9 (all length 6)
    for dc in digit_codes:
        if len(dc) == 6:
            if digits_to_codes["4"] <= dc:
                codes_to_digits[dc] = "9"
            elif digits_to_codes["1"] <= dc:
                codes_to_digits[dc] = "0"
            else:
                codes_to_digits[dc] = "6"

    digits_to_codes = {d: code for code, d in codes_to_digits.items() if d != "Unknown"}

    # now we have 2, 3 and 5 left (all length 5)
    for dc in digit_codes:
        if len(dc) == 5:
            if digits_to_codes["1"] <= dc:
                codes_to_digits[dc] = "3"
            # note that 5 is a subset of 6
            elif dc <= digits_to_codes["6"]:
                codes_to_digits[dc] = "5"
            else:
                codes_to_digits[dc] = "2"

    return codes_to_digits

def apply_map_to_display(
    displayed_digits: List[Set[str]],
    signal_code_map: Dict[Set[str],str]
) -> List[int]:
    return [signal_code_map[d] for d in displayed_digits]

with open("data-day08.txt") as f:
    display_inputs = f.readlines()

displays = [input_to_display(d) for d in display_inputs]
displays = [(map_signal_codes(d[0]), d[1]) for d in displays]
displays = [(d[0], apply_map_to_display(d[1], d[0])) for d in displays]

easy_digits = ("1", "7", "4", "8")
count_of_easy_digits = 0

for disp in displays:
    digits = disp[1]
    count_of_easy_digits += len([d for d in digits if d in easy_digits])

print("Number of Easy Digits: ", count_of_easy_digits)

total_value = sum([int("".join(d[1])) for d in displays])

print("Total value of displays: ", total_value)
