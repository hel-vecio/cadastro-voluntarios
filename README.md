# cadastro-voluntarios
Sistema criado para ajudar a comunidade local no cadastro de voluntários para as festas.
Foi utilizado a linguagem Python, o framework Tkinter e o Firebase para armazenamento dos dados

# Como executar?
**ATENÇÃO:** 
 1. **Para execução pela faculdade (atividade de extensão):** É necessário criar um arquivo "chave-firebase.json" na pasta /json e inserir os valores descritos na seção 3.2 da atividade de extensão. Caso precise, você pode solicitar esse arquivo pronto através do e-mail indicado na mesma seção. **O arquivo deve, obrigatoriamente, ter o nome chave-firebase.json** Com isso, o sistema reconhecerá e autenticará no firebase para execução completa.
 2. **Para execução por outra pessoa:** Solicite ao dono do repositório o arquivo .json de autenticação do Firebase.
 
O sistema até executa sem o .json do Firebase, porém não será possível efetuar ou visualizar cadastros.

Inserido o arquivo necessário na pasta JSON, é só realizar os seguintes pip install's (para execução via linha de comando ou IDE):

 - pip install firebase-admin 
 - pip install openpyxl