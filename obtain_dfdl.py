#!/usr/bin/python
#coding=utf-8
import pymysql
from mock_login import *
import xlrd
import numpy as np



def getConn(db):
	conn= pymysql.connect(
		host='112.74.52.18',
		port = 50070,
		user='root',
		passwd='skdfhksdhfsjhfkjhdkwtnmrentmer',
		db =db,
		charset="utf8"
		)
	return conn
def execBatch(url):
	conn=getConn('credit')
	cur = conn.cursor()
	#从指定网页爬取配置模板中数据
	#批量插入爬取的数据
	c=obtain_dfdl(url)

	try:
		cur.executemany("REPLACE into datum_customer_ele_fee(credit_ele_table_id,ele_date,ele_fee,fee_compare,ele_amount,ele_amount_compare) values(%s,%s,%s,%s,%s,%s)",c)
		conn.commit()
	except Exception as err:
		print(err)
	finally:
		cur.close()
		conn.close()
def obtain_db():
        db_account = []
        conn=getConn('credit')
        cur = conn.cursor()
        #从指定网页爬取配置模板中数据
        #批量插入爬取的数据
        try:
                cur.execute("select credit_ele_table_id,ele_table_no from datum_customer_ele_table")
                results = cur.fetchall()
                print("length results=%s" % len(results))
                for row in results:
                    value=(row[0],row[1])
                    db_account.append(value)
                conn.commit()
        except Exception as err:
                print(err)
        finally:
                cur.close()
                conn.close()
        return db_account
def obtain_dfdl_from_excel():
    arr=[]
    db_account=obtain_db()
    export_dldf(db_account)
    print("len-db-count=%s"%len(db_account))
    for i in range(len(db_account)):
        #excel_path=path+"/excel/"+item[1]+"-"+item[0]+".xls"
        item=db_account[i]
        excel_path = path + "/excel/" + item[1] + ".xls"
        print("excel_path=%s"%excel_path)
        workbook = xlrd.open_workbook(excel_path)
        data_sheet = workbook.sheets()[0]
        rowNum=data_sheet.nrows
        for i in range(2,rowNum):
            print("i=%s"%i)
            if len(data_sheet.cell_value(i, 0))==6:
                value = (item[0],data_sheet.cell_value(i, 0), data_sheet.cell_value(i, 1), data_sheet.cell_value(i, 2),
                         data_sheet.cell_value(i, 3), data_sheet.cell_value(i, 4))
                arr.append(value)

    print("arr=%s"% len(arr))
    return arr
def export_dldf(db_account):
    #db_account=obtain_db()
    for item in db_account:
        print(item[1])
        exportExcel("https://95598.gz.csg.cn/df/dldffx.do",item[1])

def obtain_dfdl(url):
    db_account=obtain_db()
    print("len-db-count=%s"%len(db_account))
    a = np.array([("0","0","0","0","0","0")])
    c=a
    for i in range(len(db_account)):
        #excel_path=path+"/excel/"+item[1]+"-"+item[0]+".xls"
        item=db_account[i]
        arr_r=obtain_from_html(url,item[1],item[0])
        if len(arr_r)>0:
            b = np.array(arr_r)
            c = np.concatenate((c, b), axis=0)
    print("arr=%s"% len(c))
    return c.tolist()

if __name__ == '__main__':
    #obtain_dfdl_from_excel()
    # 半自动处理用电数据
    execBatch("https://95598.gz.csg.cn/df/dldffx.do")
