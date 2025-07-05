#from openai import OpenAI
from google import genai
import sympy
from sympy import N,Symbol
from sympy.solvers import solve

client = genai.Client(api_key="AIzaSyBOET2LTdLEyOa1AWjUPA8XbsWbqExjXUQ")
chaveapi="AIzaSyBOET2LTdLEyOa1AWjUPA8XbsWbqExjXUQ"
def explicacao(equacao: str, raizes: list):
    payload = {
        "model": "gemini-2.0-flash",
        "contents": f"você é um professor de matemática e vai resolver essa equação: {equacao}=0 para os alunos, explique de forma didática,sem cumprimentos!, mas sem ser prolixo,o porquê dela possuir essas raízes: {raizes}, por favor."
    }
    response = client.models.generate_content(**payload)
    return response.text
def normaliza(equacao:str):
    equacao=equacao.replace("^","**")
    equacao=equacao.replace("cos","sympy.cos")
    equacao=equacao.replace("sen","sympy.sin")
    equacao=equacao.replace("tg","sympy.tan")
    equacao=equacao.replace("ln","sympy.log")
    equacao=equacao.replace("e","sympy.E")

    equacao=equacao.lower()
    return equacao
def botavariavel(equacao: str):
    equacao = normaliza(equacao)
    x = sympy.Symbol("X")
    exp = None  # Inicializa a variável
    try:
        exp = eval(equacao)
    except SyntaxError:
        exp = 'Erro de sintaxe'
    return exp
def raiz(expr:str,var:str):
    raizes=[]
    
    for solution in sympy.solve(expr,var):   
        raizes.append(N(solution))
    if len(raizes)==0:
        raizes.append('Sem solução')
    return raizes


# func.py
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import re
from math import sin, cos, tan, log, exp, sqrt, pi

def cria_grafico(equacao_str):
    try:
        # Pré-processamento da equação
        equacao_str = equacao_str.replace('^', '**').replace('X', 'x')
        
        # Verificação de segurança
        if not re.match(r'^[x0-9+\-*/\s().^sincostanlogexpsqrtpi]+$', equacao_str):
            raise ValueError("Equação contém caracteres inválidos")
        
        # Cria a figura
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.linspace(-2*np.pi, 2*np.pi, 400)
        
        # Ambiente seguro para eval
        safe_dict = {
            'x': x,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'log': np.log,
            'exp': np.exp,
            'sqrt': np.sqrt,
            'pi': np.pi
        }
        
        # Calcula os valores de y
        y = eval(equacao_str, {"__builtins__": None}, safe_dict)
        
        # Configura o gráfico
        ax.plot(x, y)
        ax.set_title(f"Gráfico de {equacao_str}")
        ax.grid(True)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        
        # Salva em memória
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return base64.b64encode(buf.read()).decode('utf-8')
    
    except Exception as e:
        plt.close()
        raise ValueError(f"Erro ao criar gráfico: {str(e)}")
