# Prompt 070: Backup

## Objetivo
Realizar backup do projeto de forma segura e documentada.

## Checklist

### 1. Planejamento
- [ ] Identificar o que backupar
- [ ] Definir frequência
- [ ] Escolher destino
- [ ] Definir retenção

### 2. Execução
- [ ] Executar backup
- [ ] Verificar integridade
- [ ] Armazenar em local seguro
- [ ] Documentar o backup

### 3. Validação
- [ ] Testar restauração
- [ ] Verificar completude
- [ ] Confirmar armazenamento
- [ ] Atualizar registros

### 4. Manutenção
- [ ] Limpar backups antigos
- [ ] Verificar espaço
- [ ] Atualizar procedimentos
- [ ] Comunicar ao time

## O que Backupar

### Sempre
- Código fonte (Git)
- Variáveis de ambiente
- Configurações
- Documentação

### Conforme Necessidade
- Banco de dados
- Arquivos de upload
- Logs importantes
- Certificados

## Tipos de Backup

### Full Backup
```bash
# Cópia completa
tar -czf backup-$(date +%Y%m%d).tar.gz /path/to/project
```

### Incremental
```bash
# Apenas mudanças desde último backup
rsync -av --progress /source/ /backup/
```

### Database
```bash
# PostgreSQL
pg_dump -U user database_name > backup.sql

# MySQL
mysqldump -u user -p database_name > backup.sql

# MongoDB
mongodump --db database_name --out /backup/
```

## Frequência Recomendada

| Componente | Frequência | Retenção |
|------------|------------|----------|
| Código | Contínuo (Git) | Indefinido |
| Database | Diário | 30 dias |
| Configurações | Semanal | 90 dias |
| Full Backup | Semanal | 1 ano |

## Armazenamento

### Local
- Pasta dedicada de backup
- Permissões restritas
- Espaço suficiente

### Remoto
- Cloud storage (S3, GCS)
- Servidor dedicado
- Criptografado

## Validação de Backup

### Verificar Integridade
```bash
# Verificar arquivo
tar -tzf backup.tar.gz

# Verificar checksum
md5sum backup.tar.gz
```

### Testar Restauração
```bash
# Criar ambiente de teste
# Restaurar backup
# Verificar dados
# Documentar resultado
```

## Template de Registro

```markdown
# Backup: YYYY-MM-DD

## Tipo
[Full | Incremental | Database]

## Componentes
- [Componente 1]
- [Componente 2]

## Tamanho
[X MB/GB]

## Destino
[Local | Remoto]

## Integridade
[Verificado | Não verificado]

## Restauração Testada
[Sim | Não]

## Próximo Backup
YYYY-MM-DD
```

## Perguntas para o Desenvolvedor

1. O que precisa ser backupado?
2. Qual a frequência adequada?
3. Onde armazenar?
4. Há dados sensíveis?
5. Quando testar restauração?

## Saída Esperada

Após completar este prompt:
- Backup executado
- Integridade verificada
- Documentação atualizada
- Próximo backup agendado

## Referências

- [Recuperação](../docs/Recuperacao.md)
- [Segurança](../docs/Seguranca.md)
- [Checklists](../checklists/)
