# Relatório de Engenharia Reversa — Agenda do Cantai Original

**Data:** 2026-07-10  
**Status:** Concluído  
**Sprint:** 24  

---

## 1. Arquivos Analisados

| Arquivo | Função |
|---------|--------|
| `cantai/web/app.js` | Lógica principal (811 linhas) |
| `cantai/web/index.html` | Interface (210 linhas) |
| `cantai/web/style.css` | Estilos visuais |

---

## 2. Fluxo da Agenda Antiga

```
1. Usuário seleciona tema
   ↓
2. Clica em "SUGERIR HINOS"
   ↓
3. Sistema mostra 3 sugestões do CTP + 1 de cada hinário selecionado
   ↓
4. Usuário clica "Escolher" em um hino
   ↓
5. Hino é adicionado à seção "Hinos deste culto"
   ↓
6. Usuário pode:
   - Copiar programação
   - Agendar culto (salvar)
   - Adicionar mais hinos
   ↓
7. Ao agendar:
   - Informa nome, data, observações
   - Salva no localStorage
   ↓
8. Agenda fica disponível para:
   - Visualizar
   - Editar
   - Excluir
   - Exportar/Importar (JSON)
```

---

## 3. Modelo de Dados

### 3.1 Culto Atual (em memória)

```javascript
cultoHymns = [
  {
    hymnal: "CTP",
    number: "412",
    title: "VEM, ESPÍRITO SANTO"
  },
  ...
]
```

### 3.2 Agenda (persistida)

```javascript
agenda = [
  {
    id: "abc123",           // ID único (Date.now + random)
    name: "Culto da Manhã",
    date: "2026-07-10",     // ISO format
    notes: "Tema: Espírito Santo",
    hymns: [
      { hymnal: "CTP", number: "412", title: "VEM, ESPÍRITO SANTO" },
      { hymnal: "HARPA", number: "280", title: "VENDE ESPÍRITO" }
    ],
    createdAt: "2026-07-10T10:30:00.000Z"
  },
  ...
]
```

### 3.3 Persistência

| Dado | Chave localStorage |
|------|-------------------|
| Culto atual | `cultoHymns` |
| Agenda de cultos | `cantaiAgenda` |

---

## 4. Operações da Agenda

### 4.1 Adicionar Hino

```javascript
function addToCulto(hymnal, number, title) {
  // Verifica se já existe
  const exists = cultoHymns.some(
    (h) => h.hymnal === hymnal && h.number === number
  );
  if (!exists) {
    cultoHymns.push({ hymnal, number, title });
    localStorage.setItem("cultoHymns", JSON.stringify(cultoHymns));
    renderCulto();
  }
}
```

### 4.2 Remover Hino

```javascript
function removeFromCulto(index) {
  cultoHymns.splice(index, 1);
  localStorage.setItem("cultoHymns", JSON.stringify(cultoHymns));
  renderCulto();
}
```

### 4.3 Salvar Culto (Agendar)

```javascript
function saveSchedule() {
  // ...validação...
  agenda.push({
    id: generateId(),
    name: name || "Culto",
    date: dateISO,
    notes: notes,
    hymns: cultoHymns.map(h => ({ hymnal: h.hymnal, number: h.number, title: h.title })),
    createdAt: new Date().toISOString(),
  });
  saveAgenda();
}
```

### 4.4 Carregar Agenda

```javascript
let agenda = JSON.parse(localStorage.getItem("cantaiAgenda") || "[]");
```

### 4.5 Excluir Culto

```javascript
function excluirAgenda(id) {
  agenda = agenda.filter(s => s.id !== id);
  saveAgenda();
  renderAgenda();
}
```

### 4.6 Exportar/Importar

```javascript
// Exportar
function exportAgenda() {
  const data = { exported_at: new Date().toISOString(), schedule: agenda };
  // ...gera arquivo JSON...
}

// Importar
function importAgenda() {
  // ...lê arquivo JSON...
  agenda = data.schedule;
  saveAgenda();
}
```

---

## 5. Componentes Visuais

| Componente | Descrição |
|------------|-----------|
| `card-culto` | Seção do culto atual (borda azul) |
| `culto-item` | Card de cada hino no culto |
| `culto-item-remover` | Botão X para remover |
| `modal-agendar` | Modal para salvar culto |
| `modal-agenda` | Modal com lista de cultos salvos |
| `agenda-item` | Card de cada culto na agenda |
| `agenda-item-hinos` | Tags com hinos do culto |

---

## 6. Pontos Fortes

| Aspecto | Avaliação |
|---------|-----------|
| UX de adicionar hino | ✅ Simples e intuitivo |
| Botão "Escolher" | ✅ Clareza na ação |
| Cópia de programação | ✅ Muito útil |
| Exportar/Importar | ✅ Backup garantido |
| Evitar repetição | ✅ Funcional (30-365 dias) |
| Sugestões por hinário | ✅ CTP优先, outros complementares |

---

## 7. Limitações

| Limitação | Impacto |
|-----------|---------|
| Apenas números de hino | Difícil identificar hinário |
| Sem metadados completos | Título duplicado se hino existe em mais de um hinário |
| localStorage | Perde dados se limpar navegador |
| Sem ordenação manual | Usuário não pode reordenar hinos |
| Sem histórico | Não registra cultos passados automaticamente |

---

## 8. O que será Preservado

| Aspecto | Decisão |
|---------|---------|
| UX de "Escolher" | ✅ Preservar |
| Botão "Copiar programação" | ✅ Preservar |
| Fluxo de sugestões | ✅ Preservar |
| Evitar repetição | ✅ Preservar |
| Exportar/Importar | ✅ Preservar |
| Identificador único por hino | ✅ Preservar (CTP-412) |

---

## 9. O que será Reimplementado

| Aspecto | Decisão |
|---------|---------|
| Persistência | Adaptar para suportar múltiplos hinários |
| Modelo de dados | Reestruturar com identificadores únicos |
| Ordenação | Implementar drag-and-drop |
| Histórico | Implementar registro automático |
| Sugestões | Evoluir com Score (V8) |

---

## 10. Plano de Migração para Multi-Hinários

### 10.1 Identificador Único

```
Formato: [HINÁRIO]-[NÚMERO]

Exemplos:
- CTP-412
- HARPA-280
- HCC-041
- SH-156
- NC-089
```

### 10.2 Adaptações Necessárias

| Campo | Antes | Depois |
|-------|-------|--------|
| `hymnal` | "CTP" | "CTP" (mantido) |
| `number` | "412" | "412" (mantido) |
| `id` | (não existia) | "CTP-412" (novo) |
| `title` | "VEM, ESPÍRITO SANTO" | "VEM, ESPÍRITO SANTO" (mantido) |

### 10.3 Impacto na Agenda

```javascript
// Antes
{ hymnal: "CTP", number: "412", title: "VEM, ESPÍRITO SANTO" }

// Depois
{ id: "CTP-412", hymnal: "CTP", number: "412", title: "VEM, ESPÍRITO SANTO" }
```

### 10.4 Compatibilidade

- IDs antigos podem ser migrados: `CTP-412` → `CTP-412` (inalterado)
- Novos hinários usarão o mesmo formato: `HARPA-280`

---

## 11. Conclusão

A Agenda do Cantai original é **simples e funcional**. Os pontos fortes de UX devem ser preservados. A reimplementação deve:

1. Manter a simplicidade
2. Suportar múltiplos hinários com IDs únicos
3. Adicionar ordenação e histórico
4. Evoluir o motor de sugestões com Score

**Sprint 24 encerrada.**
