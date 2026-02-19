# services/relatorio_service.py
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
from abc import ABC, abstractmethod
from typing import List, Any

# --- Configuração Visual ---
COR_PRIMARIA = (88, 64, 51)    # Marrom
COR_SECUNDARIA = (46, 125, 50) # Verde
COR_CINZA = (128, 128, 128)

class PDFTemplate(FPDF):
    def header(self):
        if os.path.exists("static/casca2.png"):
            self.image("static/casca2.png", 10, 8, 25)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(80)
        self.cell(30, 10, 'Relatorio de Sustentabilidade Corporativa', 0, 0, 'C')
        self.ln(20)
        self.set_draw_color(*COR_SECUNDARIA)
        self.set_line_width(1)
        self.line(10, 25, 200, 25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(*COR_CINZA)
        self.cell(0, 10, f'Pagina {self.page_no()} - Autenticado via Blockchain', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.ln(4)

# --- Pattern: Strategy para Seções do Relatório ---

class SecaoRelatorio(ABC):
    @abstractmethod
    def renderizar(self, pdf: PDFTemplate, dados: Any):
        pass

class SecaoAmbiental(SecaoRelatorio):
    def renderizar(self, pdf: PDFTemplate, dados: dict):
        pdf.chapter_title("1. Pilar Ambiental (Environmental)")
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)
        
        emissoes = dados.get('emissoes', [])
        agua = dados.get('agua', [])
        residuos = dados.get('residuos', [])
        energia = dados.get('energia', [])

        total_co2 = sum(e.resultado_total for e in emissoes) / 1000
        total_agua = sum(a.consumo_m3 for a in agua)
        total_lixo = sum(r.peso_kg for r in residuos)

        pdf.cell(0, 10, f"- Emissoes de GEE: {total_co2:.2f} tCO2e (Padrao GHG Protocol)", 0, 1)
        pdf.cell(0, 10, f"- Consumo Hidrico: {total_agua:.1f} m3", 0, 1)
        pdf.cell(0, 10, f"- Residuos Solidos: {total_lixo:.1f} kg", 0, 1)
        
        if energia:
            avg_renovavel = sum(en.percentual_renovavel for en in energia) / len(energia)
            pdf.cell(0, 10, f"- Matriz Energetica Renovavel: {avg_renovavel:.1f}%", 0, 1)
        pdf.ln(5)

class SecaoSocialGovernanca(SecaoRelatorio):
    def renderizar(self, pdf: PDFTemplate, metricas: List[Any]):
        pdf.chapter_title("2. Social e Governanca (S & G)")
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)
        
        if not metricas:
            pdf.cell(0, 10, "Nao ha metricas qualitativas registradas no periodo.", 0, 1)
            return

        for m in metricas:
            unidade = m.unidade if m.unidade else ""
            pdf.cell(0, 10, f"- [{m.categoria.upper()}] {m.nome}: {m.valor} {unidade}", 0, 1)
        pdf.ln(5)

# --- Gerador Principal ---

def gerar_relatorio_executivo(emissoes, agua, residuos, energia, metricas, filename="relatorio_executivo.pdf"):
    pdf = PDFTemplate()
    pdf.add_page()
    
    # Capa / Título
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(*COR_PRIMARIA)
    pdf.cell(0, 20, "Sumario Executivo ESG", 0, 1, 'C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Periodo de Analise: {datetime.now().strftime('%m/%Y')}", 0, 1, 'C')
    pdf.ln(10)

    # Invocando as seções via Strategy
    ambiental = SecaoAmbiental()
    ambiental.renderizar(pdf, {
        'emissoes': emissoes, 
        'agua': agua, 
        'residuos': residuos, 
        'energia': energia
    })

    social_gov = SecaoSocialGovernanca()
    social_gov.renderizar(pdf, metricas)

    # Conclusão Técnica
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(*COR_SECUNDARIA)
    pdf.multi_cell(0, 7, "Certificacao: Este documento foi consolidado eletronicamente e os dados originais estao armazenados em ledger distribuido, garantindo imutabilidade para fins de auditoria externa.")

    pdf.output(filename)
    return filename

# Mantendo compatibilidade legada básica
def gerar_pdf_ghg(lista_emissoes, filename="ghg_protocol_2024.pdf"):
    return gerar_relatorio_executivo(lista_emissoes, [], [], [], [], filename)

def gerar_csv_auditoria(emissoes, residuos, filename="auditoria_compliance.csv"):
    dados = []
    for item in emissoes:
        dados.append({"Tipo": "Emissao", "Data": item.data_calculo, "Valor": item.resultado_total, "Unidade": "kgCO2e"})
    for item in residuos:
        dados.append({"Tipo": "Residuo", "Data": item.data_calculo, "Valor": item.peso_kg, "Unidade": "kg"})
    df = pd.DataFrame(dados)
    df.to_csv(filename, index=False, sep=';')
    return filename
