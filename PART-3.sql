/*phase 3-1 Insert a new copy*/
INSERT INTO  COPY(DOCID,COPYNO,LIBID,COPYPOSITION) 
VALUES (1022,10051,7,'101A03');

/*phase 3-2 List document's copy and it's position and statue */
SELECT c.docid, c.COPYNO,c.libid, c.COPYPOSITION, r.DTIME, b.BDTIME, b.RDTIME   
FROM COPY c
left join  (select docid,copyno, libid, MAX(DTIME) DTIME from RESERVES
            group by docid,copyno, libid) r
on c.docid=r.docid
and c.copyno=r.copyno
and c.libid=r.libid
left join  (select docid,copyno, libid, MAX(BDTIME) BDTIME,
			case when MAX(RDTIME)<MAX(BDTIME) then null else MAX(RDTIME) end RDTIME 
            from BORROWS
			group by docid,copyno, libid) b 
on c.docid=b.docid
and c.copyno=b.copyno
and c.libid=b.libid
WHERE c.docid='1002'
;
 
/*phase 3-3 Insert a new reader*/
INSERT INTO READER (RTYPE,RNAME,ADDRESS)
VALUES ('Student','Michelle.E.Willams','702 NE Fulton Road Miamisburg,OH 45342');

/*phase3-4 List all Branch information*/
SELECT LNAME, LLOCATION
FROM branch;

/*phase3-5 List top 10 Borrower for some branch */
SELECT * FROM
    (SELECT 
        (@rownum:=@rownum + 1) num, R1.*
    FROM
        (SELECT 
        R.READERID, R.RNAME, COUNT(B.BORNUMBER) BN
         FROM READER AS R, BORROWS AS B
         WHERE R.READERID = B.READERID
		   AND B.LIBID = '1'
         GROUP BY R.READERID) AS R1, 
		(SELECT (@rownum:=0)) AS R2
    ORDER BY BN DESC) TOP
WHERE TOP.num <= 10
;

/*phase 3-6 List Top 10 Documents for some branch*/
SELECT * FROM
    (SELECT 
        (@rownum:=@rownum + 1) num, R1.*
    FROM
        (SELECT 
		  D.DOCID, D.TITLE, COUNT(B.BORNUMBER) BN
         FROM DOCUMENT AS D, BORROWS AS B
         WHERE D.DOCID = B.DOCID
		   AND B.LIBID = '1'
         GROUP BY D.DOCID, D.TITLE) AS R1, 
		(SELECT (@rownum:=0)) AS R2
    ORDER BY BN DESC) TOP
WHERE TOP.num <= 10;

/*phase3-7 List Top 10 Books of the year*/

SELECT * FROM
    (SELECT 
        (@rownum:=@rownum + 1) num, R1.*
    FROM
        (SELECT 
		  D.DOCID, D.TITLE, COUNT(B.BORNUMBER) BN
         FROM DOCUMENT AS D, BORROWS AS B
         WHERE D.DOCID = B.DOCID
		   AND YEAR(B.BDTIME) = '2019'
         GROUP BY D.DOCID, D.TITLE) AS R1, 
		(SELECT (@rownum:=0)) AS R2
    ORDER BY BN DESC) TOP
WHERE TOP.num <= 10;

/*phase3-8* Total fined reader and average fine*/
select count(readerid) avg_reader,avg(fine) avg_fine 
from(
     select a.readerid , SUM(lateness*0.2) AS fine
	 from 
	     (select b.readerid, 
				 case when rdtime is null and datediff(curdate(),BDtime)-20 < 0 then 0
                      when rdtime is null then datediff(curdate(),BDtime)-20
                      when datediff(rdtime,BDtime)-20 < 0 then 0
				      else datediff(rdtime,BDtime)-20 end as lateness 
		  from borrows b
	      ) a 
      group by a.readerid
      having SUM(lateness*0.2)>0
      ) f
;



/**/