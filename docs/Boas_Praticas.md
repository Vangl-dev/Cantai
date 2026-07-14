# Boas Práticas

## Visão Geral

Boas práticas são guias para escrever código de qualidade, manutenível e seguro.

## Código

### 1. Nomes Significativos
```javascript
// Ruim
const x = 10;
const fn = () => {};

// Bom
const userAge = 10;
const calculateTotal = () => {};
```

### 2. Funções Pequenas
```javascript
// Ruim
function processUser(user) {
    // 100 linhas de código
}

// Bom
function validateUser(user) { ... }
function saveUser(user) { ... }
function sendWelcomeEmail(user) { ... }
```

### 3. Evitar Magic Numbers
```javascript
// Ruim
if (user.age > 18) { ... }

// Bom
const ADULT_AGE = 18;
if (user.age > ADULT_AGE) { ... }
```

### 4. Tratar Erros
```javascript
// Ruim
try {
    await fetchData();
} catch (e) {}

// Bom
try {
    await fetchData();
} catch (error) {
    console.error('Failed to fetch data:', error);
    throw new AppError('Data fetch failed', { cause: error });
}
```

---

## Git

### 1. Commits Semânticos
```bash
feat: adicionar login
fix: corrigir erro de validação
docs: atualizar README
```

### 2. Branches Organizadas
```bash
feat/123-nome-da-feature
fix/456-nome-do-fix
```

### 3. Pull Requests Claros
- Título descritivo
- Body com contexto
- Screenshots quando aplicável
- Link para issues

---

## Segurança

### 1. Nunca Expor Credenciais
```javascript
// ERRADO
const apiKey = '1234567890';

// CORRETO
const apiKey = process.env.API_KEY;
```

### 2. Validar Entradas
```python
# ERRADO
def get_user(user_id):
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")

# CORRETO
def get_user(user_id):
    return db.query("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 3. Usar HTTPS
```bash
# ERRADO
http://api.example.com

# CORRETO
https://api.example.com
```

---

## Performance

### 1. Otimizar Queries
```sql
-- ERRADO
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- CORRETO
SELECT * FROM users WHERE email LIKE '@gmail.com';
```

### 2. Usar Cache
```javascript
// Cache simples
const cache = new Map();

async function getData(key) {
    if (cache.has(key)) {
        return cache.get(key);
    }
    const data = await fetchFromDB(key);
    cache.set(key, data);
    return data;
}
```

### 3. Lazy Loading
```javascript
// Carregar apenas quando necessário
const module = await import('./heavy-module.js');
```

---

## Documentação

### 1. README Completo
- O que é o projeto
- Como instalar
- Como usar
- Como contribuir

### 2. Código Autoexplicativo
```javascript
// Ruim
// Calcula o total
function calc(a, b) {
    return a + b;
}

// Bom
function calculateTotal(price, quantity) {
    return price * quantity;
}
```

### 3. Comentários Quando Necesário
```javascript
// Não comentar óbvio
const count = items.length;

// Comentar o "porquê"
// Usamos exponential backoff para evitar sobrecarga do servidor
await retryWithBackoff(fn, maxRetries);
```

---

## Testes

### 1. Testar Comportamento, Não Implementação
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

---

## Comunicação

### 1. Issues Descritivas
```markdown
## Bug
Login retorna 500 quando email contém caracteres especiais

## Passos para reproduzir
1. Ir para /login
2. Digitar email com caracteres especiais
3. Clicar em entrar

## Comportamento esperado
Mensagem de erro amigável

## Comportamento atual
Erro 500
```

### 2. PRs Informativos
```markdown
## O que mudou
- Adicionei validação de email
- Corrigi bug de timezone

## Como testar
1. Rodar testes
2. Testar login manualmente

## Issues
Closes #123
```

### 3. Feedback Construtivo
```markdown
// Ruim
Isso está errado.

// Bom
Que tal considerar usar um padrão diferente aqui?
Isso pode causar problemas de performance quando...
```

---

## Referências

- [Qualidade](Qualidade.md)
- [Git](Git.md)
- [Segurança](Seguranca.md)
