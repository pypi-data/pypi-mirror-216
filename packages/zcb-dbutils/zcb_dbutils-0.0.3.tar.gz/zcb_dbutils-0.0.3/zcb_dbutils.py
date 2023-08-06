# -*- coding: utf-8 -*-
# @Author: zhangcb
# @Date:   2020-03-31 09:10:04
# @Last Modified by:   zhangcb
# @Last Modified time: 2020-03-31 10:26:03

import pymysql


class DBConnection:

    def __init__(self, host, port, user, password, database, charset='utf8'):
        self.database = database
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def exec_sql_file(self, file):
        fd = open(file, 'r', encoding='utf-8')
        sql = fd.read()
        fd.close()
        sqlCommands = sql.split(";\n")

        for command in sqlCommands:
            try:
                self.cursor.execute(command)
                self.conn.commit()
            except Exception as msg:
                print(file, msg)
                return False
        return True

    def exec_sql(self, command):
        try:
            self.cursor.execute(command)
            return True;
        except Exception as msg:
            print(msg)
            return False

    def fetch_one(self, sql, args=None):
        try:
            r = self.cursor.execute(sql, args)
            result = self.cursor.fetchone()
            return result;
        except Exception as msg:
            print(msg)
            return False

    def fetch_rows(self, sql, args=None):
        try:
            r = self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            return result;
        except Exception as msg:
            print(msg)
            return False

    def showtable(self, database, table_name):
        with self.conn.cursor() as cursor:
            sqllist = '''
                    select aa.COLUMN_NAME,
                    aa.DATA_TYPE,aa.COLUMN_COMMENT, cc.TABLE_COMMENT, aa.COLUMN_TYPE
                    from information_schema.`COLUMNS` aa LEFT JOIN 
                    (select DISTINCT bb.TABLE_SCHEMA,bb.TABLE_NAME,bb.TABLE_COMMENT 
                    from information_schema.`TABLES` bb ) cc  
                    ON (aa.TABLE_SCHEMA=cc.TABLE_SCHEMA and aa.TABLE_NAME = cc.TABLE_NAME )
                    where aa.TABLE_SCHEMA = '%s' and aa.TABLE_NAME = '%s';
                    ''' % (database, table_name)
            cursor.execute(sqllist)
            result = cursor.fetchall()
            td = [
                {
                    'Field': i[0],
                    'TypeName': i[1],
                    'Comment': i[2],
                    'Type': i[4],
                } for i in result
            ]
        return td

    def show_table_indexs(self, database, table_name):
        with self.conn.cursor() as cursor:
            sqllist = '''
            select aa.INDEX_ID, aa.`NAME`,aa.TYPE,group_concat(cc.`NAME` order by cc.POS) from information_schema.INNODB_SYS_INDEXES aa left JOIN information_schema.`INNODB_SYS_TABLES` bb on aa.TABLE_ID = bb.TABLE_ID left join information_schema.INNODB_SYS_FIELDS cc on aa.INDEX_ID = cc.INDEX_ID where aa.TYPE != 1 and bb.`NAME` = '%s/%s' group by cc.INDEX_ID order by cc.POS;
            ''' % (database, table_name)
            cursor.execute(sqllist)
            result = cursor.fetchall()
            td = [
                {
                    'id': i[0],
                    'name': i[1],
                    'type': i[2],
                    'fields': i[3]
                } for i in result
            ]
        return td

