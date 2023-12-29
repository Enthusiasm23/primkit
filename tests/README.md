# primkit 测试

## 引物设计

1. 获取 header、cookie、token 连接信息
```python
url = "https://mfeprimer3.igenetech.com/muld"

# method 包括 requests 和 selenium
headers, cookies, token = primkit.fetch_web_data(url, method='requests')     
```

2. 设置引物设计参数
```python
bed_input = "chr7\t55249070\t55249073\nchr22\t42538507\t42538510..."

PRIMER_PARAMS = {
    'DB': 'hg19.fa',        # hg19.fa/mm10.fa
    'SnpFilter': 'yes',     # yes/no
    'PrimerMinSize': '17',  # 15-35
    'PrimerOptSize': '22',  # 15-35
    'PrimerMaxSize': '25',  # 15-35
    'PrimerMinTm': '58',    # 0-100
    'PrimerOptTm': '60',    # 0-100
    'PrimerMaxTm': '62',    # 0-100
    'ProdMinSize': '80',    # 0-1000000
    'ProdMaxSize': '120',   # 0-1000000
    'DimerScore': '5',      # 3-20
    'HairpinScore': '5',    # 3-20
    'Tm': '47',             # 0-100
    'SpecMinSize': '0',     # 0-1000000
    'SpecMaxSize': '500',   # 0-1000000
}

# 默认参数为 PRIMER_PARAMS， 可传入 custom_params 修改或是添加
post_data = primkit.prepare_post_data(token, bed_input, custom_params={'PrimerMinSize': '15'}, default_params=PRIMER_PARAMS)
```

3. 设计引物，返回下载链接
```python
# 使用 requests 方法
down_url = primkit.design_primers(post_data, method='requests', headers=headers, cookies=cookies)

# 使用 selenium 方法
down_url = primkit.design_primers(post_data, method='selenium')
```

4. 下载引物结果
```python
# 目前仅支持下载为 csv文件
file_path = 'test.csv'
primkit.download(down_url, 'test.csv')
```

5. 读取引物结果
```python
file_reader = primkit.FileReader()
df = file_reader.read_csv(file_path)
```

## 数据库处理

1. 初始化数据库
```python
# 如果数据库 test_db 不能存在会自动创建
db_handler = primkit.DatabaseHandler('mysql+pymysql://root:root@localhost/test_db')
```

2. 初始化数据表
```python
# 利用列表的形式先去检查表是否存在，如果不存在会根据传入列名创建
db_handler.setup_table('test_table', df.columns.to_list())
```

3. 创建数据表
```python
# 除了上述的 setup_table() 可以创建数据表以外，还提供了一下2种方式创建

# 根据列表中列名创建（但是不建议，因为创建的数据仅为varchar类型）
db_handler.create_table('test_table', df.columns.to_list())

# 推荐使用传入 dataframe 去创建表格，会自动根据 dataframe的数据列类型创建
db_handler.create_df_table('test_table', df)
```

4. 插入数据
```python
# 直接通过 dataframe 插入，使用的是 pandas 的 to_sql() 方法
db_handler.insert_df(table_name, df)

# 使用字典的形式插入，需要将空值转换
df = df.where(pd.notnull(df), None)
data_dicts = df.to_dict(orient='records')
db_handler.insert_data(table_name, data_dicts)
```

5. 获取 engine 或 connect
```python
# DatabaseHandler 也内置了返回 engine 实例对象，有更多的自定义选择
engine = db_handler.get_engine()

# 直接获取engine的连接器（不建议，因为没有显示关闭，可获取engine再连接，使用上下文管理关闭）
con = db_handler.connect_db()

# 比如插入数据
df.to_sql(table_name, con=engine, if_exists='append', index=False)
```

6. 查询数据
```python
# 根据 sql 语句查询
query = 'SELECT * FROM test_table'
result = db_handler.execute_query(query)
result.fetchall()
result.keys()

# 使用 pandas 的 read_sql() 方法查询
query = 'SELECT * FROM test_table'
engine = db_handler.get_engine()
df = pd.read_sql(query, engine)
```

## 邮件监控
```python
# host、port、user、password 必须参数，from 默认是 user，from_alias 默认 user@前缀
config = {
    'host': 'smtp.exmail.qq.com',
    'port': 465,
    'user': 'user',
    'password': 'password',
    'from': 'user',  # Optional
    'from_alias': 'user_name',  # Optional
}

# 包含2种连接方法，
# 1. 使用 yagmail 库，需要安装 yagmail 库，推荐使用
email_manager = primkit.EmailManager(config, use_yagmail=True)

# 2. 使用 smtplib 库，需要安装 smtplib 库，默认使用 ssl，即 use_ssl=True
email_manager = primkit.EmailManager(config)

# 测试连接
email_manager.test_conn()

# 发送邮件
email_manager.send_email(to_addrs=['lbfeng23@gamil.com'], subject='test', message='test', attachments=['test.csv', 'test.txt'])

# 检查邮件发件箱，使用 IMAPClient 库，目前测试阶段，并不完善，不建议使用
email_manager.check_sent(subject='test')
```

## 还有更多，敬请期待 ···