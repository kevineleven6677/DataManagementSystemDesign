import mysql.connector
libraryconn=mysql.connector.connect(user='root',password='Iamkevin67',host='localhost',database='citylibrary')
acctconn=mysql.connector.connect(user='root',password='Iamkevin67',host='localhost',database='accounts_cardnumbers')
#,auth_plugin='mysql_native_password'
libcursor=libraryconn.cursor()
acctcursor=acctconn.cursor()

#libcursor.execute("select * from Document") for library 
#acctcursor.execute("select * from Document")for acct 

#print(libcursor.fetchall())          for library 
#print(acctcursor.fetchall())          for acct 

def mainmenu():
    print("Welcome to the public library system database.")
    print("1. Reader menu")
    print("2. Administrative Menu")
    print("3. Quit" )
    selection=int(input("Enter a number:"))
    return selection


def readermenu():#menu for readers

    print(" Reader menu")
    print("1. Search a document by ID, title, or publisher name")
    print("2. Compute fine for a document copy borrowed by a reader based on the current date")
    print("3. Print the list of documents reserved by a reader and their status")
    print("4. Print the document id and document titles of documents published by a publisher.")
    print("5. Quit.")
    selection=int(input("Enter a number:"))
    return selection

def checkreturnreserve():
    print()
    #checkout doc
    #return doc
    #reserve doc
    
def adminmenu():#menu for admins to make data related adjustments

    print(" Administrative Menu")

    print("1. Add a document copy")
    print("2. Search document copy and check its status")
    print("3. Add a new reader")
    print("4. Print branch information (name and location)")
    print("5. Print top 10 most frequent borrowers in a branch and the number of books each has borrowed.")
    print("6. Print top 10 most borrowed books in a branch.")
    print("7. Print the 10 most popular books of the year")
    print("8. Find the average fine paid per reader.")
    print("9. Quit")
    selection=int(input("Enter a number:"))
    return selection  

res=0
res=mainmenu()
if res== 1:
    print("Reader Login")############Reader Authentication###########
    i=0
    while i ==0:
        card_number=input("Enter 5-digit Card Number# ")
        libcursor.execute("SELECT * from reader where readerid = " + card_number)
        cnum=libcursor.fetchall()
        if cnum == []:
            print("Incorrect Card Number#. Please Try Again.")
            i=0
        else:
            res=readermenu()
            if res == 1:
                print("Enter 1 to search a document by ID")
                print("Enter 2 to search a document by Title")
                print("Enter 3 to search a document by Publisher name")
                inp=int(input("Enter a number:"))
                if inp==1:
                    doc_id=input("Enter 4-digit Document ID: ")
                    libcursor.execute("SELECT d.DOCID, d.TITLE, p.pubname,c.copyno,c.libid,br.Lname, c.copyPosition FROM document d, publisher p,copy c,branch br WHERE d.publisherid = p.publisherid AND d.docid=c.docid AND c.libid=br.libid AND d.Docid LIKE '"+doc_id+"'ORDER BY d.docid, c.copyno") 
                    rows=libcursor.fetchall()
                    for row in rows:
                        print(row)
                    print('1.Checkout this document')
                    print('2.Return this document')
                    print('3.Reserve this document')
                    inp2=int(input("Enter the selection:"))
                    if inp2==1:
                        
                        lib_id=input("Checkout from(Number of Library):")
                        copy_no= input("Which Copy:")
                        libcursor.execute("insert into borrows(Readerid,docid,copyno,libid,BDTIME)  select "+card_number+", c.docid, c.copyno, c.libid, now() from copy c where c.docid="+doc_id+" and c.copyno="+copy_no+" and c.libid="+lib_id+" and not exists( SELECT 	* FROM copy c LEFT JOIN  borrows b ON c.docid = b.docid AND c.copyno = b.copyno  AND c.libid = b.libid WHERE c.docid = "+doc_id+" AND c.copyno = "+copy_no+" AND c.libid = "+lib_id+" and b.bdtime IS NOT NULL AND b.rdtime IS NULL)and not exists ( select * from copy c LEFT JOIN reserves r ON c.docid = r.docid AND c.copyno = r.copyno AND c.libid = r.libid where c.docid="+doc_id+" and c.copyno="+copy_no+" and c.libid="+lib_id+" and date(r.dtime) =curdate())")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                    elif inp2==2:
                        lib_id=input("Return from(Number of Library):")
                        copy_no= input("Which Copy:")
                        libcursor.execute("update borrows set rdtime = now() where readerid='"+card_number+"' and docid='"+doc_id+"' and copyno='"+copy_no+"' and libid='"+lib_id+"' and rdtime is null")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                    elif inp2==3:
                        lib_id=input("Reserve from(Number of Library)")
                        copy_no=input("Which Copy")
                        libcursor.execute("insert into reserves(readerid, docid, copyno, libid, dtime) select '"+card_number+"', '"+doc_id+"', '"+copy_no+"','"+lib_id+"', sysdate() from dual where not exists ( select *  from copy c left join borrows b on c.docid=b.docid	and c.copyno=b.copyno and c.libid=b.libid where c.docid='"+doc_id+"' and c.copyno='"+copy_no+"' and c.libid='"+lib_id+"' and bdtime is not null and rdtime is null ) and not exists (select readerid from reserves where readerid='"+card_number+"' and date(dtime)=curdate() group by readerid having count(docid)>10) and not exists (select * from reserves where docid='"+doc_id+"' and copyno='"+copy_no+"' and libid='"+lib_id+"' and readerid='"+card_number+"' and date(dtime)= curdate())")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                elif inp==2:
                    title=input("Enter Document Title: ")
                    libcursor.execute("SELECT d.DOCID, d.TITLE, p.pubname,c.copyno,c.libid,br.Lname, c.copyPosition FROM document d, publisher p,copy c,branch br WHERE d.publisherid = p.publisherid AND d.docid=c.docid AND c.libid=br.libid AND d.TITLE LIKE '%"+title+"%'ORDER BY d.docid, c.copyno") 
                    rows=libcursor.fetchall()
                    for row in rows:
                        print(row)
                    doc_id=input("Which book you are looking for?(DOCID)")
                    print('1.Checkout this document')
                    print('2.Return this document')
                    print('3.Reserve this document')
                    inp2=int(input("Enter the selection:"))
                    if inp2==1:
                        
                        lib_id=input("Checkout from(Number of Library):")
                        copy_no= input("Which Copy:")
                        libcursor.execute("insert into borrows(Readerid,docid,copyno,libid,BDTIME)  select "+card_number+", c.docid, c.copyno, c.libid, now() from copy c where c.docid="+doc_id+" and c.copyno="+copy_no+" and c.libid="+lib_id+" and not exists( SELECT 	* FROM copy c LEFT JOIN  borrows b ON c.docid = b.docid AND c.copyno = b.copyno  AND c.libid = b.libid WHERE c.docid = "+doc_id+" AND c.copyno = "+copy_no+" AND c.libid = "+lib_id+" and b.bdtime IS NOT NULL AND b.rdtime IS NULL)and not exists ( select * from copy c LEFT JOIN reserves r ON c.docid = r.docid AND c.copyno = r.copyno AND c.libid = r.libid where c.docid="+doc_id+" and c.copyno="+copy_no+" and c.libid="+lib_id+" and date(r.dtime) =curdate())")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                    elif inp2==2:
                        lib_id=input("Return from(Number of Library):")
                        copy_no= input("Which Copy:")
                        libcursor.execute("update borrows set rdtime = now() where readerid='"+card_number+"' and docid='"+doc_id+"' and copyno='"+copy_no+"' and libid='"+lib_id+"' and rdtime is null")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                    elif inp2==3:
                        lib_id=input("Reserve from(Number of Library)")
                        copy_no=input("Which Copy")
                        libcursor.execute("insert into reserves(readerid, docid, copyno, libid, dtime) select '"+card_number+"', '"+doc_id+"', '"+copy_no+"','"+lib_id+"', sysdate() from dual where not exists ( select *  from copy c left join borrows b on c.docid=b.docid	and c.copyno=b.copyno and c.libid=b.libid where c.docid='"+doc_id+"' and c.copyno='"+copy_no+"' and c.libid='"+lib_id+"' and bdtime is not null and rdtime is null ) and not exists (select readerid from reserves where readerid='"+card_number+"' and date(dtime)=curdate() group by readerid having count(docid)>10) and not exists (select * from reserves where docid='"+doc_id+"' and copyno='"+copy_no+"' and libid='"+lib_id+"' and readerid='"+card_number+"' and date(dtime)= curdate())")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                elif inp==3:
                    pubname=input("Enter Document's Publisher Name: ")
                    libcursor.execute("SELECT d.DOCID, d.TITLE, p.pubname,c.copyno,c.libid,br.Lname, c.copyPosition FROM document d, publisher p,copy c,branch br WHERE d.publisherid = p.publisherid AND d.docid=c.docid AND c.libid=br.libid AND p.pubname LIKE '%"+pubname+"%'ORDER BY d.docid, c.copyno") 
                    rows=libcursor.fetchall()
                    for row in rows:
                        print(row)
                    doc_id=input("Which book you are looking for?(DOCID)")
                    print('1.Checkout this document')
                    print('2.Return this document')
                    print('3.Reserve this document')
                    inp2=int(input("Enter the selection:"))
                    if inp2==1:
                        
                        lib_id=input("Checkout from(Number of Library):")
                        copy_no= input("Which Copy:")
                        libcursor.execute("insert into borrows(Readerid,docid,copyno,libid,BDTIME)  select "+card_number+", c.docid, c.copyno, c.libid, now() from copy c where c.docid="+doc_id+" and c.copyno="+copy_no+" and c.libid="+lib_id+" and not exists( SELECT 	* FROM copy c LEFT JOIN  borrows b ON c.docid = b.docid AND c.copyno = b.copyno  AND c.libid = b.libid WHERE c.docid = "+doc_id+" AND c.copyno = "+copy_no+" AND c.libid = "+lib_id+" and b.bdtime IS NOT NULL AND b.rdtime IS NULL)and not exists ( select * from copy c LEFT JOIN reserves r ON c.docid = r.docid AND c.copyno = r.copyno AND c.libid = r.libid where c.docid="+doc_id+" and c.copyno="+copy_no+" and c.libid="+lib_id+" and date(r.dtime) =curdate())")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                    elif inp2==2:
                        lib_id=input("Return from(Number of Library):")
                        copy_no= input("Which Copy:")
                        libcursor.execute("update borrows set rdtime = now() where readerid='"+card_number+"' and docid='"+doc_id+"' and copyno='"+copy_no+"' and libid='"+lib_id+"' and rdtime is null")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                    elif inp2==3:
                        lib_id=input("Reserve from(Number of Library)")
                        copy_no=input("Which Copy")
                        libcursor.execute("insert into reserves(readerid, docid, copyno, libid, dtime) select '"+card_number+"', '"+doc_id+"', '"+copy_no+"','"+lib_id+"', sysdate() from dual where not exists ( select *  from copy c left join borrows b on c.docid=b.docid	and c.copyno=b.copyno and c.libid=b.libid where c.docid='"+doc_id+"' and c.copyno='"+copy_no+"' and c.libid='"+lib_id+"' and bdtime is not null and rdtime is null ) and not exists (select readerid from reserves where readerid='"+card_number+"' and date(dtime)=curdate() group by readerid having count(docid)>10) and not exists (select * from reserves where docid='"+doc_id+"' and copyno='"+copy_no+"' and libid='"+lib_id+"' and readerid='"+card_number+"' and date(dtime)= curdate())")
                        libraryconn.commit()
                        print(libcursor.rowcount,"Success!")
                        #print("Scuesses")
                        
            elif res== 2:
                libcursor.execute("select a.docid, SUM(lateness*0.2) fine from (select docid, case when rdtime is null and datediff(curdate(),BDtime)-20 < 0 then 0 when rdtime is null then datediff(curdate(),BDtime)-20 when datediff(rdtime,BDtime)-20 < 0 then 0 else datediff(rdtime,BDtime)-20 end as lateness from borrows b where readerid ='"+card_number+"') a group by docid")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res== 3:
                libcursor.execute("select r.docid, d.title, r.copyno, r.libid, re.rname, case when b.bdtime is not null and b.rdtime is null then 'Borrowed' else 'Not Borrowed' end Statue from reserves r left join document d on r.docid=d.docid left join reader re on r.readerid=re.readerid left join (select docid,copyno, libid, MAX(BDTIME) BDTIME,	case when MAX(RDTIME)<MAX(BDTIME) then null else MAX(RDTIME) end RDTIME from BORROWS group by docid,copyno, libid) b on  r.docid=b.docid and r.copyno=b.copyno and r.libid=b.libid where re.readerid=r.readerid order by r.resumber desc")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res == 4:
                libcursor.execute("select docid, title, pubname from document d, publisher p where d.publisherid=p.publisherid order by d.docid")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res == 5:
                print()
                mainmenu()
            else:
                print("Incorrect Selection. Please Try Again.")
                readermenu()
            i=1
            
elif res == 2:
    print("Adminstrative Login")############Admin Authentication###########
    i=0
    while i == 0:
        IDs=(input("Enter ID:"))
        password=input("Enter password:")
        acctcursor.execute("SELECT ID, PASSWORD from ACCOUNTS WHERE ID =\'"+IDs+"\' AND PASSWORD=\'"+password+"\'")
        idpass=acctcursor.fetchall()
        if idpass== []:
            print ("Incorrect ID or password. Please try again.")
        else:
            res=adminmenu()
            if res ==1:
                print("Adding a document copy")
                docid=input("Enter the DOCID:")
                copyno=input("Enter the Copy No. for this document:")
                libid=input("Enter the Library ID corresponding with location:")
                cposition=input("Enter the position in the library where the document copy should be placed:")
                libcursor.execute("INSERT INTO COPY(DOCID,COPYNO,LIBID,COPYPOSITION) VALUES ("+docid+","+copyno+","+libid+",\'"+cposition+"\')")
                libraryconn.commit()
                #print(libcursor.rowcount,"Scuesses!")
                print(libcursor.rowcount,"New Document copy is now added.")
            elif res ==2:
                docid=input("To search for document copies and their statuses, please enter the document ID: ")
                libcursor.execute("SELECT c.docid, c.libid, c.COPYNO, c.COPYPOSITION, r.DTIME, b.BDTIME, b.RDTIME FROM COPY c left join  (select docid,copyno, libid, MAX(DTIME) DTIME from RESERVES group by docid,copyno, libid) r on c.docid=r.docid and c.copyno=r.copyno and c.libid=r.libid left join  (select docid,copyno, libid, MAX(BDTIME) BDTIME, case when MAX(RDTIME)<MAX(BDTIME) then null else MAX(RDTIME) end RDTIME from BORROWS group by docid,copyno, libid) b on c.docid=b.docid and c.copyno=b.copyno and c.libid=b.libid WHERE c.docid=\'"+docid+"\'")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res ==3:
                print("Adding a new reader:")
                rtype=input("Enter the type of reader:")
                rname=input("Enter the name of the reader:")
                address=input("Enter the Address :")
                libcursor.execute("INSERT INTO READER (RTYPE,RNAME,ADDRESS) VALUES (\'"+rtype+"\',\'"+rname+"\',\'"+address+"\')")
                libraryconn.commit()
                print(libcursor.rowcount,"New Reader is now added.")
                libcursor.execute("select readerid from reader where Rname='"+rname+"' and address='"+address+"' and rtype='"+rtype+"'")
                print("The New ReaderID is ",libcursor.fetchall())
            elif res ==4:
                print("Library Branches and their locations:")
                libcursor.execute("SELECT LNAME, LLOCATION FROM branch")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res ==5:
                branch=input("Which branch you want to know?")
                print("Listing top 10 most frequent borrowers in branch"+branch)
                libcursor.execute("SELECT * FROM (SELECT (@rownum:=@rownum + 1) num, R1.* FROM (SELECT R.READERID, R.RNAME, COUNT(B.BORNUMBER) BN FROM READER AS R, BORROWS AS B WHERE R.READERID = B.READERID AND B.LIBID = '1' GROUP BY R.READERID) AS R1, (SELECT (@rownum:=0)) AS R2 ORDER BY BN DESC) TOP WHERE TOP.num <= 10")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res ==6:
                branch=input("Which branch you want to know?")
                print("Listing top 10 most borrowed books in branch"+branch)
                libcursor.execute("SELECT * FROM (SELECT (@rownum:=@rownum + 1) num, R1.* FROM (SELECT D.DOCID, D.TITLE, COUNT(B.BORNUMBER) BN FROM DOCUMENT AS D, BORROWS AS B WHERE D.DOCID = B.DOCID AND B.LIBID = '1'GROUP BY D.DOCID, D.TITLE) AS R1, (SELECT (@rownum:=0)) AS R2 ORDER BY BN DESC) TOP WHERE TOP.num <= 10")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res ==7:
                year=input("Which year you want to check?")
                print("Listing top 10 most popular books of the year")
                libcursor.execute("SELECT * FROM (SELECT (@rownum:=@rownum + 1) num, R1.* FROM (SELECT D.DOCID, D.TITLE, COUNT(B.BORNUMBER) BN FROM DOCUMENT AS D, BORROWS AS B WHERE D.DOCID = B.DOCID AND YEAR(B.BDTIME) = '"+year+"'GROUP BY D.DOCID, D.TITLE) AS R1, (SELECT (@rownum:=0)) AS R2 ORDER BY BN DESC) TOP WHERE TOP.num <= 10")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res ==8:
                libcursor.execute("select count(readerid) avg_reader ,avg(fine) avg_fine from(select a.readerid , SUM(lateness*0.2) AS fine from (select b.readerid, case when rdtime is null and datediff(curdate(),BDtime)-20 < 0 then 0 when rdtime is null then datediff(curdate(),BDtime)-20 when datediff(rdtime,BDtime)-20 < 0 then 0 else datediff(rdtime,BDtime)-20 end as lateness from borrows b) a group by a.readerid having SUM(lateness*0.2)>0) f ")
                rows=libcursor.fetchall()
                for row in rows:
                    print(row)
            elif res ==9:
                exit()
            else:
                print("Incorrect Selection.")
                exit()
            i = 1

elif res == 3:
    exit()
else:
    print("Incorrect Selection. Please Try Again.")
    mainmenu()



