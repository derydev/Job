import sqlite3


conexao = sqlite3.connect("derijobb.db")
cursor = conexao.cursor()

try:
    cursor.execute("""
        ALTER TABLE candidaturas
        ADD COLUMN documento_id INTEGER
        REFERENCES documentos(id)
    """)

    conexao.commit()

    print("Coluna documento_id adicionada com sucesso!")

except sqlite3.OperationalError as erro:
    print(f"Erro: {erro}")

finally:
    conexao.close()