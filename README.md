# cadastro-voluntarios
Sistema criado para ajudar a comunidade local no cadastro de voluntários para as festas.
Foi utilizado a linguagem Python, o framework Tkinter e o Firebase para armazenamento dos dados

# Como executar?
**ATENÇÃO:** 
 1. **Para execução pela faculdade (atividade de extensão):** O arquivo .json que autentica o firebase está na seção 3.2 para download. O mesmo deve ser inserido dentro da pasta /json, **SEM ALTERAÇÃO DO NOME ORIGINAL.** Com isso, o sistema reconhecerá e autenticará no firebase para execução completa.
 2. **Para execução por outra pessoa:** Solicite ao dono do repositório o arquivo .json de autenticação do Firebase.
 
O sistema até executa sem o .json do Firebase, porém não será possível efetuar ou visualizar cadastros.

Inserido o arquivo necessário na pasta JSON, é só realizar os seguintes pip install's (para execução via linha de comando ou IDE):

 - pip install firebase-admin 
 - pip install openpyxl