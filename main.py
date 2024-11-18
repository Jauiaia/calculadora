# Pacotes instalados antes da primeira execução: numpy pandas streamlit matplotlib
# Script de instalação:
#       pip install numpy pandas streamlit matplotlib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Calculadora de Notas", layout="wide")

# Cabeçalho com o nome do site
st.markdown("""
# 🧮 Calculadora de Notas dos Alunos da UDESC para aprovação
### *Site Oficial: [UDESC Notas para aprovação "Exames Finais"](https://www.udesc.br/arquivos/faed/id_cpmenu/1103/Notas_Exames_Finais_15641750742861_1103.pdf)*
Calcule a média das suas notas, descubra a nota mínima necessária no exame e baixe os resultados.
---
""")

# Dividindo a interface em colunas
col1, col2 = st.columns(2)

with col1:
    # Inserir o número de notas
    number = st.number_input("Quantas notas você quer inserir?", min_value=1, step=1)

    # Inserir as notas
    if number > 0:
        st.subheader("Insira suas notas")
        nota = []
        for ii in range(int(number)):
            nota.append(st.number_input(f"Digite a nota {ii + 1}:", min_value=0.0, step=0.1))

        nota = np.array(nota)

with col2:
    st.image("https://via.placeholder.com/400x300.png?text=Calculadora+de+Notas", caption="Ferramenta moderna e intuitiva!")

# Botão para calcular
if st.button("Calcular Média e Nota Mínima"):
    if len(nota) > 0:
        media_notas = nota.mean()
        st.markdown(f"### 🎓 *Média das Notas:* {media_notas:.2f}")

        # Cálculo da nota mínima necessária
        nota_minima = (5 - media_notas * 0.6) / 0.4
        if nota_minima > 10:
            mensagem = "*Nota mínima no exame: Não é possível alcançar a média 5.*"
        elif nota_minima < 0:
            mensagem = "*Nota mínima no exame: Você já alcançou a média 5!*"
        else:
            mensagem = f"### 📘 *Nota mínima no exame:* {nota_minima:.2f}"
        st.markdown(mensagem)

        # Adicionar gráfico de barras
        st.subheader("📊 Visualização das Notas")
        fig, ax = plt.subplots()
        ax.bar(range(1, len(nota) + 1), nota, color="skyblue")
        ax.axhline(y=media_notas, color='red', linestyle='--', label='Média')
        ax.set_xlabel("Provas")
        ax.set_ylabel("Notas")
        ax.set_title("Distribuição das Notas")
        ax.legend()
        st.pyplot(fig)

        # Botão para download dos resultados
        st.subheader("📥 Baixar Resultados")
        # Criar DataFrame com as informações
        df = pd.DataFrame({
            "Notas": nota,
            "Média": [media_notas] + [""] * (len(nota) - 1),
            "Nota Mínima Exame": [nota_minima] + [""] * (len(nota) - 1)
        })

        # Criar arquivo Excel em memória
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Resultados")
        output.seek(0)

        # Botão para download
        st.download_button(
            label="Clique aqui para baixar o Excel",
            data=output,
            file_name="resultados_notas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Rodapé com o nome do site
st.markdown("""
---
*Desenvolvido por Iaia Jau | Calculadora de Notas Oficial*
""")
