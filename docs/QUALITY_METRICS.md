# QUALITY_METRICS

## Indicadores de Qualidade

**Data de Criação:** 2026-07-07
**Última Atualização:** 2026-07-07

---

## Objetivo

Definir e monitorar indicadores de qualidade para garantir que os projetos atinjam os padrões do MétodoDev.

---

## Métricas Obrigatórias

### 1. Bugs por Sprint

**Definição:** Número de bugs encontrados em cada sprint
**Meta:** ≤ 2 bugs por sprint
**Fórmula:** `Total de bugs / Número de sprints`
**Coleta:** Automated testing + Manual QA
**Frequência:** A cada sprint

---

### 2. Tempo de Retrabalho

**Definição:** Percentual do tempo gasto em correções
**Meta:** ≤ 15% do tempo total
**Fórmula:** `(Tempo de retrabalho / Tempo total) × 100`
**Coleta:** Time tracking
**Frequência:** A cada sprint

---

### 3. Cobertura de Testes

**Definição:** Percentual de código coberto por testes
**Meta:** ≥ 80% unitários, ≥ 60% integração
**Fórmula:** `(Linhas testadas / Total de linhas) × 100`
**Coleta:** Coverage tools (Jest, pytest)
**Frequência:** A cada commit

---

### 4. Documentação Atualizada

**Definição:** Percentual de documentos desatualizados
**Meta:** 0% desatualizados
**Fórmula:** `(Documentos desatualizados / Total de documentos) × 100`
**Coleta:** Revisão manual + Scripts
**Frequência:** A cada sprint

---

### 5. Auditorias Aprovadas

**Definição:** Percentual de auditorias que passam na primeira tentativa
**Meta:** ≥ 90%
**Fórmula:** `(Auditorias aprovadas / Total de auditorias) × 100`
**Coleta:** CI/CD pipeline
**Frequência:** A cada PR

---

### 6. Regressões Encontradas

**Definição:** Número de bugs que retornaram após correção
**Meta:** 0 regressões
**Fórmula:** `Total de regressões`
**Coleta:** Testes de regressão
**Frequência:** A cada sprint

---

### 7. Tempo entre Preview e Deploy

**Definição:** Dias entre aprovação do preview e deploy
**Meta:** ≤ 2 dias
**Fórmula:** `Data de deploy - Data de aprovação`
**Coleta:** Git history + Deploy logs
**Frequência:** A cada deploy

---

### 8. Percentual de Funcionalidades Testadas

**Definição:** Funcionalidades com testes próprios
**Meta:** 100%
**Fórmula:** `(Funcionalidades testadas / Total de funcionalidades) × 100`
**Coleta:** Test reports
**Frequência:** A cada feature

---

## Métricas Complementares

### 9. Tempo de Build
**Meta:** ≤ 5 minutos
**Frequência:** A cada commit

### 10. Taxa de Sucesso de Deploy
**Meta:** ≥ 99%
**Frequência:** A cada deploy

### 11. Tempo de Resposta (API)
**Meta:** ≤ 200ms
**Frequência:** Contínuo

### 12. Uptime
**Meta:** ≥ 99.9%
**Frequência:** Contínuo

---

## Dashboard de Métricas

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| Bugs/Sprint | ≤ 2 | - | ⏳ |
| Retrabalho | ≤ 15% | - | ⏳ |
| Cobertura Testes | ≥ 80% | - | ⏳ |
| Docs Atualizadas | 0% desat. | - | ⏳ |
| Auditorias OK | ≥ 90% | - | ⏳ |
| Regressões | 0 | - | ⏳ |
| Preview→Deploy | ≤ 2 dias | - | ⏳ |
| Features Testadas | 100% | - | ⏳ |

---

## Coleta de Dados

### Automática
- Testes: via CI/CD
- Build: via CI/CD
- Deploy: via scripts

### Manual
- Bugs: registrar em KNOWN_ISSUES.md
- Retrabalho: time tracking
- Documentação: revisão sprint

---

## Relatórios

### Relatório de Sprint
```markdown
# Relatório de Qualidade - Sprint [X]

## Métricas
| Métrica | Meta | Resultado | Status |
|---------|------|-----------|--------|
| Bugs | ≤ 2 | [valor] | [OK/FALHA] |

## Análise
[Análise das métricas]

## Ações Corretivas
[Ações para melhorar]
```

---

## Referências

- [Qualidade](Qualidade.md)
- [TESTING_POLICY](TESTING_POLICY.md)
- [CASE_STUDIES](CASE_STUDIES.md)
