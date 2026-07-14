# Exemplo de Post-Mortem

---

# Post-Mortem: Indisponibilidade do Sistema

## Data
2026-07-06 14:00 - 16:30 (2h30min)

## Duração
2 horas e 30 minutos

## Impacto
- **Usuários afetados:** ~500
- **Funcionalidades:** Login, API principal
- **Receita:** Estimativa de perda

## Timeline

| Hora | Evento |
|------|--------|
| 14:00 | Deploy de nova feature |
| 14:15 | Primeiros erros nos logs |
| 14:30 | Alerta de health check falhando |
| 14:45 | Time acionado |
| 15:00 | Causa identificada: query SQL com erro |
| 15:30 | Rollback iniciado |
| 16:00 | Sistema restaurado |
| 16:30 | Monitoramento confirmou estabilidade |

## Causa Raiz

Uma query SQL foi escrita com sintaxe incorreta que funcionava em SQLite (usado em testes) mas falhava em PostgreSQL (produção).

```sql
-- Errado (funciona em SQLite)
SELECT * FROM users WHERE id IN (1, 2, 3)

-- Correto (PostgreSQL)
SELECT * FROM users WHERE id = ANY(ARRAY[1, 2, 3])
```

## O que foi Feito

1. **Rollback** para versão anterior
2. **Correção** da query
3. **Testes** em ambiente de staging com PostgreSQL
4. **Deploy** da correção
5. **Monitoramento** por 2 horas

## Lições Aprendidas

1. **Testar com o mesmo banco** de produção
2. **CI/CD deve usar PostgreSQL** não SQLite
3. **Health checks mais frequentes** após deploy
4. **Rollback testado** regularmente

## Ações Preventivas

### Imediatas
- [x] Corrigir query
- [x] Atualizar CI/CD para usar PostgreSQL
- [x] Documentar lição

### Futuras
- [ ] Testes de integração com banco real
- [ ] Canary deployment
- [ ] Health checks mais granulares

## Métricas

| Métrica | Valor |
|---------|-------|
| Downtime | 2h30min |
| Usuários afetados | ~500 |
| Tempo para detectar | 15min |
| Tempo para resolver | 2h |
| Causa raiz | Query SQL |

## Agradecimentos

- Time de infraestrutura pela resposta rápida
- Time de desenvolvimento pela correção ágil
- Usuários pela paciência

---

**Última atualização:** 2026-07-06
