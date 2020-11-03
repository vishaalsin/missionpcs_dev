# import datetime
# import os
# d1 = datetime.date(2019,11,4)
# d2 = datetime.date(2020,10,20)
# diff = d2 - d1
# for i in range(diff.days + 1):
#     date = str( datetime.datetime.strftime((d1 + datetime.timedelta(i)), '%d-%m-%Y'))
#     os.system("scrapy crawl epaper -o ../../../current_affairs/"+ date + ".json -a date=\'" + str(date).replace('-','/') + '\'')

import datetime
import os

d1 = datetime.date(2019, 11, 6)
d2 = datetime.date(2020, 10, 20)
diff = d2 - d1
for i in range(diff.days + 1):
    date = str(datetime.datetime.strftime((d1 + datetime.timedelta(i)), '%d-%m-%Y'))
    os.system("python current_affairs.py \'prod\' \'" + str(date) + "\'")
