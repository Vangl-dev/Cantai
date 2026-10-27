"""Importa o Novo Cântico (NC) do PDF (e-book da novocantico.com.br).

Cada hino começa numa página nova, com um bloco de cabeçalho à esquerda
("110-A Crer e observar") seguido de um bloco por estrofe. A página 1 é
de direitos autorais.

O hinário é organizado por assunto em faixas contínuas de números; os temas
abaixo foram transcritos do "Índice por Assunto" (temas novo cantico.pdf,
que é uma imagem).
"""

import re
from pathlib import Path

from cantai.textnorm import strip_verse_number

HYMNAL = "NC"

_HEADER = re.compile(r"^(\d{1,3})(?:-([A-Z]))?\s+(.+)$")

# (primeiro hino da seção, tema)
SECTIONS: list[tuple[int, str]] = [
    (1, "Intróitos"), (3, "Deus Trino"), (11, "Deus Santo"), (15, "Deus Soberano"),
    (22, "Deus Criador"), (30, "Deus Providente"), (32, "Deus Fiel"),
    (35, "Deus Senhor"), (38, "Deus Salvador"), (49, "Deus Vencedor"),
    (55, "Gratidão"), (66, "Contrição e Arrependimento"), (77, "Perdão"),
    (81, "Espírito Instruidor"), (85, "Espírito Consolador"),
    (86, "Espírito Vivificador"), (87, "Amor de Deus"), (91, "Fé"),
    (94, "Salvação"), (99, "Testemunho"), (107, "Companhia do Senhor"),
    (116, "Aspiração"), (127, "Oração"), (131, "Santificação"), (136, "Proteção"),
    (156, "Confiança"), (175, "Fidelidade"), (178, "Fraternidade"),
    (184, "Esperança"), (192, "Lar Celestial"), (197, "Convite"), (212, "Decisão"),
    (217, "Submissão"), (219, "Dedicação"), (226, "Advento"), (230, "Natal"),
    (250, "Ministério"), (257, "Entrada Triunfal"), (260, "Paixão e Morte"),
    (271, "Ressurreição"), (280, "Ascensão"), (282, "A Grande Comissão"),
    (290, "Segunda Vinda"), (298, "Igreja Militante"), (302, "Evangelização"),
    (311, "Trabalho Cristão"), (322, "Sociedade Auxiliadora Feminina"),
    (326, "União Presbiteriana de Homens"), (327, "Discipulado e Serviço"),
    (329, "Posse de Pastor"), (330, "Batismo"), (334, "Convertidos"),
    (337, "Profissão de Fé"), (340, "Ceia do Senhor"), (347, "Dia do Senhor"),
    (350, "Escola Dominical"), (355, "Crianças"), (368, "Despedida"),
    (369, "Bíblia"), (373, "Ano Novo"), (376, "Pátria"), (381, "Cidade"),
    (382, "Mocidade"), (393, "Casamento"), (395, "Lar Cristão"),
    (396, "Aniversário"), (397, "Mãe"), (398, "Final de Culto"),
]
_OFFERTORY = "Ofertório e Améns"


def section_for(number: int, variant: str | None = None) -> str:
    """Tema (seção do índice por assunto) de um hino do NC."""
    if number == 400 and variant:
        return _OFFERTORY
    topic = SECTIONS[0][1]
    for start, name in SECTIONS:
        if number >= start:
            topic = name
    return topic


def import_novo_cantico(pdf_path: str | Path) -> list[dict]:
    """Importa os hinos numerados do Novo Cântico."""
    import pymupdf

    hymns: list[dict] = []
    current: dict | None = None
    with pymupdf.open(str(pdf_path)) as doc:
        for page_number, page in enumerate(doc):
            if page_number == 0:
                continue
            for block in page.get_text("blocks"):
                x0, text = block[0], block[4].strip()
                if not text:
                    continue
                header = _HEADER.match(text) if x0 < 20 and "\n" not in text else None
                if header:
                    number, variant = int(header.group(1)), header.group(2)
                    current = {
                        "number": number,
                        "variant": variant,
                        "title": header.group(3).strip(),
                        "stanzas": [],
                    }
                    hymns.append(current)
                elif x0 < 20:
                    current = None  # cabeçalho sem número (améns finais)
                elif current is not None:
                    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                    current["stanzas"].append("\n".join(lines))

    result = []
    for hymn in hymns:
        lyrics = "\n\n".join(hymn.pop("stanzas"))
        title = hymn["title"]
        hymn["title"] = title[0].upper() + title[1:]
        hymn["lyrics"] = lyrics
        hymn["first_line"] = strip_verse_number(lyrics.split("\n")[0]) if lyrics else ""
        hymn["topics"] = [section_for(hymn["number"], hymn["variant"])]
        result.append(hymn)
    return result
