OFFSET = 1
TOTAL_COMBINATIONS = 256
BASE_DECIMAL = 10
BITS_PER_DIGIT = 4
DONT_CARE = "-"
ACTIVE_STATE = "1"

DECIMAL_TO_5421 = {
    0: "0000", 1: "0001", 2: "0010", 3: "0011", 4: "0100",
    5: "1000", 6: "1001", 7: "1010", 8: "1011", 9: "1100"
}
VALID_5421 = {val: key for key, val in DECIMAL_TO_5421.items()}

def get_decimal(binary_str: str) -> int:
    return VALID_5421.get(binary_str, -1)

def calc_result(val_a: int, val_b: int) -> str:
    total = val_a + val_b + OFFSET
    tens_bcd = DECIMAL_TO_5421[total // BASE_DECIMAL]
    units_bcd = DECIMAL_TO_5421[total % BASE_DECIMAL]
    return tens_bcd + units_bcd

def generate_truth_table() -> dict:
    truth_table = {}
    for idx in range(TOTAL_COMBINATIONS):
        bin_input = f"{idx:08b}"
        val_a = get_decimal(bin_input[:BITS_PER_DIGIT])
        val_b = get_decimal(bin_input[BITS_PER_DIGIT:])
        
        if val_a != -1 and val_b != -1:
            truth_table[bin_input] = calc_result(val_a, val_b)
        else:
            truth_table[bin_input] = DONT_CARE * 8
            
    return truth_table

def diff_one_bit(term1: str, term2: str) -> bool:
    diff_count = sum(1 for bit1, bit2 in zip(term1, term2) if bit1 != bit2)
    return diff_count == 1

def merge_terms(term1: str, term2: str) -> str:
    merged = [bit1 if bit1 == bit2 else DONT_CARE for bit1, bit2 in zip(term1, term2)]
    return "".join(merged)

def get_prime_implicants(terms: set[str]) -> set[str]:
    new_terms, used_terms = set(), set()
    terms_list = list(terms)
    for idx, term1 in enumerate(terms_list):
        for term2 in terms_list[idx + 1:]:
            if diff_one_bit(term1, term2):
                new_terms.add(merge_terms(term1, term2))
                used_terms.update([term1, term2])
                
    new_terms.update(terms - used_terms)
    return new_terms

def get_all_implicants(terms_set: set[str]) -> set[str]:
    current_terms = terms_set
    while True:
        next_terms = get_prime_implicants(current_terms)
        if next_terms == current_terms:
            break
        current_terms = next_terms
    return current_terms

def covers_minterm(implicant: str, minterm: str) -> bool:
    return all(imp == min_bit or imp == DONT_CARE for imp, min_bit in zip(implicant, minterm))

def update_covered_minterms(implicant: str, ones_set: set[str], covered: set[str]):
    for one_term in ones_set:
        if covers_minterm(implicant, one_term):
            covered.add(one_term)

def filter_essential(implicants: set[str], ones_set: set[str]) -> set[str]:
    covered_minterms, result_implicants = set(), set()
    sorted_implicants = sorted(list(implicants), key=lambda x: x.count(DONT_CARE), reverse=True)
    
    for implicant in sorted_implicants:
        covers_new = any(covers_minterm(implicant, one) and one not in covered_minterms 
                         for one in ones_set)
        if covers_new:
            result_implicants.add(implicant)
            update_covered_minterms(implicant, ones_set, covered_minterms)
            
    return result_implicants

def minimize_function(truth_table: dict, out_idx: int) -> set[str]:
    ones_set = {in_bits for in_bits, out_bits in truth_table.items() 
                if out_bits[out_idx] == ACTIVE_STATE}
    dcs_set = {in_bits for in_bits, out_bits in truth_table.items() 
               if out_bits[out_idx] == DONT_CARE}
    
    all_implicants = get_all_implicants(ones_set | dcs_set)
    return filter_essential(all_implicants, ones_set)