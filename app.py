# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 09:34:53 2025

@author: jperezr
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Botón para descargar el archivo PDF en la barra lateral antes de la sección de ayuda
with open("comprar_semanas.pdf", "rb") as file:
    st.sidebar.download_button(
        label="Descargar PDF - Comprar Semanas",
        data=file,
        file_name="comprar_semanas.pdf",
        mime="application/pdf"
    )

# Título de la aplicación
st.title('Propuesta de Crowdfunding para Compra de Semanas de Cotización en AFORE')

# Sidebar de ayuda
st.sidebar.header('Ayuda')
st.sidebar.write("""
Este es un prototipo de aplicación para explorar la viabilidad de un modelo de crowdfunding que permite a los trabajadores 
completar sus semanas de cotización en las AFORE a través de un financiamiento colaborativo. La aplicación permite calcular 
el financiamiento necesario, simular escenarios, evaluar riesgos y analizar el modelo financiero.

### Funcionalidades principales:
- **Modelo Financiero**: Calcula el pago mensual necesario para financiar las semanas de cotización.
- **Simulación de Escenarios**: Estima cómo un trabajador puede completar sus semanas de cotización.
- **Evaluación de Riesgos**: Permite seleccionar y evaluar los riesgos asociados con el modelo.

### Desarrollado por:
Javier Horacio Pérez Ricárdez

### Copyright:
© 2025 Javier Horacio Pérez Ricárdez. Todos los derechos reservados.
""")

# Introducción
st.header('Introducción')
st.write("""
El presente documento explora la viabilidad de un modelo de negocio basado en crowdfunding para la compra de semanas de cotización en las AFORE. 
Este modelo tiene como objetivo ayudar a los trabajadores que no han alcanzado el mínimo de semanas requeridas para obtener una pensión, permitiéndoles 
completar sus aportaciones mediante financiamiento colectivo.
""")

# Sección de Modelo Financiero
st.header('1. Desarrollo del Modelo Financiero')

# Entrada de datos para el modelo financiero
st.subheader('Configuración del Financiamiento')
tasa_interes = st.number_input('Tasa de interés anual (%)', min_value=0.0, max_value=100.0, value=5.0)
monto_financiado = st.number_input('Monto financiado ($)', min_value=0.0, value=10000.0)
plazo_pago = st.number_input('Plazo de pago (años)', min_value=1, value=5)

# Cálculo de pagos mensuales
tasa_mensual = tasa_interes / 100 / 12
num_pagos = plazo_pago * 12
pago_mensual = monto_financiado * (tasa_mensual * (1 + tasa_mensual) ** num_pagos) / ((1 + tasa_mensual) ** num_pagos - 1)

st.write(f"Pago mensual estimado: ${pago_mensual:,.2f}")

# Crear un DataFrame para mostrar los pagos mensuales a lo largo del plazo
pagos = [pago_mensual] * num_pagos
df_pagos = pd.DataFrame({
    'Mes': np.arange(1, num_pagos + 1),
    'Pago Mensual': pagos
})
st.subheader('Tabla de Pagos Mensuales')
st.write(df_pagos)

# Graficar pagos mensuales
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pagos['Mes'], y=df_pagos['Pago Mensual'], mode='lines', name='Pago Mensual'))
fig.update_layout(title='Pagos Mensuales del Financiamiento',
                  xaxis_title='Meses',
                  yaxis_title='Monto ($)')
st.plotly_chart(fig)

# Simulación de Escenarios
st.header('2. Simulación de Escenarios')

# Entrada de datos para perfiles de trabajadores
salario_actual = st.number_input('Salario actual ($)', min_value=0.0, value=15000.0)
semanas_restantes = st.number_input('Semanas faltantes para la pensión', min_value=0, value=200)

# Simulación de incremento de semanas cotizadas
semanas_completadas = semanas_restantes + int(salario_actual * 0.1)  # Simulación del incremento por financiamiento
st.write(f"Semanas completas después de financiamiento: {semanas_completadas}")

# Crear un DataFrame para simular varios escenarios
escenarios = pd.DataFrame({
    'Salario': [salario_actual, salario_actual + 5000, salario_actual + 10000],
    'Semanas Restantes': [semanas_restantes, semanas_restantes - 50, semanas_restantes - 100],
    'Semanas Completadas': [semanas_completadas, semanas_completadas + 10, semanas_completadas + 20]
})
st.subheader('Tabla de Simulación de Escenarios')
st.write(escenarios)

# Graficar simulación de semanas completas
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=escenarios['Salario'], y=escenarios['Semanas Completadas'], name='Semanas Completadas'))
fig2.update_layout(title='Simulación de Semanas Completadas por Salario',
                   xaxis_title='Salario ($)',
                   yaxis_title='Semanas Completadas')
st.plotly_chart(fig2)

# Evaluación de Riesgos
st.header('3. Evaluación de Riesgos')

# Selección de riesgos
riesgos = st.multiselect(
    'Seleccione los riesgos a evaluar',
    ['Legalidad', 'Modelo de pago', 'Sostenibilidad', 'Falta de ingresos periódicos']
)

# Sugerencias de mitigación para los riesgos seleccionados
if 'Legalidad' in riesgos:
    st.write("**Sugerencia para Legalidad:** Estructurar el modelo dentro de la Modalidad 40 del IMSS.")
if 'Modelo de pago' in riesgos:
    st.write("**Sugerencia para Modelo de Pago:** Establecer contratos claros y garantías de pago.")
if 'Sostenibilidad' in riesgos:
    st.write("**Sugerencia para Sostenibilidad:** Realizar un análisis financiero detallado y escalonado.")
if 'Falta de ingresos periódicos' in riesgos:
    st.write("**Sugerencia para Falta de Ingresos Periódicos:** Implementar pagos flexibles adaptados a los beneficiarios.")

# Graficar riesgos seleccionados
if len(riesgos) > 0:
    fig3 = go.Figure()
    fig3.add_trace(go.Pie(labels=riesgos, values=[25, 25, 25, 25], hole=0.3))
    fig3.update_layout(title='Distribución de Riesgos Seleccionados')
    st.plotly_chart(fig3)

# Conclusión
st.header('Conclusión')

st.write("""
El modelo de crowdfunding para financiar aportaciones voluntarias en AFORE es innovador y factible dentro del marco legal si se estructura adecuadamente. 
A través de un enfoque regulado y estrategias de mitigación de riesgos, esta propuesta puede mejorar significativamente el acceso a pensiones en México.
""")
