from functools import reduce
from operator import mul
from typing import Tuple


types_to_op = {
    0: sum,
    1: lambda xs: reduce(mul, xs),
    2: min,
    3: max,
    5: lambda x: 1 if x[0] > x[1] else 0,
    6: lambda x: 1 if x[0] < x[1] else 0,
    7: lambda x: 1 if x[0] == x[1] else 0,
}

def read_group(packet: str) -> Tuple[bool, str, str]:
    keep_reading, group = bool(int(packet[0])), packet[1:5]
    remaining_packet = packet[5:]

    return keep_reading, group, remaining_packet

def read_literal(packet: str) -> Tuple[int, str]:
    # assume there always is at least one group?
    keep_reading, group, remaining_packet = read_group(packet)

    packet_groups = [group]

    while keep_reading:
        keep_reading, group, remaining_packet = read_group(remaining_packet)
        packet_groups.append(group)

    return int("".join(packet_groups), 2), remaining_packet

def read_tl_operator(packet: str):
    number_of_bits = int(packet[:15], 2)

    remaining_sub_packets = packet[15:15+number_of_bits]
    read_sub_packets = []
    while remaining_sub_packets:
        rsp, remaining_sub_packets = read_packet(remaining_sub_packets)

        read_sub_packets.append(rsp)

    return read_sub_packets, packet[15+number_of_bits:]

def read_sp_operator(packet: str):
    number_of_sub_packets = int(packet[:11], 2)

    remaining_sub_packets = packet[11:]
    read_sub_packets = []
    while len(read_sub_packets) < number_of_sub_packets:
        rsp, remaining_sub_packets = read_packet(remaining_sub_packets)

        read_sub_packets.append(rsp)

    return read_sub_packets, remaining_sub_packets

def read_operator(packet: str):
    if packet[0] == "0":
        # total_length_operator
        operator_packet, remaining_packet = read_tl_operator(packet[1:])
    else:
        # number_of_sub_packets_operator
        operator_packet, remaining_packet = read_sp_operator(packet[1:])

    return operator_packet, remaining_packet

def read_packet(packet: str):
    version = int(packet[:3], 2)
    packet_type = int(packet[3:6], 2)

    if packet_type == 4:
        # literal packet
        packet_value, remaining = read_literal(packet[6:])
    else:
        # operator packet
        packet_value, remaining = read_operator(packet[6:])

    return {"Version": version, "Type": packet_type, "Value": packet_value}, remaining

def hex_to_bin(hex_string: str) -> str:
    hex_to_bin_mapping = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    bin_strings = [hex_to_bin_mapping[h] for h in hex_string]

    return "".join(bin_strings)

def get_versions(packets):
    versions = []
    for p in packets:
        versions.append(p["Version"])
        if isinstance(p["Value"], list):
            versions.extend(get_versions(p["Value"]))

    return versions

literal_examples = [
    "11010001010", #10
    "110100101111111000101000", #2021
]

# example = "00111000000000000110111101000101001010010001001000000000"
# example = "11101110000000001101010000001100100000100011000001100000"

version_sum_examples = [
    "8A004A801A8002F478", # 16
    "620080001611562C8802118E34", # 12
    "C0015000016115A2E0802F182340", # 23
    "A0016C880162017C3686B18A3D4780", # 31
]

value_examples = [
    "C200B40A82", # 3
    "04005AC33890", # 54
    "880086C3E88112", # 7
    "CE00C43D881120", # 9
    "D8005AC2A8F0", # 1
    "F600BC2D8F", # 0
    "9C005AC2F8F0", # 0
    "9C0141080250320F1802104A08", # 1
]

with open("data-day16.txt") as f:
    hex_string = f.readline().strip()

parsed_packet, remaining = read_packet(hex_to_bin(value_examples[-1]))

print(parsed_packet)

def eval_packet(packet):
    if packet["Type"] == 4:
        value =  packet["Value"]
    else:
        op = types_to_op[packet["Type"]]
        value = op([eval_packet(p) for p in packet["Value"]])

    return value

print(eval_packet(parsed_packet))
