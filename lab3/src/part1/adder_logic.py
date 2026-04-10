INPUT_COMBINATIONS = [
    (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
    (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)
]
ACTIVE_STATE = 1

def calculate_sum(bit_a: int, bit_b: int, carry_in: int) -> int:
    return bit_a ^ bit_b ^ carry_in

def calculate_carry_out(bit_a: int, bit_b: int, carry_in: int) -> int:
    return (bit_a and bit_b) or (carry_in and (bit_a ^ bit_b))

def generate_truth_table() -> list[dict]:
    table = []
    for a, b, cin in INPUT_COMBINATIONS:
        table.append({
            "a": a, "b": b, "cin": cin,
            "sum": calculate_sum(a, b, cin),
            "cout": calculate_carry_out(a, b, cin)
        })
    return table

def build_sdnf_term(a: int, b: int, cin: int) -> str:
    term_a = "a" if a == ACTIVE_STATE else "!a"
    term_b = "b" if b == ACTIVE_STATE else "!b"
    term_c = "cin" if cin == ACTIVE_STATE else "!cin"
    return f"({term_a} & {term_b} & {term_c})"

def get_sdnf(truth_table: list[dict], target: str) -> str:
    terms = [build_sdnf_term(row["a"], row["b"], row["cin"])
             for row in truth_table if row[target] == ACTIVE_STATE]
    return " | ".join(terms)

def diff_by_one_bit(term1: str, term2: str) -> bool:
    return sum(1 for b1, b2 in zip(term1, term2) if b1 != b2) == 1

def merge_terms(term1: str, term2: str) -> str:
    return "".join(b1 if b1 == b2 else '-' for b1, b2 in zip(term1, term2))

def get_prime_implicants(minterms: set[str]) -> set[str]:
    new_terms, used = set(), set()
    terms_list = list(minterms)
    for i, t1 in enumerate(terms_list):
        for t2 in terms_list[i + 1:]:
            if diff_by_one_bit(t1, t2):
                new_terms.add(merge_terms(t1, t2))
                used.update([t1, t2])
    new_terms.update(minterms - used)
    return new_terms

def minimize(minterms: set[str]) -> set[str]:
    current_terms = minterms
    while True:
        next_terms = get_prime_implicants(current_terms)
        if next_terms == current_terms:
            break
        current_terms = next_terms
    return current_terms

def get_minterms_binary(truth_table: list[dict], target: str) -> set[str]:
    return {f"{r['a']}{r['b']}{r['cin']}" for r in truth_table if r[target] == ACTIVE_STATE}