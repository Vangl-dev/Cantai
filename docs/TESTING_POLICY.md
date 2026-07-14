# TESTING_POLICY

## Política de Testes Obrigatórios

**Data de Criação:** 2026-07-07
**Última Atualização:** 2026-07-07
**Status:** ATIVO - OBRIGATÓRIO

---

## Princípio Fundamental

**Test Driven Development (TDD) sempre que possível.**

Nenhuma Sprint poderá ser considerada concluída sem testes.

---

## Tipos de Teste Obrigatórios

### 1. Testes Unitários
- **Obrigatório:** SIM
- **Cobertura mínima:** 80%
- **Ferramenta:** Jest/pytest/etc
- **O que testam:** Funções isoladas

### 2. Testes de Integração
- **Obrigatório:** SIM
- **Cobertura mínima:** 60%
- **Ferramenta:** Jest/pytest/etc
- **O que testam:** Componentes juntos

### 3. Testes de Regressão
- **Obrigatório:** SIM
- **Quando:** Após cada correção de bug
- **Objetivo:** Impedir retorno do problema

### 4. Testes de Interface
- **Obrigatório:** SIM (quando aplicável)
- **Ferramenta:** Cypress/Playwright
- **O que testam:** Fluxos de usuário

### 5. Testes Manuais
- **Obrigatório:** SIM
- **Quando:** Após cada feature
- **Responsável:** Desenvolvedor

### 6. Testes de Performance
- **Obrigatório:** Quando aplicável
- **Quando:** Features com impacto de performance
- **Métricas:** Tempo de resposta, throughput

### 7. Testes de Importação/Exportação
- **Obrigatório:** Quando aplicável
- **Quando:** Features de I/O
- **O que testam:** Formatos, integridade

### 8. Testes de Banco
- **Obrigatório:** SIM
- **Quando:** Qualquer alteração de banco
- **O que testam:** Queries, migrações, integridade

### 9. Testes de Compatibilidade
- **Obrigatório:** Quando aplicável
- **Quando:** Mudanças de API ou formato
- **O que testam:** Retrocompatibilidade

---

## Regras Obrigatórias

### Regra 1: Feature Nova
```
Toda funcionalidade nova DEVE possuir testes próprios.
```

### Regra 2: Correção de Bug
```
Toda correção de bug DEVE incluir um teste que impeça o retorno do mesmo problema.
```

### Regra 3: Sprint Concluída
```
Nenhuma Sprint poderá ser considerada concluída sem testes.
```

### Regra 4: Deploy
```
Nenhum deploy poderá ocorrer sem todos os testes aprovados.
```

---

## Estrutura de Testes

```
tests/
├── unit/
│   ├── services/
│   ├── controllers/
│   └── utils/
├── integration/
│   ├── api/
│   └── database/
├── e2e/
│   └── flows/
├── regression/
│   └── bugs/
└── fixtures/
    └── data/
```

---

## Formato de Teste

### Template para Novos Testes
```javascript
describe('[Componente]', () => {
    describe('[Método]', () => {
        it('should [comportamento esperado]', () => {
            // Arrange
            // Act
            // Assert
        });
    });
});
```

### Template para Teste de Regressão
```javascript
describe('Bug Fix: [Descrição do Bug]', () => {
    it('should not [problema que ocorria]', () => {
        // Teste que garante que o bug não retorna
    });
});
```

---

## Métricas de Teste

### O que Medir
- Cobertura de código
- Taxa de passagem
- Tempo de execução
- Bugs encontrados vs prevenidos

### Meta
- **Cobertura unitária:** > 80%
- **Cobertura integração:** > 60%
- **Taxa de passagem:** 100%
- **Bugs prevenidos:** 100%

---

## Checklist de Testes

### Antes de Commit
- [ ] Testes unitários passando
- [ ] Testes de integração passando
- [ ] Cobertura mínima atingida

### Antes de Merge
- [ ] Todos os testes passando
- [ ] Testes E2E passando (se aplicável)
- [ ] Testes de regressão passando

### Antes de Deploy
- [ ] Todos os testes anteriores
- [ ] Testes manuais realizados
- [ ] Testes de performance (se aplicável)
- [ ] Testes de compatibilidade (se aplicável)

---

## Ferramentas Recomendadas

### JavaScript/TypeScript
- **Unitários:** Jest
- **Integração:** Jest + Supertest
- **E2E:** Cypress ou Playwright
- **Lint:** ESLint

### Python
- **Unitários:** pytest
- **Integração:** pytest + factory_boy
- **E2E:** Playwright
- **Lint:** Ruff

### Go
- **Unitários:** testing
- **Integração:** testing + testcontainers
- **E2E:** Selenium

---

## Referências

- [Qualidade](Qualidade.md)
- [Boas Práticas](Boas_Praticas.md)
- [Checklists](Checklists.md)

---

**IMPORTANTE:** Testes não são opcionais. São parte fundamental da qualidade do código.
