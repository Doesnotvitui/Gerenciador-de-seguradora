import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                            QTableWidget, QMessageBox, QTableWidgetItem, QHBoxLayout, QComboBox, QDialog, QFormLayout, QDialogButtonBox)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import aliased
from sqlalchemy import text

# Definir informações de conexão com o banco de dados
username = 'root'
password = 'Vz-qEact9r'
host = 'localhost'
port = 3306
database = 'seguradora'

# Criar a string de conexão
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

# Criar sessão
Session = sessionmaker(bind=engine)
session = Session()

# Declarando o mapeamento
Base = declarative_base()

# Classes de tabelas do banco de dados
class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50))
    cpf = Column(String(15))
    rg = Column(String(15))
    email = Column(String(50))
    apolices = relationship('Apolice', back_populates='cliente')
    apartamentos = relationship('Apartamento', back_populates='cliente')

class Apartamento(Base):
    __tablename__ = 'apartamento'
    id = Column(Integer, primary_key=True)
    numero_apartamento = Column(String(10))
    bloco = Column(Integer)
    valor_apartamento = Column(Integer)
    fk_id_cliente = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente', back_populates='apartamentos')
    apolices = relationship('Apolice', back_populates='apartamento')

class Apolice(Base):
    __tablename__ = 'apolice'
    id = Column(Integer, primary_key=True)
    valor_assegurado = Column(Integer)
    fk_id_cliente = Column(Integer, ForeignKey('cliente.id'))
    fk_id_apartamento = Column(Integer, ForeignKey('apartamento.id'))
    cliente = relationship('Cliente', back_populates='apolices')
    apartamento = relationship('Apartamento', back_populates='apolices')

class Acidentes(Base):
    __tablename__ = 'acidentes'
    id = Column(Integer, primary_key=True)
    quantidade_acidentes = Column(Integer)
    fk_id_cliente = Column(Integer, ForeignKey('cliente.id'))
    fk_id_apartamento = Column(Integer, ForeignKey('apartamento.id'))
    fk_id_apolice = Column(Integer, ForeignKey('apolice.id'))
    cliente = relationship('Cliente')
    apartamento = relationship('Apartamento')
    apolice = relationship('Apolice')

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

# Criação da interface gráfica
class AddRecordDialog(QDialog):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Adicionar {table_name}")
        self.table_name = table_name
        self.setGeometry(100, 100, 400, 300)

        self.layout = QFormLayout(self)

        # Definir campos para cada tabela
        if self.table_name == "Clientes":
            self.name_input = QLineEdit(self)
            self.cpf_input = QLineEdit(self)
            self.rg_input = QLineEdit(self)
            self.email_input = QLineEdit(self)
            self.layout.addRow("Nome Completo:", self.name_input)
            self.layout.addRow("CPF:", self.cpf_input)
            self.layout.addRow("RG:", self.rg_input)
            self.layout.addRow("E-mail:", self.email_input)

        elif self.table_name == "Apartamentos":
            self.name_input = QLineEdit(self)
            self.cpf_input = QLineEdit(self)
            self.rg_input = QLineEdit(self)
            self.email_input = QLineEdit(self)
            self.layout.addRow("Número do Apartamento:", self.name_input)
            self.layout.addRow("Bloco:", self.cpf_input)
            self.layout.addRow("Valor do Apartamento:", self.rg_input)
            self.layout.addRow("Cliente ID:", self.email_input)

        elif self.table_name == "Apolices":
            self.name_input = QLineEdit(self)
            self.cpf_input = QLineEdit(self)
            self.rg_input = QLineEdit(self)
            self.email_input = QLineEdit(self)
            self.layout.addRow("Valor Assegurado:", self.name_input)
            self.layout.addRow("Cliente ID:", self.cpf_input)
            self.layout.addRow("Apartamento ID:", self.rg_input)

        elif self.table_name == "Acidentes":
            self.name_input = QLineEdit(self)
            self.cpf_input = QLineEdit(self)
            self.rg_input = QLineEdit(self)
            self.email_input = QLineEdit(self)
            self.layout.addRow("Quantidade de Acidentes:", self.name_input)
            self.layout.addRow("Cliente ID:", self.cpf_input)
            self.layout.addRow("Apartamento ID:", self.rg_input)
            self.layout.addRow("Apólice ID:", self.email_input)

        # Botões para confirmar ou cancelar
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_data(self):
        """Retorna os dados inseridos no formulário"""
        if self.table_name == "Clientes":
            return (self.name_input.text(), self.cpf_input.text(), self.rg_input.text(), self.email_input.text())
        elif self.table_name == "Apartamentos":
            return (self.name_input.text(), self.cpf_input.text(), self.rg_input.text(), self.email_input.text())
        elif self.table_name == "Apolices":
            return (self.name_input.text(), self.cpf_input.text(), self.rg_input.text())
        elif self.table_name == "Acidentes":
            return (self.name_input.text(), self.cpf_input.text(), self.rg_input.text(), self.email_input.text())

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QFormLayout(self)

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.layout.addRow("Nome de usuário:", self.username_input)
        self.layout.addRow("Senha:", self.password_input)

        # Botões para confirmar ou cancelar
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_credentials(self):
        """Retorna as credenciais inseridas no formulário"""
        return self.username_input.text(), self.password_input.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerenciador de Seguradora")
        self.setGeometry(100, 100, 800, 600)

        # Chama o diálogo de login ao iniciar
        if not self.show_login_dialog():
            sys.exit(1)  # Se o login não for aceito, o programa é fechado

        # Widget principal
        widget = QWidget()
        layout = QVBoxLayout()

        # Tabela para mostrar os dados
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.cellClicked.connect(self.select_record)

        # Definir os títulos das colunas
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "RG", "E-mail"])

        # Botão para carregar os dados
        self.load_button = QPushButton("Carregar Dados")
        self.load_button.clicked.connect(self.load_data)

        # Botões para Adicionar, Atualizar e Deletar
        self.add_button = QPushButton("Adicionar")
        self.add_button.clicked.connect(self.add_record)

        # Botão para deletar
        self.delete_button = QPushButton("Deletar")
        self.delete_button.clicked.connect(self.delete_record)
        self.delete_button.setEnabled(False)  # Desativado até que um registro seja selecionado

        # Layout para os botões de controle
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        # ComboBox para selecionar a tabela
        self.table_selector = QComboBox()
        self.table_selector.addItems(["Clientes", "Apartamentos", "Apolices", "Acidentes"])
        self.table_selector.currentIndexChanged.connect(self.change_table)

        # Botão de "Voltar" (exibido após consulta avançada)
        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setVisible(False)  # Inicialmente invisível

        # Adicionando widgets ao layout
        layout.addWidget(QLabel("Selecionar Tabela"))
        layout.addWidget(self.table_selector)
        layout.addWidget(self.table)
        layout.addWidget(self.load_button)
        layout.addLayout(button_layout)

        # Adicionando o campo de entrada para consulta e o botão no layout
        self.query_input = QLineEdit(self)
        self.query_button = QPushButton("Executar Consulta Avançada")
        self.query_button.clicked.connect(self.execute_advanced_query)

        # Adicionando ao layout
        layout.addWidget(QLabel("Consulta Avançada (SQL):"))
        layout.addWidget(self.query_input)
        layout.addWidget(self.query_button)
        layout.addWidget(self.back_button)  # Adiciona o botão de Voltar ao layout

        # Definindo o layout principal
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Atributos de controle
        self.selected_record_id = None
        self.current_table = "Clientes"

    def show_login_dialog(self):
        """Exibe o diálogo de login e valida as credenciais"""
        login_dialog = LoginDialog(self)
        if login_dialog.exec() == QDialog.Accepted:
            username, password = login_dialog.get_credentials()
            # Validação de login
            if self.validate_login(username, password):
                return True  # Login bem-sucedido
            else:
                QMessageBox.critical(self, "Erro", "Credenciais inválidas! O aplicativo será fechado.")
                return False  # Login falhou
        else:
            return False  # Usuário cancelou ou fechou o diálogo

    def validate_login(self, username, password):
        """Valida o nome de usuário e a senha"""
        # Exemplo simples: validar com usuário e senha fixos
        valid_username = "admin"
        valid_password = "senha123"

        # Em um caso real, você pode fazer uma consulta ao banco de dados para verificar as credenciais.
        return username == valid_username and password == valid_password

    def execute_advanced_query(self):
        """Executar consultas avançadas usando álgebra relacional."""
        query_text = self.query_input.text()
        
        try:
            # Obter uma conexão do engine
            with engine.connect() as connection:
                # Usar text() para envolver a consulta SQL
                result = connection.execute(text(query_text))
                
                # Limpar a tabela antes de exibir os resultados
                self.table.setRowCount(0)

                # Adicionar os resultados à tabela
                for row in result:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for col, value in enumerate(row):
                        self.table.setItem(row_position, col, QTableWidgetItem(str(value)))
            
        except Exception as e:
            # Exibir erro, caso a consulta seja inválida
            print(f"Erro ao executar consulta: {e}")


    def go_back(self):
        """Voltar à visualização normal da tabela."""
        self.back_button.setVisible(False)  # Ocultar o botão de Voltar
        self.load_data()  # Carregar novamente os dados da tabela selecionada

    def load_data(self):
        """Carregar dados da tabela selecionada do banco de dados e exibir na tabela."""
        self.table.setRowCount(0)

        if self.current_table == "Clientes":
            records = session.query(Cliente).all()
            for record in records:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(str(record.id)))
                self.table.setItem(row_position, 1, QTableWidgetItem(record.fullname))
                self.table.setItem(row_position, 2, QTableWidgetItem(record.cpf))
                self.table.setItem(row_position, 3, QTableWidgetItem(record.rg))
                self.table.setItem(row_position, 4, QTableWidgetItem(record.email))
        
        # Adicione os dados das outras tabelas (Apartamentos, Apolices, Acidentes) aqui, seguindo o mesmo padrão.

    def add_record(self):
        """Adicionar novo registro à tabela"""
        dialog = AddRecordDialog(self.current_table, self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()

            if self.current_table == "Clientes":
                cliente = Cliente(fullname=data[0], cpf=data[1], rg=data[2], email=data[3])
                session.add(cliente)
                session.commit()
            elif self.current_table == "Apartamentos":
                apartamento = Apartamento(numero_apartamento=data[0], bloco=data[1], valor_apartamento=data[2], fk_id_cliente=data[3])
                session.add(apartamento)
                session.commit()
            elif self.current_table == "Apolices":
                apolice = Apolice(valor_assegurado=data[0], fk_id_cliente=data[1], fk_id_apartamento=data[2])
                session.add(apolice)
                session.commit()
            elif self.current_table == "Acidentes":
                acidente = Acidentes(quantidade_acidentes=data[0], fk_id_cliente=data[1], fk_id_apartamento=data[2], fk_id_apolice=data[3])
                session.add(acidente)
                session.commit()

            self.load_data()

    def select_record(self, row, column):
        """Selecionar registro na tabela"""
        self.selected_record_id = self.table.item(row, 0).text()
        self.delete_button.setEnabled(True)

    def delete_record(self):
        """Deletar registro da tabela"""
        if self.selected_record_id:
            if self.current_table == "Clientes":
                cliente = session.query(Cliente).filter_by(id=self.selected_record_id).first()
                session.delete(cliente)
            elif self.current_table == "Apartamentos":
                apartamento = session.query(Apartamento).filter_by(id=self.selected_record_id).first()
                session.delete(apartamento)
            elif self.current_table == "Apolices":
                apolice = session.query(Apolice).filter_by(id=self.selected_record_id).first()
                session.delete(apolice)
            elif self.current_table == "Acidentes":
                acidente = session.query(Acidentes).filter_by(id=self.selected_record_id).first()
                session.delete(acidente)

            session.commit()
            self.load_data()
            self.delete_button.setEnabled(False)

    def change_table(self):
        """Alterar a tabela atual baseada na seleção do ComboBox"""
        self.current_table = self.table_selector.currentText()
        self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
