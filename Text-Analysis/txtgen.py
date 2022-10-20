import pandas as pd
df =pd.read_csv('E:\Blackcoffee\Textanalysis\Textanalysis\spiders\content.csv')
for i in range((len(df.index))):
    f = open(f"E:\Blackcoffee\Textanalysis\Textanalysis\\txt_files\{i+1}.txt",'w',encoding="utf-8")
    f.write(str(df.values[i][0]))
    f.write("\n"+str(df.values[i][1]))
    i=+1
print("Files Generated")