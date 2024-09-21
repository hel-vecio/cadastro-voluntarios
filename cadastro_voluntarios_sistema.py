import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from firebase_admin import credentials, initialize_app, firestore
import openpyxl
import utils


############# PARA RODAR O SISTEMA ##################
# pip install firebase-admin
# pip install openpyxl
#####################################################

class VoluntarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Voluntários")
        self.root.geometry("400x370")
        self.root.resizable(False, False)
        self.centralizar_janela()
        self.carregar_tela_inicial()

        try:
            credenciais_firebase = credentials.Certificate('json/chave-firebase.json') # SE ESSE ARQUIVO NÃO ESTIVER NA PASTA, O SISTEMA NÃO FAZ CADASTRO NEM GERA A PLANILHA
            bancoVoluntarios = initialize_app(credenciais_firebase)
            self.db = firestore.client()
            print(bancoVoluntarios.project_id)
        except Exception:
            messagebox.showwarning("Erro","Chave do Firebase Admin SDK não identificada! Você pode utilizar o sistema, porém não conseguirá salvar ou visualizar dados.")

    # Tela inicial do sistema
    def carregar_tela_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        imagem_logo = tk.PhotoImage(file="img/img_tela_inicial.png")

        logo_label = tk.Label(frame, image=imagem_logo)
        logo_label.image = imagem_logo
        logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        titulo_tela = tk.Label(frame, text="Cadastro de Voluntários", font=("Arial", 16))
        titulo_tela.grid(row=1, column=0, columnspan=2, pady=0)

        botao_frame = tk.Frame(frame)
        botao_frame.grid(row=2, column=0, columnspan=2, pady=20)

        botao_novo_cadastro = tk.Button(botao_frame, text="Novo Cadastro", command=self.carregar_tela_cadastro_voluntario)
        botao_novo_cadastro.grid(row=0, column=0, padx=10)

        botao_visualizar_cadastros = tk.Button(botao_frame, text="Visualizar Cadastros", command=self.visualizar_voluntarios)
        botao_visualizar_cadastros.grid(row=0, column=1, padx=10)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    # Tela de cadastro
    def carregar_tela_cadastro_voluntario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack(expand=True, fill="both")

        titulo = tk.Label(frame, text="Novo Cadastro", font=("Arial", 14))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Nome Completo:").grid(row=1, column=0, sticky='e', padx=10, pady=5)
        self.campo_nome = tk.Entry(frame)
        self.campo_nome.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        utils.limitar_caracteres(self.campo_nome, 100)
        utils.capitalizacao(self.campo_nome)

        tk.Label(frame, text="CPF:").grid(row=2, column=0, sticky='e', padx=10, pady=5)
        self.campo_cpf = tk.Entry(frame)
        self.campo_cpf.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        utils.aplicar_mascara_cpf(self.campo_cpf)

        tk.Label(frame, text="Celular:").grid(row=3, column=0, sticky='e', padx=10, pady=5)
        self.campo_celular = tk.Entry(frame)
        self.campo_celular.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        utils.aplicar_mascara_celular(self.campo_celular)

        tk.Label(frame, text="E-mail:").grid(row=4, column=0, sticky='e', padx=10, pady=5)
        self.campo_email = tk.Entry(frame)
        self.campo_email.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        utils.limitar_caracteres(self.campo_email, 100)

        tk.Label(frame, text="Data de Nascimento:").grid(row=5, column=0, sticky='e', padx=10, pady=5)
        self.campo_data = tk.Entry(frame)
        self.campo_data.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        utils.aplicar_mascara_data(self.campo_data)

        tk.Label(frame, text="Sexo:").grid(row=6, column=0, sticky='e', padx=10, pady=5)
        self.campo_sexo = tk.Entry(frame)
        self.campo_sexo = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly")
        self.campo_sexo.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(frame, text="Função:").grid(row=7, column=0, sticky='e', padx=10, pady=5)
        self.campo_funcao = tk.Entry(frame)
        self.campo_funcao.grid(row=7, column=1, sticky="ew", padx=10, pady=5)
        utils.limitar_caracteres(self.campo_funcao, 100)
        utils.capitalizacao(self.campo_funcao)

        tk.Label(frame, text="Disponibilidade de Horário:").grid(row=8, column=0, sticky='e', padx=10, pady=5)
        self.campo_disponibilidade = tk.Entry(frame)
        self.campo_disponibilidade.grid(row=8, column=1, sticky="ew", padx=10, pady=5)
        utils.limitar_caracteres(self.campo_disponibilidade, 100)

        botao_frame = tk.Frame(frame)
        botao_frame.grid(row=9, column=0, columnspan=2, pady=20)

        botao_enviar_cadastro_firebase = tk.Button(botao_frame, text="Enviar cadastro", command=self.cadastrar_voluntario_firebase)
        botao_enviar_cadastro_firebase.grid(row=0, column=0, padx=10)

        botao_voltar = tk.Button(botao_frame, text="Voltar", command=self.carregar_tela_inicial)
        botao_voltar.grid(row=0, column=1, padx=10)

        frame.grid_columnconfigure(1, weight=1)

    # Tela que gera os voluntários já cadastrados no firebase
    def visualizar_voluntarios(self):
        try:
            voluntarios_ref = self.db.collection('voluntarios')
            voluntarios = voluntarios_ref.stream()

            caminho_arquivo = os.path.join(os.path.expanduser("~"), "Desktop", "voluntarios.xlsx")
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.append(["Nome", "CPF", "Celular", "E-mail", "Data de Nascimento", "Sexo", "Função", "Disponibilidade"])

            for voluntario in voluntarios:
                dados = voluntario.to_dict()
                worksheet.append([
                    dados.get('nome'), dados.get('cpf'), dados.get('celular'), dados.get('email'),
                    dados.get('data_nascimento'), dados.get('sexo'),
                    dados.get('funcao'), dados.get('disponibilidade')
                ])

            workbook.save(caminho_arquivo)
            self.gerar_mensagem_geracao_planilha(f"Os dados foram salvos em uma planilha em {caminho_arquivo}")

        except Exception as erro:
            self.gerar_mensagem_geracao_planilha("Erro ao obter os dados!\n" + str(erro))
            print(erro)

    def cadastrar_voluntario_firebase(self):
        nome = self.campo_nome.get()
        cpf = self.campo_cpf.get()
        celular = self.campo_celular.get()
        email = self.campo_email.get()
        data_nasc = self.campo_data.get()
        sexo = self.campo_sexo.get()
        funcao = self.campo_funcao.get()
        disponibilidade = self.campo_disponibilidade.get()

        if self.validar_dados():
            ref = self.db.collection('voluntarios')
            ref.add({
                "nome": nome,
                "cpf": cpf,
                "celular": celular,
                "email": email,
                "data_nascimento": data_nasc,
                "sexo": sexo,
                "funcao": funcao,
                "disponibilidade": disponibilidade
            })

            messagebox.showinfo("Sucesso", "Cadastro enviado com sucesso!")
            self.carregar_tela_inicial()

    def validar_dados(self):
        if not self.campo_nome.get():
            messagebox.showerror("Erro", "Informe o nome do voluntário!")
            return False
        if not utils.validar_cpf(self.campo_cpf.get()):
            messagebox.showerror("Erro", "CPF inválido!")
            return False
        if not utils.validar_celular(self.campo_celular.get()):
            messagebox.showerror("Erro", "Celular inválido!")
            return False
        if not utils.validar_email(self.campo_email.get()):
            messagebox.showerror("Erro", "E-mail inválido!")
            return False
        if not utils.validar_data_nascimento(self.campo_data.get()):
            messagebox.showerror("Erro", "Data de Nascimento inválida!")
            return False
        if not self.campo_sexo.get():
            messagebox.showerror("Erro", "Informe o campo sexo!")
            return False
        if not self.campo_funcao.get():
            messagebox.showerror("Erro", "Informe o campo função!")
            return False
        if not self.campo_disponibilidade.get():
            messagebox.showerror("Erro", "Informe o campo disponibilidade de horário!")
            return False
        return True


    def gerar_mensagem_geracao_planilha(self, message):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text=message, wraplength=280)
        label.pack(pady=(150, 0))

        btn_ok = tk.Button(self.root, text="Ok", command=self.carregar_tela_inicial)
        btn_ok.pack(pady=10)

    def centralizar_janela(self):
        largura_janela = 400
        altura_janela = 370

        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoluntarioApp(root)
    root.mainloop()
