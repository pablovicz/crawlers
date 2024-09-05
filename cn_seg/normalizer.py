import pandas as pd

import collector as cl


def clean_data(df: pd.DataFrame):
    df['content'] = df['content'].apply(lambda row: row.replace('\n', ' '))
    df['CNPJ'] = df['content'].apply(lambda row: cl.collect_cnpj(row))
    df['Telefone'] = df['content'].apply(lambda row: cl.collect_phone(row))
    df['Email'] = df['content'].apply(lambda row: cl.collect_cnpj(row))
    df['CEP'] = df['content'].apply(lambda row: cl.collect_cep(row))
    df['FAX'] = df['content'].apply(lambda row: cl.collect_fax(row))
    df['Nome'] = df['name'].apply(lambda row: row.strip())
    df['Nome_completo'] = df['name'].apply(lambda row: row.strip())
    df['FIP'] = df['content'].apply(lambda row: cl.collect_fip(row))
    df['Endereco'] = None
    df['Cidade'] = None
    df['Estado'] = None
    df['Bairro'] = None
    for index, row in df.iterrows():
        print(row['content'])
        if row['CEP'] is not None:
            address = row['content'].split('Fax:')[0]
            address = address.split('Telefone:')[0]
            address = address.replace(row['name'], '')
            address = address.replace(row['CEP'], '')
            address = address.replace('@', '')
            address = address.replace('  ', ' ')
            if row['FIP'] is not None:
                address = address.split(row['FIP'])[1]
            splitted = address.split(' - ')
            df.loc[index, 'Endereco'] = splitted[0].strip()
            if len(splitted) >= 2:
                df.loc[index, 'Bairro'] = splitted[1].strip()
                df.loc[index, 'Cidade'] = splitted[-2].strip()
                df.loc[index, 'Estado'] = splitted[-1].strip()
    for index, row in df.iterrows():
        if row['FIP'] is not None:
            rest_name = row['content'].split(row['FIP'])[0]
            rest_name = f'{rest_name}'.replace(' ', ' ')
            rest_name = rest_name.replace('@', '')
            df.loc[index, 'Nome_completo'] = rest_name