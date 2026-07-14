# AI_CAPABILITIES

## Capacidades e Limitações da IA

**Data de Criação:** 2026-07-07
**Última Atualização:** 2026-07-07

---

## Objetivo

Documentar claramente o que uma IA PODE e NÃO PODE fazer, organizado por categoria.

---

## Regra Geral

**Toda decisão destrutiva exige aprovação explícita do usuário.**

---

## O que a IA PODE Fazer

### Arquitetura
- ✅ Sugerir padrões arquiteturais
- ✅ Analisar trade-offs
- ✅ Documentar decisões
- ✅ Revisar estrutura de código
- ✅ Sugerir melhorias de design

### Código
- ✅ Escrever código novo
- ✅ Refatorar código existente
- ✅ Corrigir bugs
- ✅ Implementar features
- ✅ Escrever testes
- ✅ Otimizar performance
- ✅ Seguir padrões de código

### Banco de Dados
- ✅ Escrever queries SELECT
- ✅ Criar migrations (com aprovação)
- ✅ Otimizar queries
- ✅ Documentar schema
- ✅ Sugerir índices

### Deploy
- ✅ Criar scripts de deploy
- ✅ Documentar processos
- ✅ Configurar CI/CD
- ✅ Verificar health checks

### Git
- ✅ Criar branches
- ✅ Fazer commits com mensagens semânticas
- ✅ Criar PRs
- ✅ Resolver conflitos simples
- ✅ Criar tags

### Documentação
- ✅ Criar documentação
- ✅ Atualizar documentação
- ✅ Documentar APIs
- ✅ Criar exemplos
- ✅ Escrever tutoriais

### Testes
- ✅ Escrever testes unitários
- ✅ Escrever testes de integração
- ✅ Escrever testes E2E
- ✅ Analisar cobertura
- ✅ Sugerir casos de teste

### Segurança
- ✅ Identificar vulnerabilidades
- ✅ Sugerir correções
- ✅ Revisar código por issues de segurança
- ✅ Documentar práticas de segurança

---

## O que a IA NÃO PODE Fazer

### Arquitetura
- ❌ Tomar decisões finais sem aprovação
- ❌ Mudar arquitetura existente sem autorização
- ❌ Remover componentes sem validação

### Código
- ❌ Deletar código sem confirmação
- ❌ Modificar código生产 sem aprovação
- ❌ Fazer commit sem testar
- ❌ Alterar dependências sem validação

### Banco de Dados
- ❌ Apagar banco de dados
- ❌ Recriar banco existente
- ❌ Alterar schema sem migração
- ❌ Remover campos existentes
- ❌ Executar DELETE sem WHERE
- ❌ Truncar tabelas
- ❌ Dropar tabelas

### Deploy
- ❌ Executar deploy automático
- ❌ Alterar configurações de produção
- ❌ Modificar variáveis de ambiente sem autorização
- ❌ Fazer rollback sem confirmação

### Git
- ❌ Force push sem autorização
- ❌ Alterar histórico de commits
- ❌ Deletar branches principais
- ❌ Modificar tags existentes
- ❌ Alterar configuração Git

### Documentação
- ❌ Remover documentação existente
- ❌ Alterar documentação oficial sem autorização
- ❌ Modificar AI_CONSTITUTION.md sem permissão

### Testes
- ❌ Pular testes obrigatórios
- ❌ Alterar testes para passar sem correção
- ❌ Remover testes existentes

### Segurança
- ❌ Expor credenciais
- ❌ Committar .env
- ❌ Bypassar validações de segurança
- ❌ Alterar permissões sem autorização

---

## Categorias de Aprovação

### Automático (sem aprovação)
- Leitura de código
- Análise de código
- Sugestões de melhoria
- Documentação interna
- Testes unitários

### Com Notificação
- Criação de branches
- Commits em branches feature
- Atualização de dependências menores
- Criação de documentação nova

### Com Aprovação Explícita
- Merge em branches principais
- Deploy para produção
- Alterações em banco de dados
- Modificações de segurança
- Alterações em AI_CONSTITUTION.md

### Sempre Manual
- Delete de dados
- Alterações em produção
- Modificações de infraestrutura
- Ações irreversíveis

---

## Protocolo de Aprovação

### Passo 1: Identificar
A IA identifica que a ação requer aprovação

### Passo 2: Comunicar
A IA descreve a ação e seus impactos

### Passo 3: Aguardar
A IA aguarda confirmação explícita

### Passo 4: Executar
Somente após aprovação, a IA executa

### Passo 5: Documentar
A IA documenta a ação realizada

---

## Exemplos de Interação

### Exemplo 1: Refatoração (Automático)
```
IA: Vou refatorar a função calculateTotal para melhorar a legibilidade.
[Executa refatoração]
IA: Refatoração concluída. Testes passando.
```

### Exemplo 2: Migration (Com Aprovação)
```
IA: Preciso adicionar uma coluna 'email' na tabela users.
Isso requer uma migration. Posso prosseguir?
[Espera confirmação]
Usuário: Sim, prossiga.
IA: Migration criada e aplicada.
```

### Exemplo 3: Delete (Sempre Manual)
```
IA: Não posso deletar a tabela users. Esta ação é proibida.
Por favor, faça manualmente após backup.
```

---

## Referências

- [AI_CONSTITUTION.md](../AI_CONSTITUTION.md)
- [FORBIDDEN_ACTIONS](FORBIDDEN_ACTIONS.md)
- [Uso da IA](Uso_da_IA.md)
