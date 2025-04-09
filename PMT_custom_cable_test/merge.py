import pandas as pd

directory = 'ITk/test_KM65928'
input_files = [f'{directory}/test{i}' for i in range(5)]
output_file = f'{directory}/test'

merged_df = pd.DataFrame()

for i, file in enumerate(input_files):
    df = pd.read_csv(file)
    if i == 0:
        merged_df = df
    else:
        merged_df = pd.concat([merged_df, df], ignore_index=True)

merged_df.to_csv(output_file, index=False)
print(f'Merged files saved to {output_file}')
