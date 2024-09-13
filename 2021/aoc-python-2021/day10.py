import statistics

score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

opening_chars = ["(", "[", "{", "<"]
closing_chars = [")", "]", "}", ">"]

closer_for_opener = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

def score_completion(completion):
    score = 0
    char_scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    for ch in completion:
        score = score * 5
        score = score + char_scores[ch]

    return score

def matches(opener, closer):
    return closer == closer_for_opener[opener]

class Chunk:
    def __init__(self, opener=None, closer=None) -> None:
        self.opener = opener
        self.closer = closer

    def __repr__(self) -> str:
        return f"Chunk: opener: {self.opener}, closer: {self.closer}"

    def is_complete(self) -> bool:
        return (
            (self.opener is not None )
            and (self.closer is not None)
        )

    def is_corrupt(self) -> bool:
        return self.is_complete() and not matches(self.opener, self.closer)

def read_line(l, current_chunks=[]):
    chunks = []

    if len(l) == 0: return chunks

    token = l.pop(0)
    if token in opening_chars:
        chunk = Chunk(opener=token)
        current_chunks.append(chunk)

        chunks = read_line(l, current_chunks=current_chunks)
        chunks = [chunk] + chunks

    elif (token in closing_chars) and current_chunks:
        current_chunks.pop().closer = token
        chunks = read_line(l, current_chunks=current_chunks)

    return chunks


with open("data-day10.txt") as f:
    lines = [ list(l.strip()) for l in f.readlines()]

invalid_chars = []

lines_as_chunks = [read_line(l) for l in lines]

for l in lines_as_chunks:
    invalid_chunks = [c for c in l if c.is_corrupt()]
    invalid_chars.extend(c.closer for c in invalid_chunks)

print("Sum of corrupt chars: ", sum(score_table[ch] for ch in invalid_chars))

completion_scores = []

for l in lines_as_chunks:
    if any(c.is_corrupt() for c in l): continue
    incomplete_chunks = [c for c in l if not c.is_complete()]
    # close in reverse
    completion = [closer_for_opener[c.opener] for c in incomplete_chunks[::-1]]
    completion_scores.append(score_completion(completion))

print("Median completion score: ", statistics.median(completion_scores))
