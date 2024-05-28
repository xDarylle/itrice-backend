import pandas as pd
import re

df = pd.read_csv("data/iloilo_old.csv")
data = []

for index, row in df.iterrows():
    date = row['date']
    irrigated = row['irrigated']
    rainfeed = row['rainfeed']
    seed_type = row['seed_type']

    month = re.search(r"\w+", date).group()
    day = re.search(r"\d+ - \d+",  date).group().split(" ")
    min_day = int(day[0])
    max_day = int(day[2])

    for i in range (min_day, max_day + 1):
        n = (max_day + 1)  - min_day
        date = month + " " + str(i) + " 2023"
        irrigated_ave = irrigated / n
        rainfeed_ave = rainfeed / n
        row = [date, irrigated_ave, rainfeed_ave, seed_type]
        print(row)
        data.append(row)

new_df = pd.DataFrame(data, columns=['date', 'irrigated', 'rainfeed', 'seed_type'])
new_df.to_csv("data/iloilo.csv", index=False)



