import sqlite3
def sqliteTocsv(src):
    mydb = sqlite3.connect(src)  # 链接数据库
    cur = mydb.cursor()  # 创建游标cur来执行SQL语句

    # 获取表名
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    Tables = cur.fetchall()  # Tables 为元组列表

    for i in range(0,len(Tables)):
        # it = it[0]
        tbl_lis = []
        tbl_name = Tables[i][0]
        csvfile = getdir(src) + '/' + str(tbl_name) + ".csv"
        # 获取表的列名
        cur.execute("SELECT * FROM {}".format(tbl_name))
        col_name_list = [tuple[0] for tuple in cur.description]
        pprint.pprint(col_name_list)
        tbl_lis.append(col_name_list)

        data = cur.execute("SELECT * FROM "+str(tbl_name))

        for line in list(data):
            tbl_lis.append(list(line))
        csvdump(tbl_lis, csvfile)
