"""EduFlow — protótipo local com dados fictícios. Python 3.10+."""
import csv
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
TURMA = re.compile(r"^PRÉ (I|II) [A-Z]$")

def validar_turma(turma):
    if not TURMA.fullmatch(turma.strip().upper()):
        raise ValueError("Turma inválida. Exemplo: PRÉ I A ou PRÉ II B.")
    return turma.strip().upper()

def cadastrar_aluno(nome, turma, arquivo=None):
    if not 2 <= len(nome.strip()) <= 120:
        raise ValueError("Nome inválido")
    turma = validar_turma(turma)
    destino = Path(arquivo) if arquivo else DATA / "alunos.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    exists = destino.exists()
    with destino.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "turma"])
        if not exists or destino.stat().st_size == 0:
            writer.writeheader()
        writer.writerow({"nome": nome.strip(), "turma": turma})
    return destino

def listar_por_turma(arquivo=None):
    origem = Path(arquivo) if arquivo else DATA / "alunos.csv"
    if not origem.exists():
        return {}
    turmas = {}
    with origem.open(newline="", encoding="utf-8") as f:
        for aluno in csv.DictReader(f):
            turmas.setdefault(aluno["turma"], []).append(aluno["nome"])
    return dict(sorted(turmas.items()))

def backup(arquivo=None):
    origem = Path(arquivo) if arquivo else DATA / "alunos.csv"
    if not origem.exists():
        raise FileNotFoundError("Nenhum cadastro disponível para backup")
    pasta = origem.parent / "backups"
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / (origem.stem + "_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + origem.suffix)
    shutil.copy2(origem, destino)
    return destino

if __name__ == "__main__":
    cadastrar_aluno("Ana Exemplo", "PRÉ II A")
    cadastrar_aluno("Beatriz Exemplo", "PRÉ I C")
    print(json.dumps(listar_por_turma(), ensure_ascii=False, indent=2))
    print("Backup:", backup())
