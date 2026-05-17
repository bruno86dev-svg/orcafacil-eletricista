# Gerador de Orçamentos Profissionais - OrcaFácil ⚡

🔗 **Link da Aplicação Online:** https://orcafacil-eletricista.streamlit.app

## 📌 Descrição do Problema
Microempreendedores, como eletricistas autônomos, perdem tempo e profissionalismo ao enviar orçamentos manuais, muitas vezes desorganizados e sujeitos a erros.

## 💡 Solução
Aplicação web que automatiza o cálculo de materiais e mão de obra, gerando orçamentos organizados e profissionais de forma rápida.

## 👥 Público-alvo
Eletricistas autônomos e pequenos prestadores de serviço.

## ⚙️ Funcionalidades
- **Cadastro de Cliente Automatizado:** Busca e preenchimento de endereço em tempo real consumindo a API pública do ViaCEP.
- **Gerenciamento Dinâmico de Materiais:** Interface com tabela interativa (`st.data_editor`) que permite adicionar, editar quantidades/valores e remover itens com recálculo instantâneo.
- **Cálculo Automático:** Totalização precisa de mão de obra, materiais e valor geral do orçamento baseado em regras de negócio puras.
- **Exportação Profissional:** Geração de arquivo em formato PDF estruturado pronto para envio ao cliente.

## 🛠️ Tecnologias
- Python 3
- Streamlit (Interface Web)
- FPDF2 (Geração de PDFs em memória)
- Pytest (Testes automatizados)
- Requests (Consumo de APIs REST)

## ▶️ Como executar localmente
1. Certifique-se de ter as dependências instaladas através do ambiente virtual:
   ```bash
   pip install -r requirements.txt
