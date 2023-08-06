import sys
sys.path.append('.')

import unittest
import pandas as pd
from multisqlite3manager import to_dataframe, print_databases, print_tables, _get_databases_name_from_sql_stmt, create_connection

"""
class TestMultiSqliteManager(unittest.TestCase):

    def setUp(self):
        # Inicializando com um diretório específico contendo arquivos de banco de dados SQLite
        self.folder_path = "/path/to/your/sqlite/files"  
        self.connection = get_connection()
        
    def tearDown(self):
        # Limpeza após os testes
        self.connection.close()

    def test_get_connection(self):
        self.assertIsNotNone(self.connection)

    def test_print_databases(self):
        # Como a função print_databases() não retorna nada, é um pouco mais difícil de testar.
        # Aqui, estamos simplesmente verificando se a função pode ser chamada sem levantar uma exceção.
        try:
            print_databases(self.connection)
        except Exception as e:
            self.fail(f'print_databases() raised an exception: {e}')

    def test_print_tables(self):
        # Similarmente, estamos simplesmente verificando se a função pode ser chamada sem levantar uma exceção.
        try:
            print_tables(self.connection)
        except Exception as e:
            self.fail(f'print_tables() raised an exception: {e}')
            
    def test_get_databases_name_from_sql_stmt(self):
        # Neste exemplo, estou assumindo que você tem uma instrução SQL que seleciona de uma tabela.
        # Se o sqlglot e a função forem capazes de analisar corretamente as instruções SQL e extrair os nomes dos bancos de dados, 
        # a lista de nomes dos bancos de dados deve ser a mesma que a esperada.
        sql = "SELECT * FROM db1.table1"
        expected_db_names = ["db1"]
        self.assertEqual(_get_databases_name_from_sql_stmt(sql), expected_db_names)
"""

class TestMultiSqliteManager(unittest.TestCase):

    def setUp(self):
        # Inicializando com um diretório específico contendo arquivos de banco de dados SQLite
        self.folder_path = "/path/to/your/sqlite/files"  
        
    def test_get_databases_name_from_sql_stmt(self):
        # Neste exemplo, estou assumindo que você tem uma instrução SQL que seleciona de uma tabela.
        # Se o sqlglot e a função forem capazes de analisar corretamente as instruções SQL e extrair os nomes dos bancos de dados, 
        # a lista de nomes dos bancos de dados deve ser a mesma que a esperada.
        sql = """ 
            WITH tmp_table AS (
                SELECT * FROM db_2.table1
            )
            SELECT * FROM tmp_table;
        """
        expected_db_names = ["db_2"]
        self.assertEqual(_get_databases_name_from_sql_stmt(sql), expected_db_names)

    def test_to_dataframe(self):
        # Aqui, estou assumindo que você tem uma instrução SQL que seleciona de uma tabela.
        # Deverá ser retornado um pandas.DataFrame com os dados da tabela.
        
        sql = """  SELECT * FROM teste.tMisto UNION ALL SELECT * FROM teste_2.tMisto"""
        expected_df = pd.DataFrame
        result = to_dataframe(sql)
        print(result)
        self.assertIsInstance(result, expected_df)

    def test_create_connection(self):
        expected_connection = create_connection(["teste_2", "teste_3"])
        self.assertIsNotNone(expected_connection)

    def test_print_databases(self):
        # Como a função print_databases() não retorna nada, é um pouco mais difícil de testar.
        # Aqui, estamos simplesmente verificando se a função pode ser chamada sem levantar uma exceção.
        try:
            print_databases()
        except Exception as e:
            self.fail(f'print_databases() raised an exception: {e}')

    def test_print_tables(self):
        # Similarmente, estamos simplesmente verificando se a função pode ser chamada sem levantar uma exceção.
        try:
            print_tables("teste_2")
        except Exception as e:
            self.fail(f'print_tables() raised an exception: {e}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
