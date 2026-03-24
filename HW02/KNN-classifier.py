"""
IB031 - Domácí úkol 2
Analýza datasetu pacientů, čištění dat, EDA a trénování KNeighborsClassifier.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ─────────────────────────────────────────────
# 1. NAČTENÍ DAT
# ─────────────────────────────────────────────
df = pd.read_csv("IB031_dataset.csv")
print("=== Původní dataset ===")
print(f"Tvar: {df.shape}")
print(df.head())

# ─────────────────────────────────────────────
# 2. ČIŠTĚNÍ DAT
# ─────────────────────────────────────────────

# Chyba 1 & 2: Bílé znaky (tabulátor, mezery) v sample_id a patient_id
df["sample_id"] = df["sample_id"].str.strip()
df["patient_id"] = df["patient_id"].str.strip()

# Chyba 3: Duplicitní sample_id 'S050' – řádek s patient_id P044 má špatné sample_id
# P044 je 45. pacient (index 44), správné ID je S044
mask_wrong = (df["sample_id"] == "S050") & (df["patient_id"] == "P044")
df.loc[mask_wrong, "sample_id"] = "S044"

# Chyba 5: Normalizace nemocnic – 'st  anne' → 'St_Anne'
df["hospital"] = df["hospital"].str.strip()
df["hospital"] = df["hospital"].str.replace(r"\s+", " ", regex=True)
hospital_map = {
    "st anne": "St_Anne",
    "st_anne": "St_Anne",
    "St_Anne": "St_Anne",
    "Brno_UH": "Brno_UH",
}
df["hospital"] = df["hospital"].str.lower().str.replace(" ", "_").map(
    lambda x: "St_Anne" if "anne" in x else ("Brno_UH" if "brno" in x else x)
)

print("\n=== Dataset po čištění řetězců ===")
print(f"Unikátní nemocnice: {df['hospital'].unique()}")
print(f"Chybějící hodnoty:\n{df.isnull().sum()}")

# ─────────────────────────────────────────────
# 3. KNNImputer – doplnění chybějících hodnot
# ─────────────────────────────────────────────
# Imputujeme pouze numerické sloupce
num_cols = ["age", "TP53", "EGFR", "SEPT2"]

imputer = KNNImputer(n_neighbors=5)
df[num_cols] = imputer.fit_transform(df[num_cols])

print("\n=== Po KNNImputer ===")
print(f"Chybějící hodnoty:\n{df.isnull().sum()}")

# ─────────────────────────────────────────────
# 4. ULOŽENÍ VYČIŠTĚNÉHO DATASETU
# ─────────────────────────────────────────────
df.to_csv("IB031_dataset_clean.csv", index=False)
print("\nVyčištěný dataset uložen jako 'IB031_dataset_clean.csv'")

# Create directory for images
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# 5. EDA – Vizualizace genů podle diagnózy
# ─────────────────────────────────────────────
genes = ["TP53", "EGFR", "SEPT2"]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Distribuce aktivity genů podle diagnózy", fontsize=14, fontweight="bold")

for ax, gene in zip(axes, genes):
    for diagnosis, group in df.groupby("diagnosis"):
        ax.hist(group[gene], bins=15, alpha=0.6, label=diagnosis)
    ax.set_title(gene)
    ax.set_xlabel("Aktivita genu")
    ax.set_ylabel("Počet pacientů")
    ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "eda_histogram.png"), dpi=150)
plt.close()

# Boxploty
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Boxploty aktivity genů podle diagnózy", fontsize=14, fontweight="bold")

for ax, gene in zip(axes, genes):
    data = [df[df["diagnosis"] == d][gene].values for d in ["Healthy", "Cancer"]]
    ax.boxplot(data, labels=["Healthy", "Cancer"])
    ax.set_title(gene)
    ax.set_ylabel("Aktivita genu")

plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "eda_boxplot.png"), dpi=150)
plt.close()

# Scatter plot: TP53 vs EGFR
plt.figure(figsize=(8, 6))
for diagnosis, group in df.groupby("diagnosis"):
    plt.scatter(group["TP53"], group["EGFR"], label=diagnosis, alpha=0.7)
plt.xlabel("TP53")
plt.ylabel("EGFR")
plt.title("TP53 vs EGFR podle diagnózy")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "eda_scatter.png"), dpi=150)
plt.close()

print("EDA grafy uloženy.")

# ─────────────────────────────────────────────
# 6. PŘÍPRAVA DAT PRO MODEL
# ─────────────────────────────────────────────
X = df[genes].values
y = (df["diagnosis"] == "Cancer").astype(int)  # Cancer=1, Healthy=0

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Škálování pomocou RobustScaler (odolný voči outlierom)
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ─────────────────────────────────────────────
# 7. TRÉNOVÁNÍ KNeighborsClassifier
# ─────────────────────────────────────────────
knn = KNeighborsClassifier(n_neighbors=2, weights="uniform", metric="euclidean")
knn.fit(X_train_scaled, y_train)

y_pred = knn.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n=== Výsledky modelu KNeighborsClassifier ===")
print(f"Accuracy: {accuracy:.4f}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Healthy", "Cancer"]))

# Matice záměn
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Healthy", "Cancer"],
            yticklabels=["Healthy", "Cancer"])
plt.title(f"Matice záměn (Accuracy = {accuracy:.2f})")
plt.ylabel("Skutečná třída")
plt.xlabel("Predikovaná třída")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "confusion_matrix.png"), dpi=150)
plt.close()
print(f"Matice záměn uložena jako '{os.path.join(IMAGE_DIR, 'confusion_matrix.png')}'")

# ─────────────────────────────────────────────
# 8. VÝPIS NALEZENÝCH CHYB (shrnutí)
# ─────────────────────────────────────────────
print("""
╔══════════════════════════════════════════════════════════════╗
║           SOUHRN NALEZENÝCH CHYB A NEKONZISTENCÍ             ║
╠══════════════════════════════════════════════════════════════╣
║ 1. Bílý znak v sample_id: '\tS039' (tabulátor na začátku)   ║
║ 2. Mezera v sample_id: 'S050 ' (trailing whitespace)        ║
║ 3. Duplicitní sample_id: 'S050' pro dva různé pacienty      ║
║    (P044 a P050) → P044 opraven na 'S044'                   ║
║ 4. Mezera v patient_id: 'P000 ' (trailing whitespace)       ║
║ 5. Nekonzistentní název nemocnice: 'st  anne' místo         ║
║    'St_Anne' (malá písmena + dvojitá mezera)                 ║
║ 6. Chybějící hodnoty (NaN):                                  ║
║    - age: 1x (řádek 13)                                      ║
║    - TP53: 1x (řádek 76)                                     ║
║    - EGFR: 1x (řádek 24)                                     ║
║    - SEPT2: 4x (řádky 1, 23, 48, 98)                        ║
║    → Všechny doplněny pomocí KNNImputer (k=5)               ║
╚══════════════════════════════════════════════════════════════╝
""")
