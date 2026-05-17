import streamlit as st
import requests
from fpdf import FPDF
import io

# Configuração inicial da página web
st.set_page_config(page_title="OrcaFácil - Eletricista", page_icon="⚡", layout="wide")

st.title("⚡ OrcaFácil - Gerador de Orçamentos Profissionais")
st.markdown("---")

# --- FUNÇÃO PARA GERAR O PDF EM MEMÓRIA ---
def gerar_pdf_orcamento(cliente, endereco, cidade, servico, total_mo, materiais, total_geral):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Cabeçalho do Orçamento
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="ORÇAMENTO DE SERVIÇOS ELÉTRICOS", ln=True, align="C")
    pdf.ln(10)
    
    # Dados do Cliente
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 8, txt="Dados do Cliente e Obra:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 6, txt=f"Nome: {cliente}", ln=True)
    pdf.cell(200, 6, txt=f"Endereço: {endereco}", ln=True)
    pdf.cell(200, 6, txt=f"Cidade/UF: {cidade}", ln=True)
    pdf.ln(8)
    
    # Descrição do Serviço
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 8, txt="Descrição dos Serviços (Mão de Obra):", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, txt=servico)
    pdf.cell(200, 6, txt=f"Subtotal Mão de Obra: R$ {total_mo:.2f}", ln=True, align="R")
    pdf.ln(8)
    
    # Lista de Materiais
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 8, txt="Materiais Relacionados:", ln=True)
    
    if materiais:
        pdf.set_font("Arial", style="B", size=10)
        # Cabeçalho da tabela de materiais
        pdf.cell(90, 6, "Material", border=1)
        pdf.cell(20, 6, "Qtd", border=1, align="C")
        pdf.cell(40, 6, "Valor Un. (R$)", border=1, align="R")
        pdf.cell(40, 6, "Total (R$)", border=1, align="R", ln=True)
        
        pdf.set_font("Arial", size=10)
        for mat in materiais:
            pdf.cell(90, 6, str(mat["Material"]), border=1)
            pdf.cell(20, 6, str(mat["Qtd"]), border=1, align="C")
            pdf.cell(40, 6, f"{mat['Valor Unitário (R$)']:.2f}", border=1, align="R")
            pdf.cell(40, 6, f"{mat['Total (R$)']:.2f}", border=1, align="R", ln=True)
    else:
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 6, txt="Nenhum material adicionado.", ln=True)
    
    pdf.ln(10)
    
    # Fechamento com Valor Total Geral
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt=f"VALOR TOTAL GERAL: R$ {total_geral:.2f}", border=1, ln=True, align="C")
    
    # Retorna o PDF como bytes para o Streamlit fazer o download
    # Converte o bytearray do fpdf2 para bytes puros que o Streamlit aceita
    return bytes(pdf.output())


# 1. DADOS DO CLIENTE & ENDEREÇO VIA API VIA CEP
st.header("👥 Dados do Cliente e Obra")
col1, col2 = st.columns([1, 2])

with col1:
    cep = st.text_input("CEP da Obra", max_chars=8, help="Digite apenas os 8 números do CEP")
    logradouro, bairro, cidade, uf = "", "", "", ""

    if len(cep) == 8 and cep.isdigit():
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
            if response.status_code == 200:
                dados = response.json()
                if "erro" not in dados:
                    logradouro = dados.get("logradouro", "")
                    bairro = dados.get("bairro", "")
                    cidade = dados.get("localidade", "")
                    uf = dados.get("uf", "")
                else:
                    st.error("CEP não encontrado.")
        except requests.RequestException:
            st.error("Erro de conexão com o serviço de CEP.")

with col2:
    nome_cliente = st.text_input("Nome do Cliente")
    endereco_completo = st.text_input("Endereço Completo", value=f"{logradouro}, {bairro}" if logradouro else "")
    cidade_uf = st.text_input("Cidade / UF", value=f"{cidade} - {uf}" if cidade else "")

st.markdown("---")

# 2. ESCOPO DO SERVIÇO E MÃO DE OBRA
st.header("🛠️ Detalhes do Serviço")
col_serv1, col_serv2, col_serv3 = st.columns([2, 1, 1])

with col_serv1:
    desc_servico = st.text_area("Descrição do Serviço Elétrico", placeholder="Ex: Instalação de disjuntores.")
with col_serv2:
    valor_hora = st.number_input("Valor da Hora (R$)", min_value=0.0, value=60.0, step=5.0)
with col_serv3:
    horas_estimadas = st.number_input("Horas Estimadas", min_value=1, value=4, step=1)

total_servico = valor_hora * horas_estimadas
st.subheader(f"Total Mão de Obra: R$ {total_servico:.2f}")

st.markdown("---")

# 3. LISTA DE MATERIAIS (Gerenciamento de Estado Dinâmico e Edição Automatizada)
st.header("📦 Materiais Utilizados")

if "materiais" not in st.session_state:
    st.session_state.materiais = []

# Formulário para adicionar um novo material
with st.form("form_material", clear_on_submit=True):
    col_mat1, col_mat2, col_mat3 = st.columns([2, 1, 1])
    with col_mat1:
        nome_mat = st.text_input("Nome do Material")
    with col_mat2:
        qtd_mat = st.number_input("Quantidade", min_value=1, value=1, step=1)
    with col_mat3:
        valor_un_mat = st.number_input("Valor Unitário (R$)", min_value=0.0, value=0.0, step=1.0)
    
    if st.form_submit_button("➕ Adicionar Material") and nome_mat:
        st.session_state.materiais.append({
            "Material": nome_mat,
            "Qtd": int(qtd_mat),
            "Valor Unitário (R$)": float(valor_un_mat),
            "Total (R$)": float(qtd_mat * valor_un_mat)
        })

total_materiais = 0.0
if st.session_state.materiais:
    st.markdown("💡 *Dica: Dê dois cliques em uma célula para **editar**. Selecione a linha e aperte 'Delete' para **apagar**.*")
    
    # Exibe a tabela interativa e captura as modificações diretamente
    materiais_editados = st.data_editor(
        st.session_state.materiais,
        num_rows="dynamic",
        column_config={
            "Material": st.column_config.TextColumn("Material", required=True),
            "Qtd": st.column_config.NumberColumn("Qtd", min_value=1, step=1, required=True),
            "Valor Unitário (R$)": st.column_config.NumberColumn("Valor Unitário (R$)", min_value=0.0, format="R$ %.2f", required=True),
            "Total (R$)": st.column_config.NumberColumn("Total (R$)", format="R$ %.2f", disabled=True)  # Bloqueado para o sistema calcular
        },
        key="editor_materiais"
    )
    
    # 🔄 AUTOMATIZAÇÃO DA EDIÇÃO: reconstrói a lista recalculando os totais de cada linha
    lista_limpa = []
    for item in materiais_editados:
        if item and item.get("Material"):  # Garante que a linha não está vazia ou deletada
            try:
                # Força o recálculo automático com base no que o usuário alterou na tela
                item["Qtd"] = int(item.get("Qtd", 1))
                item["Valor Unitário (R$)"] = float(item.get("Valor Unitário (R$)", 0.0))
                item["Total (R$)"] = item["Qtd"] * item["Valor Unitário (R$)"]
                lista_limpa.append(item)
            except (ValueError, TypeError):
                continue
    
    # Se a lista mudou após a edição ou deleção, atualiza o estado e força o recálculo geral
    if lista_limpa != st.session_state.materiais:
        st.session_state.materiais = lista_limpa
        st.channels # Truque sutil para disparar o re-render
        st.rerun()

    # Calcula o total acumulado dos materiais
    total_materiais = sum(item["Total (R$)"] for item in st.session_state.materiais)
    
    if st.button("🗑️ Limpar Todos os Materiais"):
        st.session_state.materiais = []
        st.rerun()
else:
    st.info("Nenhum material adicionado ainda.")

# 4. FECHAMENTO DO VALOR TOTAL E DOWNLOAD DO PDF
st.header("💰 Resumo e Emissão do Orçamento")
valor_total_geral = total_servico + total_materiais

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="Valor Total Geral", value=f"R$ {valor_total_geral:.2f}")

with col_res2:
    st.write("")
    # Gera os bytes do PDF chamando nossa função interna
    pdf_data = gerar_pdf_orcamento(
        nome_cliente, endereco_completo, cidade_uf, 
        desc_servico, total_servico, st.session_state.materiais, valor_total_geral
    )
    
    # Botão nativo do Streamlit para baixar o arquivo gerado
    st.download_button(
        label="📥 Baixar Orçamento em PDF",
        data=pdf_data,
        file_name=f"orcamento_{nome_cliente.replace(' ', '_').lower()}.pdf",
        mime="application/pdf",
        type="primary"
    )