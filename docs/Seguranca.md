# Segurança

## Princípios Fundamentais

### 1. Nunca Confiar na Entrada
- Validar TODAS as entradas de usuário
- Sanitizar dados antes de usar
- Usar prepared statements em SQL

### 2. Defense in Depth
- Múltiplas camadas de proteção
- Não depender de uma única barreira
- Fail securely

### 3. Least Privilege
- Conceder mínimo de permissões necessário
- Revisar permissões regularmente
- Revogar acesso quando não necessário

### 4. Secure by Default
- Configurações seguras por padrão
- Exigir ação explícita para insegurança
- Documentar exceções

---

## Regras Obrigatórias

### Credenciais e Segredos

#### NUNCA fazer
- ❌ Armazenar chaves em código fonte
- ❌ Committar arquivos `.env`
- ❌ Logar credenciais
- ❌ Compartilhar segredos por chat/email
- ❌ Usar senhas fracas

#### SEMPRE fazer
- ✅ Usar variáveis de ambiente
- ✅ Usar `.env` (nunca committado)
- ✅ Usar gerenciador de segredos
- ✅ Rotacionar chaves periodicamente
- ✅ Usar senhas fortes e únicas

### Arquivo .gitignore

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

### Variáveis de Ambiente

```bash
# Exemplo de .env.example (committado)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here
```

---

## Autenticação e Autorização

### JWT (JSON Web Tokens)
- Usar para autenticação stateless
- Definir tempo de expiração curto
- Implementar refresh tokens
- Validar assinatura

### OAuth
- Usar provedores confiáveis (Google, GitHub)
- Nunca implementar OAuth do zero
- Validar state parameter
- Usar PKCE para SPAs

### Sessões
- Usar cookies HttpOnly e Secure
- Implementar timeout de sessão
- Invalidar sessões no logout
- Regenerar ID de sessão após login

---

## Validação de Entrada

### Backend
```python
# Exemplo em Python
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

### Frontend
```javascript
// Exemplo em JavaScript
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}
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

### Regras
- SEMPRE usar HTTPS em produção
- Nunca misturar conteúdo HTTP e HTTPS
- Usar TLS 1.2 ou superior
- Configurar HSTS

### Certificados
- Usar Let's Encrypt para certificados gratuitos
- Automatizar renovação
- Monitorar expiração

---

## Headers de Segurança

### Helmet.js (Node.js)
```javascript
const helmet = require('helmet');
app.use(helmet());
```

### Headers Recomendados
- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`

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

### Estratégias
- Limitar por IP
- Limitar por usuário
- Limitar por endpoint
- Implementar backoff exponencial

---

## Logging e Monitoramento

### O que Logar
- Tentativas de login (falhas e sucessos)
- Erros de aplicação
- Acesso a recursos sensíveis
- Mudanças de configuração

### O que NÃO Logar
- Senhas ou credenciais
- Dados pessoais sensíveis
- Tokens de sessão
- Informações de cartão de crédito

### Formato de Log
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

## Backup e Recuperação

### Regras
- Backups regulares automatizados
- Testar restauração periodicamente
- Armazenar backups em local seguro
- Criptografar backups sensíveis

### Frequência
- **Dados críticos:** Diário
- **Configurações:** Semanal
- **Código:** Contínuo (Git)

---

## Resposta a Incidentes

### Processo
1. **Identificar:** Reconhecer o incidente
2. **Conter:** Limitar o dano
3. **Erradicar:** Remover a causa
4. **Recuperar:** Restaurar operações
5. **Aprender:** Documentar lições

### Contato
- Definir responsável por segurança
- Ter canal de comunicação de emergência
- Documentar procedimentos

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

## Referências

- [AI_CONSTITUTION.md](../AI_CONSTITUTION.md)
- [Boas Práticas](Boas_Praticas.md)
- [Checklists de Segurança](../checklists/)
- [FORBIDDEN_ACTIONS](FORBIDDEN_ACTIONS.md)
- [DISASTER_RECOVERY](DISASTER_RECOVERY.md)
- [RISK_REGISTER](RISK_REGISTER.md)
- [AI_CAPABILITIES](AI_CAPABILITIES.md)
