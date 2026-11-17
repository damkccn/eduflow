import tempfile
import unittest
from pathlib import Path
from eduflow import cadastrar_aluno, listar_por_turma, validar_turma, backup

class TestEduFlow(unittest.TestCase):
    def test_turma(self):
        self.assertEqual(validar_turma("pré i a"), "PRÉ I A")
        with self.assertRaises(ValueError):
            validar_turma("3 B")
    def test_cadastro_e_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "alunos.csv"
            cadastrar_aluno("Ana Exemplo", "PRÉ II A", arquivo)
            self.assertEqual(listar_por_turma(arquivo)["PRÉ II A"], ["Ana Exemplo"])
            self.assertTrue(backup(arquivo).exists())

if __name__ == "__main__":
    unittest.main()
