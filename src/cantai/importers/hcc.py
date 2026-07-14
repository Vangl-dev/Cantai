"""Importador do HCC com arquitetura de relacionamentos."""

import json
from pathlib import Path
from typing import Any


# Equivalências de conteúdo confirmadas (Sprint 30)
CONTENT_EQUIVALENCES: dict[int, int] = {
    14: 56,   # LEONI
    25: 63,   # FAITHFULNESS
    34: 13,   # NATIONAL HYMN
    37: 163,  # GOD BE WITH YOU
    72: 23,   # AZMON
    91: 337,  # STILLE NACHT
    132: 368, # OLD RUGGED CROSS
    182: 190, # BLOTT EN DAG
    187: 188, # CRIMOND
    299: 103, # THE GOSPEL BELLS
    300: 237, # WOODWORTH
    329: 208, # VILLE DE HAVRE
    384: 261, # PAI NOSSO SERTANEJO
    395: 366, # NEAR THE CROSS
    399: 180, # BETHANY
    406: 409, # EIN' FESTE BURG
    465: 107, # TRUST AND OBEY
    510: 359, # BELÉM
    553: 293, # MEGALÓPOLIS
    574: 260, # MORRIS
}

# Mapeamento de tópicos HCC para canônicos
HCC_TO_CANONICAL: dict[str, str] = {
    "HCC-A PALAVRA DE DEUS": "Leitura da Palavra",
    "HCC-ADORAÇÃO E LOUVOR": "Adoração",
    "HCC-ALEGRIA CRISTÃ": "Gozo",
    "HCC-ANIVERSÁRIO": "Aniversário",
    "HCC-ANO NOVO": "Ano Novo",
    "HCC-BATISMO": "Batismo",
    "HCC-BÊNÇÃO": "Benção",
    "HCC-CASAMENTO": "Casamento",
    "HCC-COMUNHÃO": "Comunhão",
    "HCC-CONFIANÇA EM DEUS": "Confiança",
    "HCC-CONSAGRAÇÃO": "Consagracao",
    "HCC-CREDO": "Afirmação de Fé",
    "HCC-CRIANÇAS": "Criancas",
    "HCC-DEUS TRIÚNO": "Trindade",
    "HCC-DEUS, O ESPÍRITO SANTO": "Espirito Santo",
    "HCC-DEUS, O FILHO": "Adoração",
    "HCC-DEUS, O PAI": "Trindade",
    "HCC-DESPEDIDA": "Despedida",
    "HCC-ECOLOGIA": "Creacao",
    "HCC-ENSINO": "Leitura da Palavra",
    "HCC-ENVIO": "Envio",
    "HCC-ESPERANÇA": "Confiança",
    "HCC-ESPIRITO SANTO": "Espirito Santo",
    "HCC-EUCARISTIA": "Comunhao",
    "HCC-FAMÍLIA": "Familia",
    "HCC-FÉ": "Afirmação de Fé",
    "HCC-FORA DE SÉRIE": None,
    "HCC-FUNERAL": "Funeral",
    "HCC-GRAÇA": "Graca",
    "HCC-GOVERNO": "Patria",
    "HCC-INTERCESSÃO": "Intercessao",
    "HCC-IGREJA": "Igreja",
    "HCC-JULGAMENTO": "Segunda Vinda",
    "HCC-JUVENTUDE": "Juventude",
    "HCC-LOUVOR": "Adoracao",
    "HCC-MISSÕES": "Missoes",
    "HCC-MÚSICA SACRA": "Adoracao",
    "HCC-NATAL": "Natal",
    "HCC-OBRIGAÇÕES CRISTÃS": "Vida Crista",
    "HCC-OFERTÓRIO": "Ofertorio",
    "HCC-ORAÇÃO": "Oracao",
    "HCC-ORAÇÃO PELA IGREJA": "Igreja",
    "HCC-PAÍS": "Patria",
    "HCC-PAIXÃO E MORTE DE CRISTO": "Paixao de Cristo",
    "HCC-PALAVRA DE DEUS": "Leitura da Palavra",
    "HCC-PASCOA": "Pascoa",
    "HCC-PENTECOSTES": "Pentecostes",
    "HCC-POVO DE DEUS": "Igreja",
    "HCC-PROFECIAS": "Segunda Vinda",
    "HCC-QUIXAMBU": None,
    "HCC-RAiva": None,
    "HCC-RECONCILIAÇÃO": "Confissao",
    "HCC-REDENÇÃO": "Salvacao",
    "HCC-REFORMA": "Reforma",
    "HCC-RESSURREIÇÃO": "Ressurreicao",
    "HCC-SAUDADES": None,
    "HCC-SALMOS": "Louvor",
    "HCC-SANTIFICAÇÃO": "Santificacao",
    "HCC-SATANÁS": None,
    "HCC-SEGUNDA VINDA": "Segunda Vinda",
    "HCC-SERVIÇO CRISTÃO": "Servico",
    "HCC-SOCIEDADE": None,
    "HCC-SUPPLICA": "Oracao",
    "HCC-TEMPO": "Natal",
    "HCC-TESTEMUNHO": "Testemunho",
    "HCC-VIDA CRISTA": "Vida Crista",
    "HCC-VIRTUDES CRISTÃS": "Vida Crista",
}


def load_hcc_data(data_dir: Path) -> dict[str, Any]:
    """Carrega todos os dados processados do HCC."""
    cantai_dir = data_dir / "Cantai" / "cantai"
    with open(cantai_dir / "data" / "output" / "cantai.json", "r") as f:
        hcc_json = json.load(f)

    with open(cantai_dir / "data" / "temp" / "temas_hcc_topics.json", "r") as f:
        topics = json.load(f)

    with open(cantai_dir / "data" / "temp" / "metricas_hcc_final.json", "r") as f:
        metrics = json.load(f)

    with open(cantai_dir / "data" / "temp" / "melodias_hcc.json", "r") as f:
        melodies = json.load(f)

    return {
        "hymns": hcc_json["hymns"],
        "topics": topics,
        "metrics": metrics,
        "melodies": melodies,
    }


def build_topic_index(topics: dict) -> dict[int, list[str]]:
    """Constrói índice de hino → tópicos."""
    index: dict[int, list[str]] = {}
    for topic_name, data in topics.items():
        for hymn_info in data.get("hymns", []):
            num = int(hymn_info["number"])
            if num not in index:
                index[num] = []
            index[num].append(topic_name)
    return index


def load_ctp_data(data_dir: Path) -> dict[int, dict]:
    """Carrega dados do CTP para equivalências."""
    with open(data_dir / "Cantai2" / "data" / "output" / "cantai.json", "r") as f:
        ctp_json = json.load(f)

    ctp_by_number = {}
    for h in ctp_json["hymns"]:
        ctp_by_number[h["number"]] = h
    return ctp_by_number


def import_hcc(data_dir: Path) -> dict[str, Any]:
    """Importa HCC com arquitetura de relacionamentos."""
    data = load_hcc_data(data_dir)
    ctp_data = load_ctp_data(data_dir)
    topic_index = build_topic_index(data["topics"])

    hymns = []
    stats = {
        "total": 0,
        "with_theme": 0,
        "with_metric": 0,
        "with_melody": 0,
        "content_equivalences": 0,
        "melody_relationships": 0,
        "canonical_themes_added": 0,
    }

    # Build melody relationships from CTP
    ctp_melody_to_hymn: dict[str, list[int]] = {}
    for h in ctp_data.values():
        if h.get("melody"):
            melody = h["melody"].upper()
            if melody not in ctp_melody_to_hymn:
                ctp_melody_to_hymn[melody] = []
            ctp_melody_to_hymn[melody].append(h["number"])

    for hcc_hymn in data["hymns"]:
        hcc_num = hcc_hymn["number"]

        # Build hymn record
        hymn = {
            "id": f"HCC-{hcc_num:03d}",
            "hymnal": "HCC",
            "number": hcc_num,
            "title": hcc_hymn.get("title", ""),
            "first_line": hcc_hymn.get("first_line", ""),
            "lyrics": hcc_hymn.get("lyrics", ""),
            "topics_hcc": [],
            "topics_canonical": [],
            "metric": None,
            "melody": None,
            "relationships": {
                "content_equivalence": None,
                "melody_relationships": [],
            },
        }

        # Topics
        if hcc_num in topic_index:
            hcc_topics = topic_index[hcc_num]
            hymn["topics_hcc"] = hcc_topics
            stats["with_theme"] += 1

            # Map to canonical topics
            for topic in hcc_topics:
                canonical = HCC_TO_CANONICAL.get(topic)
                if canonical and canonical not in hymn["topics_canonical"]:
                    hymn["topics_canonical"].append(canonical)

        # Metric
        if str(hcc_num) in data["metrics"]:
            hymn["metric"] = data["metrics"][str(hcc_num)]
            stats["with_metric"] += 1

        # Melody
        if str(hcc_num) in data["melodies"]:
            hymn["melody"] = data["melodies"][str(hcc_num)]
            stats["with_melody"] += 1

            # Check melody relationships with CTP
            melody = hymn["melody"].upper()
            if melody in ctp_melody_to_hymn:
                for ctp_num in ctp_melody_to_hymn[melody]:
                    hymn["relationships"]["melody_relationships"].append({
                        "hymnal": "CTP",
                        "number": ctp_num,
                        "type": "same_melody",
                    })
                    stats["melody_relationships"] += 1

        # Content equivalence
        if hcc_num in CONTENT_EQUIVALENCES:
            ctp_equiv = CONTENT_EQUIVALENCES[hcc_num]
            hymn["relationships"]["content_equivalence"] = {
                "hymnal": "CTP",
                "number": ctp_equiv,
                "type": "same_hymn",
            }
            stats["content_equivalences"] += 1

            # Add canonical theme from CTP
            if ctp_equiv in ctp_data:
                ctp_hymn = ctp_data[ctp_equiv]
                for theme in ctp_hymn.get("topics", []):
                    if theme not in hymn["topics_canonical"]:
                        hymn["topics_canonical"].append(theme)
                        stats["canonical_themes_added"] += 1

        hymns.append(hymn)
        stats["total"] += 1

    return {
        "hymns": hymns,
        "stats": stats,
    }


def save_import(result: dict[str, Any], output_path: Path) -> None:
    """Salva o resultado da importação."""
    output = {
        "version": 1,
        "source": "HCC",
        "description": "Hinário da Congregação Cristã - Importado com arquitetura de relacionamentos",
        "stats": result["stats"],
        "hymns": result["hymns"],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data_dir = Path("/home/vanessa/Projetos")
    output_path = data_dir / "Cantai2" / "data" / "output" / "hcc.json"

    result = import_hcc(data_dir)
    save_import(result, output_path)

    print("=== IMPORTAÇÃO HCC CONCLUÍDA ===")
    print(f"Total de hinos: {result['stats']['total']}")
    print(f"Com tema: {result['stats']['with_theme']}")
    print(f"Com métrica: {result['stats']['with_metric']}")
    print(f"Com melodia: {result['stats']['with_melody']}")
    print(f"Equivalências de conteúdo: {result['stats']['content_equivalences']}")
    print(f"Relacionamentos por melodia: {result['stats']['melody_relationships']}")
    print(f"Temas canônicos adicionados: {result['stats']['canonical_themes_added']}")
    print(f"\nArquivo salvo em: {output_path}")
