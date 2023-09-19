import pandas
weather = pandas.read_csv('weather.csv')
print(weather)

str1="-"
dict_item_id = {}
dict_temp = {}
a=[]
b=[]
province_average=0

for i in range(len(weather)):
    dict_item_id[i] = weather["fullName"][i]
    dict_temp[i] = weather["temperature"][i]
    line=dict_item_id[i][dict_item_id[i].index(str1)+1:]
    print(line[:line.index(str1)] + str(dict_temp[i]))
    a.append(line[:line.index(str1)])
    b.append(dict_temp[i])

done={'province':a,'temperature':b}
dataframe = pandas.DataFrame(done,columns = ['province','temperature'])#columns自定义列的索引值
dataframe.to_csv('done.csv')

print("处理完毕")
