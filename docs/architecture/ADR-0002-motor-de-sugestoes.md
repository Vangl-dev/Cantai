# ADR-0002: Motor de Sugestões

**Status:** Aprovado  
**Data:** 2026-07-10  
**Decisor:** Usuário  
**Sprint:** 16  

---

## Contexto

O Cantai2 está evoluindo de um índice de hinos para um **sistema de sugestões** para planejamento de cultos. Este ADR registra as decisões arquiteturais relacionadas ao motor de sugestões.

---

## Decisões

### 1. Hinário Prioritário

O **CTP (Cantai Todos os Povos)** é o hinário prioritário do sistema.

Sempre que possível, as sugestões deverão **privilegiar o CTP**.

---

### 2. Hinários Complementares

Os demais hinários possuem função **complementar**.

São utilizados para:

- Oferecer arranjos diferentes
- Ampliar o repertório
- Evitar repetições
- Apresentar alternativas ao CTP

---

### 3. Filosofia de Sugestão

O aplicativo **NÃO** deverá apresentar listas enormes de resultados.

O comportamento padrão será sempre **sugerir um pequeno conjunto de hinos**.

---

### 4. Regra de Sugestão (Apenas CTP)

Quando existir **apenas o CTP**:

Apresentar até **3 sugestões aleatórias**.

---

### 5. Regra de Sugestão (Múltiplos Hinários)

Quando outros hinários estiverem selecionados:

| Hinário | Sugestões |
|---------|-----------|
| CTP | 3 |
| Hinário adicional | 1 cada |

**Exemplo:**

```
CTP + Harpa
→ 3 CTP + 1 Harpa

CTP + Harpa + HCC
→ 3 CTP + 1 Harpa + 1 HCC
```

---

### 6. Botão "Mais Sugestões"

O botão **"Mais sugestões"** deverá gerar um novo conjunto de sugestões.

**Regras:**

- Enquanto existirem opções inéditas: **NÃO repetir hinos**
- Quando todas as possibilidades forem apresentadas: **reiniciar o ciclo**

---

### 7. Influência da Agenda (Futuro)

Quando implementada, a Agenda deverá considerar:

- Hinos utilizados
- Período de repetição
- Histórico de cultos

**Essa funcionalidade NÃO será implementada nesta Sprint.**

Apenas registrada para referência futura.

---

## Diagrama de Fluxo

```
        [Pesquisa/Tema]
              ↓
        [Filtrar Hinos]
              ↓
    [Selecionar Hinários Ativos]
              ↓
   [Aplicar Regra de Sugestão]
              ↓
   ┌─────────┴─────────┐
   │ 3 CTP + 1 cada    │
   │ hinário adicional  │
   └─────────┬─────────┘
              ↓
        [Exibir Cards]
              ↓
   ┌─────────┴─────────┐
   │ Ver letra │ Escolher│
   └─────────┬─────────┘
              ↓
        [Mais sugestões?]
              ↓
    [Embaralhar/Novo Sorteio]
```

---

## Consequências

- A interface deverá refletir a filosofia de sugestões
- O CTP sempre terá prioridade nas sugestões
- A quantidade de resultados será controlada (máx. 3 + 1 por hinário)
- O motor de sugestões será expandido futuramente com a Agenda

---

## Referências

- `ADR-0001-interface-e-fluxo.md` — Decisões anteriores
- `web/index.html` — Interface atual
- `docs/Fluxo.md` — Documentação de fluxo
