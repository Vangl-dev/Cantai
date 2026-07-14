# ADR-0001: Interface e Fluxo do Cantai2

**Status:** Aprovado  
**Data:** 2026-07-10  
**Decisor:** Usuário  

---

## Contexto

O Cantai2 está em fase de definição arquitetural. As decisões abaixo foram aprovadas e devem guiar todas as implementações futuras.

---

## Decisões

### 1. Natureza do Sistema

O Cantai2 **NÃO** é um leitor de hinos.

Seu objetivo principal é auxiliar no **planejamento de cultos**.

O objeto central do domínio é a **Agenda de Culto**.

O catálogo de hinos existe para apoiar essa finalidade.

---

### 2. Fluxo Principal Aprovado

```
Pesquisa
   ↓
Tema
   ↓
Hinários
   ↓
Resultados
   ↓
Ver letra  |  Escolher
   ↓              ↓
Consulta     Agenda (futura)
```

---

### 3. Botão "Escolher"

O botão "Escolher" **NÃO** abre o hino.

Sua finalidade é **adicionar o hino ao planejamento do culto**.

Enquanto a Agenda não existir, permanecerá como placeholder.

---

### 4. Botão "Ver letra"

O botão "Ver letra" tem finalidade **exclusivamente consultiva**.

Nunca deverá alterar a Agenda.

---

### 5. Layout da Interface

A disposição dos elementos foi aprovada e deverá permanecer:

```
Logo
  ↓
Título
  ↓
Subtítulo
  ↓
Busca
  ↓
Tema
  ↓
Hinários
  ↓
Resultados
```

Mudanças estruturais somente mediante nova aprovação do usuário.

---

### 6. Identidade Visual

A identidade visual do **Cantai original** passa a ser a referência oficial.

Novas funcionalidades deverão respeitar:

- Paleta de cores
- Tipografia
- Bordas
- Espaçamentos
- Estilo dos cards
- Estilo dos botões

---

### 7. Componentes Estáveis

Os componentes abaixo passam a ser considerados **estáveis**:

| Componente | Status |
|------------|--------|
| Modelo Hymn | ✅ Congelado |
| Parser CTP | ✅ Congelado |
| Exportador JSON | ✅ Congelado |
| Busca | ✅ Congelada |
| Importador de Temas | ✅ Congelado |
| Interface Base | ✅ Congelada |
| Identidade Visual | ✅ Congelada |

Alterações nesses componentes somente mediante **autorização explícita do usuário**.

---

### 8. Funcionalidades Previstas

As seguintes funcionalidades estão previstas para o roadmap:

- Importador de Métricas
- Exibição de Métricas
- Hinos relacionados por Métrica
- Importador de Melodias
- Hinos relacionados por Melodia
- **Agenda de Culto**
- Histórico
- Evitar Repetição

Nenhuma dessas funcionalidades deverá exigir mudanças na arquitetura já aprovada.

---

## Consequências

- Todas as Sprints devem respeitar estas decisões
- Alterações em componentes congelados requerem autorização prévia
- A Agenda de Culto será o próximo módulo a ser implementado
- A identidade visual do Cantai original é a referência oficial

---

## Referências

- `web/style-modelo.css` — Referência visual
- `web/index.html` — Interface atual
- `docs/Fluxo.md` — Documentação de fluxo
- `docs/Decisoes_Arquiteturais.md` — Decisões anteriores
