# Checklists

## Visão Geral

Checklists são ferramentas essenciais para garantir que nada seja esquecido. Todo checklist deve ser preenchido antes de avançar para a próxima fase.

## Princípios

### 1. Checklist é Obrigatório
- NÃO pular checklists
- NÃO assinalar sem verificar
- Documentar exceções

### 2. Checklist é VIVO
- Atualizar conforme necessidade
- Adicionar novos itens quando aprender
- Remover itens obsoletos

### 3. Checklist é COMUNICAÇÃO
- Mostra progresso
- Identifica bloqueios
- Facilita handoff

---

## Checklists Disponíveis

### 1. Nova Sprint
**Quando:** Início de cada sprint
**Arquivo:** `checklists/nova-sprint.md`

### 2. Release
**Quando:** Preparar para release
**Arquivo:** `checklists/release.md`

### 3. Deploy
**Quando:** Fazer deploy
**Arquivo:** `checklists/deploy.md`

### 4. Backup
**Quando:** Realizar backup
**Arquivo:** `checklists/backup.md`

### 5. Banco de Dados
**Quando:** Mudanças em banco
**Arquivo:** `checklists/banco-de-dados.md`

### 6. Documentação
**Quando:** Atualizar documentação
**Arquivo:** `checklists/documentacao.md`

### 7. Segurança
**Quando:** Revisão de segurança
**Arquivo:** `checklists/seguranca.md`

### 8. Validação
**Quando:** Validação final
**Arquivo:** `checklists/validacao.md`

### 9. Git
**Quando:** Operações Git
**Arquivo:** `checklists/git.md`

### 10. Checkpoint
**Quando:** Ao término de cada etapa
**Arquivo:** `checklists/checkpoint.md`

### 11. Validação de Deploy
**Quando:** Antes de cada deploy
**Arquivo:** `checklists/validacao-deploy.md`

---

## Como Usar Checklists

### Passo 1: Selecionar Checklist
Escolha o checklist adequado para a tarefa

### Passo 2: Preencher
Marque cada item após verificar

### Passo 3: Documentar Exceções
Se algo não se aplicar, documente o motivo

### Passo 4: Revisar
Antes de finalizar, revise todo o checklist

### Passo 5: Arquivar
Guarde o checklist preenchido para referência

---

## Formato de Checklist

```markdown
# Checklist: [Nome]

## Pré-requisitos
- [ ] Item 1
- [ ] Item 2

## Passos
- [ ] Passo 1
- [ ] Passo 2

## Validação
- [ ] Validação 1
- [ ] Validação 2

## Pós-requisitos
- [ ] Item final 1
- [ ] Item final 2

## Observações
- [Campo para notas]
```

---

## Checklist Automatizado

### Quando Automatizar
- Verificações que podem ser scriptadas
- Validações de código
- Verificações de segurança
- Builds e deploys

### Como Automatizar
```bash
# Exemplo de script de validação
#!/bin/bash
echo "Rodando lint..."
npm run lint

echo "Rodando testes..."
npm test

echo "Verificando segurança..."
npm audit

echo "Checklist automatizado completo!"
```

---

## Métricas de Checklist

### O que Medir
- Taxa de conclusão
- Tempo médio de preenchimento
- Itens mais esquecidos
- Exceções mais comuns

### Como Usar
- Identificar gargalos
- Melhorar processos
- Atualizar checklists
- Treinar time

---

## Referências

- [Fluxo de Desenvolvimento](Fluxo.md)
- [Qualidade](Qualidade.md)
- [Boas Práticas](Boas_Praticas.md)
