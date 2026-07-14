# TESTING

## Visão Geral

Este documento define a estratégia de testes para o projeto.

## Tipos de Teste

### 1. Unitários
- **O que testam:** Funções isoladas
- **Velocidade:** Rápido
- **Cobertura:** > 80%
- **Ferramenta:** [Jest/pytest/etc]

### 2. Integração
- **O que testam:** Componentes juntos
- **Velocidade:** Médio
- **Cobertura:** > 60%
- **Ferramenta:** [Jest/pytest/etc]

### 3. E2E (End-to-End)
- **O que testam:** Fluxo completo
- **Velocidade:** Lento
- **Cobertura:** Fluxos críticos
- **Ferramenta:** [Cypress/Playwright/etc]

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
└── fixtures/
    └── data/
```

---

## Convenções

### Nomenclatura
```javascript
// Arquivo: tests/unit/services/user.test.js
describe('UserService', () => {
    describe('createUser', () => {
        it('should create a new user', () => {});
        it('should throw error for invalid email', () => {});
    });
});
```

### Estrutura
```javascript
describe('Componente', () => {
    beforeEach(() => {
        // Setup
    });

    afterEach(() => {
        // Cleanup
    });

    it('should [comportamento esperado]', () => {
        // Arrange
        // Act
        // Assert
    });
});
```

---

## Cobertura

### Meta
- **Unitários:** > 80%
- **Integração:** > 60%
- **E2E:** Fluxos críticos

### Relatório
```bash
# Gerar relatório
npm test -- --coverage

# Abrir relatório
open coverage/lcov-report/index.html
```

---

## Comandos

```bash
# Rodar todos os testes
npm test

# Rodar testes unitários
npm test -- --testPathPattern=unit

# Rodar testes de integração
npm test -- --testPathPattern=integration

# Rodar com cobertura
npm test -- --coverage

# Rodar testes específicos
npm test -- --testNamePattern="should create user"
```

---

## Fixtures

### Dados de Teste
```javascript
// tests/fixtures/users.js
module.exports = {
    validUser: {
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
    },
    invalidUser: {
        email: 'invalid',
        name: '',
        password: '123'
    }
};
```

### Mocks
```javascript
// Mock de serviço externo
jest.mock('../../../services/email', () => ({
    sendEmail: jest.fn().mockResolvedValue(true)
}));
```

---

## CI/CD

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

---

## Melhores Práticas

### 1. Testar Comportamento
```javascript
// Ruim
expect(calculate.toString()).toContain('return');

// Bom
expect(calculate(2, 3)).toBe(5);
```

### 2. Testes Independentes
```javascript
// Cada teste deve poder rodar isolado
beforeEach(() => {
    setupTestDatabase();
});

afterEach(() => {
    cleanupTestDatabase();
});
```

### 3. Nomes Descritivos
```javascript
// Ruim
it('test 1', () => {});

// Bom
it('should return 404 when user not found', () => {});
```

### 4. Evitar Testes Frágeis
```javascript
// Ruim - depende de estado externo
it('should work', () => {
    expect(database.count()).toBe(5);
});

// Bom - isolado
it('should create user', async () => {
    const user = await createUser({ name: 'Test' });
    expect(user.id).toBeDefined();
});
```

---

## Debug

### Jest
```bash
# Modo watch
npm test -- --watch

# Debug no Chrome
node --inspect-brk node_modules/.bin/jest --runInBand
```

### Cypress
```bash
# Abrir Cypress UI
npx cypress open

# Rodar headless
npx cypress run
```

---

## Checklist de Teste

### Antes de Commit
- [ ] Testes unitários passando
- [ ] Testes de integração passando
- [ ] Cobertura mínima atingida
- [ ] Sem testes frágeis

### Antes de Merge
- [ ] Todos os testes passando
- [ ] Testes E2E passando
- [ ] Cobertura revisada
- [ ] Testes documentados

---

## Referências

- [Qualidade](../docs/Qualidade.md)
- [Boas Práticas](../docs/Boas_Praticas.md)

---

**Última atualização:** YYYY-MM-DD
