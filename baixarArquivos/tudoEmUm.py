import os
import pandas as pd 

with open(r"C:\Users\vfrei\Documents\arquivosBMF\tudoEmUm.txt", 'a') as arquivo_write:
  arquivo_write.write("Data;0;1;2;3;4;5;6\n")

for filename in os.listdir(r"C:\Users\vfrei\Documents\arquivosBMF"):
    ano = '20' + filename[2:4]
    mês = filename[4:6]
    dia = filename[6:8]
    if 'tudoEmUm.txt' in filename:
      continue
    with open(rf"C:\Users\vfrei\Documents\arquivosBMF\{filename}", 'r') as arquivo_read:
        lines = arquivo_read.readlines()
        with open(r"C:\Users\vfrei\Documents\arquivosBMF\tudoEmUm.txt", 'a') as arquivo_write:
          for line in lines:
            if not f"{ano}{mês}{dia}" in line:
              arquivo_write.write(f"{ano}{mês}{dia};{line}")
            else:
              arquivo_write.write('')
    
    print(filename) 

df = pd.read_csv(r"C:\Users\vfrei\Documents\arquivosBMF\tudoEmUm.txt", delimiter=';')
print(df)
df.to_csv(r"C:\Users\vfrei\Documents\arquivosBMF\tudoEmUm.csv", index=False, sep=';')
