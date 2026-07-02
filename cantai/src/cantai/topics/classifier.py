"""Classificador de hinos por conteúdo textual (título, primeira linha, letra).

Utiliza palavras-chave para associar temas quando não há índice temático disponível.
"""

import re
import unicodedata

_KEYWORD_RULES: list[tuple[list[str], list[str]]] = [
    # Adoração
    (
        ["adorar", "adorai", "adoramos", "adoro", "adoração", "prostrar", "ajoelhar", "majestade"],
        ["Adoração"],
    ),
    # Louvor
    (
        ["louvar", "louvai", "louvor", "exaltar", "exaltação", "aleluias", "aleluia",
         "glorificar", "magnificar"],
        ["Louvor"],
    ),
    # Santidade
    (["santo", "santa", "santidade", "santificai", "sagrado"], ["Santidade"]),
    # Trindade
    (["trindade", "trílogo", "trino", "pai", "filho", "deus trino"], ["Trindade"]),
    # Santa Ceia
    (["ceia", "eucaristia", "pão", "cálice", "vinho", "partir o pão", "memorial"], ["Santa Ceia"]),
    # Natal
    (["belém", "natal", "nascimento", "presépio", "estrela", "magos", "menino jesus"], ["Natal"]),
    # Páscoa
    (["páscoa", "ressuscitou", "túmulo vazio", "vitória sobre a morte"], ["Páscoa"]),
    # Pentecostes
    (["pentecostes", "fogo", "línguas", "venting", "sopro", "spiit"], ["Pentecostes"]),
    # Missões
    (["missão", "missões", "evangelizar", "missionário", "ir até as nações", "mundi"], ["Missões"]),
    # Evangelização
    (["evangelho", "salvação", "converter", "conversão", "pregar", "proclamar"], ["Evangelização"]),
    # Consagração
    (["consagrar", "consagração", "entregar a vida", "dedicar", "ofertar"], ["Consagração"]),
    # Confiança
    (["confiar", "confiança", "amparo", "refúgio", "abrigo", "rocha", "força"], ["Confiança"]),
    # Esperança
    (["esperança", "esperar", "aguardar", "próxima vinda", "segunda vinda"], ["Esperança"]),
    # Consolo
    (["consolo", "conforto", "descanso", "paz", "tranquilidade", "alivio"], ["Consolo"]),
    # Chamado
    (["chamar", "chamado", "segue-me", "discípulo", "mandamentos"], ["Chamado"]),
    # Oração
    (["orar", "oração", "oramos", "súplica", "clamar", "implorar", "rogar"], ["Oração"]),
    # Família
    (["família", "lar", "casa", "mãe", "pai", "filhos", "irmãos"], ["Família"]),
    # Casamento
    (["casamento", "casar", "noivos", "esposa", "esposo", "matrimônio"], ["Casamento"]),
    # Batismo
    (["batismo", "batizar", "batizado", "águas", "imersão"], ["Batismo"]),
    # Funeral
    (["funeral", "sepultamento", "falecimento", "partiu", "eternidade", "túmulo"], ["Funeral"]),
    # Ressurreição
    (["ressurreição", "ressuscitou", "ressuscitar", "vivo está"], ["Ressurreição"]),
    # Vida Cristã
    (["vida cristã", "caminho", "perseverar", "fiel", "obediente"], ["Vida Cristã"]),
    # Gratidão
    (["agradecer", "gratidão", "graças", "agradecemos", "damos graças"], ["Gratidão"]),
    # Serviço
    (["servir", "serviço", "servir ao senhor", "diácono", "ministério"], ["Serviço"]),
    # Soberania de Deus
    (["soberano", "soberania", "onipotente", "providência"], ["Soberania de Deus"]),
    # Redenção
    (["redenção", "redimir", "resgatar", "libertar", "preço"], ["Redenção"]),
    # Cruz
    (["cruz", "crucificado", "crucifixão", "paixão", "sofrimento"], ["Cruz"]),
    # Graça
    (["graça", "gracioso", "misericórdia", "perdão", "perdoar"], ["Graça"]),
    # Salvação
    (["salvo", "salvar", "salvação", "libertação", "livre"], ["Salvação"]),
    # Comunhão
    (["comunhão", "unidade", "irmãos", "juntos", "igreja", "congregação"], ["Comunhão"]),
]


def classify_by_lyrics(title: str, first_line: str, lyrics: str) -> list[str]:
    """Classifica um hino com base em seu conteúdo textual.

    Analisa título, primeira linha e letra completa.
    Retorna lista de temas canônicos identificados.
    """
    text = f"{title} {first_line} {lyrics}".lower()
    text = _normalize(text)

    matched_topics: set[str] = set()

    for keywords, topics in _KEYWORD_RULES:
        for kw in keywords:
            kw_norm = _normalize(kw)
            if kw_norm in text:
                for topic in topics:
                    matched_topics.add(topic)
                break

    if not matched_topics:
        matched_topics = _extract_fallback_topics(text)

    return sorted(matched_topics)


def _normalize(text: str) -> str:
    """Normaliza texto para comparação."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _extract_fallback_topics(text: str) -> set[str]:
    """Extrai temas a partir das palavras mais relevantes quando nenhum keyword match."""
    fallback_words = {
        "esperança": "Esperança",
        "aleluia": "Louvor",
        "graça": "Graça",
        "jesus": "Adoração",
        "cristo": "Adoração",
        "reino": "Evangelização",
        "cordeiro": "Santa Ceia",
        "pai": "Trindade",
        "espírito": "Pentecostes",
        "amor": "Vida Cristã",
        "vida": "Vida Cristã",
        "luz": "Adoração",
        "paz": "Consolo",
        "força": "Confiança",
        "fiel": "Confiança",
        "bondade": "Graça",
        "misericordia": "Graça",
        "gloria": "Louvor",
        "triunfo": "Louvor",
        "vitória": "Louvor",
        "céu": "Esperança",
        "terra": "Missões",
        "mundo": "Missões",
        "nacoes": "Missões",
        "povo": "Comunhão",
        "igreja": "Comunhão",
    }

    matched: set[str] = set()
    for word, topic in fallback_words.items():
        if word in text:
            matched.add(topic)
            if len(matched) >= 3:
                break

    return matched
