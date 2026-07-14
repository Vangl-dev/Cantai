# RECOVERY

## Visão Geral

Este documento define procedimentos de recuperação para o projeto.

## Contatos de Emergência

| Papel | Nome | Telefone | Email |
|-------|------|----------|-------|
| Responsável Técnico | [nome] | [fone] | [email] |
| DBA | [nome] | [fone] | [email] |
| Infraestrutura | [nome] | [fone] | [email] |

---

## Tipos de Incidentes

### 1. Sistema Fora do Ar

#### Sintomas
- Aplicação não responde
- Erro 500 em produção
- Health check falhando

#### Procedimento
1. **Verificar** logs de erro
2. **Identificar** causa raiz
3. **Corrigir** o problema
4. **Testar** em staging
5. **Deploy** correção
6. **Monitorar** estabilidade

#### Rollback
```bash
# Docker
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# PM2
pm2 deploy production revert 1

# Git
git revert HEAD
git push origin main
```

---

### 2. Dados Corrompidos

#### Sintomas
- Dados inconsistentes
- Erros de integridade
- Usuários reportando problemas

#### Procedimento
1. **Parar** escritas no banco
2. **Avaliar** escopo da corrupção
3. **Restaurar** do backup
4. **Validar** integridade
5. **Retomar** operações
6. **Documentar** incidente

#### Restauração
```bash
# PostgreSQL
pg_restore -d database_name backup.dump

# MySQL
mysql -u user -p database_name < backup.sql

# MongoDB
mongorestore --db database_name backup/
```

---

### 3. Vazamento de Dados

#### Sintomas
- Acesso não autorizado
- Dados sensíveis expostos
- Atividade suspeita

#### Procedimento
1. **Conter** o incidente
2. **Avaliar** impacto
3. **Notificar** afetados
4. **Corrigir** vulnerabilidade
5. **Fortalecer** segurança
6. **Documentar** lições

#### Notificação
- [ ] Usuários afetados
- [ ] Autoridades (se necessário)
- [ ] Time interno
- [ ] Público (se necessário)

---

### 4. Performance Degradada

#### Sintomas
- Lentidão extrema
- Timeouts
- Memory leak

#### Procedimento
1. **Monitorar** métricas
2. **Identificar** gargalo
3. **Otimizar** código/infra
4. **Testar** mudanças
5. **Deploy** otimização
6. **Validar** melhoria

---

## Backup

### Configuração Atual
| Componente | Frequência | Horário | Retenção |
|------------|------------|---------|----------|
| Database | Diário | 02:00 | 30 dias |
| Code | Contínuo | - | Indefinido |
| Config | Semanal | Domingo 03:00 | 90 dias |

### Verificação de Backup
```bash
# Verificar último backup
ls -la /backups/

# Testar restauração
pg_restore --list backup.dump
```

---

## Testes de Recuperação

### Frequência
- **Mensal:** Teste de restauração de backup
- **Trimestral:** Teste de failover
- **Semestral:** Simulação completa de desastre

### Procedimento de Teste
1. Criar ambiente de teste
2. Restaurar backup
3. Validar integridade
4. Documentar resultados
5. Melhorar procedimentos

---

## Post-Mortem

### Template
```markdown
# Post-Mortem: [Título]

## Data
YYYY-MM-DD HH:MM

## Duração
[X horas]

## Impacto
[Descrição do impacto]

## Timeline
- HH:MM - Evento 1
- HH:MM - Evento 2
- HH:MM - Resolução

## Causa Raiz
[Análise detalhada]

## O que foi feito
[Ações tomadas]

## Lições Aprendidas
[Insights]

## Ações Preventivas
[Medidas para evitar recorrência]
```

---

## Checklists de Emergência

### Checklist Inicial
- [ ] Incidente identificado
- [ ] Time notificado
- [ ] Escopo avaliado
- [ ] Ação tomada

### Checklist de Resolução
- [ ] Problema resolvido
- [ ] Sistema estável
- [ ] Monitoramento ativo
- [ ] Documentação atualizada

### Checklist Pós-Incidente
- [ ] Post-mortem escrito
- [ ] Lições documentadas
- [ ] Ações preventivas implementadas
- [ ] Time comunicado

---

## Recursos

### Links Úteis
- [Dashboard de Monitoramento](url)
- [Logs de Produção](url)
- [Documentação de Deploy](url)
- [Guia de Troubleshooting](url)

### Comandos Úteis
```bash
# Verificar status do serviço
systemctl status [service]

# Verificar logs
journalctl -u [service] -f

# Reiniciar serviço
systemctl restart [service]
```

---

**Última atualização:** YYYY-MM-DD
