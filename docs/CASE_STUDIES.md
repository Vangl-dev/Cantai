# CASE_STUDIES

## Estudos de Caso

**Data de Criação:** 2026-07-07
**Última Atualização:** 2026-07-07

---

## Objetivo

Registrar estudos de caso reais para documentar problemas encontrados, soluções adotadas e lições aprendidas. Cada estudo serve como referência para futuros projetos.

---

## Estudo de Caso 1: Projeto Cantai

### Contexto
Projeto de gestão de eventos e presença com foco em igrejas e organizações religiosas.

### Problemas Encontrados

#### 1. Falta de Estrutura Inicial
**Problema:** Projeto iniciado sem padrões definidos
**Causa:** Pressa para entregar funcionalidades
**Impacto:** Código desorganizado, dificuldade de manutenção
**Solução:** adoção do MétodoDev

#### 2. Ausência de Testes
**Problema:** Nenhum teste automatizado
**Causa:** Priorização de velocidade sobre qualidade
**Impacto:** Bugs recorrentes, regressões frequentes
**Solução:** Implementação de TDD

#### 3. Documentação Insuficiente
**Problema:** Decisões não documentadas
**Causa:** Falta de processo
**Impacto:** Dificuldade para novos desenvolvedores
**Solução:** DOCUMENTATION_POLICY

#### 4. Deploy Manual
**Problema:** Deploy sem validação
**Causa:** Falta de CI/CD
**Impacto:** Erros em produção
**Solução:** VALIDATION_BEFORE_DEPLOY

#### 5. Falta de Versionamento
**Problema:** Commits sem padrão
**Causa:** Falta de convenção
**Impacto:** Histórico confuso
**Solução:** GIT_POLICY

### Retrabalho
- **Estimativa:** 40% do tempo gasto em retrabalho
- **Causa principal:** Bugs que poderiam ser evitados com testes
- **Custo:** Tempo significativo desperdiçado

### Regressões
- **Frequência:** Aproximadamente 1 por sprint
- **Causa:** Falta de testes de regressão
- **Impacto:** Funcionalidades quebradas após correções

### Soluções Adotadas
1. Implementação do MétodoDev
2. Criação de testes automatizados
3. Documentação de decisões
4. Processo de deploy automatizado

### Melhorias com MétodoDev
| Antes | Depois |
|-------|--------|
| 0% testes | 80%+ cobertura |
| Sem documentação | Documentação completa |
| Deploy manual | Deploy automatizado |
| Bugs recorrentes | Testes de regressão |

### Como MétodoDev Evita Problemas
1. **TESTING_POLICY.md:** TDD obrigatório
2. **FORBIDDEN_ACTIONS.md:** Ações destrutivas proibidas
3. **PROJECT_MEMORY.md:** Histórico preservado
4. **DISASTER_RECOVERY.md:** Procedimentos de recuperação
5. **CHECKLISTS:** Validação em cada etapa

---

## Estudo de Caso 2: Projeto EraserID

### Contexto
*[A ser documentado quando houver dados disponíveis]*

### Status
**Fase:** Planejamento
**Documentação:** Em andamento

### Estrutura para Documentação
- [ ] Contexto do projeto
- [ ] Problemas encontrados
- [ ] Causas identificadas
- [ ] Retrabalho medido
- [ ] Regressões catalogadas
- [ ] Soluções adotadas
- [ ] Melhorias com MétodoDev

---

## Estudo de Caso 3: Projeto LexProof

### Contexto
*[A ser documentado quando houver dados disponíveis]*

### Status
**Fase:** Planejamento
**Documentação:** Em andamento

### Estrutura para Documentação
- [ ] Contexto do projeto
- [ ] Problemas encontrados
- [ ] Causas identificadas
- [ ] Retrabalho medido
- [ ] Regressões catalogadas
- [ ] Soluções adotadas
- [ ] Melhorias com MétodoDev

---

## Estudo de Caso 4: Calculadora TJSP

### Contexto
*[A ser documentado quando houver dados disponíveis]*

### Status
**Fase:** Planejamento
**Documentação:** Em andamento

### Estrutura para Documentação
- [ ] Contexto do projeto
- [ ] Problemas encontrados
- [ ] Causas identificadas
- [ ] Retrabalho medido
- [ ] Regressões catalogadas
- [ ] Soluções adotadas
- [ ] Melhorias com MétodoDev

---

## Template para Novos Estudos

```markdown
# Estudo de Caso: [Nome do Projeto]

## Contexto
[Descrição do projeto]

## Problemas Encontrados

### Problema 1: [Título]
**Problema:** [Descrição]
**Causa:** [Causa raiz]
**Impacto:** [Impacto]
**Solução:** [Solução adotada]

## Retrabalho
- **Estimativa:** [X% do tempo]
- **Causa principal:** [Descrição]
- **Custo:** [Impacto]

## Regressões
- **Frequência:** [Frequência]
- **Causa:** [Causa]
- **Impacto:** [Impacto]

## Soluções Adotadas
1. [Solução 1]
2. [Solução 2]

## Melhorias com MétodoDev
| Antes | Depois |
|-------|--------|
| [Métrica] | [Resultado] |

## Como MétodoDev Evita Problemas
1. [Documentação do MétodoDev que resolve]
2. [Outro documento]
```

---

## Referências

- [PROJECT_MEMORY](PROJECT_MEMORY.md)
- [Lições Aprendidas](Licoes_Aprendidas.md)
- [QUALITY_METRICS](QUALITY_METRICS.md)
