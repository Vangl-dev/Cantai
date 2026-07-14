# ADR-0003: Evolução do Motor de Sugestões

**Status:** Aprovado  
**Data:** 2026-07-10  
**Decisor:** Usuário  
**Sprint:** 17  

---

## Contexto

O Motor de Sugestões do Cantai2 será evolutivo. A implementação ocorrerá em etapas, cada uma adicionando inteligência ao algoritmo de sugestão.

---

## Versões Planejadas

### Versão 1 — Aleatório Simples ✅ (Atual)

Seleciona aleatoriamente um pequeno conjunto de hinos.

**Status:** Implementado na Sprint 16.

---

### Versão 2 — Evitar Repetição

Evita repetir sugestões já apresentadas.

Enquanto existirem opções inéditas, o sistema não repetirá hinos.

Quando todas as possibilidades forem apresentadas, reinicia o ciclo.

---

### Versão 3 — Hinários Selecionados

Considera os hinários selecionados pelo usuário.

**Distribuição padrão:**

| Hinário | Sugestões |
|---------|-----------|
| CTP | 3 |
| Hinário adicional | 1 cada |

---

### Versão 4 — Agenda de Culto

Considera a Agenda de Culto.

Não sugerir automaticamente hinos já escolhidos para o mesmo culto.

---

### Versão 5 — Histórico

Considera o Histórico de cultos.

Evitar repetição conforme configuração do usuário.

**Exemplos de período:**

- 30 dias
- 60 dias
- 90 dias
- 180 dias

---

### Versão 6 — Métricas

Considera as Métricas dos hinos.

Permite sugerir hinos equivalentes (mesma métrica).

---

### Versão 7 — Melodias

Considera Melodias.

Permite sugerir hinos com a mesma melodia.

---

### Versão 8 — Sistema de Pontuação (Score)

Cada hino poderá receber pontos.

**Critérios de pontuação:**

| Critério | Pontos |
|----------|--------|
| Tema correspondente | +N |
| Hinário prioritário (CTP) | +N |
| Não utilizado recentemente | +N |
| Mesmo período litúrgico | +N |
| Outros critérios futuros | +N |

O algoritmo escolherá entre os hinos com **maior pontuação**, mantendo uma pequena aleatoriedade para evitar sugestões sempre idênticas.

---

## Fluxo de Evolução

```
V1: Aleatório
    ↓
V2: + Evitar repetição
    ↓
V3: + Hinários selecionados
    ↓
V4: + Agenda de Culto
    ↓
V5: + Histórico
    ↓
V6: + Métricas
    ↓
V7: + Melodias
    ↓
V8: + Sistema de Pontuação
```

---

## Decisões Definitivas

### 1. Natureza do Sistema

O Cantai2 **NÃO** é um índice.

É um **sistema de sugestões**.

---

### 2. Métrica de Sucesso

O sucesso do aplicativo **NÃO** será medido pela quantidade de resultados encontrados.

Será medido pela **qualidade das sugestões apresentadas**.

---

### 3. Objetivo do Sistema

O objetivo do sistema é **reduzir a carga de decisão da pianista**.

Nunca apresentar listas enormes como comportamento padrão.

---

### 4. Prioridade de Hinários

O CTP permanecerá como **hinário prioritário**.

Os demais hinários terão papel **complementar**.

---

## Consequências

- Cada versão será implementada em Sprint separada
- A evolução é incremental e não quebra funcionalidades existentes
- O motor de sugestões será o coração do Cantai2
- A qualidade das sugestões é mais importante que a quantidade

---

## Referências

- `ADR-0001-interface-e-fluxo.md` — Decisões de interface
- `ADR-0002-motor-de-sugestoes.md` — Motor de Sugestões V1
- `web/index.html` — Interface atual
