from datetime import datetime
import re
import tkinter as tk

# TODA LÓGICA DE VALIDAÇÃO E MÁSCARAS FICA AQUI
def limitar_caracteres(valor, limite):
    def callback(event):
        texto = valor.get()
        if len(texto) > limite:
            valor.delete(limite, tk.END)

    valor.bind("<KeyRelease>", callback)


def capitalizacao(valor):
    def callback(event):
        texto = valor.get()

        texto_formatado = texto.title()
        valor.delete(0, tk.END)
        valor.insert(0, texto_formatado)

    valor.bind("<KeyRelease>", callback)


def aplicar_mascara_cpf(cpf):
    def callback(event):
        texto = cpf.get().replace(".", "").replace("-", "")
        novo_texto = ""

        if not texto.isdigit():
            texto = ''.join(filter(str.isdigit, texto))

        if len(texto) > 0:
            novo_texto += texto[:3]
        if len(texto) > 3:
            novo_texto += "." + texto[3:6]
        if len(texto) > 6:
            novo_texto += "." + texto[6:9]
        if len(texto) > 9:
            novo_texto += "-" + texto[9:11]

        cpf.delete(0, tk.END)
        cpf.insert(0, novo_texto[:14])

    cpf.bind("<KeyRelease>", callback)


def aplicar_mascara_data(data):
    def callback(event):
        texto = data.get().replace("/", "")
        novo_texto = ""

        if not texto.isdigit():
            texto = ''.join(filter(str.isdigit, texto))

        if len(texto) > 0:
            novo_texto += texto[:2]
        if len(texto) > 2:
            novo_texto += "/" + texto[2:4]
        if len(texto) > 4:
            novo_texto += "/" + texto[4:8]

        data.delete(0, tk.END)
        data.insert(0, novo_texto[:10])

    data.bind("<KeyRelease>", callback)


def aplicar_mascara_celular(celular):
    def callback(event):
        texto = celular.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        novo_texto = ""

        if not texto.isdigit():
            texto = ''.join(filter(str.isdigit, texto))

        if len(texto) > 0:
            novo_texto += "(" + texto[:2] + ") "
        if len(texto) > 2:
            novo_texto += texto[2:7]
        if len(texto) > 6:
            novo_texto += "-" + texto[7:11]

        celular.delete(0, tk.END)
        celular.insert(0, novo_texto)

    celular.bind("<KeyRelease>", callback)


def validar_cpf(cpf):
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False
    numeros = [int(digit) for digit in cpf if digit.isdigit()]
    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False

    soma_produtos = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
    digito_calculado = (soma_produtos * 10 % 11) % 10
    if numeros[9] != digito_calculado:
        return False

    soma_produtos = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
    digito_calculado = (soma_produtos * 10 % 11) % 10
    if numeros[10] != digito_calculado:
        return False

    return True


def validar_data_nascimento(data_nasc):
    try:
        data_nasc = datetime.strptime(data_nasc, "%d/%m/%Y")
        data_atual = datetime.now()
        if data_nasc > data_atual:
            return False
        return True
    except ValueError:
        return False


def validar_email(emaiL):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', emaiL):
        return False
    return True


def validar_celular(celular):
    celular = celular.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if len(celular) != 11 or not celular.isdigit():
        return False
    return True
