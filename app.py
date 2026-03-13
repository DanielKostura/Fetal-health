import streamlit as st
import pandas as pd
import altair as alt

# 1. Základní nastavení
st.set_page_config(page_title="Analýza Fetal Health", layout="wide")
st.title("Interaktivní analýza CTG vyšetření")
st.info("Krok 1: Inicializace aplikace proběhla.")

try:
    # 2. Načtení dat pomocí tvé přesné cesty (používáme 'r' před stringem kvůli zpětným lomítkům ve Windows)
    file_path = r"C:\Users\oujes\Documents\3\IB031\Fetal-health\fetal_health_clean.csv"
    df = pd.read_csv(file_path)
    
    # Odstranění chybějících hodnot a mapování
    df = df.dropna()
    health_mapping = {1.0: "1 - Normal", 2.0: "2 - Suspect", 3.0: "3 - Pathological"}
    df["Health Category"] = df["fetal_health"].map(health_mapping)
    
    st.success(f"Krok 2: Data úspěšně načtena! Počet řádků k vizualizaci: {len(df)}")
    
    # 3. Vykreslení grafů
    try:
        brush = alt.selection_interval(name="brush")
        
        scatter = alt.Chart(df).mark_circle(size=60, opacity=0.6).encode(
            x=alt.X('baseline value:Q', scale=alt.Scale(zero=False), title='Baseline FHR'),
            y=alt.Y('accelerations:Q', title='Accelerations per sec'),
            color=alt.condition(brush, 'Health Category:N', alt.value('lightgray'))
        ).properties(
            width=500, height=400, title="Závislost tepu na akceleracích"
        )
        
        # Ošetření verzí Altairu (někdy způsobuje tichý pád)
        try:
            scatter = scatter.add_params(brush)
        except AttributeError:
            scatter = scatter.add_selection(brush)

        bars = alt.Chart(df).mark_bar().encode(
            x=alt.X('Health Category:N', title='Zdravotní stav plodu'),
            y=alt.Y('count():Q', title='Počet vyšetření'),
            color=alt.Color('Health Category:N', legend=None)
        ).properties(
            width=300, height=400, title="Počty dle zdraví"
        ).transform_filter(brush)

        # Spojení a zobrazení
        chart = scatter | bars
        st.altair_chart(chart, use_container_width=True)
        st.success("Krok 3: Grafy úspěšně vykresleny!")

    except Exception as e_chart:
        st.error(f"Chyba při vykreslování grafu: {e_chart}")

except FileNotFoundError:
    st.error(f"Soubor nebyl nalezen na cestě: {file_path}. Zkontroluj překlepy v názvu.")
except Exception as e_data:
    st.error(f"Chyba při zpracování dat: {e_data}")