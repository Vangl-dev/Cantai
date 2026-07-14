# Relatório — Sprint 28: Mapa Canônico de Equivalências

**Data:** 2026-07-10  
**Status:** Concluído  

---

## 1. Arquivos Encontrados

### 1.1 Projeto Cantai Original (`/home/vanessa/Projetos/Cantai/`)

| Arquivo | Formato | Registros | Hinários | Qualidade | Reutilização |
|---------|---------|-----------|----------|-----------|--------------|
| `canonical_topics.yaml` | YAML | 78 tópicos | CTP, HARPA, CC, SH | ✅ Alta | ✅ Direta |
| `cantai/data/output/cantai.json` | JSON | 609 hinos | HCC apenas | ⚠️ Parcial | ⚠️ Adaptar |
| `cantai/data/input/temas_harpa_crista.md` | Markdown | ~520 linhas | HARPA | ✅ Alta | ✅ Adaptar |
| `cantai/data/input/temas_SALMOS-HINOS.md` | Markdown | ~1065 linhas | SH | ✅ Alta | ✅ Adaptar |
| `cantai/data/input/markdown_índice_ctp.md` | Markdown | ~2293 linhas | CTP | ✅ Alta | ✅ Já integrado |
| `cantai/data/input/HinarioCTP_metricas.md` | Markdown | ~873 linhas | CTP | ✅ Alta | ✅ Já integrado |

### 1.2 Importadores (referência)

| Arquivo | Hinário | Função |
|---------|---------|--------|
| `importers/ctp.py` | CTP | Importador principal |
| `importers/harpa.py` | HARPA | Importador Harpa Cristã |
| `importers/hcc.py` | HCC | Importador HCC |
| `importers/cantor_cristao.py` | CC | Importador Cantor Cristão |
| `importers/salmos_hinos.py` | SH | Importador Salmos e Hinos |
| `importers/novo_cantico.py` | NC | Importador Novo Cântico |

### 1.3 Dados HCC processados (temp)

| Arquivo | Conteúdo |
|---------|----------|
| `temas_hcc_topics.json` | Tópicos HCC processados |
| `metricas_hcc_final.json` | Métricas HCC |
| `melodias_hcc.json` | Melodias HCC |

---

## 2. Descrição do canonical_topics.yaml

O arquivo `canonical_topics.yaml` é o **mapear canônico de tópicos** entre hinários.

### Estrutura:

```yaml
Tópico Canônico:
  aliases:
    - Variante 1
    - Variante 2

  CTP:
    - Nome no CTP

  HARPA:
    - Nome na Harpa

  CC:
    - Nome no Cantor Cristão

  SH:
    - Nome em Salmos e Hinos
```

### Exemplo:

```yaml
Adoração:
  aliases:
    - Adoração e Louvor

  CTP:
    - Adoração

  HARPA:
    - "DEUS, O FILHO: Louvores"

  CC:
    - ADORAÇÃO E LOUVOR

  SH:
    - Convite à Adoração e Louvor
```

### Estatísticas:

- **78 tópicos canônicos** definidos
- **4 hinários** mapeados (CTP, HARPA, CC, SH)
- **Aliases** para variações de nomenclatura
- **Cobertura parcial** — alguns tópicos não existem em todos os hinários

---

## 3. Formato Proposto para o Mapa Canônico

### 3.1 Mapa de Tópicos (já existe)

Manter o formato YAML do `canonical_topics.yaml` com a estrutura atual.

### 3.2 Mapa de Equivalências entre Hinos (novo)

Propor formato JSON para equivalências entre hinos específicos:

```json
{
  "version": 1,
  "description": "Mapa de equivalências entre hinos dos hinários",
  "equivalences": [
    {
      "canonical_id": "CTP-412",
      "hymnal": "CTP",
      "number": 412,
      "title": "VEM, ESPÍRITO SANTO",
      "metric": "8.7.8.7.8.8.7",
      "melody": "MIT FREUDEN ZART",
      "topics": ["Espirito Santo", "Pentecostes"],
      "equivalents": [
        {
          "hymnal": "HARPA",
          "number": 278,
          "title": "VEM, ESPÍRITO SANTO",
          "confidence": "official"
        },
        {
          "hymnal": "HCC",
          "number": 185,
          "title": "VENDE, ESPÍRITO",
          "confidence": "official"
        },
        {
          "hymnal": "SH",
          "number": 121,
          "title": "VEM, ESPÍRITO SANTO",
          "confidence": "official"
        }
      ]
    }
  ]
}
```

### 3.3 Campos do Mapa

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `canonical_id` | string | ID único canônico (CTP-412) |
| `hymnal` | string | Hinário de origem |
| `number` | int | Número do hino |
| `title` | string | Título oficial |
| `metric` | string | Métrica (se disponível) |
| `melody` | string | Melodia (se disponível) |
| `topics` | array | Tópicos canônicos |
| `equivalents` | array | Hinos equivalentes em outros hinários |
| `confidence` | string | Nível de confiança (official/inferred/pending) |

---

## 4. Fluxo Arquitetural da Herança de Temas

```
                    ┌─────────────────────┐
                    │   canonical_topics   │
                    │       .yaml          │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │   CTP    │    │  HARPA   │    │   HCC    │
        │ (ref.)   │    │          │    │          │
        └────┬─────┘    └────┬─────┘    └────┬─────┘
             │                │                │
             ▼                ▼                ▼
        ┌─────────────────────────────────────────┐
        │         Temas Canônicos Herdados         │
        │  CTP-412 → HARPA-278 → HCC-185          │
        │  Tema: "Espirito Santo" (herdado do CTP) │
        └─────────────────────────────────────────┘
```

### Regras de Herança:

1. **CTP é a referência** — seus temas são os canônicos
2. **Equivalência oficial** → herda tema do CTP
3. **Sem equivalência** → mantém tema próprio
4. **Tema canônico** → usado para navegação e sugestões
5. **Tema original** → preservado para referência

---

## 5. Plano de Migração dos Demais Hinários

### Fase 1: Preparação (Sprint 28 - Atual)

- ✅ Mapear tópicos canônicos (canonical_topics.yaml)
- ✅ Identificar fontes de dados disponíveis
- ✅ Definir formato do Mapa de Equivalências

### Fase 2: Importação HCC (Sprint futura)

- Importar 609 hinos do HCC
- Mapear equivalências com CTP usando métricas e melodias
- Integrar tópicos HCC ao mapa canônico

### Fase 3: Importação Harpa (Sprint futura)

- Importar ~640 hinos da Harpa Cristã
- Mapear equivalências usando tópicos do canonical_topics.yaml
- Validar comThemeProvider cruzada

### Fase 4: Importação SH e CC (Sprint futura)

- Importar Salmos e Hinos (~650 hinos)
- Importar Cantor Cristão (~500 hinos)
- Completar mapa de equivalências

### Fase 5: Novo Cântico (Sprint futura)

- Importar Novo Cântico (~300 hinos)
- Finalizar mapa canônico completo

---

## 6. Regras Arquiteturais Registradas

### Regra 1: Temas Canônicos
> Os temas canônicos do Cantai2 são os temas do CTP.

### Regra 2: Temas Originais
> Os demais hinários poderão manter seus temas originais.

### Regra 3: Herança por Equivalência
> Quando existir equivalência oficial entre hinos, o tema canônico será herdado do CTP.

### Regra 4: Preservação da Classificação
> A classificação original do hinário será preservada. Ela NÃO será descartada.

### Regra 5: Sem Equivalência
> Quando não existir equivalência, o hino permanecerá apenas com sua classificação própria até futura revisão.

---

## 7. Conclusão

O Mapa Canônico de Equivalências está estruturado e documentado. Os componentes essenciais são:

1. **canonical_topics.yaml** — Mapa de tópicos entre hinários (78 tópicos)
2. **Formato JSON proposto** — Mapa de equivalências entre hinos
3. **Regras de herança** — Definidas e documentadas
4. **Plano de migração** — 5 fases até hinário completo

**Sprint 28 encerrada.**
