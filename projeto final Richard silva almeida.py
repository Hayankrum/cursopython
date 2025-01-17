import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from random import randint

# Função para calcular os gastos
def calcular_gastos(gastos_mensais, periodo_meses, impostos):
    impostos_totais = sum(impostos.values()) / 100
    
    gastos_totais = {servico: (valor + valor * impostos_totais) for servico, valor in gastos_mensais.items()}
    total_periodo = {servico: valor * periodo_meses for servico, valor in gastos_totais.items()}
    
    # Usando NumPy para operações vetoriais rápidas
    gastos_totais_array = np.array(list(gastos_totais.values()))
    total_periodo_array = np.array(list(total_periodo.values()))
    
    return gastos_totais, total_periodo, gastos_totais_array, total_periodo_array

# Função para visualização
def plotar_gastos(gastos_periodo, gastos_iniciais, salario_mensal, icms):
    servicos = list(gastos_periodo.keys())
    valores_iniciais = list(gastos_iniciais.values())
    valores_calculados = list(gastos_periodo.values())
    
    total_gastos = np.sum(valores_calculados)
    sobrou = salario_mensal - total_gastos

    # Gráfico de barras com valores originais e calculados
    plt.figure(figsize=(14, 6))
    bar_width = 0.35
    index = range(len(servicos))
    
    # Barras para valores originais e calculados
    barras_iniciais = plt.bar(index, valores_iniciais, bar_width, label="Valor Original", color="skyblue")
    barras_calculados = plt.bar([i + bar_width for i in index], valores_calculados, bar_width, label="Valor com ICMS", color="lightcoral")
    
    # Adicionar os valores nas barras
    for i, valor in enumerate(valores_iniciais):
        plt.text(i - 0.15, valor + 0.02, f"R${valor:.2f}", ha='center', va='bottom', fontsize=10, color="blue")
    
    for i, valor in enumerate(valores_calculados):
        plt.text(i + bar_width - 0.15, valor + 0.02, f"R${valor:.2f}", ha='center', va='bottom', fontsize=10, color="red")
    
    plt.title(f"Gastos por Serviço (ICMS: {icms}%)")
    plt.xlabel("Serviços")
    plt.ylabel("Valor em Reais")
    plt.xticks([i + bar_width / 2 for i in index], servicos)
    plt.legend()

    # Exibição do gráfico de barras
    plt.tight_layout()
    plt.show()

    # Gráfico de pizza
    plt.figure(figsize=(8, 8))
    all_valores = valores_iniciais + valores_calculados
    all_servicos = servicos + [f"{servico} - com ICMS" for servico in servicos]
    
    plt.pie(all_valores, labels=all_servicos, autopct="%1.1f%%", startangle=140, colors=["skyblue", "lightcoral"]*len(servicos))
    plt.title(f"Distribuição de Gastos (ICMS: {icms}%)")
    plt.show()

    # Exibição do valor restante
    print(f"\nTotal de Gastos: R${total_gastos:.2f}")
    print(f"Valor sobrando do salário: R${sobrou:.2f}")
    print(f"Valor total de ICMS aplicado: R${total_gastos * (icms / 100):.2f}")

# Função para coletar dados do usuário
def coletar_dados_usuario():
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

# Função para obter a cotação do ICMS em tempo real
def obter_icms_em_tempo_real():
    # Aqui podemos usar uma API ou consulta para obter valores atualizados de ICMS
    icms = 18  # Simulando uma taxa fixa de ICMS (isso pode ser dinâmico)
    print(f"Taxa de ICMS em tempo real: {icms}%")
    return icms

# Função para exibir explicações sobre os impostos
def exibir_explicacoes(icms):
    print("\n-- Explicações sobre os impostos e taxas --")
    print(f"ICMS: Imposto sobre Circulação de Mercadorias e Serviços. Taxa atual: {icms}%.")
    print("ISS: Imposto Sobre Serviços. A taxa varia dependendo do município e do serviço prestado.\n")

# Função para exibir o menu
def exibir_menu():
    print("\n-- Menu Principal --")
    print("1. Calcular gastos")
    print("2. Ver ICMS em tempo real")
    print("3. Explicações sobre ICMS e ISS")
    print("4. Sair")

# Função principal
def main():
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
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executando o programa
main()
