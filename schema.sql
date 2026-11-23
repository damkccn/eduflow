-- EduFlow 2.0: esquema inicial (SQLite). Dados reais não devem ser publicados.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS escolas (
 id INTEGER PRIMARY KEY,
 nome TEXT NOT NULL CHECK(length(trim(nome)) >= 2)
);
CREATE TABLE IF NOT EXISTS usuarios (
 id INTEGER PRIMARY KEY,
 escola_id INTEGER NOT NULL REFERENCES escolas(id),
 nome TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE,
 perfil TEXT NOT NULL CHECK(perfil IN ('professor','coordenador'))
);
CREATE TABLE IF NOT EXISTS turmas (
 id INTEGER PRIMARY KEY,
 escola_id INTEGER NOT NULL REFERENCES escolas(id),
 nome TEXT NOT NULL,
 ano_letivo INTEGER NOT NULL CHECK(ano_letivo BETWEEN 2000 AND 2200),
 UNIQUE(escola_id, nome, ano_letivo)
);
CREATE TABLE IF NOT EXISTS professores_turmas (
 professor_id INTEGER NOT NULL REFERENCES usuarios(id),
 turma_id INTEGER NOT NULL REFERENCES turmas(id),
 PRIMARY KEY(professor_id, turma_id)
);
CREATE TABLE IF NOT EXISTS alunos (
 id INTEGER PRIMARY KEY,
 escola_id INTEGER NOT NULL REFERENCES escolas(id),
 nome TEXT NOT NULL CHECK(length(trim(nome)) >= 2)
);
CREATE TABLE IF NOT EXISTS matriculas (
 id INTEGER PRIMARY KEY,
 aluno_id INTEGER NOT NULL REFERENCES alunos(id),
 turma_id INTEGER NOT NULL REFERENCES turmas(id),
 ano_letivo INTEGER NOT NULL,
 UNIQUE(aluno_id, ano_letivo)
);
CREATE TABLE IF NOT EXISTS criterios (
 id INTEGER PRIMARY KEY,
 escola_id INTEGER NOT NULL REFERENCES escolas(id),
 descricao TEXT NOT NULL,
 ativo INTEGER NOT NULL DEFAULT 1 CHECK(ativo IN (0,1))
);
CREATE TABLE IF NOT EXISTS avaliacoes (
 id INTEGER PRIMARY KEY,
 matricula_id INTEGER NOT NULL REFERENCES matriculas(id),
 bimestre INTEGER NOT NULL CHECK(bimestre BETWEEN 1 AND 4),
 professor_id INTEGER NOT NULL REFERENCES usuarios(id),
 status TEXT NOT NULL DEFAULT 'rascunho' CHECK(status IN ('rascunho','finalizada')),
 observacao_geral TEXT NOT NULL DEFAULT '',
 UNIQUE(matricula_id, bimestre)
);
CREATE TABLE IF NOT EXISTS respostas (
 avaliacao_id INTEGER NOT NULL REFERENCES avaliacoes(id) ON DELETE CASCADE,
 criterio_id INTEGER NOT NULL REFERENCES criterios(id),
 nivel TEXT NOT NULL CHECK(nivel IN ('nao_observado','em_desenvolvimento','desenvolvido')),
 observacao TEXT NOT NULL DEFAULT '',
 PRIMARY KEY(avaliacao_id, criterio_id)
);
