"""Catálogo único de temas do Cantai.

Cada hinário possui seus próprios nomes de temas. Este módulo define:
- CANONICAL_TOPICS: lista dos temas únicos do Cantai
- SYNONYMS: sinônimos que apontam para o tema canônico
- *_TO_CANONICAL: mapeamento dos temas originais de cada hinário para o canônico
"""

CANONICAL_TOPICS: list[str] = [
    "Ação de Graças",
    "Adoração",
    "Advento",
    "Afirmação de Fé",
    "Aniversário",
    "Ano Novo",
    "Ascensão do Senhor",
    "Batismo",
    "Batismo do Senhor",
    "Batismo Infantil",
    "Bênção",
    "Casamento",
    "Ciclo do Natal",
    "Comunhão",
    "Confiança",
    "Confissão",
    "Consagração",
    "Contrição",
    "Convite à Adoração",
    "Credo",
    "Crianças",
    "Cristo Rei",
    "Declaração de Perdão",
    "Dia da Mulher",
    "Dia do Senhor",
    "Dia dos Pais",
    "Diaconia",
    "Domingo de Ramos",
    "Emerência",
    "Envio",
    "Epifania",
    "Espírito Santo",
    "Evangelho",
    "Família",
    "FATIPI",
    "Funeral",
    "Igreja",
    "Intercessão",
    "Introito",
    "IPIB",
    "Jubilação",
    "Juventude",
    "Leitura da Palavra",
    "Leitura do Evangelho",
    "Louvor",
    "Missão",
    "Missões",
    "Natal",
    "Ofertório",
    "Oração",
    "Oração de Confissão",
    "Oração de Gratidão",
    "Oração Eucarística",
    "Oração por Iluminação",
    "Orações",
    "Pai Nosso",
    "Paixão de Cristo",
    "Palavra de Deus",
    "Páscoa",
    "Partir do Pão",
    "Pátria",
    "Pentecostes",
    "Primícias",
    "Proclamação da Palavra",
    "Profissão de Fé",
    "Quaresma",
    "Reforma",
    "Ressurreição",
    "Santa Ceia",
    "Santificação",
    "Saudação da Paz",
    "Segunda Vinda",
    "Semana da Paixão",
    "Tempo Pascal",
    "Testemunho",
    "Transfiguração do Senhor",
    "Trindade",
    "UMPI",
]

SYNONYMS: dict[str, list[str]] = {
    "Ação de Graças": [
        "Ação de Graças",
        "Gratidão",
        "GRATIDÃO",
    ],
    "Adoração": [
        "Adoração",
        "Louvor",
        "Louvores",
        "Adoração e Louvor",
        "Exaltação",
        "Glória",
        "Magnificar",
        "Deus, o Filho - Louvores",
        "Culto - Abertura",
    ],
    "Advento": [
        "Advento",
        "Esperança",
    ],
    "Afirmação de Fé": [
        "Afirmação de Fé",
        "Credo (Após o)",
        "Profissão de Fé",
    ],
    "Aniversário": [
        "Aniversário",
    ],
    "Ano Novo": [
        "Ano Novo",
        "Passagem do Ano",
        "Passagem do ano",
        "ANO NOVO",
    ],
    "Ascensão do Senhor": [
        "Ascensão do Senhor",
        "Ascensão",
    ],
    "Batismo": [
        "Batismo",
        "Batismo nas águas",
        "Igreja - Batismo",
        "BATISMO",
    ],
    "Batismo do Senhor": [
        "Batismo do Senhor",
    ],
    "Batismo Infantil": [
        "Batismo Infantil",
    ],
    "Bênção": [
        "Bênção",
        "Bênção Apostólica",
    ],
    "Casamento": [
        "Casamento",
        "Matrimônio",
        "X. IGREJA - G. Casamento",
    ],
    "Ciclo do Natal": [
        "Ciclo do Natal",
    ],
    "Comunhão": [
        "Comunhão",
        "União Fraternal",
    ],
    "Confiança": [
        "Confiança",
        "Firmeza",
        "Proteção e Ajuda",
        "Guia",
    ],
    "Confissão": [
        "Confissão",
    ],
    "Consagração": [
        "Consagração",
        "Igreja - Consagração",
        "Obediência",
        "VIDA CRISTA - CONSAGRAÇÃO",
    ],
    "Contrição": [
        "Contrição",
    ],
    "Convite à Adoração": [
        "Convite à Adoração",
        "Convite à Adoração e Louvor",
        "Louvores ao Deus Trino",
        "Introito",
    ],
    "Credo": [
        "Credo",
    ],
    "Crianças": [
        "Crianças",
        "CRIANÇAS",
        "XII. CRIANÇAS",
    ],
    "Cristo Rei": [
        "Cristo Rei",
        "Cristo, Rei do Universo",
    ],
    "Declaração de Perdão": [
        "Declaração de Perdão",
        "Perdão",
    ],
    "Dia da Mulher": [
        "Dia da Mulher",
        "Dia Internacional da Mulher",
        "Dia das Mães",
    ],
    "Dia do Senhor": [
        "Dia do Senhor",
    ],
    "Dia dos Pais": [
        "Dia dos Pais",
    ],
    "Diaconia": [
        "Diaconia",
        "Diacônia",
    ],
    "Domingo de Ramos": [
        "Domingo de Ramos",
        "Entrada Triunfal",
    ],
    "Emerência": [
        "Emerência",
        "Emergência",
    ],
    "Envio": [
        "Envio",
        "Envio (Após o)",
        "Comissionamento",
        "FATIPI",
        "IPIB",
        "UMPI",
    ],
    "Epifania": [
        "Epifania",
        "Manifestação de Cristo",
    ],
    "Espírito Santo": [
        "Espírito Santo",
        "Deus, o Espírito Santo",
        "ESPÍRITO SANTO",
    ],
    "Evangelho": [
        "Evangelho",
        "Salvação",
        "Culto - Evangelho",
    ],
    "Família": [
        "Família",
        "Lar",
    ],
    "FATIPI": [
        "FATIPI",
    ],
    "Funeral": [
        "Funeral",
        "Consolação",
    ],
    "Igreja": [
        "Igreja",
    ],
    "Intercessão": [
        "Intercessão",
    ],
    "Introito": [
        "Introito",
    ],
    "IPIB": [
        "IPIB",
    ],
    "Jubilação": [
        "Jubilação",
    ],
    "Juventude": [
        "Juventude",
        "Mocidade",
    ],
    "Leitura da Palavra": [
        "Leitura da Palavra",
        "Leitura da Palavra (Após a)",
        "Leitura Bíblica",
        "Para Leitura Bíblica",
    ],
    "Leitura do Evangelho": [
        "Leitura do Evangelho",
        "Leitura do Evangelho (Antes ou após a)",
        "Leitura do Evangelho (Após a)",
    ],
    "Louvor": [
        "Louvor",
    ],
    "Missão": [
        "Missão",
        "Evangelização",
    ],
    "Missões": [
        "Missões",
        "Evangelização Mundial",
    ],
    "Natal": [
        "Natal",
        "Nascimento",
        "Nascimento de Cristo",
        "Deus, o Filho - Natal",
        "Seu nascimento (Natal)",
        "CRISTO - NATAL DE",
    ],
    "Ofertório": [
        "Ofertório",
        "Ofertório (Antes do)",
    ],
    "Oração": [
        "Oração",
        "Súplica",
        "Clamor",
        "Reunião de Oração",
        "IX. ORAÇÃO E SÚPLICA",
    ],
    "Oração de Confissão": [
        "Oração de Confissão",
        "Oração de Confissão (Antes ou após a)",
        "Oração de Confissão (Após a)",
    ],
    "Oração de Gratidão": [
        "Oração de Gratidão",
        "Oração de Gratidão (Após a)",
    ],
    "Oração Eucarística": [
        "Oração Eucarística",
        "Oração Eucarística (Após a)",
        "Oração Eucarística (Na)",
    ],
    "Oração por Iluminação": [
        "Oração por Iluminação",
    ],
    "Orações": [
        "Orações",
        "Orações (Após as)",
        "Orações de Intercessão (Após as)",
    ],
    "Pai Nosso": [
        "Pai Nosso",
    ],
    "Paixão de Cristo": [
        "Paixão de Cristo",
        "Cruz",
    ],
    "Palavra de Deus": [
        "Palavra de Deus",
        "Bíblia",
        "Escrituras",
        "A Palavra do Senhor",
        "BÍBLIA",
        "Culto - Palavra do Senhor",
    ],
    "Páscoa": [
        "Páscoa",
        "Tempo Pascal",
        "Semana da Paixão",
        "Transfiguração do Senhor",
    ],
    "Partir do Pão": [
        "Partir do Pão",
        "Partir do Pão (Após o)",
    ],
    "Pátria": [
        "Pátria",
    ],
    "Pentecostes": [
        "Pentecostes",
    ],
    "Primícias": [
        "Primícias",
    ],
    "Proclamação da Palavra": [
        "Proclamação da Palavra",
        "Proclamação da Palavra (Após a)",
    ],
    "Profissão de Fé": [
        "Profissão de Fé",
    ],
    "Quaresma": [
        "Quaresma",
        "Quaresma (Início da)",
    ],
    "Reforma": [
        "Reforma",
        "Reforma Protestante",
    ],
    "Ressurreição": [
        "Ressurreição",
        "Ressurreição e Ascensão",
        "Deus, o Filho - Sua Ressurreição",
        "Sua ressurreição",
        "CRISTO - RESSURREIÇÃO DE",
    ],
    "Santa Ceia": [
        "Santa Ceia",
        "Ceia do Senhor",
        "Santa Ceia (Após a)",
        "Santa Ceia (Após a Celebração da)",
        "Santa Ceia (Durante a)",
        "Ceia",
        "Igreja - Ceia do Senhor",
    ],
    "Santificação": [
        "Santificação",
        "Vida Santa",
        "Santidade",
    ],
    "Saudação da Paz": [
        "Saudação da Paz",
    ],
    "Segunda Vinda": [
        "Segunda Vinda",
        "Volta de Cristo",
        "Volta do Senhor",
        "Sua segunda vinda",
        "CRISTO - A VOLTA DE",
    ],
    "Semana da Paixão": [
        "Semana da Paixão",
    ],
    "Tempo Pascal": [
        "Tempo Pascal",
    ],
    "Testemunho": [
        "Testemunho",
    ],
    "Transfiguração do Senhor": [
        "Transfiguração do Senhor",
    ],
    "Trindade": [
        "Trindade",
        "Deus, o Pai",
    ],
    "UMPI": [
        "UMPI",
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
