from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.post("/generar-informe-ds44")
async def generar_informe_ds44(archivo_excel: UploadFile = File(...)):
    try:
        contents = await archivo_excel.read()
        xls = pd.ExcelFile(BytesIO(contents))
        df = xls.parse('Check list', header=2)
        df_filtrado = df[df['No Cumple'] == 'x']
        df_filtrado = df_filtrado[['Sistema de Gestión de\nSeguridad y Salud en el Trabajo (SGSST)', 'Artículo']]
        df_filtrado.columns = ['Pregunta', 'Artículo']
        df_filtrado = df_filtrado.dropna()

        observaciones = []
        for _, row in df_filtrado.iterrows():
            observaciones.append(f"""
🔹 Artículo: {row['Artículo']}
🔸 Pregunta: {row['Pregunta']}
📝 Observación técnica: Se detecta un incumplimiento del artículo {row['Artículo']}, asociado al ítem auditado. Esta situación debe ser corregida a la brevedad.
✅ Medida sugerida: Aplicar las medidas correspondientes que aseguren el cumplimiento del artículo mencionado y dejar registro documental como respaldo.
""")

        informe = "\n\n".join(observaciones) if observaciones else "No se detectaron incumplimientos en el archivo."
        return JSONResponse(content={"informe": informe})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})