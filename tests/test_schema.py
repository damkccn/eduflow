"""Testes de esquema do EduFlow 2.0. Executar: python -m unittest discover -s tests -v"""
import sqlite3
import unittest
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / "schema.sql"

class TestSchema(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA.read_text(encoding="utf-8"))
        self.db.execute("INSERT INTO escolas (id,nome) VALUES (1,'Escola Exemplo')")
        self.db.execute("INSERT INTO turmas (id,escola_id,nome,ano_letivo) VALUES (1,1,'PRÉ I A',2027)")
        self.db.execute("INSERT INTO alunos (id,escola_id,nome) VALUES (1,1,'Ana Exemplo')")
        self.db.execute("INSERT INTO matriculas (id,aluno_id,turma_id,ano_letivo) VALUES (1,1,1,2027)")
        self.db.execute("INSERT INTO usuarios (id,escola_id,nome,email,perfil) VALUES (1,1,'Professora Exemplo','prof@exemplo.invalid','professor')")
    def tearDown(self):
        self.db.close()
    def test_matricula_unica_por_ano(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO matriculas (aluno_id,turma_id,ano_letivo) VALUES (1,1,2027)")
    def test_nao_permite_bimestre_invalido(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO avaliacoes (matricula_id,bimestre,professor_id) VALUES (1,5,1)")
    def test_uma_avaliacao_por_bimestre(self):
        self.db.execute("INSERT INTO avaliacoes (matricula_id,bimestre,professor_id) VALUES (1,1,1)")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO avaliacoes (matricula_id,bimestre,professor_id) VALUES (1,1,1)")
    def test_resposta_por_criterio(self):
        self.db.execute("INSERT INTO criterios (id,escola_id,descricao) VALUES (1,1,'Interage com colegas')")
        self.db.execute("INSERT INTO avaliacoes (id,matricula_id,bimestre,professor_id) VALUES (1,1,1,1)")
        self.db.execute("INSERT INTO respostas (avaliacao_id,criterio_id,nivel,observacao) VALUES (1,1,'em_desenvolvimento','Exemplo fictício')")
        self.assertEqual(self.db.execute("SELECT nivel FROM respostas").fetchone()[0], "em_desenvolvimento")
    def test_chave_estrangeira(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO matriculas (aluno_id,turma_id,ano_letivo) VALUES (999,1,2027)")

if __name__ == "__main__":
    unittest.main()
