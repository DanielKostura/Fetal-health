import streamlit as st
import pandas as pd
import altair as alt

# --- Základní nastavení ---
st.set_page_config(page_title="Analýza Fetal Health", layout="wide")
st.title("Interaktivní analýza CTG vyšetření")

file_path = "fetal_health.csv" 
try:
    # 1. Načtení dat
    df = pd.read_csv(file_path, sep=';')
    df = df.dropna()
    health_mapping = {1.0: "1 - Normal", 2.0: "2 - Suspect", 3.0: "3 - Pathological"}
    df["Health Category"] = df["fetal_health"].map(health_mapping)

    # 2. Vytvoření NEZÁVISLÝCH výběrů pro každý interaktivní graf
    brush1 = alt.selection_interval(name="brush1")
    brush3 = alt.selection_interval(name="brush3")
    brush4 = alt.selection_interval(name="brush4")
    selection_legend = alt.selection_point(fields=["Health Category"], bind="legend")

    color_scale = alt.Scale(
        domain=["1 - Normal", "2 - Suspect", "3 - Pathological"],
        range=["#1D9E75", "#EF9F27", "#E24B4A"]
    )

    # 3. Společná podmínka (bod se obarví jen tehdy, když projde VŠEMI filtry)
    color_condition = alt.condition(
        brush1 & brush3 & brush4 & selection_legend,
        alt.Color("Health Category:N", scale=color_scale, legend=alt.Legend(title="Kategorie")),
        alt.value("lightgray")
    )

    # --- GRAF 1: Accelerations vs Fetal movement ---
    scatter1 = alt.Chart(df).mark_circle(size=55).encode(
        x=alt.X("accelerations:Q", title="Accelerations (per sec)"),
        y=alt.Y("fetal_movement:Q", title="Fetal movement (per sec)"),
        color=color_condition,
        tooltip=["Health Category:N", "accelerations:Q", "fetal_movement:Q"]
    ).add_params(
        brush1, selection_legend # Připojujeme POUZE brush1
    ).properties(width=450, height=350, title="1. Accelerations vs Fetal movement")

    # --- GRAF 2: Sloupcový graf (Počty) ---
    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X('Health Category:N', title='Zdravotní stav plodu', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('count():Q', title='Počet vyšetření'),
        color=alt.Color('Health Category:N', scale=color_scale, legend=None)
    ).transform_filter(brush1).transform_filter(brush3).transform_filter(brush4).transform_filter(selection_legend).properties(
        width=300, height=350, title="2. Počty dle zdraví"
    )

    # --- GRAF 3: Fetal movement vs Baseline FHR ---
    scatter2 = alt.Chart(df).mark_circle(size=55).encode(
        x=alt.X("baseline value:Q", scale=alt.Scale(zero=False), title="Baseline FHR (bpm)"),
        y=alt.Y("fetal_movement:Q", title="Fetal movement (per sec)"),
        color=color_condition,
        tooltip=["Health Category:N", "baseline value:Q", "fetal_movement:Q"]
    ).add_params(
        brush3, selection_legend # Připojujeme POUZE brush3
    ).properties(width=450, height=350, title="3. Fetal movement vs Baseline FHR")

    # --- GRAF 4: Strip plot s dynamickými průměry ---
    strip_acc = alt.Chart(df).mark_circle(size=40).encode(
        x=alt.X("Health Category:N", title="Fetal health", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("accelerations:Q", title="Accelerations (per sec)"),
        color=color_condition,
        tooltip=["Health Category:N", "accelerations:Q"]
    ).add_params(
        brush4, selection_legend # Připojujeme POUZE brush4
    )

    # Černé čárky pro průměr filtrujeme podle všech aktivních výběrů
    tick_acc = alt.Chart(df).mark_tick(
        color="black", thickness=3, size=40
    ).encode(
        x=alt.X("Health Category:N"),
        y=alt.Y("mean(accelerations):Q")
    ).transform_filter(brush1).transform_filter(brush3).transform_filter(brush4).transform_filter(selection_legend)

    layered_strip = (strip_acc + tick_acc).properties(
        width=300, height=350, title="4. Distribuce accelerations"
    )

    # --- FINÁLNÍ SPOJENÍ ---
    top_row = scatter1 | bars
    bottom_row = scatter2 | layered_strip
    final_chart = top_row & bottom_row

    st.altair_chart(final_chart, use_container_width=True)

except Exception as e:
    st.error(f"Něco se pokazilo při vykreslování: {e}")
