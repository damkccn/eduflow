# EduFlow — Automação de avaliações escolares

**Status:** protótipo didático local e integração escolar em desenvolvimento.

## Executar
Requer Python 3.10+:

```bash
python eduflow.py
```

O script cria **alunos fictícios**, organiza registros por turma (ex.: PRÉ I A e PRÉ II B), gera CSV e salva um backup separado. Os arquivos gerados ficam em `data/`, ignorado pelo Git.

Testes: `python -m unittest discover -v`.

## Evolução
Integração com Google Sheets e Apps Script, avaliação por aluno, painel de coordenação e backups automatizados. Essas integrações **não estão implementadas no código demonstrativo deste repositório**.

**Privacidade:** nunca publique informações reais de alunos, credenciais ou JSON de conta de serviço.

[Portfólio](https://damkccn.github.io/damaris-portfolio/cases/eduflow.html) · [Instruções](DEVELOPMENT.md)
