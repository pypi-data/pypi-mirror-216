# dbutils

使用方法
```python
from zcb_dbutils import DBConnection
dbconn = DBConnection(host='localhost', port=3306, user='root', password='', database='mysql')

# 查询单条数据
row = dbconn.fetch_one('select * from table limit 1')
# 查询多条数据
rows = dbconn.fetch_rows('select * from table')
```