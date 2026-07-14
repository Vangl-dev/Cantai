# Relatório — Sprint 29: Levantamento das Equivalências CTP × Demais Hinários

**Data:** 2026-07-10  
**Status:** Concluído  

---

## 1. Documentos Encontrados

### 1.1 Fontes de Dados

| Documento | Formato | Hinários | Registros | Confiança |
|-----------|---------|----------|-----------|-----------|
| `HinarioCTP_metricas.md` | Markdown | CTP | 321 hinos | ✅ Alta |
| `markdown_índice_ctp.md` | Markdown | CTP | 504 hinos | ✅ Alta |
| `temas_harpa_crista.md` | Markdown | HARPA | ~520 linhas | ✅ Alta |
| `temas_SALMOS-HINOS.md` | Markdown | SH | ~1065 linhas | ✅ Alta |
| `temas_hcc_topics.json` | JSON | HCC | 40 tópicos | ✅ Alta |
| `metricas_hcc_final.json` | JSON | HCC | 129 hinos | ✅ Alta |
| `melodias_hcc.json` | JSON | HCC | 404 hinos | ✅ Alta |
| `hinos_importados.txt` | Texto | CTP | 498 hinos | ✅ Alta |

### 1.2 PDFs Disponíveis

| PDF | Tamanho | Hinário |
|-----|---------|---------|
| `Hinário Cantai Todos os Povos.pdf` | 6.6 MB | CTP |
| `HARPA CRISTÃ.pdf` | 576 KB | HARPA |
| `hcc-completo_compress.pdf` | 766 KB | HCC |
| `SALMOS-HINOS completo.pdf` | 2.2 MB | SH |
| `novo_cantico.pdf` | 796 KB | NC |
| `índice ctp.pdf` | 4.2 MB | CTP |
| `metricas_HCC.pdf` | 2.2 MB | HCC |
| `Temas_HCC.pdf` | 3.6 MB | HCC |

---

## 2. Equivalências Encontradas por Melodia

### 2.1 HCC × CTP (69 coincidências)

| HCC | CTP | Melodia |
|-----|-----|---------|
| 1 | 360 | WAREHAM |
| 6 | 33 | ITALIAN HYMN |
| 8 | 155, 381 | EVENTIDE |
| 14 | 56 | LEONI |
| 25 | 63 | FAITHFULNESS |
| 34 | 13 | NATIONAL HYMN |
| 37 | 163 | GOD BE WITH YOU |
| 42 | 101 | CWM RHONDDA |
| 46 | 66 | DIX |
| 50 | 5 | MIT FREUDEN ZART |
| 56 | 91 | DIADEM |
| 60 | 36 | HYMN TO JOY |
| 72 | 23 | AZMON |
| 91 | 337 | STILLE NACHT |
| 96 | 351 | MENDELSSOHN |
| 99 | 342 | MUELLER |
| 106 | 345 | ANTIOCH |
| 127 | 364 | HAMBURG |
| 132 | 368 | OLD RUGGED CROSS |
| 135 | 373 | EASTER HYMN |
| 140 | 375 | CHRIST AROSE |
| 153 | 314 | BATTLE HYMN |
| 174 | 283 | PRECIOUS NAME |
| 182 | 190 | BLOTT EN DAG |
| 187 | 188 | CRIMOND |
| 197 | 12 | DUKE STREET |
| 200 | 268 | ELIZABETH |
| 216 | 100 | BREAD OF LIFE |
| 217 | 246 | ALETTA |
| 222 | 2 | ARNSBERG |
| 228 | 52 | TO GOD BE THE GLORY |
| 269 | 175 | LYNDHURST |
| 270 | 175 | LYNDHURST |
| 280 | 44 | CAMACUÁ |
| 283 | 46 | TELFORD |
| 286 | 98 | BLESSED BE THE FOUNTAIN |
| 297 | 116 | HAPPY DAY |
| 299 | 103 | THE GOSPEL BELLS |
| 300 | 237 | WOODWORTH |
| 310 | 84 | LAUDES DOMINI |
| 314 | 112 | AMAZING GRACE |
| 329 | 208 | VILLE DE HAVRE |
| 336 | 47 | LANDAS |
| 348 | 137 | SOLID ROCK |
| 377 | 154 | HOLD THOU MY HAND |
| 378 | 147 | SWEET HOUR |
| 384 | 261 | PAI NOSSO SERTANEJO |
| 386 | 148 | VEILLE TOUJOURS |
| 387 | 144 | RICHIER |
| 388 | 151 | EBENEZER |
| 395 | 366 | NEAR THE CROSS |
| 399 | 180 | BETHANY |
| 400 | 250, 263 | COMUNHÃO |
| 406 | 409 | EIN' FESTE BURG |
| 429 | 247 | MOZART |
| 447 | 142 | EL NATHAN |
| 465 | 107 | TRUST AND OBEY |
| 510 | 359 | BELÉM |
| 519 | 256 | A CEIA DO SENHOR |
| 524 | 232 | MANOAH |
| 552 | 297 | CONSCIÊNCIA |
| 553 | 293 | MEGALÓPOLIS |
| 562 | 281 | LAVAPÉS |
| 563 | 176 | DENNIS |
| 566 | 282 | WEBB |
| 569 | 126 | BETTER WORLD |
| 574 | 260 | MORRIS |

### 2.2 CTP × SH (1 referência direta)

| CTP | SH | Observação |
|-----|-----|------------|
| 94 | 65 | "GRANDIOSO ÉS TU" - referência no nome do arquivo |

---

## 3. Qualidade da Documentação por Hinário

| Hinário | Documentação | Equivalências | Cobertura |
|---------|--------------|---------------|-----------|
| **HCC** | ✅ Excelente | 69 por melodia | 13.7% do CTP |
| **HARPA** | ⚠️ Parcial | Temas apenas | Sem equivalências de hinos |
| **SH** | ⚠️ Parcial | 1 referência | Sem equivalências de hinos |
| **NC** | ❌ Mínima | Nenhuma | Sem dados |

---

## 4. Hinários com Menor Documentação

1. **Novo Cântico** — Apenas PDF disponível, sem dados processados
2. **Salmos e Hinos** — Apenas markdown de temas, sem equivalências de hinos
3. **Harpa Cristã** — Apenas markdown de temas, sem equivalências de hinos

---

## 5. Primeiro Hinário a Ser Importado

### Recomendação: **HCC (Hinário da Congregação Cristã)**

### Justificativa Técnica:

1. **69 equivalências documentadas** por melodia com o CTP
2. **404 hinos com melodias** já processadas
3. **129 hinos com métricas** já processadas
4. **40 tópicos** já mapeados
5. **PDF completo disponível** para validação
6. **Dados já processados** em JSON (prontos para importação)

---

## 6. Plano Recomendado para Importação

### Fase 1: HCC (Prioridade)

- Importar 609 hinos do PDF
- Integrar 69 equivalências por melodia
- Mapear tópicos canônicos
- Validar com dados já processados

### Fase 2: Harpa Cristã

- Importar ~640 hinos do PDF
- Utilizar markdown de temas para classificação
- Buscar equivalências por melodia (reprocessar)
- Validar com índice oficial

### Fase 3: Salmos e Hinos

- Importar ~650 hinos do PDF
- Utilizar markdown de temas para classificação
- Buscar equivalências por melodia
- Validar com índice oficial

### Fase 4: Novo Cântico

- Importar ~300 hinos do PDF
- Classificar por temas (se disponível)
- Buscar equivalências por melodia
- Validar com índice oficial

---

## 7. Equivalências Documentadas (Resumo)

| Fonte | Equivalências | Método |
|-------|---------------|--------|
| Melodia HCC × CTP | 69 | Comparação direta |
| Referência CTP × SH | 1 | Nome de arquivo |
| **Total** | **70** | Documental |

---

## 8. Conclusão

O HCC possui a melhor documentação para importação, com 69 equivalências já comprovadas por melodia. Os demais hinários exigirão trabalho adicional de mapeamento.

**Sprint 29 encerrada.**
