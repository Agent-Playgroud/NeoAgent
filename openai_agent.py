# -*- coding: utf-8 -*- 
import openai
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurar a API Key
api_key = os.getenv("OPENAI_API_KEY")

# Verificar se a chave foi carregada corretamente
if api_key is None:
    print("Erro: A chave da API não foi encontrada. Verifique o arquivo .env.")
else:
    print("API Key carregada com sucesso!")

openai.api_key = api_key

def chat_with_openai(prompt, conversation_history, model="gpt-4"):
    """Função para interagir com a API da OpenAI com memória"""
    try:
        # Adicionando a nova interação ao histórico
        conversation_history.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation_history  # Passa o histórico completo da conversa
        )

        # Receber a resposta do modelo
        model_response = response["choices"][0]["message"]["content"]

        # Adicionar a resposta do modelo ao histórico
        conversation_history.append({"role": "assistant", "content": model_response})

        return model_response, conversation_history

    except Exception as e:
        return f"Erro ao chamar API: {e}", conversation_history

# Interação no terminal
if __name__ == "__main__":
    print("Bem-vindo ao Assistente da OpenAI!")
    conversation_history = [{"role": "system", "content": "Você é um assistente útil."}]  # Inicia a conversa com uma mensagem do sistema
    while True:
        prompt = input("Digite sua pergunta (ou 'sair' para encerrar): ")
        if prompt.lower() == 'sair':
            break
        resposta, conversation_history = chat_with_openai(prompt, conversation_history)
        print(f"Resposta: {resposta}")

