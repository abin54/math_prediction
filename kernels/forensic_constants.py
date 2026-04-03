# Forensic Constants Hub: Ancient Science Mappings

# --- TAMIL ALPHABET PHONETIC FILTER (UYIR MEI) ---
# 12 Vowels (Uyir) x 18 Consonants (Mei) -> Vibrational Numbers 1-9
VOWELS = {
    "A": 1, "AA": 1, "I": 2, "II": 2, "U": 3, "UU": 3, 
    "E": 4, "EE": 4, "AI": 5, "O": 6, "OO": 6, "AU": 7
}
CONSONANTS = {
    "K": 1, "NG": 2, "CH": 3, "NJ": 4, "T": 5, "N": 6, 
    "TH": 7, "NP": 8, "M": 9, "Y": 1, "R": 2, "L": 3, 
    "V": 4, "ZH": 5, "LL": 6, "RR": 7, "NN": 8, "S": 9
}

# --- PANCHA BOOTHA (FIVE ELEMENTS) ---
# Fire, Earth, Air, Water, Ether
PANCHA_BOOTHA = {
    "FIRE": [1, 6],
    "EARTH": [2, 7],
    "AIR": [3, 8],
    "WATER": [4, 9],
    "ETHER": [5, 0]
}

# --- TAMIL HORA (PLANETARY CYCLE) ---
# Ruler of the Day and Hour
HORA_RULERS = {
    "SUN": [1, 4, 6],
    "MON": [2, 7],
    "MAR": [9],
    "MER": [5],
    "JUP": [3],
    "VEN": [6, 2],
    "SAT": [8, 0]
}

# --- NAKSHATRA (VIBRATIONAL POINTS) ---
# Ashwini to Revati (1-27) mapped to 1-9
NAKSHATRA_POINTS = {i: ((i-1) % 9) + 1 for i in range(1, 28)}

def get_element_of_number(n):
    for el, nums in PANCHA_BOOTHA.items():
        if n % 10 in nums:
            return el
    return "UNKNOWN"

def get_hora_of_number(n):
    for ruler, nums in HORA_RULERS.items():
        if n % 10 in nums:
            return ruler
    return "UNKNOWN"
