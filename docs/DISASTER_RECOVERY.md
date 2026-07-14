# DISASTER_RECOVERY

## Política de Recuperação de Desastres

**Data de Criação:** 2026-07-07
**Última Atualização:** 2026-07-07
**Status:** ATIVO - OBRIGATÓRIO

---

## Objetivo

Definir procedimentos para recuperação de desastres e garantir continuidade do negócio.

---

## Tipos de Desastre

### 1. Perda de Banco de Dados
- Corrupção
- Exclusão acidental
- Falha de hardware

### 2. Perda de Arquivos
- Exclusão acidental
- Corrupção
- Ransomware

### 3. Falha de Sistema
- Servidor fora do ar
- Deploy quebrado
- Dependência externa falha

### 4. Erro da IA
- Ação destrutiva executada
- Dados corrompidos por IA
- Configurações alteradas indevidamente

---

## Procedimentos de Recuperação

### 1. Recuperação de Banco

#### Passos
1. **Identificar** o escopo da perda
2. **Verificar** backups disponíveis
3. **Restaurar** do backup mais recente
4. **Validar** integridade dos dados
5. **Documentar** o incidente

#### Comandos
```bash
# PostgreSQL
pg_restore -d database_name backup.dump

# MySQL
mysql -u user -p database_name < backup.sql

# MongoDB
mongorestore --db database_name backup/
```

#### Validação
```sql
-- Verificar contagem de registros
SELECT COUNT(*) FROM tabela_principal;

-- Verificar integridade
SELECT * FROM information_schema.table_constraints;
```

---

### 2. Recuperação de JSON

#### Passos
1. **Identificar** JSON corrompido
2. **Localizar** última versão funcional
3. **Restaurar** JSON
4. **Validar** estrutura
5. **Testar** funcionalidade

#### Comandos
```bash
# Verificar JSON válido
cat arquivo.json | python -m json.tool

# Restaurar do backup
cp backups/arquivo.json.bak config/arquivo.json
```

---

### 3. Recuperação de Configurações

#### Passos
1. **Identificar** configuração alterada
2. **Verificar** .env.example
3. **Restaurar** configurações
4. **Testar** aplicação
5. **Documentar** mudança

#### Comandos
```bash
# Restaurar .env
cp .env.example .env

# Editar manualmente
nano .env
```

---

### 4. Rollback de Versões

#### Passos
1. **Identificar** versão estável
2. **Criar** branch de rollback
3. **Aplicar** rollback
4. **Testar** funcionamento
5. **Deploy** rollback

#### Comandos
```bash
# Identificar última tag estável
git tag -l

# Criar branch de rollback
git checkout -b rollback/v1.0.0 v1.0.0

# Push
git push origin rollback/v1.0.0
```

---

### 5. Recuperação Após Erro da IA

#### Passos
1. **Identificar** o que foi alterado
2. **Verificar** histórico Git
3. **Reverter** alterações
4. **Validar** estado anterior
5. **Documentar** o erro

#### Comandos
```bash
# Ver alterações recentes
git status
git diff

# Reverter último commit
git revert HEAD

# Reverter para commit específico
git checkout <commit-hash> -- arquivo
```

---

### 6. Reconstrução Completa

#### Passos
1. **Clonar** repositório
2. **Restaurar** banco de backup
3. **Configurar** variáveis de ambiente
4. **Instalar** dependências
5. **Rodar** migrações
6. **Testar** tudo

#### Comandos
```bash
# Clonar
git clone https://github.com/org/repo.git
cd repo

# Instalar
npm install

# Configurar
cp .env.example .env
# Editar .env

# Migrar
npm run migrate

# Testar
npm test
```

---

### 7. Restauração por Git

#### Passos
1. **Identificar** commit estável
2. **Resetar** para commit
3. **Forçar** push (se necessário)
4. **Validar** estado

#### Comandos
```bash
# Ver histórico
git log --oneline

# Resetar para commit
git reset --hard <commit-hash>

# Forçar push (CUIDADO)
git push --force origin main
```

**⚠️ ATENÇÃO:** Force push é operação destrutiva. Usar apenas em emergências.

---

### 8. Restauração por Backup

#### Passos
1. **Localizar** backup
2. **Verificar** integridade
3. **Restaurar** backup
4. **Validar** dados
5. **Testar** funcionalidade

#### Comandos
```bash
# Listar backups
ls -la backups/

# Verificar integridade
tar -tzf backups/backup_20260707.tar.gz

# Restaurar
tar -xzf backups/backup_20260707.tar.gz -C /
```

---

## Checklists de Recuperação

### Checklist Geral
- [ ] Incidente identificado
- [ ] Escopo avaliado
- [ ] Time notificado
- [ ] Backup verificado
- [ ] Procedimento selecionado
- [ ] Recuperação executada
- [ ] Validação realizada
- [ ] Documentação atualizada

### Checklist de Validação
- [ ] Dados integrais
- [ ] Funcionalidade testada
- [ ] Performance verificada
- [ ] Logs verificados
- [ ] Monitoramento ativo

---

## Contatos de Emergência

| Papel | Nome | Contato |
|-------|------|---------|
| Responsável Técnico | [nome] | [contato] |
| DBA | [nome] | [contato] |
| Infraestrutura | [nome] | [contato] |

---

## Referências

- [Recuperação](Recuperacao.md)
- [Segurança](Seguranca.md)
- [FORBIDDEN_ACTIONS](FORBIDDEN_ACTIONS.md)

---

**IMPORTANTE:** Sempre criar backup antes de qualquer operação de recuperação.
