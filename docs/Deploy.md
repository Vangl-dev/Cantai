# Deploy

## Visão Geral

Este documento define o processo de deploy seguro e confiável para os projetos do framework.

## Princípios

### 1. Deploy é uma Operação Segura
- Sempre ter rollback disponível
- Testar antes de production
- Documentar cada deploy

### 2. Automatização é Chave
- CI/CD para todos os projetos
- Deploy via pipeline
- Verificações automáticas

### 3. Transparência Total
- Log de cada deploy
- Notificação ao time
- Health checks pós-deploy

---

## Tipos de Deploy

### Blue-Green
- Dois ambientes idênticos
- Troca instantânea
- Rollback rápido

### Canary
- Deploy gradual
- Monitoramento em tempo real
- Rollback se houver erro

### Rolling
- Atualização incremental
- Zero downtime
- Mais lento que blue-green

---

## Processo de Deploy

### 1. Pré-Deploy
```bash
# Checklist
- [ ] Código testado
- [ ] Lint passando
- [ ] Build OK
- [ ] Variáveis de ambiente configuradas
- [ ] Backup confirmado
- [ ] Time notificado
```

### 2. Deploy
```bash
# Exemplo com Docker
docker-compose -f docker-compose.prod.yml up -d

# Exemplo com PM2
pm2 deploy production

# Exemplo com Vercel
vercel --prod
```

### 3. Pós-Deploy
```bash
# Verificações
- [ ] Health check OK
- [ ] Logs sem erros
- [ ] Funcionalidades testadas
- [ ] Performance OK
- [ ] Notificação enviada
```

---

## Variáveis de Ambiente

### Organização
```
# Produção
DATABASE_URL=postgresql://...
API_KEY=xxx
SECRET_KEY=xxx

# Staging
DATABASE_URL=postgresql://...
API_KEY=xxx
SECRET_KEY=xxx
```

### Segurança
- NUNCA committar variáveis de ambiente
- Usar gerenciador de segredos
- Rotacionar periodicamente
- Ter ambiente separado por stage

---

## Health Checks

### Endpoint Recomendado
```javascript
// GET /health
{
    "status": "ok",
    "timestamp": "2026-07-06T12:00:00Z",
    "version": "1.0.0",
    "checks": {
        "database": "ok",
        "cache": "ok",
        "external": "ok"
    }
}
```

### Verificações
- Aplicação respondendo
- Banco de dados conectado
- Cache funcionando
- Serviços externos acessíveis

---

## Rollback

### Quando Usar
- Erro em production
- Performance degradada
- Funcionalidade quebrada
- Dados corrompidos

### Processo
1. Identificar problema
2. Decidir por rollback
3. Executar rollback
4. Verificar estabilidade
5. Documentar incidente

### Comandos
```bash
# Docker
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Git
git revert HEAD
git push origin main

# PM2
pm2 deploy production revert 1
```

---

## Monitoramento

### Métricas Importantes
- Tempo de resposta
- Taxa de erro
- Uso de memória
- Uso de CPU
- Conexões de banco

### Ferramentas
- Prometheus + Grafana
- Datadog
- New Relic
- Sentry (erros)

### Alertas
- Erro rate > 1%
- Response time > 2s
- Memory > 80%
- Disk > 90%

---

## Checklist de Deploy

### Antes do Deploy
- [ ] Código revisado e aprovado
- [ ] Testes passando
- [ ] Lint passando
- [ ] Build successful
- [ ] Variáveis de ambiente OK
- [ ] Backup confirmado
- [ ] Time notificado
- [ ] Rollback planejado

### Durante o Deploy
- [ ] Deploy iniciado
- [ ] Health checks passando
- [ ] Sem erros nos logs
- [ ] Funcionalidades testadas

### Após o Deploy
- [ ] Deploy completo
- [ ] Monitoramento ativo
- [ ] Performance OK
- [ ] Notificação enviada
- [ ] CHANGELOG atualizado
- [ ] Tag criada

---

## Ambientes

### Desenvolvimento
- Local
- Dados de teste
- Debug ativado

### Staging
- Espelho de produção
- Dados anonimizados
- Performance monitoring

### Produção
- Ambiente real
- Dados reais
- Segurança máxima

---

## Referências

- [Segurança](Seguranca.md)
- [Recuperação](Recuperacao.md)
- [Checklists de Deploy](../checklists/)
