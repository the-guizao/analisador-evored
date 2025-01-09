import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Função para gerar gráficos e PDFs para cada aluno
def gerar_pdf_para_alunos(arquivo_excel,logo_path):
    # Lendo a planilha Excel com os dados
    dados = pd.read_excel(arquivo_excel)
    
    # Obter a lista de alunos únicos
    alunos_unicos = dados['Nome'].unique()
    
    for aluno in alunos_unicos:
        # Filtrar as linhas para o aluno atual
        dados_aluno = dados[dados['Nome'] == aluno]
        
        # Obter os títulos dos simulados e as notas gerais
        simulados = dados_aluno['Simulado'].values
        notas_gerais = dados_aluno['Nota Geral'].values
        
        # Obter as notas das competências (colunas 4 a 8)
        competencias = dados_aluno[['Competência 1', 'Competência 2', 'Competência 3', 'Competência 4', 'Competência 5']].values
        competencias_labels = ['Competência 1', 'Competência 2', 'Competência 3', 'Competência 4', 'Competência 5']
        
        # Criar gráfico de evolução das notas gerais
        plt.figure(figsize=(8, 4))
        plt.plot(range(1, len(simulados) + 1), notas_gerais, marker='o', linestyle='-', color='b')
        plt.title(f'Evolução das Notas Gerais - {aluno}')
        plt.xlabel('Simulados')
        plt.ylabel('Nota Geral')
        plt.xticks(ticks=range(1, len(simulados) + 1), labels=range(1, len(simulados) + 1))  # Usar números para os simulados
        plt.grid(True)
        
        # Salvar gráfico como imagem temporária
        plt.savefig(f'grafico_{aluno}.png')
        plt.close()

        # Gerar o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.image(logo_path, x=160, y=10, w=40)

        # Adicionar o título
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório de Notas - {aluno}", ln=True, align='C')
        
        # Adicionar o gráfico ao PDF
        pdf.image(f'grafico_{aluno}.png', x=10, y=30, w=180)
        
        # Adicionar tabela de notas ao PDF
        pdf.ln(120)  # Espaço antes da tabela
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Tabela de Notas e Competências:", ln=True, align='L')

        # Adicionar cabeçalho da tabela (Simulado na linha de cima)

        # Para cada simulado, escrever o título acima e as notas das competências abaixo
        for i in range(len(simulados)):
            # Mesclando linha com o título do simulado (simulando mesclagem)
            pdf.cell(190, 10, f'{simulados[i]}', 1)
            pdf.ln()
            pdf.cell(40, 10, 'Nota Geral', 1)  # Célula vazia para o primeiro "Simulado"
            pdf.cell(30, 10, 'Competência 1', 1)
            pdf.cell(30, 10, 'Competência 2', 1)
            pdf.cell(30, 10, 'Competência 3', 1)
            pdf.cell(30, 10, 'Competência 4', 1)
            pdf.cell(30, 10, 'Competência 5', 1)
            pdf.ln()
            pdf.cell(40, 10, f'{notas_gerais[i]}', 1)
            
            # Adicionando as competências abaixo do título do simulado
            for nota_comp in competencias[i]:
                pdf.cell(30, 10, str(nota_comp), 1)
            pdf.ln()
        for comp_idx, comp_label in enumerate(competencias_labels):
                comp_notas = competencias[:, comp_idx]
            
                # Criar gráfico de evolução das competências
                plt.figure(figsize=(8, 4))
                plt.plot(range(1, len(simulados) + 1), comp_notas, marker='o',  linestyle='-', color='g')
                plt.title(f'Evolução da {comp_label} - {aluno}')    
                plt.xlabel('Simulados') 
                plt.ylabel(f'Nota {comp_label}')    
                plt.xticks(ticks=range(1, len(simulados) + 1), labels=range(1,  len(simulados) + 1))  # Usar números para os simulados
                plt.grid(True)  

                # Salvar gráfico como imagem temporária
                plt.savefig(f'grafico_{comp_label}_{aluno}.png')
                plt.close()

                # Adicionar o gráfico de competência ao PDF
                pdf.add_page()  # Nova página para cada competência
                pdf.image(logo_path, x=160, y=10, w=40)  # Adicionar logo na nova página também
                pdf.image(f'grafico_{comp_label}_{aluno}.png', x=10, y=30, w=180)

        # Salvar o PDF para o aluno
        pdf.output(f'relatorio_{aluno}.pdf')
        print(f'Relatório gerado para {aluno}.')

# Exemplo de uso da função
gerar_pdf_para_alunos('dados.xlsx', 'logo.png')
