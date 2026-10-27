# Scripts antigos (arquivados em 2026-10-27)

Estes scripts foram substituídos e **não devem ser rodados**:

- `apply_themes.py` e `apply_metrics.py` recriavam `data/output/cantai.json` do
  zero a partir do PDF, apagando correções feitas depois. O `apply_metrics.py`
  também usava o importador de métricas antigo, que aplicava a métrica errada a
  dezenas de hinos.
- `validate.py` e `audit_equivalences.py` liam o formato antigo dos dados
  (`hymn_equivalences.json`, um formato por hinário).

O que os substitui:

- `cantai build` gera tudo em `web/data` a partir de `data/base`, sem alterar a base.
- `pytest` confere os dados publicados (contagens, métricas conhecidas,
  equivalências, se `web/data` está atualizado).
