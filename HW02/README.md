# IB031 – Domáci úkol 2

Analýza datasetu pacientov brnenských nemocníc, čistenie dát a trénovanie klasifikačného modelu KNeighborsClassifier na predikciu diagnózy (Healthy / Cancer) na základe génovej expresie.

---

## Obsah archívu

```
Archív/
├── KNN-classifier.py        # Hlavný skript (čistenie, EDA, trénovanie modelu)
├── IB031_dataset.csv        # Vstupný dataset (manuálně upravený, messy)
├── IB031_dataset_clean.csv  # Vyčistený dataset (generovaný skriptom)
├── README.md                # Táto dokumentácia
└── changes_in_dataset.txt       # Súpis nájdených chýb a nekonzistencií
```

---

## Požiadavky

- Python 3.8+
- Knižnice: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`

Inštalácia závislostí:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

---

## Spustenie

1. Uisti sa, že `IB031_dataset.csv` a `KNN-classifier.py` sú v **rovnakom priečinku**.
2. Otvor terminál v danom priečinku a spusti:

```bash
python3 KNN-classifier.py
```

> **Poznámka pre Windows:** Ak Python nie je v PATH, použi `python` alebo `py` namiesto `python3`.

---

## Čo skript robí

### 1. Načítanie dát
Načíta pôvodný súbor `IB031_dataset.csv`.

### 2. Čistenie dát
Skript automaticky opraví nasledujúce chyby:

| # | Chyba | Oprava |
|---|-------|--------|
| 1 | Tabulátor na začiatku `sample_id` (`\tS039`) | `str.strip()` |
| 2 | Medzery v `sample_id` a `patient_id` | `str.strip()` |
| 3 | Duplicitné `sample_id = S050` pre pacientov P044 a P050 | P044 premenovaný na `S044` |
| 4 | Nekonzistentný formát nemocnice (`st  anne`, `St  Anne`, `BRNO_UH`) | Normalizácia na `St_Anne` / `Brno_UH` |
| 5 | Chýbajúce hodnoty v `age`, `TP53`, `EGFR`, `SEPT2` | Doplnenie cez `KNNImputer(n_neighbors=5)` |

### 3. EDA – vizualizácia
Skript uloží do pracovného priečinka tri grafy:
- `eda_histogram.png` – histogramy aktivity génov podľa diagnózy
- `eda_boxplot.png` – boxploty génov podľa diagnózy
- `eda_scatter.png` – scatter plot TP53 vs EGFR

### 4. Trénovanie modelu
- **Algoritmus:** `KNeighborsClassifier`
- **Parametre:** `n_neighbors=2`, `weights="uniform"`, `metric="euclidean"`
- **Škálovanie:** `RobustScaler` (odolný voči outlierom)
- **Rozdelenie dát:** `test_size=0.25`, `random_state=42`
- **Vstupy modelu:** geny `TP53`, `EGFR`, `SEPT2`
- **Výstup:** diagnóza `Healthy` / `Cancer`

Skript vypíše Accuracy, Classification Report a uloží maticu zámen ako `confusion_matrix.png`.

### 5. Výstupné súbory

Po spustení skript vygeneruje:

```
IB031_dataset_clean.csv   # vyčistený dataset
eda_histogram.png
eda_boxplot.png
eda_scatter.png
confusion_matrix.png
```

---

## Očakávané výsledky

```
Accuracy: 0.92

              precision    recall  f1-score
     Healthy       1.00      0.88      0.93
      Cancer       0.82      1.00      0.90
    accuracy                           0.92
```

---

## Nájdené chyby v datasete

Stručný prehľad:

- Nekonzistentné pomenovania hodnôt v atribútoch hospital a diagnosis.
- Duplicitné hodnoty.
- Chýbajúce hodnoty.
- Šum v hodnotách ("O" -> Nan, ~13 -> 13).
- Nekonzistencia neuvedených hodnôt.
 
Stručný zoznam nájdených chýb a nekonzistencií najdete také v súbore **`changes_in_dataset.txt`**.


Podrobný prehľad všetkých nájdených chýb a nekonzistencií:

- Whitespace v identifikátoroch (`\t`, trailing medzery)
- Duplicitné `sample_id` pre dvoch rôznych pacientov
- Duplicitný riadok (S074 sa opakuje na konci súboru)
- Nekonzistentný formát stĺpca `hospital` (4 rôzne varianty zápisu)
- Malé písmená v `diagnosis` (`cancer` namiesto `Cancer`)
- Neplatné textové hodnoty v číselných stĺpcoch (`O`, `ND`, `error`, `~13`, `?`)
- Excel auto-korekcia dátumu (`Sep-02` v stĺpci `SEPT2`)
- Chýbajúce hodnoty (NaN) v `age`, `TP53`, `EGFR`, `SEPT2`
