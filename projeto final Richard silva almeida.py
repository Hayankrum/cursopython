import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque
from random import randint
import networkx as nx
from scipy.linalg import lu


"""
Richard Silva Almeida.

Este código contém dois projetos em um:

Projeto 1: Cálculo de Gastos
Objetivo: Calcular os gastos mensais de um usuário, aplicar impostos sobre serviços e visualizar os gastos em gráficos.

Projeto 2: Rede de Comunicação
Objetivo: Analisar a estrutura de uma rede de comunicação usando a matriz de adjacência, decomposição LU e visualização gráfica.
"""

# --- Funções para o Projeto de Cálculo de Gastos ---

def calcular_gastos(gastos_mensais, periodo_meses, impostos):
    """
    Calcula os gastos totais com ICMS e o total para um determinado período.
    Args:
    - gastos_mensais: dicionário com os valores dos serviços mensais.
    - periodo_meses: número de meses para o cálculo.
    - impostos: dicionário com as taxas de ICMS e ISS.

    Retorna:
    - gastos_totais: gastos após a aplicação dos impostos.
    - total_periodo: gastos totais para o período.
    - gastos_totais_array: array com os gastos totais.
    - total_periodo_array: array com o total do período.
    """
    impostos_totais = sum(impostos.values()) / 100
    gastos_totais = {servico: (valor + valor * impostos_totais) for servico, valor in gastos_mensais.items()}
    total_periodo = {servico: valor * periodo_meses for servico, valor in gastos_totais.items()}
    gastos_totais_array = np.array(list(gastos_totais.values()))
    total_periodo_array = np.array(list(total_periodo.values()))
    
    return gastos_totais, total_periodo, gastos_totais_array, total_periodo_array

def plotar_gastos(gastos_periodo, gastos_iniciais, salario_mensal, icms):
    """
    Gera gráficos de barras e pizza para visualizar os gastos.
    Args:
    - gastos_periodo: dicionário com os gastos totais por serviço.
    - gastos_iniciais: dicionário com os valores iniciais dos serviços.
    - salario_mensal: o salário mensal do usuário.
    - icms: a taxa de ICMS aplicada.
    """
    servicos = list(gastos_periodo.keys())
    valores_iniciais = list(gastos_iniciais.values())
    valores_calculados = list(gastos_periodo.values())
    total_gastos = np.sum(valores_calculados)
    sobrou = salario_mensal - total_gastos

    # Gráfico de barras
    plt.figure(figsize=(14, 6))
    bar_width = 0.35
    index = range(len(servicos))
    
    barras_iniciais = plt.bar(index, valores_iniciais, bar_width, label="Valor Original", color="skyblue")
    barras_calculados = plt.bar([i + bar_width for i in index], valores_calculados, bar_width, label="Valor com ICMS", color="lightcoral")
    
    # Exibindo valores nas barras
    for i, valor in enumerate(valores_iniciais):
        plt.text(i - 0.15, valor + 0.02, f"R${valor:.2f}", ha='center', va='bottom', fontsize=10, color="blue")
    
    for i, valor in enumerate(valores_calculados):
        plt.text(i + bar_width - 0.15, valor + 0.02, f"R${valor:.2f}", ha='center', va='bottom', fontsize=10, color="red")
    
    plt.title(f"Gastos por Serviço (ICMS: {icms}%)")
    plt.xlabel("Serviços")
    plt.ylabel("Valor em Reais")
    plt.xticks([i + bar_width / 2 for i in index], servicos)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Gráfico de pizza
    plt.figure(figsize=(8, 8))
    all_valores = valores_iniciais + valores_calculados
    all_servicos = servicos + [f"{servico} - com ICMS" for servico in servicos]
    
    plt.pie(all_valores, labels=all_servicos, autopct="%1.1f%%", startangle=140, colors=["skyblue", "lightcoral"]*len(servicos))
    plt.title(f"Distribuição de Gastos (ICMS: {icms}%)")
    plt.show()

    # Exibindo valores de gastos totais e sobrando
    print(f"\nTotal de Gastos: R${total_gastos:.2f}")
    print(f"Valor sobrando do salário: R${sobrou:.2f}")
    print(f"Valor total de ICMS aplicado: R${total_gastos * (icms / 100):.2f}")

def coletar_dados_usuario():
    """
    Coleta os dados do usuário sobre salário, gastos e impostos.
    Retorna:
    - salario_mensal: salário do usuário.
    - gastos_mensais: dicionário com os valores dos serviços.
    - impostos: dicionário com as taxas de impostos.
    - periodo_meses: número de meses para cálculo.
    """
    salario_mensal = float(input("Informe sua média salarial mensal (em reais): "))
    gastos_mensais = {}
    servicos = ["Energia", "Água", "Wi-Fi", "Compras Domésticas"]
    for servico in servicos:
        valor = float(input(f"Informe o valor médio mensal para {servico} (em reais): "))
        gastos_mensais[servico] = valor
    impostos = {}
    impostos_nome = ["ICMS", "ISS"]
    for imposto in impostos_nome:
        taxa = float(input(f"Informe a taxa de {imposto} (em %): "))
        impostos[imposto] = taxa
    periodo_meses = int(input("Informe o número de meses para o cálculo: "))
    return salario_mensal, gastos_mensais, impostos, periodo_meses

def obter_icms_em_tempo_real():
    """
    Simula a obtenção da taxa de ICMS em tempo real.
    Retorna:
    - icms: a taxa de ICMS.
    """
    icms = 18  # Taxa de ICMS simulada
    print(f"Taxa de ICMS em tempo real: {icms}%")
    return icms

def exibir_explicacoes(icms):
    """
    Exibe explicações sobre os impostos ICMS e ISS.
    Args:
    - icms: a taxa de ICMS.
    """
    print("\n-- Explicações sobre os impostos e taxas --")
    print(f"ICMS: Imposto sobre Circulação de Mercadorias e Serviços. Taxa atual: {icms}%.")
    print("ISS: Imposto Sobre Serviços. A taxa varia dependendo do município e do serviço prestado.\n")

# --- Funções para o Projeto de Rede de Comunicação (com LU) ---

def calcular_grau(matriz):
    """
    Calcula o grau de cada nó na rede.
    Args:
    - matriz: matriz de adjacência da rede.

    Retorna:
    - grau: lista com o grau de cada nó.
    """
    return np.sum(matriz, axis=1)

def exibir_matriz_adjacencia(matriz):
    """
    Exibe a matriz de adjacência da rede.
    Args:
    - matriz: matriz de adjacência da rede.
    """
    print("Matriz de Adjacência (aqui rolam os contatos secretos!):")
    print(matriz)

def decomposicao_LU(matriz):
    """
    Realiza a decomposição LU de uma matriz.
    Args:
    - matriz: matriz a ser decomposta.

    Retorna:
    - P, L, U: matrizes de permutação, lower e upper resultantes da decomposição.
    """
    P, L, U = lu(matriz)
    print("\nMatriz de Permutação P (o plano secreto de movimentação dos nós):")
    print(P)
    print("\nMatriz L (Lower - quem está por baixo da hierarquia):")
    print(L)
    print("\nMatriz U (Upper - quem está lá no topo da cadeia alimentar):")
    print(U)
    return P, L, U

def desenhar_grafo(matriz):
    """
    Desenha o grafo a partir da matriz de adjacência.
    Args:
    - matriz: matriz de adjacência da rede.
    """
    G = nx.from_numpy_array(matriz)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700)
    plt.title('Rede de Comunicação - O Show das Conexões!')
    plt.show()

def analisar_conexoes(matriz):
    """
    Analisa as conexões da rede e calcula o grau de cada nó.
    Args:
    - matriz: matriz de adjacência da rede.

    Retorna:
    - graus: grau de cada nó.
    """
    graus = calcular_grau(matriz)
    print("\nGrau de Conexão dos Nós (quem está bombando nas conexões?):")
    for i, grau in enumerate(graus):
        print(f"Nó {i}: {grau} conexões (ele é popular, hein?)")
    return graus

# --- Função Principal com Menu ---

def exibir_menu():
    """
    Exibe o menu principal para o usuário escolher o que deseja fazer.
    """
    print("\n------- Menu Principal -------")
    print("------ mescla contidas -------")
    print("1. Calcular gastos")
    print("2. Ver ICMS em tempo real")
    print("3. Explicações sobre ICMS e ISS")
    print("4. Análise de Conexões (rede de comunicação)")
    print("5. Sair")

def main():
    """
    Função principal que executa o programa com o menu de opções.
    """
    icms = obter_icms_em_tempo_real()
    
    while True:
        exibir_menu()
        opcao = int(input("\nEscolha uma opção: "))
        
        if opcao == 1:
            salario_mensal, gastos_mensais, impostos, periodo_meses = coletar_dados_usuario()
            gastos_totais, total_periodo, gastos_totais_array, total_periodo_array = calcular_gastos(gastos_mensais, periodo_meses, impostos)
            print("\nGastos Totais por Serviço:")
            for servico, valor in gastos_totais.items():
                print(f"{servico}: R${valor:.2f}")
            print("\nGastos Totais para o Período:")
            for servico, valor in total_periodo.items():
                print(f"{servico}: R${valor:.2f}")
            plotar_gastos(total_periodo, gastos_mensais, salario_mensal, icms)
        
        elif opcao == 2:
            print(f"\nTaxa de ICMS em tempo real: {icms}%")
        
        elif opcao == 3:
            exibir_explicacoes(icms)
        
        elif opcao == 4:
            n = 5
            M = np.random.randint(0, 2, size=(n, n))
            np.fill_diagonal(M, 0)
            exibir_matriz_adjacencia(M)
            graus = analisar_conexoes(M)
            P, L, U = decomposicao_LU(M)
            desenhar_grafo(M)
        
        elif opcao == 5:
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executando o programa
main()
