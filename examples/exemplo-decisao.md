# Exemplo de DECISION

---

# DECISION-001: Usar PostgreSQL como banco principal

## Status
Aceita

## Data
2026-07-06

## Autor
Vanessa

## Contexto

O projeto precisa de um banco de dados relacional robusto, com suporte a:
- Dados relacionais complexos
- JSON nativo
- Boas práticas de segurança
- Performance para grande volume

## Decisão

Usar PostgreSQL como banco de dados principal do projeto.

## Consequências

### Positivas
- Suporte nativo a JSON (JSONB)
- Índices avançados
- Extensões poderosas (PostGIS, pg_trgm)
- Comunidade ativa
- Documentação excelente

### Negativas
- Necessidade de expertise em PostgreSQL
- Configuração inicial mais complexa
- Menos "famoso" que MySQL para iniciantes

## Alternativas Consideradas

### MySQL
**Prós:**
- Mais popular
- Mais fácil de encontrar desenvolvedores
- Simples de configurar

**Contras:**
- Suporte a JSON limitado
- Menos features avançadas
- Licenciamento duvidoso (Oracle)

**Por que rejeitada:**
Falta de suporte a JSON avançado e concerns sobre licenciamento.

### MongoDB
**Prós:**
- Flexível
- Bom para dados não estruturados
- Escalável horizontalmente facilmente

**Contras:**
- Não relacional
- Menos consistência
- Consistency eventual

**Por que rejeitada:**
Dados são majoritariamente relacionais, e precisamos de transações ACID.

### Firebase
**Prós:**
- Fácil de usar
- Real-time
- Serverless

**Contras:**
- Vendor lock-in
- Custo pode escalar
- Menos controle

**Por que rejeitada:**
Vendor lock-in e custo imprevisível.

## Aprovação

- **Aprovado por:** Vanessa
- **Data:** 2026-07-06
- **Revisão:** Nenhuma pendente

## Referências

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Why PostgreSQL?](https://www.postgresql.org/about/)

---

**Última atualização:** 2026-07-06
