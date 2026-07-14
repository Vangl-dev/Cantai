# Roadmap - Cantai2

## Visão

O Cantai2 é um sistema de sugestões e planejamento de cultos. Possui 3 hinários integrados: CTP, HCC e Salmos e Hinos (SH). O objetivo é auxiliar a pianista no planejamento de hinos para cultos.

## Fases

### Fase 1: Fundação ✅ CONCLUÍDA
- [x] Estrutura do projeto
- [x] Modelo de domínio Hymn
- [x] Parser CTP
- [x] Exportador JSON
- [x] Preview funcional
- [x] Busca textual
- [x] Importação de temas
- [x] Importação de métricas
- [x] Importação de melodias

### Fase 2: Funcionalidades ✅ CONCLUÍDA
- [x] Motor de Sugestões V1
- [x] Agenda de Culto
- [x] Listas Salvas
- [x] Navegação contínua
- [x] Navegação por relacionamentos

### Fase 3: Multi-Hinários ✅ CONCLUÍDA
- [x] Arquitetura de relacionamentos
- [x] Importação HCC (609 hinos)
- [x] Importação SH (621 hinos)
- [x] Equivalências de conteúdo (111)
- [x] Registro Canônico de Temas (25 temas)
- [x] Motor de Sugestões V2
- [x] Destaque de equivalências CTP
- [x] Navegação multi-hinários
- [x] Persistência de seleção

### Fase 4: Evolução ⏳ FUTURO
- [ ] Importação Harpa Cristã
- [ ] Importação Novo Cântico
- [ ] Histórico de cultos
- [ ] Evitar repetição
- [ ] Motor Inteligente de Sugestões
- [ ] Sistema de Pontuação (Score)

## Métricas Atuais

### CTP
| Métrica | Valor |
|---------|-------|
| Total de hinos | 504 |
| Hinos com temas | 501 |
| Hinos com métrica | 323 |
| Hinos com melodia | 323 |

### HCC
| Métrica | Valor |
|---------|-------|
| Total de hinos | 609 |
| Hinos com tema | 418 |
| Hinos com melodia | 400 |
| Equivalências | 20 + 69 |

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

## Referências

- [PROJECT_STATE.md](PROJECT_STATE.md)
- [CHANGELOG.md](../CHANGELOG.md)
- [docs/architecture/](architecture/)
