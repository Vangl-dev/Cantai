# Uso da IA

## Visão Geral

Este documento define como a Inteligencial Artificial deve ser utilizada nos projetos do framework MétodoDev.

## Princípios Fundamentais

### 1. IA como Ferramenta
- IA auxilia, não substitui o desenvolvedor
- Decisões finais são do desenvolvedor
- IA deve ser transparente sobre limitações

### 2. IA como Parceira
- IA pode sugerir melhorias
- IA pode identificar problemas
- IA pode automatizar tarefas repetitivas

### 3. IA como Documentadora
- IA pode gerar documentação
- IA pode explicar código
- IA pode registrar decisões

---

## Como a IA deve Trabalhar

### Ao Iniciar uma Tarefa
1. Ler a documentação relevante
2. Entender o contexto atual
3. Perguntar se houver dúvida
4. Seguir os prompts na ordem correta

### Ao Desenvolver
1. Seguir padrões do projeto
2. Testar enquanto desenvolve
3. Documentar decisões significativas
4. Comunicar progresso

### Ao Completar
1. Rodar testes
2. Rodar lint
3. Atualizar documentação
4. Registrar lições aprendidas

---

## Prompts Disponíveis

### Uso dos Prompts

Cada prompt tem um número e um nome:
- `000-abertura.md` - Início de projeto
- `010-planejamento.md` - Planejamento de sprint
- `020-sprint.md` - Durante a sprint
- `030-debug.md` - Quando há bugs
- `040-refatoracao.md` - Melhoria de código
- `050-documentacao.md` - Documentação
- `060-release.md` - Preparar release
- `070-backup.md` - Backup
- `080-recuperacao.md` - Recuperação
- `090-encerramento.md` - Fim de sprint/projeto

### Ordem de Uso
1. Começar pelo 000 para novos projetos
2. Seguir a ordem numérica
3. Usar prompts conforme a necessidade
4. Não pular etapas

---

## Regras para a IA

### O que a IA DEVE fazer
- Seguir AI_CONSTITUTION.md
- Perguntar quando houver dúvida
- Documentar decisões
- Respeitar a estrutura de pastas
- Usar prompts na ordem correta
- Preencher checklists obrigatórios

### O que a IA NÃO DEVE fazer
- Ignorar AI_CONSTITUTION.md
- Pular etapas do fluxo
- Commitar sem testar
- Expor credenciais
- Modificar AI_CONSTITUTION.md sem autorização
- Tomar decisões arquiteturais sem registro

### Comunicação
- Informar o que está fazendo
- Alertar sobre riscos
- Sugerir alternativas
- Pedir confirmação para ações destrutivas

---

## Integração com Ferramentas

### Git
- Usar mensagens semânticas
- Seguir convenção de branches
- Não commitar sem testar

### CI/CD
- Rodar testes automaticamente
- Rodar lint automaticamente
- Verificar segurança

### Documentação
- Manter README.md atualizado
- Manter ARCHITECTURE.md atualizado
- Registrar decisões em DECISIONS.md

---

## Limitações da IA

### O que a IA NÃO pode fazer
- Tomar decisões de negócio
- Substituir revisão humana
- Garantir alta precisão
- Entender contexto sem explicitação

### O que a IA pode fazer
- Sugerir soluções
- Identificar padrões
- Automatizar tarefas repetitivas
- Gerar documentação
- Explicar código

---

## Métricas de Uso

### Como Avaliar
- Qualidade das sugestões
- Tempo economizado
- Redução de erros
- Satisfação do desenvolvedor

### Melhoria Contínua
- Coletar feedback
- Ajustar prompts
- Atualizar documentação
- Compartilhar lições

---

## Referências

- [AI_CONSTITUTION.md](../AI_CONSTITUTION.md)
- [Prompts](../prompts/)
- [Fluxo de Desenvolvimento](Fluxo.md)
