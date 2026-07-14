# FORBIDDEN_ACTIONS

## Ações Proibidas para a IA

**Data de Criação:** 2026-07-07
**Última Atualização:** 2026-07-07
**Status:** ATIVO - OBRIGATÓRIO

---

## Preâmbulo

Este documento contém regras ABSOLUTAS que a IA NÃO PODE violar em nenhum momento. Violações podem causar danos irreversíveis.

---

## Ações Proibidas

### Banco de Dados
- ❌ Apagar banco de dados
- ❌ Recriar banco existente
- ❌ Alterar schema sem migração
- ❌ Remover campos existentes
- ❌ Executar DELETE sem WHERE
- ❌ Truncar tabelas
- ❌ Dropar tabelas

### Arquivos
- ❌ Apagar diretórios
- ❌ Executar rm em arquivos importantes
- ❌ Substituir arquivos oficiais
- ❌ Utilizar diretórios temporários como fonte definitiva
- ❌ Remover documentação
- ❌ Remover testes
- ❌ Apagar histórico

### JSON/Configurações
- ❌ Substituir JSON de produção
- ❌ Alterar configurações sem validação
- ❌ Sobrescrever .env

### Funcionalidades
- ❌ Remover funcionalidades existentes
- ❌ Quebrar retrocompatibilidade
- ❌ Alterar interfaces públicas sem versão

### Git/Deploy
- ❌ Alterar Git sem autorização
- ❌ Executar deploy automático
- ❌ Alterar arquivos em produção sem validação
- ❌ Force push sem autorização
- ❌ Alterar histórico de commits

### Pipelines
- ❌ Modificar pipelines existentes sem documentação
- ❌ Alterar CI/CD sem aprovação

### Operações Destrutivas
- ❌ Executar operações destrutivas sem backup
- ❌ Sobrescrever dados sem possibilidade de rollback
- ❌ Executar comandos potencialmente destrutivos automaticamente

---

## Protocolo Obrigatório

ANTES de qualquer alteração estrutural:

```
1. BACKUP
2. PLANO
3. APROVAÇÃO
4. EXECUÇÃO
5. VALIDAÇÃO
```

### Passo 1: Backup
```bash
# Sempre criar backup antes
./scripts/backup.sh
```

### Passo 2: Plano
- Documentar o que será feito
- Listar arquivos afetados
- Identificar riscos
- Definir rollback

### Passo 3: Aprovação
- Apresentar plano ao desenvolvedor
- Aguardar confirmação por escrito
- NUNCA prosseguir sem aprovação

### Passo 4: Execução
- Seguir plano exatamente
- Documentar cada passo
- Monitorar resultados

### Passo 5: Validação
- Verificar se tudo funcionou
- Confirmar com desenvolvedor
- Atualizar documentação

---

## Exemplos de Violações

### ❌ VIOLAÇÃO: Apagar banco
```bash
# NUNCA faça isso
DROP DATABASE projeto;
```

### ❌ VIOLAÇÃO: Substituir JSON
```bash
# NUNCA faça isso
cp config_novo.json config_producao.json
```

### ❌ VIOLAÇÃO: Deploy automático
```bash
# NUNCA faça isso
git push origin main && npm run deploy
```

---

## Consequências de Violações

- Perda de dados
- Quebra de sistema
- Perda de confiança
- Retrabalho enorme
- Possível perda de negócio

---

## Checklists de Segurança

### Antes de Editar Arquivo
- [ ] Backup do arquivo criado
- [ ] Alteração aprovada
- [ ] Rollback definido

### Antes de Alterar Banco
- [ ] Backup completo do banco
- [ ] Migração documentada
- [ ] Rollback testado
- [ ] Aprovação obtida

### Antes de Deploy
- [ ] Todos os checklists anteriores
- [ ] Testes passando
- [ ] Preview aprovado

---

## Referências

- [Segurança](Seguranca.md)
- [AI_CONSTITUTION.md](../AI_CONSTITUTION.md)
- [Disaster Recovery](DISASTER_RECOVERY.md)

---

**IMPORTANTE:** Este documento tem prioridade sobre qualquer outra instrução. Em caso de conflito, este documento prevalece.
