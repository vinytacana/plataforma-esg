# services/relatorio_service.py
import pandas as pd
from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Relatório de Impacto ESG & Emissões', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def gerar_csv_consolidado(lista_emissoes, lista_energia, filename="relatorio_esg.csv"):
    """
    Gera um CSV combinando dados de Emissões e Energia para análise de dados.
    """
    dados = []
    
    # Processa Emissões
    for item in lista_emissoes:
        dados.append({
            "Tipo": "Inventário GEE",
            "ID": item.id,
            "Data": item.data_calculo,
            "Detalhe 1": f"Gasolina: {item.consumo_gasolina_l}L",
            "Detalhe 2": f"Diesel: {item.consumo_diesel_l}L",
            "Resultado Principal": f"{item.resultado_total:.2f} kgCO2e",
            "Nota Científica": "Metodologia GHG Protocol (Escopos 1, 2, 3)"
        })

    # Processa Energia
    for item in lista_energia:
        dados.append({
            "Tipo": "Eficiência Energética",
            "ID": item.id,
            "Data": item.data_calculo,
            "Detalhe 1": f"Total: {item.consumo_total} kWh",
            "Detalhe 2": f"Renovável: {item.percentual_renovavel:.1f}%",
            "Resultado Principal": f"{item.emissoes_totais_tco2e:.4f} tCO2e",
            "Nota Científica": "Cálculo Vetorial (GWP: CO2, CH4, N2O)"
        })

    df = pd.DataFrame(dados)
    df.to_csv(filename, index=False)
    return filename

def gerar_pdf_certificado(lista_emissoes, lista_energia, filename="certificado_esg.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Resumo Executivo
    total_emissoes_kg = sum(e.resultado_total for e in lista_emissoes)
    total_energia_tco2e = sum(e.emissoes_totais_tco2e for e in lista_energia)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Resumo Executivo", 0, 1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Este documento certifica o processamento dos dados ambientais da organização. "
                          f"Foram analisados {len(lista_emissoes)} registros de emissões diretas e "
                          f"{len(lista_energia)} registros de matriz energética.")
    pdf.ln(5)
    
    # Tabela de Resultados
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, f"Total Inventariado (GEE): {total_emissoes_kg:.2f} kgCO2e", 0, 1, fill=True)
    pdf.cell(0, 10, f"Pegada de Carbono (Energia): {total_energia_tco2e:.4f} tCO2e", 0, 1, fill=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Declaração Metodológica:", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, 
        "Os cálculos utilizam vetores estequiométricos baseados no IPCC AR6 e fatores do Sistema Interligado Nacional (SIN). "
        "Considera-se o Potencial de Aquecimento Global (GWP) para CO2, CH4 e N2O."
    )
    
    pdf.output(filename)
    return filename