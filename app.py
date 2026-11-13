import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Vida Útil de Alimentos",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILO VISUAL
st.markdown("""
<style>
.stApp {
    background-color: #F7FAFF;
    color: #102744;
}
[data-testid="stSidebar"] {
    background-color: #E3EAF5;
}
h1, h2, h3 {
    color: #102744;
}
.stTabs [data-baseweb="tab"] {
    background-color: #E8F0FC;
    border-radius: 8px;
    padding: 12px;
}
.stTabs [aria-selected="true"] {
    background-color: #CDE0FF;
    color: #1557A0;
}
[data-testid="stMetric"] {
    background: #E8F0FC;
    border-radius: 12px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)

# BARRA LATERAL
with st.sidebar:
    st.header("⚙️ Panel de controles")

    alimento = st.radio(
        "Selecciona el tipo de alimento:",
        [
            "Carnes y Pescados",
            "Lácteos y Huevos",
            "Comida Preparada / Guisados"
        ]
    )

    temperatura = st.slider(
        "Temperatura de almacenamiento (°C)",
        min_value=-20,
        max_value=45,
        value=7
    )

    horas = st.number_input(
        "Horas almacenadas:",
        min_value=0.0,
        max_value=10000.0,
        value=12.0,
        step=1.0
    )

    st.caption(
        f"Tiempo introducido: {horas/24:.2f} días"
    )

    st.divider()

    st.markdown("### 👩‍🔬 Integrantes")
    st.write("Diana Soto")
    st.write("Daniela Trevizo")
    st.write("Andrea Ochoa")
    st.write("Ximena Garfio")
    st.write("Sofía Ontiveroz")

    st.divider()

    st.markdown("""
    **Curso:** Programación

    **Facultad:** Ciencias Químicas, UACH

    **Docente:** José Manuel Nápoles Duarte
    """)

# ENCABEZADO
st.title(
    "🥦 Aplicación para la Estimación "
    "de Vida Útil de Alimentos"
)

st.write(
    "Simulador educativo sobre la influencia de "
    "la temperatura, el tiempo y las señales "
    "de deterioro en la conservación de alimentos."
)

# FUNCIONES DE EVALUACIÓN
def evaluar_conservacion(temp, tiempo):
    if temp <= -18:
        return (
            "Congelación",
            "La congelación adecuada detiene el crecimiento "
            "de muchos microorganismos, pero no los elimina."
        )

    if temp <= 4:
        return (
            "Refrigeración",
            "La refrigeración reduce el crecimiento microbiano. "
            "El tiempo seguro depende del alimento y de su manejo."
        )

    if temp < 60:
        if tiempo > 2:
            return (
                "Advertencia",
                "Un alimento perecedero mantenido más de dos "
                "horas en la zona de peligro generalmente "
                "debe desecharse."
            )
        return (
            "Zona de peligro",
            "La temperatura favorece el crecimiento de "
            "microorganismos. Evita prolongar el almacenamiento."
        )

    return (
        "Evaluación especial",
        "El calentamiento y la conservación en caliente "
        "requieren condiciones específicas."
    )

estado, mensaje = evaluar_conservacion(
    temperatura, horas
)

# PESTAÑAS PRINCIPALES (Se agregó tab5)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Curva de Proliferación",
    "🌡️ Zona Peligrosa",
    "📋 Recomendaciones",
    "🔬 Estado del Alimento",
    "📜 Normas NOM"
])

# PESTAÑA 1
with tab1:
    st.subheader(
        "Influencia de la temperatura en la conservación"
    )

    st.info(
        "La siguiente gráfica es una representación "
        "educativa de un índice relativo, no una "
        "predicción validada de vida útil."
    )

    temperaturas = np.linspace(-20, 45, 150)

    # Índice ilustrativo, no modelo microbiológico
    indice = 100 / (
        1 + np.exp(
            np.clip((temperaturas - 8) / 6, -50, 50)
        )
    )

    df = pd.DataFrame({
        "Temperatura": temperaturas,
        "Índice ilustrativo": indice
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Temperatura"],
        y=df["Índice ilustrativo"],
        mode="lines",
        name="Índice ilustrativo",
        line=dict(color="#2476DB", width=4)
    ))

    fig.add_vline(
        x=temperatura,
        line_dash="dash",
        line_color="#E55B55",
        annotation_text="Temperatura seleccionada"
    )

    fig.update_layout(
        title="Índice ilustrativo de conservación",
        xaxis_title="Temperatura (°C)",
        yaxis_title="Índice relativo (sin unidades)",
        template="plotly_white",
        height=430
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Temperatura", f"{temperatura} °C")
    col2.metric("Tiempo", f"{horas:g} horas")
    col3.metric("Condición", estado)

    if estado == "Advertencia":
        st.error(mensaje)
    elif estado == "Zona de peligro":
        st.warning(mensaje)
    else:
        st.info(mensaje)

# PESTAÑA 2
with tab2:
    st.subheader("🌡️ Zona de peligro alimentario")

    st.write(
        "Como referencia educativa, la zona de peligro "
        "para muchos alimentos perecederos se encuentra "
        "aproximadamente entre 4 °C y 60 °C."
    )

    fig2 = go.Figure()

    fig2.add_trace(go.Bar(
        x=["Congelación", "Refrigeración",
           "Zona de peligro", "Caliente"],
        y=[1, 1, 1, 1],
        marker_color=[
            "#79B7F2",
            "#55B7A0",
            "#F1B34B",
            "#E46C64"
        ],
        text=[
            "≤ -18 °C",
            "≤ 4 °C",
            "4–60 °C aprox.",
            "≥ 60 °C"
        ],
        textposition="inside"
    ))

    fig2.update_layout(
        title="Rangos orientativos de temperatura",
        yaxis_visible=False,
        showlegend=False,
        height=340
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.warning(
        "Regla general: muchos alimentos perecederos "
        "no deben permanecer más de 2 horas a "
        "temperatura ambiente, o 1 hora si el "
        "ambiente supera aproximadamente 32 °C."
    )

    st.caption(
        "Los rangos no sustituyen las instrucciones "
        "específicas de conservación o cocción."
    )

# PESTAÑA 3
with tab3:
    st.subheader("📋 Recomendaciones de conservación")

    if alimento == "Carnes y Pescados":
        st.write("""
        **Carnes y pescados**

        - Refrigerar a 4 °C o menos.
        - Evitar la contaminación cruzada.
        - Mantener separados los alimentos crudos.
        - Cocinar hasta la temperatura interna adecuada.
        - Congelar si no se consumirán dentro
          del periodo recomendado.
        """)

    elif alimento == "Lácteos y Huevos":
        st.write("""
        **Lácteos y huevos**

        - Mantener refrigerados los productos perecederos.
        - Revisar las instrucciones del fabricante.
        - Evitar dejarlos a temperatura ambiente.
        - Desechar productos con señales sospechosas
          de deterioro.
        """)

    else:
        st.write("""
        **Comida preparada y guisados**

        - Refrigerar oportunamente las sobras.
        - Guardar en recipientes limpios y cerrados.
        - Utilizar recipientes poco profundos
          para favorecer el enfriamiento.
        - Como referencia general, consumir las
          sobras refrigeradas en 3 a 4 días.
        """)

    st.divider()
    st.markdown("### Resultado de tus controles")
    st.write(f"**Alimento:** {alimento}")
    st.write(f"**Temperatura:** {temperatura} °C")
    st.write(f"**Tiempo:** {horas:g} horas")
    st.info(mensaje)

# PESTAÑA 4
with tab4:
    st.subheader("🔬 Evaluación del estado del alimento")

    st.write(
        "Selecciona los cambios observados para "
        "conocer sus posibles causas microbiológicas."
    )

    signos = st.multiselect(
        "¿Qué observaste en el alimento?",
        [
            "Moho visible",
            "Coloración extraña",
            "Olor desagradable",
            "Textura viscosa",
            "Envase inflado o con fugas",
            "Sin cambios visibles"
        ]
    )

    if st.button("🔎 Evaluar alimento"):
        if not signos:
            st.info(
                "Selecciona al menos una característica."
            )

        elif "Sin cambios visibles" in signos and len(signos) > 1:
            st.warning(
                "Selecciona las señales observadas o "
                "'Sin cambios visibles', pero no ambas."
            )

        elif signos == ["Sin cambios visibles"]:
            st.info(
                "La ausencia de cambios visibles no "
                "garantiza que un alimento sea seguro. "
                "También importan el tiempo, la "
                "temperatura y la manipulación."
            )

        else:
            st.error(
                "⚠️ Se detectaron posibles señales "
                "de deterioro. No pruebes el alimento "
                "para comprobar su seguridad."
            )

            if "Moho visible" in signos:
                st.markdown("### 🍄 Moho visible")
                st.write(
                    "Los mohos son hongos que pueden "
                    "desarrollarse sobre los alimentos. "
                    "Algunos producen micotoxinas. "
                    "En alimentos blandos o húmedos, "
                    "el crecimiento puede extenderse "
                    "más allá de la parte visible."
                )
                st.warning(
                    "Desecha pan, sobras, carnes y "
                    "alimentos blandos con moho. "
                    "Algunos quesos duros tienen "
                    "recomendaciones específicas."
                )

            if "Coloración extraña" in signos:
                st.markdown("### 🎨 Coloración anormal")
                st.write(
                    "Los cambios de color pueden deberse "
                    "a oxidación, reacciones químicas "
                    "o actividad microbiana. "
                    "El color por sí solo no permite "
                    "determinar si un alimento es seguro."
                )

            if "Olor desagradable" in signos:
                st.markdown("### 👃 Olor desagradable")
                st.write(
                    "Algunos microorganismos degradan "
                    "proteínas y otros componentes, "
                    "generando sustancias volátiles "
                    "responsables de olores anormales."
                )

            if "Textura viscosa" in signos:
                st.markdown("### 🦠 Textura viscosa")
                st.write(
                    "Algunas bacterias producen sustancias "
                    "que modifican la textura y pueden "
                    "generar una superficie viscosa."
                )

            if "Envase inflado o con fugas" in signos:
                st.markdown("### 📦 Envase alterado")
                st.write(
                    "Un envase anormalmente inflado "
                    "puede indicar producción de gases "
                    "por microorganismos o problemas "
                    "de conservación. No lo abras "
                    "ni lo pruebes si sospechas "
                    "deterioro, especialmente en conservas."
                )

            st.warning(
                "Ante señales sospechosas, la opción "
                "más prudente es desechar el alimento. "
                "No basta con quitar la parte dañada "
                "o calentarlo para garantizar su seguridad."
            )

# PESTAÑA 5: NORMATIVA MEXICANA (NOM)
with tab5:
    st.subheader("📜 Normas Oficiales Mexicanas (NOM) en Inocuidad Alimentaria")

    st.write(
        "En México, la Secretaría de Salud (a través de COFEPRIS) "
        "establece las regulaciones técnicas obligatorias para "
        "garantizar la inocuidad, conservación y correcta información "
        "de los alimentos."
    )

    # 1. Evaluación dinámica de la temperatura según NOM-251-SSA1-2009
    st.markdown("### 🌡️ Cumplimiento térmico según la NOM-251-SSA1-2009")

    if temperatura <= -18:
        st.success(
            f"**Temperatura seleccionada ({temperatura} °C):** Cumple con el parámetro "
            "de **congelación** de la NOM-251-SSA1-2009 (máximo -18 °C)."
        )
    elif temperatura <= 4:
        st.success(
            f"**Temperatura seleccionada ({temperatura} °C):** Cumple con el parámetro "
            "de **refrigeración** de la NOM-251-SSA1-2009 (máximo 4 °C)."
        )
    elif temperatura < 60:
        st.error(
            f"**Temperatura seleccionada ({temperatura} °C):** Fuera de rango seguro. "
            "La NOM-251-SSA1-2009 exige mantener los alimentos perecederos a "
            "**4 °C o menos** (en frío) o a **60 °C o más** (en caliente)."
        )
    else:
        st.success(
            f"**Temperatura seleccionada ({temperatura} °C):** Cumple con el parámetro "
            "de **mantenimiento en caliente** de la NOM-251-SSA1-2009 (mínimo 60 °C)."
        )

    st.divider()

    # 2. Normativa específica según el alimento seleccionado en la barra lateral
    st.markdown(f"### 📌 Normas aplicables a: *{alimento}*")

    if alimento == "Carnes y Pescados":
        st.info("""
        - **NOM-213-SSA1-2018:** Disposiciones y especificaciones sanitarias para productos cárnicos procesados y establecimientos dedicados a su proceso.
        - **NOM-242-SSA1-2009:** Especificaciones sanitarias y métodos de prueba para productos de la pesca frescos, refrigerados, congelados y procesados (exige mantener productos frescos en hielo o refrigeración $\le 4\text{ }^\circ\text{C}$).
        - **NOM-194-SSA1-2004:** Especificaciones sanitarias en establecimientos dedicados al sacrificio, almacenamiento, transporte y expendio de carne.
        """)

    elif alimento == "Lácteos y Huevos":
        st.info("""
        - **NOM-243-SSA1-2010:** Disposiciones y especificaciones sanitarias para leche, fórmula láctea, producto lácteo combinado y derivados lácteos (quesos, yogur, crema). Establece criterios microbiológicos y de pasteurización.
        - **NOM-159-SSA1-2016:** Disposiciones y especificaciones sanitarias para huevo y sus productos (huevo líquido, deshidratado o congelado), incluyendo control de *Salmonella*.
        """)

    else:
        st.info("""
        - **NOM-251-SSA1-2009 (Apartado de expendio y servicios de alimentos):** Regula directamente la preparación de guisados y comida lista para consumo.
        - Exige **enfriamiento rápido** de alimentos preparados (de $60\text{ }^\circ\text{C}$ a $20\text{ }^\circ\text{C}$ en máximo 2 horas, y de $20\text{ }^\circ\text{C}$ a $4\text{ }^\circ\text{C}$ en máximo 2 horas adicionales).
        - *Nota histórica:* Esta norma sustituyó y unificó a la anterior **NOM-093-SSA1-1994** sobre preparación de alimentos.
        """)

    st.divider()

    # 3. Tabla resumen de NOMs transversales
    st.markdown("### 📑 Resumen de Normas Generales de Conservación y Etiquetado")

    df_noms = pd.DataFrame({
        "Clave de la Norma": [
            "NOM-251-SSA1-2009",
            "NOM-051-SCFI/SSA1-2010",
            "NOM-127-SSA1-2021",
            "NOM-120-SSA1-1994 (Histórica)"
        ],
        "Título / Enfoque": [
            "Prácticas de higiene para el proceso de alimentos, bebidas o suplementos alimenticios.",
            "Especificaciones generales de etiquetado para alimentos y bebidas no alcohólicas preenvasados.",
            "Agua para uso y consumo humano. Límites permisibles de calidad y tratamientos.",
            "Bienes y servicios. Prácticas de higiene y sanidad para el proceso de alimentos (antecedente de la NOM-251)."
        ],
        "Relación con la Vida Útil": [
            "Define temperaturas de refrigeración (≤ 4 °C), congelación (≤ -18 °C), sistema PEPS y control de plagas.",
            "Obliga a declarar fecha de caducidad o consumo preferente y leyendas de conservación (ej. 'Manténgase en refrigeración').",
            "Garantiza que el agua o hielo en contacto directo con los alimentos no sea fuente de contaminación microbiana.",
            "Sentó las bases de las Buenas Prácticas de Manufactura (BPM) en la industria alimentaria mexicana."
        ]
    })

    st.dataframe(df_noms, use_container_width=True, hide_index=True)

    # 4. Conceptos clave de la normativa mexicana
    with st.expander("🔍 Conceptos clave en la normativa mexicana (Caducidad vs. Consumo Preferente y PEPS)"):
        st.markdown("""
        * **Fecha de Caducidad (NOM-051):** Fecha límite en que se considera que las características sanitarias y de calidad de un producto perecedero se mantienen. **Después de esta fecha no debe comercializarse ni consumirse** por riesgo microbiológico.
        * **Fecha de Consumo Preferente (NOM-051):** Fecha en que, bajo determinadas condiciones de almacenamiento, expira el periodo durante el cual el producto es totalmente comercializable y mantiene sus cualidades específicas (sabor, textura), aunque aún puede ser seguro después de esa fecha si el envase está íntegro.
        * **Sistema PEPS (NOM-251):** *Primeras Entradas, Primeras Salidas*. Serie de operaciones que consiste en garantizar la rotación de los productos de acuerdo con su fecha de recepción, vida útil o fecha de caducidad.
        """)

# FUENTES
st.divider()

with st.expander("📚 Fuentes de información"):
    st.markdown("""
    - [COFEPRIS / DOF - Normas Oficiales Mexicanas en materia de Alimentos](https://www.gob.mx/cofepris)
    - [NOM-251-SSA1-2009 - Prácticas de higiene para el proceso de alimentos](https://www.dof.gob.mx/)
    - [FDA - Food Safety](https://www.fda.gov/food)
    - [USDA - Food Safety and Inspection Service](https://www.fsis.usda.gov/)
    - [OMS - Inocuidad de los alimentos](https://www.who.int/health-topics/food-safety)
    """)

st.caption(
    "Proyecto académico de Programación | "
    "Facultad de Ciencias Químicas - UACH | "
    "Simulador educativo, no certificación de inocuidad."
)
