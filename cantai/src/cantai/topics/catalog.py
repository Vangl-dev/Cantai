"""Catálogo único de temas do Cantai.

Cada hinário possui seus próprios nomes de temas. Este módulo define:
- CANONICAL_TOPICS: lista dos temas únicos do Cantai
- SYNONYMS: sinônimos que apontam para o tema canônico
- *_TO_CANONICAL: mapeamento dos temas originais de cada hinário para o canônico
"""

CANONICAL_TOPICS: list[str] = [
    "Adoração",
    "Santidade",
    "Trindade",
    "Ceia do Senhor",
    "Natal",
    "Páscoa",
    "Pentecostes",
    "Espírito Santo",
    "Missões",
    "Evangelização",
    "Consagração",
    "Confiança",
    "Esperança",
    "Despedida",
    "Chamado",
    "Oração",
    "Família",
    "Casamento",
    "Batismo",
    "Juventude",
    "Crianças",
    "Funeral",
    "Ressurreição",
    "Segunda Vinda",
    "Vida Cristã",
    "Gratidão",
    "Ano Novo",
    "Palavra de Deus",
    "Serviço",
    "Soberania de Deus",
    "Redenção",
    "Graça",
    "Salvação",
]

SYNONYMS: dict[str, list[str]] = {
    "Adoração": [
        "Adoração",
        "Louvor",
        "Louvores",
        "Adoração e Louvor",
        "Convite à Adoração",
        "Convite à Adoração e Louvor",
        "Louvores ao Deus Trino",
        "Exaltação",
        "Glória",
        "Magnificar",
        "Introito",
        "Deus, o Filho - Louvores",
        "Culto - Abertura",
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
        "Cristo, Rei do Universo",
    ],
    "Ceia do Senhor": [
        "Ceia do Senhor",
        "Santa Ceia",
        "Santa Ceia (Após a Celebração da)",
        "Santa Ceia (Durante a)",
        "Comunhão",
        "Ceia",
        "Igreja - Ceia do Senhor",
        "Partir do Pão (Após o)",
        "Oração Eucarística",
        "Oração Eucarística (Após a)",
        "Oração Eucarística (Na)",
        "Pai Nosso",
        "Igreja",
        "União Fraternal",
    ],
    "Natal": [
        "Natal",
        "Nascimento",
        "Ciclo do Natal",
        "Epifania",
        "Deus, o Filho - Natal",
        "Seu nascimento (Natal)",
        "CRISTO - NATAL DE",
        "IV. JESUS CRISTO - B. Nascimento",
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
    ],
    "Espírito Santo": [
        "Espírito Santo",
        "Deus, o Espírito Santo",
        "ESPÍRITO SANTO",
        "V. ESPÍRITO SANTO",
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
        "VIDA CRISTA - CONSAGRAÇÃO",
        "VIII. VIDA CRISTÃ - C. Consagração Pessoal",
    ],
    "Confiança": [
        "Confiança",
        "Firmeza",
        "Proteção e Ajuda",
        "Guia",
        "VIII. VIDA CRISTÃ - J. Confiança",
    ],
    "Esperança": [
        "Esperança",
        "Advento",
    ],
    "Despedida": [
        "Despedida",
        "Consolo",
        "Encerramento",
        "Final do Culto",
        "Paz e Descanso",
        "SAUDAÇÕES - DESPEDIDAS",
        "VI. CULTO PÚBLICO - F. Encerramento do Culto",
        "XIII. ASSUNTOS ESPECIAIS - L. Despedida",
        "Culto - Encerramento",
    ],
    "Chamado": [
        "Chamado",
        "Admoestação",
    ],
    "Oração": [
        "Oração",
        "Súplica",
        "Clamor",
        "Reunião de Oração",
        "Oração por Iluminação",
        "Oração de Confissão (Antes ou após a)",
        "Oração de Confissão (Após a)",
        "Orações (Após as)",
        "Orações de Intercessão (Após as)",
        "Oração de Gratidão (Após a)",
        "Intercessão",
        "IX. ORAÇÃO E SÚPLICA",
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
        "X. IGREJA - G. Casamento",
    ],
    "Batismo": [
        "Batismo",
        "Batismo Infantil",
        "Batismo do Senhor",
        "Batismo nas águas",
        "Igreja - Batismo",
        "BATISMO",
        "X. IGREJA - B. Batismo e Recepção de Membros",
    ],
    "Juventude": [
        "Juventude",
    ],
    "Crianças": [
        "Crianças",
        "CRIANÇAS",
        "XII. CRIANÇAS",
    ],
    "Funeral": [
        "Funeral",
    ],
    "Ressurreição": [
        "Ressurreição",
        "Ascensão",
        "Deus, o Filho - Sua Ressurreição",
        "Sua ressurreição",
        "CRISTO - RESSURREIÇÃO DE",
        "IV. JESUS CRISTO - F. Ressurreição e Ascenção",
    ],
    "Segunda Vinda": [
        "Segunda Vinda",
        "Volta de Cristo",
        "Volta do Senhor",
        "Sua segunda vinda",
        "CRISTO - A VOLTA DE",
        "IV. JESUS CRISTO - G. Segunda Vinda",
    ],
    "Vida Cristã": [
        "Vida Cristã",
        "Declaração de Perdão",
        "Declaração de Perdão (Após a)",
        "Confissão",
        "Contrição",
        "Quaresma",
        "Quaresma (Início da)",
        "VIII. VIDA CRISTÃ",
    ],
    "Gratidão": [
        "Gratidão",
        "Ação de Graças",
        "GRATIDÃO",
        "VIII. VIDA CRISTÃ - H. Gratidão e Ação de graças",
    ],
    "Ano Novo": [
        "Ano Novo",
        "Passagem do Ano",
        "Passagem do ano",
        "ANO NOVO",
        "XIII. ASSUNTOS ESPECIAIS - A. Ano Novo",
    ],
    "Palavra de Deus": [
        "Palavra de Deus",
        "Bíblia",
        "Leitura Bíblica",
        "A Palavra do Senhor",
        "BÍBLIA",
        "XIII. ASSUNTOS ESPECIAIS - E. Bíblia",
        "VI. CULTO PÚBLICO - D. Para Leitura Bíblica",
        "Culto - Palavra do Senhor",
    ],
    "Serviço": [
        "Serviço",
        "Diacônia",
    ],
    "Soberania de Deus": [
        "Soberania de Deus",
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
