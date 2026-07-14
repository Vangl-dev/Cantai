# SECURITY

## Visão Geral

Este documento define práticas e procedimentos de segurança para o projeto.

## Regras Fundamentais

### NUNCA fazer
- ❌ Armazenar chaves em código fonte
- ❌ Committar arquivos `.env`
- ❌ Logar credenciais
- ❌ Compartilhar segredos por chat/email
- ❌ Usar senhas fracas

### SEMPRE fazer
- ✅ Usar variáveis de ambiente
- ✅ Usar `.env` (nunca committado)
- ✅ Usar gerenciador de segredos
- ✅ Rotacionar chaves periodicamente
- ✅ Usar senhas fortes e únicas

---

## Variáveis de Ambiente

### Arquivo .env.example
```bash
# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# API Keys
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here

# Autenticação
JWT_SECRET=your-jwt-secret-here
JWT_EXPIRATION=24h

# Serviços Externos
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=password
```

### .gitignore
```gitignore
# Env
.env
.env.local
.env.*.local

# Secrets
credentials.json
secrets.json
*.key
*.pem
```

---

## Autenticação

### JWT (JSON Web Tokens)
```javascript
// Geração
const token = jwt.sign(
    { userId: user.id },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
);

// Validação
const decoded = jwt.verify(token, process.env.JWT_SECRET);
```

### Senhas
```python
# Hash com bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash
hashed = pwd_context.hash("password")

# Verificação
is_valid = pwd_context.verify("password", hashed)
```

---

## Validação de Entrada

### Backend
```python
# Exemplo Pydantic
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    name: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v.lower()
```

### SQL Injection
```python
# ERRADO
query = f"SELECT * FROM users WHERE id = {user_id}"

# CORRETO
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

---

## HTTPS e TLS

### Configuração
```nginx
# Nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

### Headers de Segurança
```javascript
// Helmet.js
const helmet = require('helmet');
app.use(helmet());
```

---

## Rate Limiting

### Configuração
```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])

@app.route("/api/resource")
@limiter.limit("10 per minute")
def get_resource():
    return jsonify(data)
```

---

## Logging Seguro

### O que Logar
- Tentativas de login
- Erros de aplicação
- Acesso a recursos sensíveis

### O que NÃO Logar
- Senhas ou credenciais
- Dados pessoais sensíveis
- Tokens de sessão

### Formato
```json
{
    "timestamp": "2026-07-06T12:00:00Z",
    "level": "error",
    "message": "Login failed",
    "ip": "192.168.1.1",
    "user": "user@example.com"
}
```

---

## Checklist de Segurança

### Antes de Commit
- [ ] Não há credenciais expostas
- [ ] Não há dados sensíveis em logs
- [ ] Variáveis de ambiente estão em .gitignore
- [ ] Validação de entrada está implementada

### Antes de Deploy
- [ ] HTTPS está configurado
- [ ] Headers de segurança estão ativos
- [ ] Rate limiting está configurado
- [ ] Logging está funcionando

### Mensal
- [ ] Revisar dependências para vulnerabilidades
- [ ] Verificar permissões de acesso
- [ ] Testar backups
- [ ] Revisar logs de segurança

---

## Resposta a Incidentes

### Processo
1. **Identificar:** Reconhecer o incidente
2. **Conter:** Limitar o dano
3. **Erradicar:** Remover a causa
4. **Recuperar:** Restaurar operações
5. **Aprender:** Documentar lições

### Contatos
- Responsável de segurança: [nome]
- Advogado: [nome]
- Comunicação: [canal]

---

## Referências

- [AI_CONSTITUTION.md](../AI_CONSTITUTION.md)
- [Segurança](../docs/Seguranca.md)

---

**Última atualização:** YYYY-MM-DD
