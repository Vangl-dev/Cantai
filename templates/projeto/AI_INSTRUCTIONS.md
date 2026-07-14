# AI_INSTRUCTIONS.md

## Instruções para Inteligência Artificial

**Projeto:** [Nome do Projeto]
**Versão:** 1.0.0
**Última Atualização:** YYYY-MM-DD

---

## Contexto do Projeto

### O que é
[Descrição do projeto]

### Objetivo
[Objetivo principal]

### Público-alvo
[Quem vai usar]

---

## Regras para a IA

### Geral
1. **SEGUIR** AI_CONSTITUTION.md em todos os momentos
2. **PERGUNTAR** quando houver dúvida
3. **DOCUMENTAR** decisões significativas
4. **RESPEITAR** a estrutura de pastas do projeto
5. **ATUALIZAR** PROJECT_MEMORY.md a cada sprint

### Código
1. **SEGUIR** padrões de código do projeto
2. **TESTAR** enquanto desenvolve
3. **COMMITAR** com mensagens semânticas
4. **NÃO COMMITAR** sem testar

### Testes (Obrigatório)
1. **TDD** sempre que possível
2. **TODA feature** nova deve ter testes
3. **TODA correção** de bug deve ter teste de regressão
4. **NENHUMA sprint** é concluída sem testes
5. **NENHUM deploy** sem todos os testes aprovados

### Documentação
1. **ATUALIZAR** README.md quando necessário
2. **ATUALIZAR** CHANGELOG.md para mudanças significativas
3. **REGISTRAR** decisões em DECISIONS.md
4. **DOCUMENTAR** lições aprendidas
5. **ATUALIZAR** PROJECT_MEMORY.md

### Ações Proibidas
1. **NUNCA** apagar banco de dados
2. **NUNCA** substituir JSON de produção
3. **NUNCA** apagar diretórios
4. **NUNCA** remover funcionalidades existentes
5. **NUNCA** quebrar retrocompatibilidade
6. **NUNCA** executar deploy automático
7. **NUNCA** alterar Git sem autorização

### Segurança
1. **NUNCA** expor credenciais
2. **NUNCA** committar .env
3. **SEMPRE** usar variáveis de ambiente
4. **VALIDAR** todas as entradas
5. **CRIAR** backup antes de migrações
6. **PREFERIR** UPDATE em vez de DELETE

### Protocolo Obrigatório
ANTES de qualquer alteração estrutural:
1. BACKUP
2. PLANO
3. APROVAÇÃO
4. EXECUÇÃO
5. VALIDAÇÃO

---

## Estrutura do Projeto

```
[projeto]/
├── src/
├── tests/
├── docs/
├── .env.example
├── README.md
└── [outros arquivos importantes]
```

---

## Stack Tecnológica

| Componente | Tecnologia |
|------------|------------|
| Backend | [tecnologia] |
| Frontend | [tecnologia] |
| Banco | [tecnologia] |
| Cache | [tecnologia] |
| Testes | [tecnologia] |

---

## Comandos Importantes

```bash
# Instalar dependências
npm install

# Rodar desenvolvimento
npm run dev

# Rodar testes
npm test

# Rodar lint
npm run lint

# Build
npm run build
```

---

## Fluxo de Trabalho

### 1. Iniciar Tarefa
1. Ler esta documentação
2. Entender contexto atual
3. Perguntar se houver dúvida
4. Seguir prompts na ordem

### 2. Desenvolver
1. Seguir padrões do projeto
2. Testar enquanto desenvolve
3. Documentar decisões
4. Comunicar progresso

### 3. Completar
1. Rodar testes
2. Rodar lint
3. Atualizar documentação
4. Registrar lições

---

## Padrões Específicos

### Nomenclatura
- **Variáveis:** camelCase
- **Funções:** camelCase
- **Classes:** PascalCase
- **Constantes:** UPPER_SNAKE_CASE
- **Arquivos:** kebab-case

### Estrutura de Componentes
```javascript
// Exemplo de componente
export function ComponentName({ prop1, prop2 }) {
    // Lógica
    return (
        // JSX
    );
}
```

### Estrutura de Serviço
```javascript
// Exemplo de serviço
export class ServiceName {
    constructor(dependency) {
        this.dependency = dependency;
    }

    async method() {
        // Lógica
    }
}
```

---

## Checklist da IA

### Antes de Commitar
- [ ] Código segue padrões
- [ ] Testes passando
- [ ] Lint sem erros
- [ ] Sem secrets expostos
- [ ] Documentação atualizada

### Antes de Merge
- [ ] Review feito
- [ ] Testes adicionados
- [ ] CHANGELOG atualizado
- [ ] Decisões documentadas

---

## Contato

- **Responsável:** [Nome]
- **Email:** [email]
- **Canal:** [slack/teams/etc]

---

**Última atualização:** YYYY-MM-DD
