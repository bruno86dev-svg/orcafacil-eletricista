import streamlit as st
from fpdf import FPDF
from src.orcamento import buscar_cep, Orcamento

# Configuração inicial da página web
st.set_page_config(page_title="OrcaFácil - Eletricista", page_icon="⚡", layout="wide")

st.title("⚡ OrcaFácil - Gerador de Orçamentos Profissionais")
st.markdown("---")

# --- FUNÇÃO PARA GERAR O PDF EM MEMÓRIA ---
def gerar_pdf_orcamento(orcamento_obj, endereco, cidade_uf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Cabeçalho
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="ORÇAMENTO DE SERVIÇOS ELÉTRICOS", ln=True, align="C")
    pdf.ln(10)
    
    # Dados do Cliente
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 8, txt="Dados do Cliente e Obra:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 6, txt=f"Nome: {orcamento_obj.cliente}", ln=True)
    pdf.cell(200, 6, txt=f"Endereço: {endereco}", ln=True)
    pdf.cell(200, 6, txt=f"Cidade/UF: {cidade_uf}", ln=True)
    pdf.ln(8)
    
    # Descrição do Serviço
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 8, txt="Descrição dos Serviços (Mão de Obra):", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, txt=orcamento_obj.servico)
    pdf.cell(200, 6, txt=f"Subtotal Mão de Obra: R$ {orcamento_obj.valor_mao_de_obra:.2f}", ln=True, align="R")
    pdf.ln(8)
    
    # Tabela de Materiais
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 8, txt="Materiais Relacionados:", ln=True)
    
    if orcamento_obj.materiais:
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(90, 6, "Material", border=1)
        pdf.cell(20, 6, "Qtd", border=1, align="C")
        pdf.cell(40, 6, "Valor Un. (R$)", border=1, align="R")
        pdf.cell(40, 6, "Total (R$)", border=1, align="R", ln=True)
        
        pdf.set_font("Arial", size=10)
        for mat in orcamento_obj.materiais:
            total_item = mat["quantidade"] * mat["preco_unitario"]
            pdf.cell(90, 6, str(mat["nome"]), border=1)
            pdf.cell(20, 6, str(mat["quantidade"]), border=1, align="C")
            pdf.cell(40, 6, f"{mat['preco_unitario']:.2f}", border=1, align="R")
            pdf.cell(40, 6, f"{total_item:.2f}", border=1, align="R", ln=True)
    else:
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 6, txt="Nenhum material adicionado.", ln=True)
    
    pdf.ln(10)
    
    # Fechamento
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt=f"VALOR TOTAL GERAL: R$ {orcamento_obj.calcular_total():.2f}", border=1, ln=True, align="C")
    
    return bytes(pdf.output())


# 1. DADOS DO CLIENTE & ENDEREÇO USANDO SUA FUNÇÃO BUSCAR_CEP
st.header("👥 Dados do Cliente e Obra")
col1, col2 = st.columns([1, 2])

with col1:
    cep = st.text_input("CEP da Obra", max_chars=8, help="Digite apenas os 8 números do CEP")
    logradouro, bairro, cidade, uf = "", "", "", ""

    if len(cep) == 8 and cep.isdigit():
        dados_endereco = buscar_cep(cep)
        if dados_endereco:
            logradouro = dados_endereco.get("logradouro", "")
            bairro = dados_endereco.get("bairro", "")
            cidade = dados_endereco.get("localidade", "")
            uf = dados_endereco.get("uf", "")

with col2:
    nome_cliente = st.text_input("Nome do Cliente", value="Cliente Padrão" if not cep else "")
    endereco_completo = st.text_input("Endereço Completo", value=f"{logradouro}, {bairro}" if logradouro else "")
    cidade_uf = st.text_input("Cidade / UF", value=f"{cidade} - {uf}" if cidade else "")

st.markdown("---")

# 2. ESCOPO DO SERVIÇO E MÃO DE OBRA
st.header("🛠️ Detalhes do Serviço")
col_serv1, col_serv2, col_serv3 = st.columns([2, 1, 1])

with col_serv1:
    desc_servico = st.text_area("Descrição do Serviço Elétrico", value="Instalação Elétrica Geral")
with col_serv2:
    valor_hora = st.number_input("Valor da Hora (R$)", min_value=0.0, value=60.0, step=5.0)
with col_serv3:
    horas_estimadas = st.number_input("Horas Estimadas", min_value=1, value=4, step=1)

total_mo = valor_hora * horas_estimadas
st.subheader(f"Total Mão de Obra: R$ {total_mo:.2f}")

st.markdown("---")

# 3. LISTA DE MATERIAIS USANDO DATA_EDITOR
st.header("📦 Materiais Utilizados")

if "lista_para_editor" not in st.session_state:
    st.session_state.lista_para_editor = []

with st.form("form_material", clear_on_submit=True):
    col_mat1, col_mat2, col_mat3 = st.columns([2, 1, 1])
    with col_mat1:
        nome_mat = st.text_input("Nome do Material")
    with col_mat2:
        qtd_mat = st.number_input("Quantidade", min_value=1, value=1, step=1)
    with col_mat3:
        valor_un_mat = st.number_input("Valor Unitário (R$)", min_value=0.0, value=0.0, step=1.0)
    
    if st.form_submit_button("➕ Adicionar Material") and nome_mat:
        st.session_state.lista_para_editor.append({
            "Material": nome_mat,
            "Qtd": int(qtd_mat),
            "Valor Unitário (R$)": float(valor_un_mat),
            "Total (R$)": float(qtd_mat * valor_un_mat)
        })

if st.session_state.lista_para_editor:
    st.markdown("💡 *Dica: Dois cliques para **editar**. Selecione a linha e aprete 'Delete' para **apagar**.*")
    
    materiais_editados = st.data_editor(
        st.session_state.lista_para_editor,
        num_rows="dynamic",
        column_config={
            "Material": st.column_config.TextColumn("Material", required=True),
            "Qtd": st.column_config.NumberColumn("Qtd", min_value=1, step=1, required=True),
            "Valor Unitário (R$)": st.column_config.NumberColumn("Valor Unitário (R$)", min_value=0.0, format="R$ %.2f", required=True),
            "Total (R$)": st.column_config.NumberColumn("Total (R$)", format="R$ %.2f", disabled=True)
        },
        key="editor_materiais"
    )
    
    lista_limpa = []
    for item in materiais_editados:
        if item and item.get("Material"):
            item["Qtd"] = int(item.get("Qtd", 1))
            item["Valor Unitário (R$)"] = float(item.get("Valor Unitário (R$)", 0.0))
            item["Total (R$)"] = item["Qtd"] * item["Valor Unitário (R$)"]
            lista_limpa.append(item)
            
    if lista_limpa != st.session_state.lista_para_editor:
        st.session_state.lista_para_editor = lista_limpa
        st.rerun()

# --- MONTAGEM DO OBJETO DE ACORDO COM A SUA CLASSE ---
orcamento_final = Orcamento(nome_cliente, desc_servico)
orcamento_final.definir_mao_de_obra(total_mo)

for m in st.session_state.lista_para_editor:
    orcamento_final.adicionar_material(m["Material"], m["Qtd"], m["Valor Unitário (R$)"])

st.markdown("---")

# 4. FECHAMENTO USANDO MÉTODOS DA CLASSE
st.header("💰 Resumo e Emissão do Orçamento")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="Valor Total Geral", value=f"R$ {orcamento_final.calcular_total():.2f}")

with col_res2:
    st.write("")
    pdf_data = gerar_pdf_orcamento(orcamento_final, endereco_completo, cidade_uf)
    
    st.download_button(
        label="📥 Baixar Orçamento em PDF",
        data=pdf_data,
        file_name=f"orcamento_{nome_cliente.replace(' ', '_').lower()}.pdf",
        mime="application/pdf",
        type="primary"
    )