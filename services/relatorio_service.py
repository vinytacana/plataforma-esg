# services/relatorio_service.py
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import os

# --- Configuração Visual ---
COR_PRIMARIA = (88, 64, 51)    # Marrom
COR_SECUNDARIA = (46, 125, 50) # Verde
COR_CINZA = (128, 128, 128)

class PDFTemplate(FPDF):
    def header(self):
        # Logo
        if os.path.exists("static/casca2.png"):
            self.image("static/casca2.png", 10, 8, 25)
        
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(80)
        self.cell(30, 10, 'Plataforma Casca ESG - Enterprise', 0, 0, 'C')
        self.ln(20)
        
        # Linha Verde
        self.set_draw_color(*COR_SECUNDARIA)
        self.set_line_width(1)
        self.line(10, 25, 200, 25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(*COR_CINZA)
        self.cell(0, 10, f'Página {self.page_no()} - Documento Auditado via Blockchain', 0, 0, 'C')

# --- Funções Auxiliares de Gráfico ---
def gerar_chart_pizza(s1, s2, s3):
    filename = "temp_pie.png"
    sizes = [s1, s2, s3]
    if sum(sizes) == 0: sizes = [1, 1, 1] # Evita erro se vazio
    
    plt.figure(figsize=(5, 4))
    plt.pie(sizes, labels=['Escopo 1', 'Escopo 2', 'Escopo 3'], 
            colors=['#C62828', '#FF9800', '#4DB6AC'], autopct='%1.1f%%')
    plt.title('Emissões por Escopo')
    plt.savefig(filename)
    plt.close()
    return filename

def gerar_chart_projecao(total_atual):
    """Gera um gráfico de linha simulando a meta de redução"""
    filename = "temp_line.png"
    anos = ['2025', '2026', '2027', '2028', '2029', '2030']
    # Simulação: Redução de 5% ao ano
    metas = [total_atual * (0.95 ** i) for i in range(6)]
    
    plt.figure(figsize=(6, 3))
    plt.plot(anos, metas, marker='o', color='green', linestyle='--')
    plt.title('Trajetória de Descarbonização (Meta: -5% a.a.)')
    plt.grid(True, alpha=0.3)
    plt.ylabel('tCO2e')
    plt.savefig(filename)
    plt.close()
    return filename

# --- 1. RELATÓRIO TÉCNICO (GHG PROTOCOL) ---
def gerar_pdf_ghg(lista_emissoes, filename="ghg_protocol_2024.pdf"):
    pdf = PDFTemplate()
    pdf.add_page()
    
    # Dados
    total = sum(e.resultado_total for e in lista_emissoes) / 1000 # em toneladas
    s1 = sum(e.resultado_escopo1 for e in lista_emissoes)
    s2 = sum(e.resultado_escopo2 for e in lista_emissoes)
    s3 = sum(e.resultado_escopo3 for e in lista_emissoes)
    
    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Inventário de Emissões - Padrão GHG Protocol", 0, 1, 'C')
    pdf.ln(5)
    
    # Resumo
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 7, f"Este relatório consolida os dados de emissões diretas e indiretas conforme a norma ISO 14064. O total inventariado para o período é de {total:.2f} tCO2e.")
    pdf.ln(5)
    
    # Gráfico
    img = gerar_chart_pizza(s1, s2, s3)
    pdf.image(img, x=50, w=110)
    os.remove(img)
    
    # Tabela Técnica
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 10, "Escopo", 1, 0, 'L', fill=True)
    pdf.cell(90, 10, "Emissão (kgCO2e)", 1, 1, 'R', fill=True)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, "Escopo 1 (Combustão Estacionária/Móvel)", 1, 0)
    pdf.cell(90, 10, f"{s1:.2f}", 1, 1, 'R')
    pdf.cell(100, 10, "Escopo 2 (Energia Elétrica - Grid)", 1, 0)
    pdf.cell(90, 10, f"{s2:.2f}", 1, 1, 'R')
    pdf.cell(100, 10, "Escopo 3 (Logística e Viagens)", 1, 0)
    pdf.cell(90, 10, f"{s3:.2f}", 1, 1, 'R')
    
    pdf.output(filename)
    return filename

# --- 2. PLANO ESTRATÉGICO (DESCARBONIZAÇÃO) ---
def gerar_plano_descarbonizacao(lista_emissoes, filename="plano_descarbonizacao.pdf"):
    pdf = PDFTemplate()
    pdf.add_page()
    
    total_kg = sum(e.resultado_total for e in lista_emissoes)
    total_ton = total_kg / 1000
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Plano Estratégico de Descarbonização 2025-2030", 0, 1, 'C')
    pdf.ln(10)
    
    # Gráfico de Projeção
    img_proj = gerar_chart_projecao(total_ton)
    pdf.image(img_proj, x=20, w=170)
    os.remove(img_proj)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Metas Estabelecidas:", 0, 1)
    
    pdf.set_font("Arial", size=12)
    metas = [
        "1. Redução de 5% ao ano nas emissões de Escopo 1 (Substituição de Frota).",
        "2. Migração para 100% de Energia Renovável (I-REC) até 2026.",
        "3. Implementação de Política de 'Aterro Zero' para resíduos até 2028.",
        "4. Compensação das emissões residuais via plantio de árvores nativas."
    ]
    
    for meta in metas:
        pdf.cell(0, 8, meta, 0, 1)
        
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 6, "Nota: Este plano é baseado na baseline de emissões atuais. O cumprimento das metas depende da adesão aos protocolos operacionais sugeridos pela Casca.")

    pdf.output(filename)
    return filename

# --- 3. DADOS BRUTOS (CSV) ---
def gerar_csv_auditoria(lista_emissoes, lista_residuos, filename="auditoria_compliance.csv"):
    dados = []
    
    # Consolidando tudo em uma tabela auditável
    for i, item in enumerate(lista_emissoes):
        dados.append({
            "ID_Registro": f"GHG-{item.id}",
            "Data": item.data_calculo,
            "Categoria": "Emissao GEE",
            "Detalhe": f"Escopo 1: {item.resultado_escopo1:.1f} | Energia: {item.consumo_eletricidade_kwh}",
            "Impacto_Total_kgCO2e": item.resultado_total,
            "Quimica_CO2": item.total_co2,
            "Quimica_CH4": item.total_ch4,
            "Status": "Calculado"
        })
        
    for item in lista_residuos:
        dados.append({
            "ID_Registro": f"RES-{item.id}",
            "Data": item.data_calculo,
            "Categoria": "Residuos",
            "Detalhe": f"{item.tipo} enviado para {item.destino}",
            "Impacto_Total_kgCO2e": item.emissao_calculada,
            "Quimica_CO2": 0,
            "Quimica_CH4": item.emissao_calculada if item.destino == 'aterro' else 0,
            "Status": "Rastreado"
        })

    df = pd.DataFrame(dados)
    df.to_csv(filename, index=False, sep=';') # Ponto e vírgula para abrir fácil no Excel BR
    return filename