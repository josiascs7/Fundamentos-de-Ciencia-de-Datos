import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats

BASE = "Datasets/Parte_1/"

# -----------------------------------------------
# EJERCICIO 1 - BACTERIAS
# -----------------------------------------------
print("=" * 60)
print("EJERCICIO 1 - Bacterias")
print("=" * 60)

df_bact = pd.read_csv(BASE + "bacterias.csv", sep=";")
df_bact.columns = df_bact.columns.str.strip()
print(df_bact)
print("\nEstadisticas descriptivas:")
print(df_bact[["bacterias_vivas", "segundos"]].describe())

# EDA: scatter original
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].scatter(df_bact["segundos"], df_bact["bacterias_vivas"], color="steelblue", s=80)
axes[0].set_xlabel("Tiempo de exposicion (segundos)")
axes[0].set_ylabel("Bacterias vivas")
axes[0].set_title("Bacterias vs Tiempo (escala original)")

df_bact["log_bacterias"] = np.log(df_bact["bacterias_vivas"])

axes[1].scatter(df_bact["segundos"], df_bact["log_bacterias"], color="darkorange", s=80)
axes[1].set_xlabel("Tiempo de exposicion (segundos)")
axes[1].set_ylabel("log(Bacterias vivas)")
axes[1].set_title("log(Bacterias) vs Tiempo (escala log)")
plt.tight_layout()
plt.savefig("output_practica1_ej1_eda.png", dpi=100)
plt.close()

r_orig = df_bact["segundos"].corr(df_bact["bacterias_vivas"])
r_log  = df_bact["segundos"].corr(df_bact["log_bacterias"])
print(f"\nCorrelacion (escala original): {r_orig:.4f}")
print(f"Correlacion (escala log):      {r_log:.4f}")

# Modelo log-lineal
mod_bact = smf.ols("log_bacterias ~ segundos", data=df_bact)
res_bact = mod_bact.fit()
print("\n", res_bact.summary())

b0 = res_bact.params["Intercept"]
b1 = res_bact.params["segundos"]
print(f"\nModelo ajustado: log(bacterias) = {b0:.4f} + ({b1:.4f}) * segundos")
print(f"  Equivalente: bacterias = e^{b0:.4f} * e^({b1:.4f} * t)")
print(f"  = {np.exp(b0):.2f} * {np.exp(b1):.4f}^t")
print(f"\nR2 = {res_bact.rsquared:.4f}")
print(f"Cada segundo adicional reduce log(bacterias) en {b1:.4f}")
print(f"  Multiplica las bacterias por e^({b1:.4f}) = {np.exp(b1):.4f}")

# Grafico modelo ajustado
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_bact["segundos"], df_bact["bacterias_vivas"], color="steelblue", s=80, label="Datos")
t_seq = np.linspace(df_bact["segundos"].min(), df_bact["segundos"].max(), 200)
pred_log = res_bact.predict(pd.DataFrame({"segundos": t_seq}))
ax.plot(t_seq, np.exp(pred_log), color="red", lw=2, label="Modelo ajustado")
ax.set_xlabel("Tiempo (segundos)")
ax.set_ylabel("Bacterias vivas")
ax.set_title("Modelo de regresion: bacterias vs tiempo")
ax.legend()
plt.tight_layout()
plt.savefig("output_practica1_ej1_modelo.png", dpi=100)
plt.close()

# Analisis de residuos
residuos_bact = res_bact.resid
fitted_bact   = res_bact.fittedvalues

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].scatter(fitted_bact, residuos_bact, color="steelblue", s=60)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("Valores ajustados")
axes[0].set_ylabel("Residuos")
axes[0].set_title("Residuos vs Valores ajustados")

axes[1].hist(residuos_bact, bins=6, color="steelblue", edgecolor="white")
axes[1].set_xlabel("Residuos")
axes[1].set_title("Histograma de residuos")

sm.qqplot(residuos_bact, line="s", ax=axes[2])
axes[2].set_title("Q-Q Plot de residuos")
plt.tight_layout()
plt.savefig("output_practica1_ej1_residuos.png", dpi=100)
plt.close()

print("\n--- Tests de normalidad ---")
stat_sw, p_sw = stats.shapiro(residuos_bact)
print(f"Shapiro-Wilk: estadistico={stat_sw:.4f}, p-valor={p_sw:.4f}")
if p_sw > 0.05:
    print("  -> No se rechaza normalidad de los residuos (p > 0.05)")
else:
    print("  -> Se rechaza normalidad (p <= 0.05)")


# -----------------------------------------------
# EJERCICIO 2 - ESPERANZA DE VIDA
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 2 - Esperanza de vida y anios de educacion")
print("=" * 60)

df_vida = pd.read_csv(BASE + "estudio_vida.csv")
df_vida.columns = df_vida.columns.str.strip()

df_2015 = df_vida[df_vida["Year"] == 2015][["Country", "Life expectancy", "Schooling"]].copy()
df_2015.columns = ["Country", "Life_expectancy", "Schooling"]
df_2015 = df_2015.dropna(subset=["Life_expectancy", "Schooling"])
print(f"Observaciones en 2015 (sin NAs): {len(df_2015)}")
print(df_2015[["Life_expectancy", "Schooling"]].describe())

r_vida = df_2015["Schooling"].corr(df_2015["Life_expectancy"])
print(f"\nCorrelacion de Pearson (Schooling vs Life_expectancy): {r_vida:.4f}")

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_2015["Schooling"], df_2015["Life_expectancy"], color="steelblue", alpha=0.6, s=60)
ax.set_xlabel("Anios de educacion (Schooling)")
ax.set_ylabel("Esperanza de vida (anios)")
ax.set_title("Esperanza de vida vs Anios de educacion (2015)")
plt.tight_layout()
plt.savefig("output_practica1_ej2_eda.png", dpi=100)
plt.close()

mod_vida = smf.ols("Life_expectancy ~ Schooling", data=df_2015)
res_vida = mod_vida.fit()
print("\n", res_vida.summary())

b0_v = res_vida.params["Intercept"]
b1_v = res_vida.params["Schooling"]
print(f"\nModelo ajustado: Life_expectancy = {b0_v:.4f} + {b1_v:.4f} * Schooling")
print(f"R2 = {res_vida.rsquared:.4f}")
print(f"Por cada anio adicional de educacion, la esperanza de vida aumenta {b1_v:.4f} anios.")

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_2015["Schooling"], df_2015["Life_expectancy"], color="steelblue", alpha=0.6, s=60, label="Datos")
s_seq = np.linspace(df_2015["Schooling"].min(), df_2015["Schooling"].max(), 200)
pred_vida = res_vida.predict(pd.DataFrame({"Schooling": s_seq}))
ax.plot(s_seq, pred_vida, color="red", lw=2, label="Regresion ajustada")
ax.set_xlabel("Anios de educacion")
ax.set_ylabel("Esperanza de vida")
ax.set_title("Modelo de regresion lineal")
ax.legend()
plt.tight_layout()
plt.savefig("output_practica1_ej2_modelo.png", dpi=100)
plt.close()

residuos_vida = res_vida.resid
fitted_vida   = res_vida.fittedvalues

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].scatter(fitted_vida, residuos_vida, color="steelblue", alpha=0.6, s=60)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("Valores ajustados")
axes[0].set_ylabel("Residuos")
axes[0].set_title("Residuos vs Valores ajustados")

axes[1].hist(residuos_vida, bins=10, color="steelblue", edgecolor="white")
axes[1].set_xlabel("Residuos")
axes[1].set_title("Histograma de residuos")

sm.qqplot(residuos_vida, line="s", ax=axes[2])
axes[2].set_title("Q-Q Plot de residuos")
plt.tight_layout()
plt.savefig("output_practica1_ej2_residuos.png", dpi=100)
plt.close()

stat_sw2, p_sw2 = stats.shapiro(residuos_vida)
print(f"\nShapiro-Wilk: estadistico={stat_sw2:.4f}, p-valor={p_sw2:.4f}")
if p_sw2 > 0.05:
    print("  -> No se rechaza normalidad de los residuos (p > 0.05)")
else:
    print("  -> Se rechaza normalidad (p <= 0.05)")

print("\n[OK] practica1.py completado.")
