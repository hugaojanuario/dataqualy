# DataQualy

Ferramenta open source para validar a qualidade de dados em projetos de migração entre sistemas.

O projeto compara dados da origem e do destino, executa regras de qualidade com PySpark e gera um relatório com divergências encontradas.

## Problema que resolve

Durante uma migração, precisamos confirmar se os dados foram convertidos corretamente. A ferramenta ajudará a identificar:

- diferenças na quantidade de registros;
- registros ausentes no destino;
- chaves duplicadas;
- relacionamentos quebrados e registros órfãos;
- campos obrigatórios nulos;
- diferenças entre valores;
- datas inválidas;
- possíveis problemas de encoding;
- arquivos e anexos ausentes ou alterados.

## Arquitetura planejada

```text
Fonte (CSV, PostgreSQL ou Firebird)
                  │
                  ▼
               PySpark
                  │
                  ▼
       Regras configuradas em YAML
                  │
                  ▼
        Relatório de qualidade HTML
```

## Stack

- Python 3.11
- Java 17
- PySpark
- YAML
- PostgreSQL
- Firebird
- Pytest
- Docker
- GitHub Actions

## Escopo por versão

### Versão 1 — MVP

- comparar dois arquivos CSV;
- validar contagem de registros;
- encontrar duplicidades;
- encontrar registros ausentes;
- validar campos obrigatórios;
- gerar um relatório local.

### Versão 2 — Bancos de dados

- conexão JDBC com PostgreSQL;
- comparação entre tabelas;
- validação de relacionamentos e registros órfãos.

### Versão 3 — Cenário real de migração

- conexão com Firebird e PostgreSQL;
- regras configuráveis em YAML;
- tratamento de tipos, datas e encoding.

### Versão 4 — Distribuição

- interface de linha de comando;
- relatório HTML;
- execução com Docker;
- testes automatizados no GitHub Actions.

### Versão 5 — Evoluções

- validação de anexos;
- comparação de arquivos por hash;
- histórico de execuções;
- dashboard de qualidade.

## Estrutura planejada

```text
migration-data-quality/
├── configs/
│   └── example.yml
├── data/
│   ├── source/
│   └── target/
├── reports/
├── src/
│   └── migration_quality/
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Exemplo de configuração

```yaml
migration:
  name: example_migration

checks:
  - name: total_records
    rule: count_matches
    source:
      file: data/source/records.csv
    target:
      file: data/target/records.csv

  - name: duplicate_ids
    rule: unique
    target:
      file: data/target/records.csv
      key: id
```

## Uso planejado

```bash
dataqualy validate --config configs/example.yml
```

Saída:

```text
reports/validation-report.html
```

## Privacidade

Este repositório não utiliza dados, credenciais, nomes, estruturas proprietárias ou códigos de clientes. Os exemplos serão genéricos e criados exclusivamente para demonstração.

## Status

Projeto em desenvolvimento. A primeira entrega será a comparação de dois arquivos CSV utilizando PySpark.

## Licença

Será definida antes da primeira publicação estável.

