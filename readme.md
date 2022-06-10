#### primeiro clone o repositorio

    git clone https://github.com/JonasCaetanoSz/pimeiro-CRUD.git
    
#### agora e hora de instalar as bibliotecas que vão ser usadas

    cd primeiro-crud && pip install requirements.txt
   
## 🚀 iniciando 

    python server.py
    
## 📚 Utilizando 

após iniciar o server.py, um servidor local vai se iniciado em <a href="http://127.0.0.1:5000/"  target="_blank"> localhost </a>. todas as operações do CRUD podem ser usadas por lá, as funções disponiveis são :

- criar conta
- fazer login
- fazer logout
- trocar senha
- apagar conta
- gerenciamento de cache (sessionID)

## :ok_man: Bugs registrados

- é raro mais pode acontencer de a função que gera o sessionID criar uma sequencia que já está sendo usado por outra conta.
- quando faz login a sessão antiga é apagada do banco de dados e o outro dispositivo que está usando e desconectado.

## 📝 Licença

Este software está distribuido sobre a licença <a href='https://github.com/JonasCaetanoSz/pimeiro-CRUD/blob/master/license.md' target="_blank" > MIT </a>

### :anchor: Versão 1.0.0
