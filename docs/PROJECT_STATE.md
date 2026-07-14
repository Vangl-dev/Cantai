# PROJECT_STATE.md - Cantai2

## Estado Atual

**Versão:** 0.4.0
**Status:** Funcional
**Última Atualização:** 2026-07-13
**Sprint Atual:** Sprint 50 - Concluída

## Contexto

O projeto Cantai2 é um sistema de sugestões e planejamento de cultos. Possui 3 hinários integrados: CTP, HCC e Salmos e Hinos (SH). A interface permite busca, sugestões por tema, navegação por equivalências e planejamento de cultos.

## Fases do Projeto

### Fase 1: Fundação ✅ CONCLUÍDA
- Parser CTP
- Exportador JSON
- Busca
- Temas
- Métricas
- Melodias
- Preview

### Fase 2: Funcionalidades ✅ CONCLUÍDA
- Sugestões (Motor V1)
- Agenda de Culto
- Listas Salvas
- Navegação contínua

### Fase 3: Multi-Hinários ✅ CONCLUÍDA
- Arquitetura de relacionamentos
- Importação HCC (609 hinos)
- Importação SH (621 hinos)
- Equivalências de conteúdo (111)
- Registro Canônico de Temas (25 temas)

### Fase 4: Evolução ⏳ FUTURO
- Importação Harpa Cristã
- Importação Novo Cântico
- Histórico de cultos
- Evitar repetição
- Motor Inteligente de Sugestões

## Componentes Congelados

- 🟢 Modelo Hymn
- 🟢 Parser CTP
- 🟢 Parser HCC
- 🟢 Parser SH
- 🟢 Exportador JSON
- 🟢 Busca
- 🟢 Importador de Temas
- 🟢 Importador de Métricas
- 🟢 Interface Base
- 🟢 Identidade Visual
- 🟢 Motor de Sugestões
- 🟢 Agenda
- 🟢 Listas Salvas
- 🟢 Dados Oficiais CTP
- 🟢 Dados Oficiais HCC
- 🟢 Dados Oficiais SH
- 🟢 Registro Canônico de Temas
- 🟢 Mapa de Equivalências

## Métricas

### CTP
| Métrica | Valor |
|---------|-------|
| Total de hinos | 504 |
| Hinos com temas | 501 |
| Hinos com métrica | 323 |
| Hinos com melodia | 323 |
| Total de temas | 82 |

### HCC
| Métrica | Valor |
|---------|-------|
| Total de hinos | 609 |
| Hinos com tema | 418 |
| Hinos com melodia | 400 |
| Equivalências de conteúdo | 20 |
| Relacionamentos por melodia | 69 |

### SH
| Métrica | Valor |
|---------|-------|
| Total de hinos | 621 |
| Hinos com temas | 183 |
| Equivalências com CTP | 60 |

### Total
| Métrica | Valor |
|---------|-------|
| Total de hinos | 1.734 |
| Total de temas canônicos | 25 |
| Total de equivalências | 111 |

## Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `data/output/cantai.json` | JSON do CTP |
| `data/output/hcc.json` | JSON do HCC |
| `data/output/sh.json` | JSON do SH |
| `data/hymn_equivalences.json` | Mapa de equivalências |
| `data/canonical_topics.json` | Registro Canônico de Temas |
| `web/index.html` | Interface principal |
| `src/cantai/tools/validate.py` | Suíte de validação |
| `src/cantai/tools/audit_equivalences.py` | Auditoria de equivalências |

## Pendências

- [x] SH: Investigar exibição de métricas → **Conclusão: SH não possui dados de métricas em nenhuma fonte oficial. Campo `metric` existe no model e UI mas nunca foi populado para SH.**
- [x] SH: Investigar exibição de "⭐ Também no CTP" → **Corrigido: índice reverso adicionado no JS para mapear SH/HCC IDs de volta ao CTP.**
- [ ] Importação da Harpa Cristã
- [ ] Importação de Novo Cântico
- [ ] Histórico de cultos
- [ ] Evitar repetição
- [ ] Motor Inteligente de Sugestões
