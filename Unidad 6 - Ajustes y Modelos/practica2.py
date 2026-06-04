import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats

BASE2 = "Datasets/Parte_2/"

# -----------------------------------------------
# EJERCICIO 1 - STUDENT DATA
# -----------------------------------------------
print("=" * 60)
print("EJERCICIO 1 - Calificaciones y horas de estudio")
print("=" * 60)

df_est = pd.read_csv(BASE2 + "student_data.csv")
print(df_est.head())
print(df_est.describe())

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_est["hours_studied"], df_est["exam_scores"], color="steelblue", alpha=0.5, s=40)
ax.set_xlabel("Horas de estudio semanales")
ax.set_ylabel("Calificacion final")
ax.set_title("Calificacion vs Horas de estudio")
plt.tight_layout()
plt.savefig("output_p2_ej1_scatter.png", dpi=100)
plt.close()

r, p_val = stats.pearsonr(df_est["hours_studied"], df_est["exam_scores"])
print(f"\nCorrelacion de Pearson: {r:.4f}  (p-valor: {p_val:.4e})")

mod_est = smf.ols("exam_scores ~ hours_studied", data=df_est)
res_est = mod_est.fit()
print(res_est.summary())

b0_e = res_est.params["Intercept"]
b1_e = res_est.params["hours_studied"]
print(f"\nModelo: exam_scores = {b0_e:.4f} + {b1_e:.4f} * hours_studied")
print(f"R2 = {res_est.rsquared:.4f}")

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_est["hours_studied"], df_est["exam_scores"], color="steelblue", alpha=0.5, s=40, label="Datos")
h_seq = np.linspace(df_est["hours_studied"].min(), df_est["hours_studied"].max(), 200)
ax.plot(h_seq, res_est.predict(pd.DataFrame({"hours_studied": h_seq})), color="red", lw=2, label="Modelo")
ax.set_xlabel("Horas de estudio")
ax.set_ylabel("Calificacion")
ax.set_title("Regresion lineal ajustada")
ax.legend()
plt.tight_layout()
plt.savefig("output_p2_ej1_modelo.png", dpi=100)
plt.close()


# -----------------------------------------------
# EJERCICIO 2 - TEORICO (verificacion numerica)
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 2 - Regresion multiple (teorico)")
print("=" * 60)

b0, b1, b2, b3, b4 = 10000, 5000, 2000, -1500, -15000
print(f"Modelo: precio = {b0} + {b1}*x1 + {b2}*x2 + ({b3})*x3 + ({b4})*x4")
sup, hab, ant = 80, 3, 10
p_urbano    = b0 + b1*sup + b2*hab + b3*ant + b4*0
p_suburbano = b0 + b1*sup + b2*hab + b3*ant + b4*1
print(f"\nVerificacion numerica (sup={sup}, hab={hab}, ant={ant}):")
print(f"  Precio urbano    (x4=0): ${p_urbano:,.0f}")
print(f"  Precio suburbano (x4=1): ${p_suburbano:,.0f}")
print(f"  Diferencia: ${p_urbano - p_suburbano:,.0f} -> urbano es MAS CARO")
print("\nRespuesta correcta: d)")
print("  a) FALSA: suburbanas son mas baratas (b4 = -15000)")
print("  b) FALSA: coeficiente de antiguedad es -1500, no +10000")
print("  c) FALSA: b2=2000 es el mismo para urbanas y suburbanas (sin interaccion)")
print("  d) CORRECTA: urbana cuesta $15000 mas que suburbana con iguales caracteristicas")


# -----------------------------------------------
# EJERCICIO 3 - PINGUINOS
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 3 - Pinguinos Palmer")
print("=" * 60)

df_peng = pd.read_csv(BASE2 + "penguins.csv")
df_peng = df_peng.dropna(subset=["bill_length_mm", "flipper_length_mm", "species"])
print(f"Observaciones (sin NAs): {len(df_peng)}")
print(df_peng["species"].value_counts())

palette = {"Adelie": "steelblue", "Chinstrap": "darkorange", "Gentoo": "seagreen"}
fig, ax = plt.subplots(figsize=(8, 5))
for sp, grp in df_peng.groupby("species"):
    ax.scatter(grp["flipper_length_mm"], grp["bill_length_mm"], label=sp,
               color=palette[sp], alpha=0.6, s=50)
ax.set_xlabel("Longitud de la aleta (mm)")
ax.set_ylabel("Longitud del pico (mm)")
ax.set_title("Longitud de pico vs Longitud de aleta por especie")
ax.legend()
plt.tight_layout()
plt.savefig("output_p2_ej3_scatter_especies.png", dpi=100)
plt.close()

# Modelo 1
mod_p1 = smf.ols("bill_length_mm ~ flipper_length_mm", data=df_peng)
res_p1 = mod_p1.fit()
print("\nModelo 1:")
print(res_p1.summary())

# Modelo 2: flipper + species
mod_p2 = smf.ols("bill_length_mm ~ flipper_length_mm + C(species)", data=df_peng)
res_p2 = mod_p2.fit()
print("\nModelo 2:")
print(res_p2.summary())

print(f"\nComparacion de modelos:")
print(f"  Modelo 1 -> R2 ajustado: {res_p1.rsquared_adj:.4f}")
print(f"  Modelo 2 -> R2 ajustado: {res_p2.rsquared_adj:.4f}")
mejor = "Modelo 2" if res_p2.rsquared_adj > res_p1.rsquared_adj else "Modelo 1"
print(f"  Mejor modelo: {mejor}")

nuevo_pinguino = pd.DataFrame({"flipper_length_mm": [191], "species": ["Chinstrap"]})
pred_pico = res_p2.predict(nuevo_pinguino)
print(f"\nPrediccion (Chinstrap, flipper=191mm): bill_length = {pred_pico.values[0]:.2f} mm")


# -----------------------------------------------
# EJERCICIO 4 - RENDIMIENTO ESTUDIANTES
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 4 - Rendimiento en examenes")
print("=" * 60)

df_rend = pd.read_csv(BASE2 + "dataset_rendimiento.csv")
print(df_rend.head())
print(f"\nCategorias de Desayuno: {df_rend['Desayuno'].unique()}")
print(df_rend["Desayuno"].value_counts())

mod_rend = smf.ols("Rendimiento ~ Horas_de_Estudio + C(Desayuno)", data=df_rend)
res_rend = mod_rend.fit()
print("\n", res_rend.summary())

print(f"\nR2 = {res_rend.rsquared:.4f}")
print("\nSignificancia (alpha=0.05):")
for var, pv in res_rend.pvalues.items():
    sig = "[OK] Significativa" if pv < 0.05 else "[NO] No significativa"
    print(f"  {var}: p={pv:.4f} -> {sig}")

nuevo_est = pd.DataFrame({"Horas_de_Estudio": [5.5], "Desayuno": ["Saludable"]})
pred_rend = res_rend.predict(nuevo_est)
print(f"\nPrediccion (5.5h, Saludable): rendimiento = {pred_rend.values[0]:.2f}")


# -----------------------------------------------
# EJERCICIO 5 - ADVERTISING
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 5 - Publicidad y ventas")
print("=" * 60)

df_adv = pd.read_csv(BASE2 + "advertising.csv")
print(df_adv.head())
print(df_adv.describe())

corr_tv   = df_adv["TV"].corr(df_adv["Sales"])
corr_radio = df_adv["Radio"].corr(df_adv["Sales"])
corr_news  = df_adv["Newspaper"].corr(df_adv["Sales"])
print(f"\nCorrelaciones con Sales:")
print(f"  TV:        {corr_tv:.4f}")
print(f"  Radio:     {corr_radio:.4f}")
print(f"  Newspaper: {corr_news:.4f}")
medio_max = max([("TV", corr_tv), ("Radio", corr_radio), ("Newspaper", corr_news)], key=lambda x: abs(x[1]))
print(f"  -> Mas asociado: {medio_max[0]} (r={medio_max[1]:.4f})")

mod_adv_full = smf.ols("Sales ~ TV + Radio + Newspaper", data=df_adv)
res_adv_full = mod_adv_full.fit()
print("\nModelo completo:")
print(res_adv_full.summary())

print("\nSignificancia (alpha=0.05):")
for var, pv in res_adv_full.pvalues.items():
    sig = "[OK]" if pv < 0.05 else "[NO] no significativa"
    print(f"  {var}: p={pv:.4f} {sig}")

mod_adv_red = smf.ols("Sales ~ TV + Radio", data=df_adv)
res_adv_red = mod_adv_red.fit()
print("\nModelo reducido (sin Newspaper):")
print(res_adv_red.summary())

b_tv = res_adv_red.params["TV"]
print(f"\nCoeficiente TV: {b_tv:.4f}")
print(f"  Por cada $1000 adicionales en TV, las ventas aumentan {b_tv*1000:.2f} unidades")

residuos_adv = res_adv_red.resid
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(residuos_adv, bins=20, color="steelblue", edgecolor="white")
axes[0].set_xlabel("Residuos")
axes[0].set_title("Distribucion de residuos (modelo final)")
sm.qqplot(residuos_adv, line="s", ax=axes[1])
axes[1].set_title("Q-Q Plot")
plt.tight_layout()
plt.savefig("output_p2_ej5_residuos.png", dpi=100)
plt.close()

stat_sw_adv, p_sw_adv = stats.shapiro(residuos_adv)
print(f"\nShapiro-Wilk: estadistico={stat_sw_adv:.4f}, p-valor={p_sw_adv:.4f}")


# -----------------------------------------------
# EJERCICIO 6 - AUTO
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 6 - Consumo de autos")
print("=" * 60)

df_auto = pd.read_excel(BASE2 + "auto.xlsx")
print(df_auto.head())
print(f"Columnas: {df_auto.columns.tolist()}")

if df_auto["horsepower"].dtype == object:
    df_auto["horsepower"] = pd.to_numeric(df_auto["horsepower"], errors="coerce")
df_auto = df_auto.dropna(subset=["mpg", "horsepower"])
print(f"Filas validas: {len(df_auto)}")

n_ford  = df_auto["name"].str.lower().str.contains("ford").sum()
pct_ford = n_ford / len(df_auto) * 100
print(f"\n% Ford: {n_ford}/{len(df_auto)} = {pct_ford:.2f}%")

origin_map = {1: "Americano", 2: "Europeo", 3: "Japones"}
df_auto["origin_label"] = df_auto["origin"].map(origin_map)
fig, ax = plt.subplots(figsize=(7, 4))
df_auto["origin_label"].value_counts().plot(kind="bar", ax=ax, color=["steelblue", "darkorange", "seagreen"])
ax.set_xlabel("Origen")
ax.set_ylabel("Cantidad de autos")
ax.set_title("Distribucion de autos por origen")
ax.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig("output_p2_ej6_origen.png", dpi=100)
plt.close()

mod_auto = smf.ols("mpg ~ horsepower", data=df_auto)
res_auto = mod_auto.fit()
print("\nModelo simple:")
print(res_auto.summary())
b0_a = res_auto.params["Intercept"]
b1_a = res_auto.params["horsepower"]
print(f"\nModelo: mpg = {b0_a:.4f} + ({b1_a:.4f}) * horsepower")
print(f"Relacion: {'negativa' if b1_a < 0 else 'positiva'}")
print(f"Por cada caballo de fuerza adicional, el consumo cambia {b1_a:.4f} mpg")
print(f"R2 = {res_auto.rsquared:.4f} ({res_auto.rsquared*100:.1f}% de variabilidad explicada)")

hp_seq = np.linspace(df_auto["horsepower"].min(), df_auto["horsepower"].max(), 300)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(df_auto["horsepower"], df_auto["mpg"], color="steelblue", alpha=0.4, s=30)
axes[0].plot(hp_seq, res_auto.predict(pd.DataFrame({"horsepower": hp_seq})), color="red", lw=2)
axes[0].set_xlabel("Horsepower")
axes[0].set_ylabel("MPG")
axes[0].set_title("Regresion lineal simple")

mod_auto2 = smf.ols("mpg ~ horsepower + I(horsepower**2)", data=df_auto)
res_auto2 = mod_auto2.fit()
print(f"\nModelo cuadratico: R2 = {res_auto2.rsquared:.4f}")

pred_quad = res_auto2.predict(pd.DataFrame({"horsepower": hp_seq}))
axes[1].scatter(df_auto["horsepower"], df_auto["mpg"], color="steelblue", alpha=0.4, s=30)
axes[1].plot(hp_seq, pred_quad, color="darkorange", lw=2)
axes[1].set_xlabel("Horsepower")
axes[1].set_ylabel("MPG")
axes[1].set_title("Regresion cuadratica (mejora)")
plt.tight_layout()
plt.savefig("output_p2_ej6_modelos.png", dpi=100)
plt.close()


# -----------------------------------------------
# EJERCICIO 7 - USA HOUSING
# -----------------------------------------------
print("\n" + "=" * 60)
print("EJERCICIO 7 - Precios de viviendas en EE.UU.")
print("=" * 60)

df_house = pd.read_excel(BASE2 + "USA_Housing.xlsx")
df_house.columns = df_house.columns.str.strip().str.lower().str.replace(" ", "_")
print(f"Columnas: {df_house.columns.tolist()}")
print(f"Shape: {df_house.shape}")
print(df_house.describe())

print(f"\nNAs por columna:\n{df_house.isnull().sum()}")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df_house["price"], bins=40, color="steelblue", edgecolor="white")
ax.set_xlabel("Precio de venta")
ax.set_ylabel("Frecuencia")
ax.set_title("Distribucion del precio de las viviendas")
plt.tight_layout()
plt.savefig("output_p2_ej7_hist_precio.png", dpi=100)
plt.close()

skew_price = df_house["price"].skew()
print(f"\nAsimetria del precio: {skew_price:.4f}")

num_cols = df_house.select_dtypes(include=[np.number]).columns.tolist()
corr_matrix = df_house[num_cols].corr()
print(f"\nCorrelaciones con price:\n{corr_matrix['price'].sort_values(ascending=False)}")

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
            vmin=-1, vmax=1, linewidths=0.5)
ax.set_title("Heatmap de correlaciones")
plt.tight_layout()
plt.savefig("output_p2_ej7_heatmap.png", dpi=100)
plt.close()

corr_with_price = corr_matrix["price"].drop("price").abs()
best_var = corr_with_price.idxmax()
print(f"\nVariable mas correlacionada con price: {best_var} (r={corr_with_price[best_var]:.4f})")

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_house[best_var], df_house["price"], alpha=0.1, s=10, color="steelblue")
ax.set_xlabel(best_var)
ax.set_ylabel("Precio")
ax.set_title(f"Price vs {best_var}")
plt.tight_layout()
plt.savefig("output_p2_ej7_scatter.png", dpi=100)
plt.close()

predictores = [c for c in num_cols if c != "price"]
formula_full = "price ~ " + " + ".join(predictores)
print(f"\nModelo completo: {formula_full}")
mod_house_full = smf.ols(formula_full, data=df_house)
res_house_full = mod_house_full.fit()
print(res_house_full.summary())

print("\nSignificancia (alpha=0.05):")
for var, pv in res_house_full.pvalues.items():
    sig = "[OK]" if pv < 0.05 else "[NO] no significativa"
    print(f"  {var}: p={pv:.4f} {sig}")

no_sig = [v for v, pv in res_house_full.pvalues.items() if pv >= 0.05 and v != "Intercept"]
print(f"\nVariables NO significativas: {no_sig}")

if no_sig:
    predictores_red = [p for p in predictores if p not in no_sig]
    formula_red = "price ~ " + " + ".join(predictores_red)
else:
    formula_red = formula_full
    predictores_red = predictores

print(f"\nModelo reducido: {formula_red}")
mod_house_red = smf.ols(formula_red, data=df_house)
res_house_red = mod_house_red.fit()
print(res_house_red.summary())

print(f"\nComparacion de modelos:")
print(f"  Modelo completo -> R2 ajustado: {res_house_full.rsquared_adj:.6f}")
print(f"  Modelo reducido -> R2 ajustado: {res_house_red.rsquared_adj:.6f}")

print("\nCoeficientes del modelo final:")
for var, coef in res_house_red.params.items():
    print(f"  {var}: {coef:.4f}")

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df_house["price"], res_house_red.fittedvalues, alpha=0.2, s=10, color="steelblue")
lims = [min(df_house["price"].min(), res_house_red.fittedvalues.min()),
        max(df_house["price"].max(), res_house_red.fittedvalues.max())]
ax.plot(lims, lims, "r--", lw=1.5, label="Prediccion perfecta")
ax.set_xlabel("Valores reales")
ax.set_ylabel("Valores predichos")
ax.set_title("Valores predichos vs reales")
ax.legend()
plt.tight_layout()
plt.savefig("output_p2_ej7_pred_vs_real.png", dpi=100)
plt.close()

print("\n[OK] practica2.py completado.")
