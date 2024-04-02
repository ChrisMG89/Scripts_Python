import json

# Datos proporcionados
data = """
	A	B	C	D	E
C1	9	18	18	18	18
C2	5	18	18	18	18
C3	2	18	18	18	18
C4	17	18	18	18	0
C5	10	18	18	0	0
C6	0	0	18	18	0
C7	0	0	18	18	0
					
C6	7	18	0	0	0
C7	3	18	0	0	0
C8	18	18	18	0	0
C9	14	18	18	0	0
C10	10	18	18	0	0
C11	7	18	18	0	0
C12	3	18	18	0	0
C13	18	18	0	0	0
C14	14	18	0	0	0
C15	10	18	0	0	0
C16	7	18	0	0	0
C17	3	18	0	0	0
					
B1	18	18	0	0	0
B2	18	18	0	0	0
B3	18	18	0	0	0
B7	14	18	18	0	0
B8	14	18	18	0	0
B9	14	18	18	0	0
B10	14	18	18	0	0
B11	14	18	18	0	0
B12	14	18	18	0	0
B13	14	18	18	0	0
B14	14	18	18	0	0
B15	14	18	18	0	0
B16	14	18	18	0	0
B17	14	18	18	0	0
					
B1	0	0	18	18	3
B2	0	0	18	18	3
B3	0	0	18	18	3
A1	18	18	6	0	0
A2	18	18	10	0	0
A3	18	18	10	0	0
A4	18	18	10	0	0
A6	18	18	18	3	0
A7	18	18	18	13	0
					
B0	18	18	18	3	0
A8	18	18	18	14	0
A9	18	18	18	17	0
A10	18	18	18	18	2
A11	18	18	18	18	3
A12	18	18	18	18	9
A13	18	18	18	18	13
A14	18	18	18	18	17
A15	15	18	3	0	0
					
AA16	6	18	0	0	0
AA17	7	18	0	0	0
AA18	10	18	0	0	0
AA19	10	18	0	0	0
AA20	14	18	0	0	0
AA21	14	18	0	0	0
AA22	18	18	0	0	0
AA23	18	18	0	0	0
AA24	18	18	0	0	0
AA25	18	18	0	0	0
AA26	7	18	0	0	0
AA27	7	18	0	0	0
AA28	10	18	0	0	0
AA29	14	18	0	0	0
					
A21	18	18	13	0	0
A22	18	18	13	0	0
A23	18	18	14	0	0
A24	18	18	18	0	0
A25	18	C	18	0	0
A26	18	18	18	2	0
A27	18	18	18	6	0
A28	18	18	18	7	0
A29	18	18	18	9	0
A30	18	18	18	10	0
A31	18	18	18	12	0
					
A32	18	18	18	14	0
A33	18	18	18	14	0
A34	18	18	18	18	0
A35	18	18	18	18	2
A36	18	18	18	18	2
A37	18	18	18	18	3
A38	18	18	18	18	7
A39	18	18	18	18	7
A40	0	0	18	18	10
					
A40	18	18	0	0	0
A41	18	18	18	18	9
A42	18	18	18	18	10
A43	18	18	18	18	10
A44	18	18	18	18	14
A45	18	18	18	18	13
A46	18	18	18	18	17
A47	18	18	18	18	17

"""

# Dividir los datos en líneas y columnas
lines = data.strip().split('\n')
headers = lines[0].split('\t')[1:]
inversores = {}

# Procesar los datos y generar el diccionario
for line in lines[1:]:
    elements = line.split('\t')
    pergola_volada = elements[0]
    inversores[pergola_volada] = {}

    for header, value in zip(headers, elements[1:]):
        inversores[pergola_volada][header] = int(value) if value.strip() else 0

# Guardar el diccionario como JSON
with open('output.json', 'w') as json_file:
    json.dump(inversores, json_file, indent=2)

print("Archivo JSON generado correctamente.")