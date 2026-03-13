import pandas as pd
import altair as alt

# 1. Načítanie dát
# Uisti sa, že súbor 'fetal_health.xlsx' máš v rovnakom priečinku ako tento skript
df = pd.read_excel('fetal_health.xlsx')

# 2. Príprava dát: Pre mapovanie číselných kategórií na textové podľa zadania 
health_map = {1.0: '1 - Normal', 2.0: '2 - Suspect', 3.0: '3 - Pathological'}
df['fetal_health_label'] = df['fetal_health'].map(health_map)

# Ošetrenie pre prípad chýbajúcich hodnôt a obmedzenie veľkosti datasetu pre Altair (štandardne berie max 5000 riadkov)
df = df.dropna(subset=['baseline value', 'abnormal_short_term_variability', 'fetal_health'])

# 3. Vytvorenie interaktívneho výberu (štetec / brush)
# Toto umožní používateľovi vybrať oblasť v grafe [cite: 10]
brush = alt.selection_interval()

# 4. Prvý graf: Bodový graf (Scatter plot)
scatter = alt.Chart(df).mark_point(filled=True, size=60).encode(
    x=alt.X('baseline value:Q', title='Základná srdcová frekvencia (FHR)'),
    y=alt.Y('abnormal_short_term_variability:Q', title='Abnormálna krátkodobá variabilita (%)'),
    # Farba sa zmení na sivú, ak bod nie je vo vybranej oblasti
    color=alt.condition(brush, 'fetal_health_label:N', alt.value('lightgray'), title='Zdravie plodu'),
    tooltip=['baseline value', 'abnormal_short_term_variability', 'fetal_health_label']
).add_params(
    brush # Pridanie interaktivity do grafu
).properties(
    width=500,
    height=350,
    title='Závislosť variability od FHR (Potiahnutím myšou vyberte oblasť)'
)

# 5. Druhý graf: Stĺpcový graf (Bar chart)
bars = alt.Chart(df).mark_bar().encode(
    x=alt.X('count():Q', title='Počet záznamov'),
    y=alt.Y('fetal_health_label:N', title='Zdravie plodu (Kategória)'),
    color=alt.Color('fetal_health_label:N', legend=None)
).transform_filter(
    brush # Tento graf sa vyfiltruje na základe výberu v prvom grafe 
).properties(
    width=500,
    height=150,
    title='Distribúcia zdravotného stavu pre vybrané body'
)

# 6. Spojenie grafov pod seba a zobrazenie
dashboard = (scatter & bars).configure_view(
    strokeWidth=0
)

# Zobrazenie v Jupyter Notebooku
dashboard

# Ak by si chcel graf uložiť ako samostatnú interaktívnu webovú stránku, odkomentuj riadok nižšie:
# dashboard.save('interaktivna_vizualizacia.html')