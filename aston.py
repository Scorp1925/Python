import pandas as pd

#Создадим DataFrame

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'Karl', 'Nina'],
    'Age': [25, 30, 35, 40, 45],
    'Salary': [50000, 55000, 60000, 65000, 70000]
}
df = pd.DataFrame(data)

#Увеличение возраста на 1 год
df['Age'] = df['Age'] + 1
print("После увеличения возраста")
print(df)