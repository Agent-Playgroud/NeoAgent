<h1 align="center">Neo Agent </h1>

<p align="center">🚀 Aplicação para bate papo com agente de IA generativa</p>

<p align="center">
 <a href="#objetivo">Objetivo</a> •
 <a href="#Features">Features</a> • 
 <a href="#Pré-Requisitos">Pré-Requisitos</a> • 
 <a href="#Rodando o Back End (servidor)">Rodando o Back End (servidor) •
 <a href="#tecnologias">Tecnologias</a> • 
 <a href="#Autores">Autores</a>
 <a href="#License">Licença</a> • 
</p>

<h4 align="center"> 
	🚧  Status >>> 🚀 Em construção...  🚧
</h4>

<h4 align="center">  
	Objetivo
</h4>

Esta aplicação tem por objetivo proporcionar conversas interativas com agentes de IA generativa de temas diferentes, indo de recomendações de filmes a adivinhações divertidas.

### Features

- [x] Login de usuário 
- [x] Escolha de agente
- [ ] Converse com seu agente


### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
• Python na versão 3.5 
• SQL Server
• Conta no Google

### 🎲 Rodando o Back End (servidor)

```bash
# Clone este repositório
$ git clone <https://github.com/tgmarinho/nlw1>

# Acesse a pasta do projeto no terminal/cmd
$ cd NeoAgent

# Ative o ambiente virtual da oasta do projeto
$ .venv\Scripts\activate

# Execute a aplicação no cmd
$ streamlit run main_page.py

# O servidor inciará na porta:8501 - acesse <http://localhost:8501> ou espere seu navehgador padrão abri-lo
```


### 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

•	Python → Linguagem principal para desenvolvimento.
•	FastAPI → API para interação com o OpenAI e outras funções.
•	SQL Server → Banco de dados para armazenar usuários, agentes e arquivos.
•	Streamlit → Framework para criar a interface interativa do sistema.
•	streamlit-authenticator → Gerenciamento de login via Google.
•	OpenAI API → Utilizada para o processamento e resposta dos agentes.
•	OAuth 2.0 (Google Login) → Autenticação via conta do Google.
•	pyodbc → Biblioteca para interagir com SQL Server
•	dotenv → Gerenciamento de variáveis de ambiente.


###  Autores

Os autores desse criativo projeto são: 
Raphael Ramalho
Thais
João

License

Copyright (c) <2020> <Grupo 4 Desafio acelerado>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
