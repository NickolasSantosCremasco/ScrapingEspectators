import re


KEYWORD_WEIGHTS = {
    "criando": 3,
    "construindo": 3,
    "empreendendo": 3,
    "startup": 2,
    "produto": 2,
    "negócio": 2,
    "aprendendo": 2,
    "estudando": 1,
    "python": 1,
    "programação": 1,
    "software": 1,
}


INTENT_PATTERNS = [
    r"estou tentando",
    r"quero aprender",
    r"não sei por onde começar",
    r"primeiro projeto",
    r"em transição",
]


def calculate_relevance_score(text: str) -> float:
    """
    Calcula score baseado em sinais de intenção e palavras-chave.
    """
    if not text:
        return 0.0

    text = text.lower()
    score = 0.0

    # Palavras-chave
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in text:
            score += weight

    # Padrões de intenção
    for pattern in INTENT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            score += 3

    return score