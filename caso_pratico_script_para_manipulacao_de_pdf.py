# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 15:41:08 2026

@author: aroberto
"""

from PyPDF2 import PdfReader, PdfWriter
import os

print(len("Analista de Dados com 9 anos de experiência na MIRA Angola. Actuei na implementação de processos técnicos, gestão de Call Center, limpeza, validação e tratamento de dados, além da criação de dashboards e reports. Participei em projectos como Finscope 2022, MIRA TV e NPS. Tenho conhecimentos em Python, Machine Learning e frequento a formação Inteligência Artificial."))

lista_de_pdfs = {
    'pdfs/pdf_exemplo.pdf':[0],
    'pdfs/pdf_exemplo2.pdf':[0,1,2],
    'pdfs/pdf_exemplo3.pdf':[2,5]
    }

class ManipuladorPdfs():
    
    def __init__(self, lista_de_pdfs, marca_de_agua, pdf_final):
        """
        Parameters
        ----------
        lista_de_pdfs : Dicionario
            Lista de todos os pdfs e as páginas a seleccionar para criar em
            novo ficheiro
        marca_de_agua : string
            texto com o endereço do pdf que usaremos como marca de água
        pdf_final : string
            texto com a localização e o nome do ficheiro final
        Returns
        -------
        None.

        """
        self.lista_de_pdfs = lista_de_pdfs
        self.marca_de_agua = marca_de_agua
        self.pdf_final = pdf_final
        self.pdf_readers = {}
        self.writer = None
    
    
    def carregar_pdfs(self):
        """
            Método responsável pelo carregamento dos pdfs e as suas respectivas páginas
            caso os mesmos existirem. Percorre as chaves de lista_de_pdfs e guarda em
            pdf_readers
        """
        for key in self.lista_de_pdfs.keys():
            
            try:
                reader = PdfReader(key)
                self.pdf_readers[key] = reader
            except Exception as e:
                print(f"Erro: {e}")

    def extrair_paginas(self):
        """
            Método que percorre a lista_de_pdfs e faz as estrações das páginas de cada ficheiro
            da lista caso os mesmos existirem. Caso não, um alerta de erro será mostrado.
        """
        self.writer = PdfWriter()
        
        for file, paginas in self.lista_de_pdfs.items():
            reader = self.pdf_readers[file]
            if isinstance(paginas, list) and all(type(x) is int for x in paginas):
                for indice in paginas:
                    
                    if indice < len(reader.pages):
                        pagina = reader.pages[indice]
                        self.writer.add_page(pagina)
                    else:
                        print(f"Erro ao extrair a página {indice} do ficheiro {file}")
            else:
                print(f"Existe um índice não númerico dentro de {paginas}")
                return
                    
    def aplicar_marca_agua(self):
        """
            Verifica se o pdf marca_de_agua existe. se existir, identifica a página que usaremos
            como marca de água e adicionar em cada página existente em writer. Por último,
            guardamos novamente en self.writer.
        """
        if not os.path.exists(self.marca_de_agua):
            print(f"O ficheiro {self.marca_de_agua} não existe")
            return
        elif self.marca_de_agua is None:
            print('O Caminho do ficheiro é invalido')
            return
        
        marca_agua = PdfReader(self.marca_de_agua)
        
        watermark_page = marca_agua.pages[0]
        
        pdf_writer = PdfWriter()
        
        for pagina in self.writer.pages:
            pagina.merge_page(watermark_page)
            pdf_writer.add_page(pagina)
            
        self.writer = pdf_writer
        
    def guardar_pdf(self):
        """
            Método que guarda o novo ficheiro com a marca de água adicionado em todas as páginas
            criado resultante da combinação dos ficheiros da lista_de_pdfs
        """
        if self.writer is None:
            print("O ficheiro está vazio.")
            return
        
        try:
            with open(self.pdf_final, "wb") as file:
                
                self.writer.write(file)

                print("O pdf foi criado com sucesso.")
            
        except Exception as e:
            print("Algo inexperado aconteceu durante a criação do pdf")
            print(e)
            
    def processar(self):
        """
            Método responsavel pelo processamento da classe. desde o carregamento dos pdfs até
            a criação do novo pdf com a marca de água em cada página.
        """
        self.carregar_pdfs()
        self.extrair_paginas()
        self.aplicar_marca_agua()
        self.guardar_pdf()


pdf_marca_agua = "pdfs/pdf_watermark.pdf"
pdf_final = "pdfs/pdf_final.pdf"

m = ManipuladorPdfs(lista_de_pdfs, pdf_marca_agua, pdf_final)

m.processar()
 