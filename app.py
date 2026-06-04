import pandas as pd
import scipy.stats
import streamlit as st
import time

# Estado persistente
if "experiment_no" not in st.session_state:
    st.session_state.experiment_no = 0

if "df_experiment_results" not in st.session_state:
    st.session_state.df_experiment_results = pd.DataFrame(
        columns=["no", "iterations", "mean"]
    )

st.header("Jogando uma moeda")

# Área reservada para o gráfico
chart_placeholder = st.empty()


def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_no = 0
    outcome_1_count = 0
    means = []

    for r in trial_outcomes:
        outcome_no += 1

        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        means.append(mean)

        # Atualiza o gráfico
        chart_placeholder.line_chart(
            pd.DataFrame({"Média": means})
        )

        time.sleep(0.05)

    return mean


number_of_trials = st.slider(
    "Número de tentativas?",
    min_value=1,
    max_value=1000,
    value=10
)

start_button = st.button("Executar")

if start_button:
    st.write(
        f"Executando o experimento de {number_of_trials} tentativas."
    )

    st.session_state.experiment_no += 1

    mean = toss_coin(number_of_trials)

    novo_resultado = pd.DataFrame(
        [{
            "no": st.session_state.experiment_no,
            "iterations": number_of_trials,
            "mean": mean
        }]
    )

    st.session_state.df_experiment_results = pd.concat(
        [st.session_state.df_experiment_results, novo_resultado],
        ignore_index=True
    )

st.subheader("Histórico de experimentos")
st.dataframe(
    st.session_state.df_experiment_results,
    use_container_width=True
)
