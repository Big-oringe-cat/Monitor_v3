# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import datetime


def chart(req):

    first_day=req.REQUEST.get('first_day','')
    end_day=req.REQUEST.get('end_day','')
    if first_day == "" or end_day == "":
        end_day=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        first_day= (datetime.datetime.now() - datetime.timedelta(days = 10))
        first_day = first_day.strftime("%Y-%m-%d")
    sql="select left(insert_time,10),count(*) from notice_info where insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1" 
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    table_list=[]
    for row in cur:
        table_list.append({'insert_time':row[0],'count':row[1]})

    sql1="select left(insert_time,10),count(*) from  notice_info b,monitor_info a where  a.sn=b.monitor_sn and a.monitor_type=0 and b.insert_time > '"+first_day+"'  and b.insert_time <= '"+end_day+" 23:59:59' group by 1" 
    conn1,cur1=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur1,sql1)
    ShareMethod.views.connClose(conn1,cur1)
    table_list1=[]
    for row1 in cur1:
        table_list1.append({'insert_time':row1[0],'count':row1[1]})

    sql2="select left(insert_time,10),count(*) from  notice_info b,monitor_info a where  a.sn=b.monitor_sn and a.monitor_type=1 and b.insert_time > '"+first_day+"'  and b.insert_time <= '"+end_day+" 23:59:59' group by 1" 
    conn2,cur2=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur2,sql2)
    ShareMethod.views.connClose(conn2,cur2)
    table_list2=[]
    for row2 in cur2:
        table_list2.append({'insert_time':row2[0],'count':row2[1]})

#    sql3="select substring_index(alarm_uname,',',1) as 进展为空,count(*) as 数量 from notice_info where reason is null and insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59'  group by 1 order by 2 desc" 
#    conn3,cur3=ShareMethod.views.connDB()
#    ShareMethod.views.exeQuery(cur3,sql3)
#    ShareMethod.views.connClose(conn3,cur3)
#    table_list3=[]
#    for row3 in cur3:
#        table_list3.append({'alarm_uname':row3[0],'count':row3[1]})

#    sql4="select substring_index(alarm_uname,',',1) as 进展为空,count(*) as 数量 from notice_info where is_recover=0  and ignore_identifier=0 and insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1 order by 2 desc" 
#    conn4,cur4=ShareMethod.views.connDB()
#    ShareMethod.views.exeQuery(cur4,sql4)
#    ShareMethod.views.connClose(conn4,cur4)
#    table_list4=[]
#    for row4 in cur4:
#        table_list4.append({'alarm_uname':row4[0],'count':row4[1]})

    sql5="select comment,count(*) as 数量 from notice_info where is_recover=0  and insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1 order by 2 desc" 
    conn5,cur5=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur5,sql5)
    ShareMethod.views.connClose(conn5,cur5)
    table_list5=[]
    for row5 in cur5:
        table_list5.append({'comment':row5[0],'count':row5[1]})

    sql6="select note_taker,count(*) as 数量 from notice_info where is_recover=1  and insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1 order by 2 desc" 
    conn6,cur6=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur6,sql6)
    ShareMethod.views.connClose(conn6,cur6)
    table_list6=[]
    for row6 in cur6:
        table_list6.append({'alarm_uname':row6[0],'count':row6[1]})

#    sql7="select substring_index(alarm_uname,',',1) as 进展为空,count(*) as 数量 from notice_info where is_recover=0  and ignore_identifier=1 and insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1 order by 2 desc" 
#    conn7,cur7=ShareMethod.views.connDB()
#    ShareMethod.views.exeQuery(cur7,sql7)
#    ShareMethod.views.connClose(conn7,cur7)
#    table_list7=[]
#    for row7 in cur7:
#        table_list7.append({'alarm_uname':row7[0],'count':row7[1]})
    sql8="select alarm_uname,count(*) as 数量 from notice_info where is_recover=0 and reason is Null and ignore_identifier=0  group by 1 order by 2 desc" 
    conn8,cur8=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur8,sql8)
    ShareMethod.views.connClose(conn8,cur8)
    table_list8=[]
    for row8 in cur8:
        table_list8.append({'alarm_uname':row8[0],'count':row8[1]})
    sql9="select alarm_uname,count(*) as 数量 from notice_info where is_recover=0 and reason is not Null and ignore_identifier=0  and  comment!='余额预警' group by 1 order by 2 desc" 
    conn9,cur9=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur9,sql9)
    ShareMethod.views.connClose(conn9,cur9)
    table_list9=[]
    for row9 in cur9:
        table_list9.append({'alarm_uname':row9[0],'count':row9[1]})
    return render_to_response('chart.html',locals())

def alarm_statistics(req):
    first_day=req.REQUEST.get('first_day','')
    end_day=req.REQUEST.get('end_day','')

    if first_day == "" or end_day == "":
        end_day=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        first_day= (datetime.datetime.now() - datetime.timedelta(days = 10))
        first_day = first_day.strftime("%Y-%m-%d")
    sql="select comment,sum(alarm_amount) as count from notice_info where insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1 order by 2 desc limit 10"
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    table_list=[]
    for row in cur:
        table_list.append({'comment':row[0],'count':row[1]})

    sql1="select comment,count(*) as count from notice_info where insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59' group by 1 order by 2 desc limit 10"
    conn1,cur1=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur1,sql1)
    ShareMethod.views.connClose(conn1,cur1)
    table_list1=[]
    for row1 in cur1:
        table_list1.append({'comment':row1[0],'count':row1[1]})
    return render_to_response('alarm_statistics.html',locals())

def select(req):
    first_day=req.REQUEST.get('first_day','')
    end_day=req.REQUEST.get('end_day','')
    if first_day == "" or end_day == "":
        end_day=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        first_day= (datetime.datetime.now() - datetime.timedelta(days = 10))
        first_day = first_day.strftime("%Y-%m-%d")
    session_tmp = req.session
    for key, value in session_tmp.items():
        print ("session----------->"+key + ' : ' + str(value))
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))

    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    alarmtype=req.REQUEST.get('name').strip()
    sql= "select * from notice_info where comment like '%"+alarmtype+"%' and comment!='余额预警' and insert_time > '"+first_day+"'  and insert_time <= '"+end_day+" 23:59:59'"
    sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=0 and reason is not null and ignore_identifier=0 and comment!='余额预警'"
    print ("ere",sql)

    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    if(search=='alarm_value'):
        sql += " and alarm_uname like '"+ value +"%'"
        sql2 += " and alarm_uname like '"+ value +"%'"
    if(search=='monitor_level'):
        if(value=='紧急'):
            sql += " and monitor_level like '0' "
            sql2 += " and monitor_level like '0' "
        elif(value=='重要'):
            sql += " and monitor_level like '1' "
            sql2 += " and monitor_level like '1' "
        elif(value=='一般'):
            sql += " and monitor_level like '2' "
            sql2 += " and monitor_level like '2' "
        else:
            sql += " and monitor_level like '%" + value + "%'"
            sql2 += " and monitor_level like '%" + value + "%'"
    if(search=='recover'):
        if(value=='恢复'):
            sql += " and is_recover like '1' "
            sql2 += " and is_recover like '1' "
        elif(value=='未恢复'):
            sql += " and is_recover like '0' "
            sql2 += " and is_recover like '0' "
        else:
            sql += " and is_recover like '%" + value + "%'"
            sql2 += " and is_recover like '%" + value + "%'"
    if(search=='status'):
        if(value=='已发送'):
            sql += " and status like '1' "
            sql2 += " and status like '1' "
        elif(value=='未发送'):
            sql += " and status like '0' "
            sql2 += " and status like '0' "
        else:
            sql += " and status like '%" + value + "%'"
            sql2 += " and status like '%" + value + "%'"
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            pass
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
        sql += " order by update_time desc "
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)

    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination2(sql, pageType, curPage, allPostCounts)

    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    conn2,cur2=ShareMethod.views.connDB()
    deal = ""
    monitor_sn=""
    for row in cur:
        sql2="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur2,sql2)
        for row2 in cur2:
            deal=row2[0]
            monitor_sn=row2[1]
        alarm_uname=row[15].split(',')
        if len(alarm_uname) == 1:
            alarm_uname2=""
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19])})
        elif len(alarm_uname) == 2:
            alarm_uname2=""
            alarm_uname2=alarm_uname[1]
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19])})
        else:
            alarm_uname2=[]
            for i in range(1,(len(alarm_uname))):
                alarm_uname2.append(alarm_uname[i])
            alarm_uname2=','.join(alarm_uname2)
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19])})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('alarm_details.html',locals())

def alarm_detail(req):
    id=req.REQUEST.get('id',0)
    sn=req.REQUEST.get('sn','0')
    print('whello',sn)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from monitor_info where sn="+id)
    sql="select comment from monitor_info where sn='" +id+"'"
    sql2="select content from notice_info where sn="+sn
    print ('whello ',sql2)
    conn1,cur1=ShareMethod.views.connDB()  
    ShareMethod.views.exeQuery(cur1,sql)
    conn2,cur2=ShareMethod.views.connDB()  
    ShareMethod.views.exeQuery(cur2,sql2)
    ShareMethod.views.connClose(conn,cur) 
    ShareMethod.views.connClose(conn1,cur1)
    ShareMethod.views.connClose(conn2,cur2) 
    commentList=[]
    for row in cur1:
        commentList.append({'comment':row[0]})
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'monitor_command':row[1],'warning_content':row[2],'comment':row[3],'monitor_type':row[4],'expect_result':row[5],'monitor_level':str(row[6]),'alarm_count':row[7],'alarm_frequency':row[8],'alarm_time':row[9],'deal_way':row[10],'sensitivity':row[11]})
    print(table_list)
    contentList=[]
    for row in cur2:
        contentList.append({'alarm_content':row[0]})
    print("whello",contentList)
    return render_to_response('monitor_info_detail.html',{'table_list':table_list,'commentList':commentList,'contentList':contentList})

