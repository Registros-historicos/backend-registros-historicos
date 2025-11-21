from io import BytesIO
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo


def dataframe_to_styled_excel_bytes(
        df: pd.DataFrame,
        sheet_name: str = "Sheet1",
        table_name: str = "Table1",
        column_mapping: dict = None,
        report_title: str = None
) -> BytesIO:
    output = BytesIO()

    if column_mapping:
        df = df.rename(columns=column_mapping)

    # 4 filas de encabezado (3 institucionales + 1 título reporte)
    header_rows_count = 4
    start_row_idx = header_rows_count

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name, startrow=start_row_idx)

        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        max_col = df.shape[1] if df.shape[1] > 0 else 1
        last_col_letter = get_column_letter(max_col)

        # Definimos los colores AQUÍ para usarlos en ambas partes
        # Nota: Agregué un 4to color para el título
        header_colors = ["5B9BD5", "9DC3E6", "BDD7EE", "BDD7EE"]

        # -----------------------------------------------------------
        # PARTE 1: ENCABEZADO INSTITUCIONAL (Filas 1, 2, 3)
        # -----------------------------------------------------------
        headers_text = [
            "TECNOLÓGICO NACIONAL DE MÉXICO",
            "SECRETARÍA DE EXTENSIÓN Y VINCULACIÓN",
            "DIRECCIÓN DE VINCULACIÓN E INTERCAMBIO ACADEMICO"
        ]

        for i, text in enumerate(headers_text):
            row_num = i + 1
            cell = worksheet[f"A{row_num}"]
            cell.value = text
            cell.font = Font(bold=True, size=12, color="000000")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            # Usa los colores 0, 1 y 2
            cell.fill = PatternFill(start_color=header_colors[i], end_color=header_colors[i], fill_type="solid")
            worksheet.merge_cells(f"A{row_num}:{last_col_letter}{row_num}")

        # -----------------------------------------------------------
        # PARTE 2: TÍTULO DEL REPORTE ESPECÍFICO (Fila 4)
        # -----------------------------------------------------------
        row_num_title = 4
        title_text = report_title.upper() if report_title else "REPORTE GENERAL"

        cell_title = worksheet[f"A{row_num_title}"]
        cell_title.value = title_text

        # CAMBIOS AQUÍ:
        # 1. Usamos header_colors[3] (el cuarto color de tu lista)
        # 2. Mantenemos el texto negro para que contraste bien con el azul claro
        bg_color = header_colors[3]

        cell_title.font = Font(bold=True, size=14, color="000000")
        cell_title.alignment = Alignment(horizontal="center", vertical="center")
        cell_title.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")

        worksheet.merge_cells(f"A{row_num_title}:{last_col_letter}{row_num_title}")

        # -----------------------------------------------------------
        # PARTE 3: TABLA DE DATOS (El resto sigue igual)
        # -----------------------------------------------------------
        table_start_row = start_row_idx + 1
        table_end_row = table_start_row + df.shape[0]
        table_ref = f"A{table_start_row}:{last_col_letter}{table_end_row}"

        tab = Table(displayName=table_name, ref=table_ref)
        style = TableStyleInfo(
            name="TableStyleMedium9",
            showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False,
        )
        tab.tableStyleInfo = style
        try:
            worksheet.add_table(tab)
        except ValueError:
            pass

        # Estética de columnas
        for col_idx in range(1, max_col + 1):
            cell = worksheet.cell(row=table_start_row, column=col_idx)
            cell.alignment = Alignment(horizontal="center", vertical="center")

        for i, col in enumerate(df.columns, start=1):
            col_letter = get_column_letter(i)
            try:
                max_len = max(df[col].astype(str).map(len).max(), len(str(col)))
            except Exception:
                max_len = len(str(col))
            worksheet.column_dimensions[col_letter].width = (max_len + 4)

        for idx, col in enumerate(df.columns, start=1):
            if pd.api.types.is_integer_dtype(df[col].dtype):
                fmt = '#,##0'
            elif pd.api.types.is_float_dtype(df[col].dtype):
                fmt = '#,##0.00'
            elif pd.api.types.is_datetime64_any_dtype(df[col].dtype):
                fmt = 'YYYY-MM-DD'
            else:
                fmt = None

            if fmt:
                for row in range(table_start_row + 1, table_end_row + 1):
                    c = worksheet.cell(row=row, column=idx)
                    c.number_format = fmt
                    if fmt != '#,##0.00':
                        c.alignment = Alignment(horizontal='center')

        worksheet.freeze_panes = f"A{table_start_row + 1}"

    output.seek(0)
    return output
