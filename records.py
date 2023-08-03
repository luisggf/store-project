# import pandas as pd
# from store import *

# def generate_ordered_partitions(input_filename, output_filename, M):
#     # Leitura do arquivo CSV
#     df = pd.read_csv(input_filename, chunksize=M)
    
#     # Variáveis de controle
#     current_idx = 0
#     partition_number = 1
#     congelados = []


#     for vetor in df:
#         partition_df = pd.DataFrame(columns=df.columns)

#         records_to_select = min(vetor['Product Code'])
#         partition_df.
#         partition_df.to_csv(f"{output_filename}part{partition_number}.csv", index=False)
#         partition_number += 1
        




    
    # while current_idx < num_records:
    #     # Inicialmente, criamos um novo DataFrame vazio para a partição atual
    #     partition_df = pd.DataFrame(columns=df_sorted.columns)
        
    #     # Selecionar M registros ou o que restar, caso seja menor que M
    #     records_to_select = min(M, num_records - current_idx)
        
    #     # Preencher o DataFrame da partição com os registros selecionados
    #     # Modificação: Ordenar os registros pelo campo 'Product Code'
    #     partition_df = df_sorted.iloc[current_idx:current_idx + records_to_select].sort_values(by='Product Code')
    #     current_idx += records_to_select
        
    #     # Gravar a partição em um novo arquivo CSV
    #     partition_df.to_csv(f"{output_filename}part{partition_number}.csv", index=False)
    #     partition_number += 1
        
    #     # Tratar registros congelados, caso existam
    #     if congelados:
    #         df_congelados = pd.DataFrame(congelados, columns=df_sorted.columns)
    #         df_sorted = pd.concat([df_sorted, df_congelados], ignore_index=True)
    #         congelados.clear()
        
    #     # Continuar com a próxima iteração dos passos 2 a 5
    #     while current_idx < num_records and df_sorted.loc[current_idx, "Product Code"] == partition_df.iloc[-1]["Product Code"]:
    #         congelados.append(df_sorted.loc[current_idx])
    #         current_idx += 1

    # # Verificar se ainda há registros congelados não processados
    # if congelados:
    #     df_congelados = pd.DataFrame(congelados, columns=df_sorted.columns)
    #     df_sorted = pd.concat([df_sorted, df_congelados], ignore_index=True)

    # # Gravar a última partição em um novo arquivo CSV
    # partition_df.to_csv(f"{output_filename}part{partition_number}.csv", index=False)


