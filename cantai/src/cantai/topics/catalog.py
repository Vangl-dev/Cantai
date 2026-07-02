"""Catálogo único de temas do Cantai.

Cada hinário possui seus próprios nomes de temas. Este módulo define:
- CANONICAL_TOPICS: lista dos temas únicos do Cantai
- SYNONYMS: sinônimos que apontam para o tema canônico
- *_TO_CANONICAL: mapeamento dos temas originais de cada hinário para o canônico
"""

CANONICAL_TOPICS: list[str] = [
    "Adoração",
    "Louvor",
    "Santidade",
    "Trindade",
    "Santa Ceia",
    "Comunhão",
    "Natal",
    "Páscoa",
    "Pentecostes",
    "Missões",
    "Evangelização",
    "Consagração",
    "Confiança",
    "Esperança",
    "Consolo",
    "Chamado",
    "Oração",
    "Família",
    "Casamento",
    "Batismo",
    "Juventude",
    "Crianças",
    "Funeral",
    "Ressurreição",
    "Vida Cristã",
    "Gratidão",
    "Serviço",
    "Soberania de Deus",
    "Redenção",
    "Cruz",
    "Graça",
    "Salvação",
]

SYNONYMS: dict[str, list[str]] = {
    "Adoração": [
        "Adoração",
        "Exaltação",
        "Glória",
        "Magnificar",
        "Louvores ao Deus Trino",
        "Introito",
        "Convite à Adoração",
    ],
    "Louvor": [
        "Louvor",
        "Jubilação",
        "Gozo",
        "Satisfação",
    ],
    "Santidade": [
        "Santidade",
        "Afirmação de Fé",
        "Credo (Após o)",
        "Profissão de Fé",
        "Reforma Protestante",
    ],
    "Trindade": [
        "Trindade",
        "Deus, o Pai",
        "Deus, o Filho - Louvores",
        "Deus, o Espírito Santo",
        "Cristo, Rei do Universo",
    ],
    "Santa Ceia": [
        "Santa Ceia",
        "Santa Ceia (Após a Celebração da)",
        "Santa Ceia (Durante a)",
        "Igreja - Ceia do Senhor",
        "Partir do Pão (Após o)",
        "Oração Eucarística",
        "Oração Eucarística (Após a)",
        "Oração Eucarística (Na)",
        "Pai Nosso",
    ],
    "Comunhão": [
        "Comunhão",
        "Igreja",
        "União Fraternal",
    ],
    "Natal": [
        "Natal",
        "Ciclo do Natal",
        "Epifania",
        "Deus, o Filho - Natal",
    ],
    "Páscoa": [
        "Páscoa",
        "Tempo Pascal",
        "Semana da Paixão",
        "Domingo de Ramos",
        "Transfiguração do Senhor",
        "Ascensão do Senhor",
    ],
    "Pentecostes": [
        "Pentecostes",
        "Espírito Santo",
    ],
    "Missões": [
        "Missões",
        "Missão",
        "Envio",
        "Envio (Após o)",
        "FATIPI",
        "IPIB",
        "UMPI",
    ],
    "Evangelização": [
        "Evangelização",
        "Evangelho",
        "Culto - Evangelho",
        "Culto - Apelo",
        "Culto - Decisão",
        "Testemunho",
    ],
    "Consagração": [
        "Consagração",
        "Igreja - Consagração",
        "Ofertório",
        "Ofertório (Antes do)",
        "Primícias",
        "Obediência",
        "Diacônia",
        "Serviço",
    ],
    "Confiança": [
        "Confiança",
        "Firmeza",
        "Proteção e Ajuda",
        "Guia",
    ],
    "Esperança": [
        "Esperança",
        "Segunda Vinda",
        "Advento",
        "Passagem do Ano",
        "Ano Novo",
    ],
    "Consolo": [
        "Consolo",
        "Paz e Descanso",
        "Despedida",
    ],
    "Chamado": [
        "Chamado",
        "Admoestação",
    ],
    "Oração": [
        "Oração",
        "Oração por Iluminação",
        "Oração de Confissão (Antes ou após a)",
        "Oração de Confissão (Após a)",
        "Orações (Após as)",
        "Orações de Intercessão (Após as)",
        "Oração de Gratidão (Após a)",
        "Intercessão",
        "Súplica",
    ],
    "Família": [
        "Família",
        "Lar",
        "Aniversário",
        "Dia Internacional da Mulher",
        "Dia das Mães",
        "Dia dos Pais",
    ],
    "Casamento": [
        "Casamento",
        "Matrimônio",
    ],
    "Batismo": [
        "Batismo",
        "Batismo Infantil",
        "Batismo do Senhor",
        "Igreja - Batismo",
    ],
    "Juventude": [
        "Juventude",
    ],
    "Crianças": [
        "Crianças",
    ],
    "Funeral": [
        "Funeral",
    ],
    "Ressurreição": [
        "Ressurreição",
        "Deus, o Filho - Sua Ressurreição",
    ],
    "Vida Cristã": [
        "Vida Cristã",
        "Declaração de Perdão",
        "Declaração de Perdão (Após a)",
        "Confissão",
        "Contrição",
        "Quaresma",
        "Quaresma (Início da)",
    ],
    "Gratidão": [
        "Gratidão",
        "Ação de Graças",
    ],
    "Serviço": [
        "Serviço",
        "Diacônia",
    ],
    "Soberania de Deus": [
        "Soberania de Deus",
        "Glória",
    ],
    "Redenção": [
        "Redenção",
        "Paixão de Cristo",
        "Cruz",
    ],
    "Graça": [
        "Graça",
        "Emergência",
    ],
    "Salvação": [
        "Salvação",
        "Leitura da Palavra (Após a)",
        "Leitura do Evangelho (Antes ou após a)",
        "Leitura do Evangelho (Após a)",
        "Proclamação da Palavra (Após a)",
    ],
}


def _build_reverse_map() -> dict[str, str]:
    """Constrói mapeamento reverso: tema original (normalizado) → canônico."""
    reverse: dict[str, str] = {}
    for canonical, variants in SYNONYMS.items():
        for variant in variants:
            reverse[variant.lower().strip()] = canonical
    return reverse


_REVERSE_MAP = _build_reverse_map()


def resolve_topic(original: str) -> str:
    """Resolve um tema original para o tema canônico do Cantai.

    Se não encontrar mapeamento, retorna o tema original.
    """
    key = original.lower().strip()
    return _REVERSE_MAP.get(key, original)


def resolve_topics(original_topics: list[str]) -> list[str]:
    """Resolve uma lista de temas originais para canônicos, sem duplicatas.

    Retorna lista ordenada de temas canônicos únicos.
    """
    resolved = set()
    for t in original_topics:
        resolved.add(resolve_topic(t))
    return sorted(resolved)


CTP_TO_CANONICAL: dict[str, str] = {}
for _canon, _variants in SYNONYMS.items():
    for _v in _variants:
        CTP_TO_CANONICAL[_v.lower().strip()] = _canon

HARPAS_TO_CANONICAL: dict[str, str] = {}
for _canon, _variants in SYNONYMS.items():
    for _v in _variants:
        HARPAS_TO_CANONICAL[_v.lower().strip()] = _canon

CC_TO_CANONICAL: dict[str, str] = {}
for _canon, _variants in SYNONYMS.items():
    for _v in _variants:
        CC_TO_CANONICAL[_v.lower().strip()] = _canon

SH_TO_CANONICAL: dict[str, str] = {}
for _canon, _variants in SYNONYMS.items():
    for _v in _variants:
        SH_TO_CANONICAL[_v.lower().strip()] = _canon

NC_TO_CANONICAL: dict[str, str] = {}
for _canon, _variants in SYNONYMS.items():
    for _v in _variants:
        NC_TO_CANONICAL[_v.lower().strip()] = _canon
