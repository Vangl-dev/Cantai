#!/usr/bin/env python3
"""
Ferramenta de Auditoria de Equivalências - Cantai2

Este script localiza candidatos a equivalências entre hinários
que ainda não foram cadastrados no mapa de equivalências.

IMPORTANTE: Este script NÃO altera nenhum arquivo.
Ele apenas gera um relatório de candidatos.
"""

import json
import re
import time
from pathlib import Path
from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
    """Normaliza texto para comparação."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def calculate_similarity(a: str, b: str) -> float:
    """Calcula similaridade entre duas strings (0-1)."""
    return SequenceMatcher(None, a, b).ratio()


def load_data(data_dir: Path) -> dict:
    """Carrega todos os dados dos hinários."""
    data = {}
    
    # CTP
    ctp_path = data_dir / 'output' / 'cantai.json'
    if ctp_path.exists():
        with open(ctp_path, 'r', encoding='utf-8') as f:
            data['CTP'] = json.load(f)['hymns']
    
    # HCC
    hcc_path = data_dir / 'output' / 'hcc.json'
    if hcc_path.exists():
        with open(hcc_path, 'r', encoding='utf-8') as f:
            data['HCC'] = json.load(f)['hymns']
    
    # SH
    sh_path = data_dir / 'output' / 'sh.json'
    if sh_path.exists():
        with open(sh_path, 'r', encoding='utf-8') as f:
            data['SH'] = json.load(f)['hymns']
    
    # Equivalences
    equiv_path = data_dir / 'hymn_equivalences.json'
    if equiv_path.exists():
        with open(equiv_path, 'r', encoding='utf-8') as f:
            data['equivalences'] = json.load(f)
    else:
        data['equivalences'] = {}
    
    return data


def get_existing_equivalents(equivalences: dict) -> set:
    """Retorna conjunto de IDs que já possuem equivalência."""
    existing = set()
    for key, value in equivalences.items():
        existing.add(key)
        if value.get('equivalents'):
            for eq in value['equivalents']:
                existing.add(eq['id'])
    return existing


def find_exact_title_matches(data: dict, existing: set) -> list:
    """Encontra matches de título idêntico."""
    candidates = []
    
    hymnals = ['CTP', 'HCC', 'SH']
    
    for i, h1_hymnal in enumerate(hymnals):
        for h2_hymnal in hymnals[i+1:]:
            if h1_hymnal not in data or h2_hymnal not in data:
                continue
            
            for h1 in data[h1_hymnal]:
                h1_id = f"{h1_hymnal}-{h1['number']}"
                if h1_id in existing:
                    continue
                
                for h2 in data[h2_hymnal]:
                    h2_id = f"{h2_hymnal}-{h2['number']}"
                    if h2_id in existing:
                        continue
                    
                    # Check if already paired
                    if any(eq['id'] == h2_id for eq in 
                           data['equivalences'].get(h1_id, {}).get('equivalents', [])):
                        continue
                    
                    # Compare titles
                    t1 = normalize_text(h1['title'])
                    t2 = normalize_text(h2['title'])
                    
                    if t1 == t2 and len(t1) > 3:
                        candidates.append({
                            'h1': {'hymnal': h1_hymnal, 'id': h1_id, 'title': h1['title'], 'first_line': h1.get('first_line', '')},
                            'h2': {'hymnal': h2_hymnal, 'id': h2_id, 'title': h2['title'], 'first_line': h2.get('first_line', '')},
                            'confidence': 5,
                            'reason': 'Título idêntico'
                        })
    
    return candidates


def find_exact_first_line_matches(data: dict, existing: set) -> list:
    """Encontra matches de primeira linha idêntica."""
    candidates = []
    
    hymnals = ['CTP', 'HCC', 'SH']
    
    for i, h1_hymnal in enumerate(hymnals):
        for h2_hymnal in hymnals[i+1:]:
            if h1_hymnal not in data or h2_hymnal not in data:
                continue
            
            for h1 in data[h1_hymnal]:
                h1_id = f"{h1_hymnal}-{h1['number']}"
                if h1_id in existing:
                    continue
                
                fl1 = h1.get('first_line', '')
                if not fl1:
                    continue
                
                norm_fl1 = normalize_text(fl1)
                if len(norm_fl1) < 10:
                    continue
                
                for h2 in data[h2_hymnal]:
                    h2_id = f"{h2_hymnal}-{h2['number']}"
                    if h2_id in existing:
                        continue
                    
                    fl2 = h2.get('first_line', '')
                    if not fl2:
                        continue
                    
                    norm_fl2 = normalize_text(fl2)
                    if len(norm_fl2) < 10:
                        continue
                    
                    # Skip if titles are identical (already caught)
                    t1 = normalize_text(h1['title'])
                    t2 = normalize_text(h2['title'])
                    if t1 == t2:
                        continue
                    
                    # Check if already paired
                    if any(eq['id'] == h2_id for eq in 
                           data['equivalences'].get(h1_id, {}).get('equivalents', [])):
                        continue
                    
                    if norm_fl1 == norm_fl2:
                        candidates.append({
                            'h1': {'hymnal': h1_hymnal, 'id': h1_id, 'title': h1['title'], 'first_line': fl1},
                            'h2': {'hymnal': h2_hymnal, 'id': h2_id, 'title': h2['title'], 'first_line': fl2},
                            'confidence': 4,
                            'reason': 'Primeira linha idêntica'
                        })
    
    return candidates


def find_similar_title_matches(data: dict, existing: set) -> list:
    """Encontra matches de título semelhante."""
    candidates = []
    
    hymnals = ['CTP', 'HCC', 'SH']
    
    for i, h1_hymnal in enumerate(hymnals):
        for h2_hymnal in hymnals[i+1:]:
            if h1_hymnal not in data or h2_hymnal not in data:
                continue
            
            for h1 in data[h1_hymnal]:
                h1_id = f"{h1_hymnal}-{h1['number']}"
                if h1_id in existing:
                    continue
                
                for h2 in data[h2_hymnal]:
                    h2_id = f"{h2_hymnal}-{h2['number']}"
                    if h2_id in existing:
                        continue
                    
                    # Check if already paired
                    if any(eq['id'] == h2_id for eq in 
                           data['equivalences'].get(h1_id, {}).get('equivalents', [])):
                        continue
                    
                    t1 = normalize_text(h1['title'])
                    t2 = normalize_text(h2['title'])
                    
                    if t1 == t2:
                        continue
                    
                    similarity = calculate_similarity(t1, t2)
                    
                    if similarity >= 0.8 and len(t1) > 5:
                        candidates.append({
                            'h1': {'hymnal': h1_hymnal, 'id': h1_id, 'title': h1['title'], 'first_line': h1.get('first_line', '')},
                            'h2': {'hymnal': h2_hymnal, 'id': h2_id, 'title': h2['title'], 'first_line': h2.get('first_line', '')},
                            'confidence': 3,
                            'reason': f'Título semelhante ({similarity:.0%})'
                        })
    
    return candidates


def find_melody_matches(data: dict, existing: set) -> list:
    """Encontra matches de melodia idêntica."""
    candidates = []
    
    hymnals = ['CTP', 'HCC', 'SH']
    
    for i, h1_hymnal in enumerate(hymnals):
        for h2_hymnal in hymnals[i+1:]:
            if h1_hymnal not in data or h2_hymnal not in data:
                continue
            
            for h1 in data[h1_hymnal]:
                h1_id = f"{h1_hymnal}-{h1['number']}"
                if h1_id in existing:
                    continue
                
                m1 = h1.get('melody', '')
                if not m1:
                    continue
                
                for h2 in data[h2_hymnal]:
                    h2_id = f"{h2_hymnal}-{h2['number']}"
                    if h2_id in existing:
                        continue
                    
                    m2 = h2.get('melody', '')
                    if not m2:
                        continue
                    
                    # Check if already paired
                    if any(eq['id'] == h2_id for eq in 
                           data['equivalences'].get(h1_id, {}).get('equivalents', [])):
                        continue
                    
                    if m1 == m2:
                        candidates.append({
                            'h1': {'hymnal': h1_hymnal, 'id': h1_id, 'title': h1['title'], 'melody': m1},
                            'h2': {'hymnal': h2_hymnal, 'id': h2_id, 'title': h2['title'], 'melody': m2},
                            'confidence': 2,
                            'reason': f'Mesma melodia: {m1}'
                        })
    
    return candidates


def generate_report(candidates: list, output_path: Path) -> None:
    """Gera o relatório de candidatos."""
    
    # Sort by confidence (highest first)
    candidates.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Count by confidence
    confidence_counts = {}
    for c in candidates:
        conf = c['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    lines = []
    lines.append("# Relatório de Candidatos a Equivalências")
    lines.append("")
    lines.append(f"Total de candidatos: {len(candidates)}")
    lines.append("")
    lines.append("## Distribuição por Nível de Confiança")
    lines.append("")
    
    stars = {5: '★★★★★', 4: '★★★★☆', 3: '★★★☆☆', 2: '★★☆☆☆', 1: '★☆☆☆☆'}
    
    for conf in sorted(confidence_counts.keys(), reverse=True):
        lines.append(f"- {stars.get(conf, '?')}: {confidence_counts[conf]} candidatos")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for c in candidates:
        lines.append(f"### {stars.get(c['confidence'], '?')}")
        lines.append("")
        lines.append(f"**{c['h1']['id']}** — {c['h1']['title']}")
        lines.append("")
        lines.append(f"**{c['h2']['id']}** — {c['h2']['title']}")
        lines.append("")
        lines.append(f"**Motivo:** {c['reason']}")
        lines.append("")
        
        if c['h1'].get('first_line') and c['h2'].get('first_line'):
            lines.append(f"Primeira linha 1: {c['h1']['first_line'][:60]}")
            lines.append("")
            lines.append(f"Primeira linha 2: {c['h2']['first_line'][:60]}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    """Função principal."""
    start_time = time.time()
    
    # Paths
    project_dir = Path(__file__).parent.parent.parent.parent
    data_dir = project_dir / 'data'
    reports_dir = project_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    output_path = reports_dir / 'equivalence_candidates.md'
    
    stars = {5: '★★★★★', 4: '★★★★☆', 3: '★★★☆☆', 2: '★★☆☆☆', 1: '★☆☆☆☆'}
    
    print("=" * 60)
    print("FERRAMENTA DE AUDITORIA DE EQUIVALÊNCIAS")
    print("=" * 60)
    
    print("\nCarregando dados...")
    data = load_data(data_dir)
    
    print(f"  CTP: {len(data.get('CTP', []))} hinos")
    print(f"  HCC: {len(data.get('HCC', []))} hinos")
    print(f"  SH: {len(data.get('SH', []))} hinos")
    print(f"  Equivalências existentes: {len(data.get('equivalences', {}))}")
    
    existing = get_existing_equivalents(data.get('equivalences', {}))
    print(f"  IDs com equivalência: {len(existing)}")
    
    print("\nProcurando candidatos...")
    
    candidates = []
    
    print("  1. Títulos idênticos...")
    exact_title = find_exact_title_matches(data, existing)
    candidates.extend(exact_title)
    print(f"     Encontrados: {len(exact_title)}")
    
    print("  2. Primeiras linhas idênticas...")
    exact_fl = find_exact_first_line_matches(data, existing)
    candidates.extend(exact_fl)
    print(f"     Encontrados: {len(exact_fl)}")
    
    print("  3. Títulos semelhantes...")
    similar_title = find_similar_title_matches(data, existing)
    candidates.extend(similar_title)
    print(f"     Encontrados: {len(similar_title)}")
    
    print("  4. Mesma melodia...")
    melody = find_melody_matches(data, existing)
    candidates.extend(melody)
    print(f"     Encontrados: {len(melody)}")
    
    print(f"\nTotal de candidatos: {len(candidates)}")
    
    print("\nGerando relatório...")
    generate_report(candidates, output_path)
    print(f"  Salvo em: {output_path}")
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"\nCandidatos encontrados: {len(candidates)}")
    
    confidence_counts = {}
    for c in candidates:
        conf = c['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    for conf in sorted(confidence_counts.keys(), reverse=True):
        print(f"  {stars.get(conf, '?')}: {confidence_counts[conf]}")
    
    print(f"\nTempo de execução: {elapsed:.2f}s")
    print(f"\nNenhum arquivo foi alterado.")
    
    print("\n" + "=" * 60)
    print("AUDITORIA CONCLUÍDA")
    print("=" * 60)


if __name__ == '__main__':
    main()
