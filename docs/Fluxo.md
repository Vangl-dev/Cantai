# Fluxo de Desenvolvimento

## Visão Geral

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  ABERTURA   │───▶│ PLANEJAMENTO│───▶│   SPRINT    │
│  (000)      │    │  (010)      │    │   (020)     │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                   ┌─────────────┐            │
                   │  RELEASE    │◀───────────┤
                   │  (060)      │            │
                   └─────────────┘            │
                          │                   │
                   ┌─────────────┐            │
                   │  DEPLOY     │◀───────────┘
                   │  (070)      │
                   └─────────────┘
```

## Fases Detalhadas

### Fase 0: Abertura (Prompt 000)
**Quando:** Início de um novo projeto
**O que fazer:**
1. Criar estrutura base usando template
2. Preencher README.md com contexto do projeto
3. Configurar AI_INSTRUCTIONS.md
4. Criar PROJECT_STATE.md inicial
5. Registrar primeira decisão em DECISIONS.md

**Checklist:**
- [ ] Template copiado
- [ ] README.md preenchido
- [ ] AI_INSTRUCTIONS.md configurado
- [ ] PROJECT_STATE.md criado
- [ ] Primeira decisão registrada

---

### Fase 1: Planejamento (Prompt 010)
**Quando:** Antes de cada sprint significativa
**O que fazer:**
1. Revisar PROJECT_STATE.md
2. Definir objetivos da sprint
3. Criar tarefas com estimativas
4. Priorizar usando critérios claros
5. Atualizar ROADMAP.md

**Checklist:**
- [ ] PROJECT_STATE.md revisado
- [ ] Objetivos definidos
- [ ] Tarefas criadas
- [ ] Estimativas feitas
- [ ] ROADMAP.md atualizado

---

### Fase 2: Sprint (Prompt 020)
**Quando:** Desenvolvimento ativo
**O que fazer:**
1. Seguir tarefas na ordem de prioridade
2. Testar cada tarefa antes de avançar
3. Commitar com mensagens semânticas
4. Atualizar CHANGELOG quando relevante
5. Documentar bloqueios imediatamente

**Checklist:**
- [ ] Tarefas seguindo prioridade
- [ ] Testes passando
- [ ] Commits semânticos
- [ ] CHANGELOG atualizado
- [ ] Bloqueios documentados

---

### Fase 3: Debug (Prompt 030)
**Quando:** Ao encontrar bugs
**O que fazer:**
1. Documentar o bug em KNOWN_ISSUES.md
2. Criar issue no GitHub (se aplicável)
3. Investigar causa raiz
4. Implementar correção
5. Testar a correção
6. Registrar lição aprendida

**Checklist:**
- [ ] Bug documentado
- [ ] Causa raiz identificada
- [ ] Correção implementada
- [ ] Testes passando
- [ ] Lição registrada

---

### Fase 4: Refatoração (Prompt 040)
**Quando:** Quando código precisa de melhoria
**O que fazer:**
1. Identificar o que refatorar
2. Garantir testes existentes
3. Refatorar incrementalmente
4. Rodar testes após cada mudança
5. Documentar o que mudou

**Checklist:**
- [ ] Áreas identificadas
- [ ] Testes existentes confirmados
- [ ] Refatoração incremental
- [ ] Testes passando
- [ ] Mudanças documentadas

---

### Fase 5: Documentação (Prompt 050)
**Quando:** Quando documentação está desatualizada
**O que fazer:**
1. Revisar documentação existente
2. Atualizar README.md
3. Atualizar ARCHITECTURE.md
4. Adicionar exemplos se necessário
5. Verificar links internos

**Checklist:**
- [ ] Documentação revisada
- [ ] README.md atualizado
- [ ] ARCHITECTURE.md atualizado
- [ ] Exemplos adicionados
- [ ] Links verificados

---

### Fase 6: Release (Prompt 060)
**Quando:** Preparar para release
**O que fazer:**
1. Preencher checklist de release
2. Atualizar CHANGELOG
3. Criar tag de versão
4. Atualizar PROJECT_STATE.md
5. Notificar stakeholders

**Checklist:**
- [ ] Checklist de release preenchido
- [ ] CHANGELOG atualizado
- [ ] Tag criada
- [ ] PROJECT_STATE.md atualizado
- [ ] Notificação enviada

---

### Fase 7: Deploy
**Quando:** Fazer deploy
**O que fazer:**
1. Preencher checklist de deploy
2. Verificar variáveis de ambiente
3. Confirmar backup
4. Executar deploy
5. Verificar health checks
6. Documentar o deploy

**Checklist:**
- [ ] Checklist de deploy preenchido
- [ ] Variáveis de ambiente verificadas
- [ ] Backup confirmado
- [ ] Deploy executado
- [ ] Health checks passando
- [ ] Deploy documentado

---

### Fase 8: Backup (Prompt 070 - Backup)
**Quando:** Regularmente ou antes de mudanças grandes
**O que fazer:**
1. Preencher checklist de backup
2. Executar script de backup
3. Verificar integridade do backup
4. Armazenar backup em local seguro
5. Documentar o backup

**Checklist:**
- [ ] Checklist de backup preenchido
- [ ] Backup executado
- [ ] Integridade verificada
- [ ] Backup armazenado
- [ ] Backup documentado

---

### Fase 9: Recuperação (Prompt 080)
**Quando:** Quando algo dá errado
**O que fazer:**
1. Verificar RECOVERY.md
2. Identificar o problema
3. Executar procedimento de recuperação
4. Verificar se funcionou
5. Documentar o incidente

**Checklist:**
- [ ] RECOVERY.md verificado
- [ ] Problema identificado
- [ ] Recuperação executada
- [ ] Verificação realizada
- [ ] Incidente documentado

---

### Fase 10: Encerramento (Prompt 090)
**Quando:** Fim de sprint ou projeto
**O que fazer:**
1. Atualizar PROJECT_STATE.md
2. Registrar lições aprendidas
3. Atualizar ROADMAP.md
4. Fechar issues resolvidas
5. Comunicar resultados

**Checklist:**
- [ ] PROJECT_STATE.md atualizado
- [ ] Lições registradas
- [ ] ROADMAP.md atualizado
- [ ] Issues fechadas
- [ ] Resultados comunicados

---

## Prompts

Cada fase tem um prompt associado na pasta `prompts/`. Use-os na ordem numérica:

| Fase | Prompt | Arquivo |
|------|--------|---------|
| Abertura | 000 | 000-abertura.md |
| Planejamento | 010 | 010-planejamento.md |
| Sprint | 020 | 020-sprint.md |
| Debug | 030 | 030-debug.md |
| Refatoração | 040 | 040-refatoracao.md |
| Documentação | 050 | 050-documentacao.md |
| Release | 060 | 060-release.md |
| Backup | 070 | 070-backup.md |
| Recuperação | 080 | 080-recuperacao.md |
| Encerramento | 090 | 090-encerramento.md |

---

## Padrão de Sprint Obrigatório

Toda Sprint deverá seguir exatamente a sequência:

```
1. Planejamento
2. Implementação
3. Testes unitários
4. Testes de integração
5. Auditoria
6. Preview local
7. Correções
8. Nova bateria de testes
9. Atualização da documentação
10. Atualização da memória do projeto
11. Backup
12. Aprovação do usuário
13. Commit
14. Deploy
```

**É proibido pular etapas.**

---

## Checkpoints

Ao término de cada etapa executar automaticamente:

- ✓ Build
- ✓ Auditoria
- ✓ Testes
- ✓ Preview
- ✓ Backup
- ✓ Atualização da documentação
- ✓ Atualização do changelog
- ✓ Atualização do roadmap
- ✓ Atualização do PROJECT_MEMORY

---

## Validação Antes do Deploy

Nenhum deploy poderá ocorrer sem:

- ✔ Build concluído
- ✔ Todos os testes aprovados
- ✔ Auditorias aprovadas
- ✔ Preview aprovado pelo usuário
- ✔ Backup realizado
- ✔ Changelog atualizado
- ✔ Roadmap atualizado
- ✔ PROJECT_MEMORY atualizado
- ✔ Documentação sincronizada
- ✔ Versionamento Git correto

---

## Referências

- [Checklists](../checklists/)
- [Prompts](../prompts/)
- [Qualidade](Qualidade.md)
- [FORBIDDEN_ACTIONS](FORBIDDEN_ACTIONS.md)
- [TESTING_POLICY](TESTING_POLICY.md)
- [DISASTER_RECOVERY](DISASTER_RECOVERY.md)
