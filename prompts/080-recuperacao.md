# Prompt 080: Recuperação

## Objetivo
Recuperar o sistema após um incidente ou desastre.

## Checklist

### 1. Identificação
- [ ] Identificar o problema
- [ ] Avaliar impacto
- [ ] Notificar time
- [ ] Iniciar registro

### 2. Contenção
- [ ] Limitar dano
- [ ] Isolar componente
- [ ] Manter comunicação
- [ ] Documentar ações

### 3. Erradicação
- [ ] Identificar causa raiz
- [ ] Remover causa
- [ ] Implementar correção
- [ ] Testar correção

### 4. Recuperação
- [ ] Restaurar sistema
- [ ] Verificar integridade
- [ ] Monitorar estabilidade
- [ ] Confirmar resolução

### 5. Pós-Incidente
- [ ] Escrever post-mortem
- [ ] Documentar lições
- [ ] Implementar prevenção
- [ ] Comunicar resultado

## Tipos de Incidente

### Sistema Fora do Ar
```bash
# Verificar logs
tail -f /var/log/app/error.log

# Reiniciar serviço
systemctl restart app

# Verificar health check
curl http://localhost:3000/health
```

### Dados Corrompidos
```bash
# Parar escritas
# Avaliar escopo
# Restaurar backup
# Validar integridade
# Retomar operações
```

### Vazamento de Dados
```bash
# Conter incidente
# Avaliar impacto
# Notificar afetados
# Corrigir vulnerabilidade
# Documentar lições
```

## Template de Post-Mortem

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

## Contatos de Emergência

| Papel | Nome | Contato |
|-------|------|---------|
| Responsável Técnico | [nome] | [contato] |
| DBA | [nome] | [contato] |
| Infraestrutura | [nome] | [contato] |

## Comandos Úteis

```bash
# Verificar status do serviço
systemctl status [service]

# Verificar logs
journalctl -u [service] -f

# Reiniciar serviço
systemctl restart [service]

# Verificar espaço em disco
df -h

# Verificar memória
free -m

# Verificar processos
top
```

## Perguntas para o Desenvolvedor

1. Qual é o problema?
2. Quando começou?
3. Qual o impacto?
4. Já tentou corrigir?
5. Precisa de ajuda?

## Saída Esperada

Após completar este prompt:
- Incidente resolvido
- Sistema restaurado
- Post-mortem escrito
- Lições documentadas
- Ações preventivas implementadas

## Referências

- [Recuperação](../docs/Recuperacao.md)
- [Segurança](../docs/Seguranca.md)
- [Lições Aprendidas](../docs/Licoes_Aprendidas.md)
