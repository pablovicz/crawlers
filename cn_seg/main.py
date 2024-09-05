import os
from pathlib import Path
from normalizer import clean_data
from collector import collect_data

print('#' * 50)
print(f'#           CNSEG - COLLECTOR')
print('#' * 50)
print()
url = 'https://cnseg.org.br/sobre-nos/o-mercado-segurador/associados'
out_path = Path(os.getcwd()).joinpath('collected.csv')
print(f'from -> {url}')
print(f'to -> {out_path}')
df = collect_data(url, out_path, separator="|")
clean_data(df)

df.sort_values(by=['Nome'], ascending=True, inplace=True)
columns = ['Nome', 'Nome_completo', 'FIP', 'Telefone', 'Email', 'Endereco', 'CEP', 'Cidade', 'Estado']
df[columns].to_excel(str(out_path).replace('.csv', '.xlsx'))

print()
print('#' * 50)
print(f'# DONE')
print('#' * 50)
