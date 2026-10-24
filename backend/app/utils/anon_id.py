import secrets

ADJECTIVES = ["kabut", "senja", "embun", "fajar", "malam", "hujan", "bayang", "sunyi"]
NOUNS = ["rahasia", "pelangi", "angin", "bulan", "kelana", "cahaya", "riak", "jejak"]


def generate_anon_id() -> str:
    adjective = secrets.choice(ADJECTIVES)
    noun = secrets.choice(NOUNS)
    number = secrets.randbelow(100)
    return f"{adjective}_{noun}{number:02d}"
