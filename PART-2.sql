/*2-1 search document by title, id , publisher*/
/*Search by title*/
SELECT 
    DOCID, TITLE, p.pubname
FROM
    document d,
    publisher p
WHERE
    d.publisherid = p.publisherid
        AND title LIKE '%internet%'
ORDER BY docid
;

/*Search by DOCID*/
SELECT 
    DOCID, TITLE, p.pubname
FROM
    document d,
    publisher p
WHERE
    d.publisherid = p.publisherid
        AND Docid LIKE '1002'
ORDER BY docid
;
/*Search by Publisher's name*/

SELECT 
    d.DOCID, d.TITLE, p.pubname, c.copyno, c.libid, br.Lname, c.copyPosition
FROM
    document d, publisher p, copy c, branch br
WHERE d.publisherid = p.publisherid
  AND d.docid = c.docid
  AND c.libid = br.libid
  AND p.pubname LIKE '%publishing%'
ORDER BY d.docid , c.copyno

;

/*2-2 Document Check out*/

insert into borrows(Readerid,docid,copyno,libid,BDTIME) 
select '1', c.docid, c.copyno, c.libid, now() 
from copy c 
where c.docid='1001' 
and c.copyno='10001'
and c.libid='1'
and not exists(
				SELECT 
				*
                FROM copy c
                LEFT JOIN  borrows b 
                     ON c.docid = b.docid
                     AND c.copyno = b.copyno
                     AND c.libid = b.libid
                WHERE c.docid = '1001' AND c.copyno = '10001'
                  AND c.libid = '1'
                  and b.bdtime IS NOT NULL 
                  AND b.rdtime IS NULL  
                )
and not exists ( select * 
				 from copy c
				LEFT JOIN reserves r 
                     ON c.docid = r.docid
                     AND c.copyno = r.copyno
                     AND c.libid = r.libid
                 where c.docid='1001'
                   and c.copyno='10001'
                   and c.libid='1'
                   and date(r.dtime) =curdate()
				 )
;

/* return document*/
update borrows
set rdtime = now() 
where readerid='1' and docid='1001' and copyno='10001' and libid='1' and rdtime is null

;

/* reserve document */
insert into reserves(readerid, docid, copyno, libid, dtime)
select '1', '1001', '10001','1', sysdate()
from dual
where not exists ( select *  from copy c
                   left join borrows b  
	                      on c.docid=b.docid
						and c.copyno=b.copyno
                        and c.libid=b.libid
				   where c.docid='1001'
                     and c.copyno='10001'
                     and c.libid='1'
                     and bdtime is not null
                     and rdtime is null
                     )
and not exists (select readerid from reserves
                where readerid='1' and date(dtime)=curdate()
                group by readerid
                having count(docid)>10)
and not exists (select * from reserves 
				where docid='1001'
                  and copyno='10001'
                  and libid='1'
                  and readerid='1'
                  and date(dtime)= curdate())
;

/*compute the fine*/


select a.docid, SUM(lateness*0.2)  fine
  from 
	  (select docid, 
			case when rdtime is null and datediff(curdate(),BDtime)-20 < 0 then 0
                 when rdtime is null then datediff(curdate(),BDtime)-20
                 when datediff(rdtime,BDtime)-20 < 0 then 0
				 else datediff(rdtime,BDtime)-20 end as lateness 
	   from borrows b
	   where readerid ='12320') a
    group by docid


;
/*print the list of document reserve by reader and their status*/

select r.docid, d.title, r.copyno, r.libid, re.rname,  
	   case when b.bdtime is not null and b.rdtime is null then 'Borrowed' else 'Not Borrowed' end Statue 
from reserves r
left join document d
on r.docid=d.docid
left join reader re
on r.readerid=re.readerid
left join (select docid,copyno, libid, MAX(BDTIME) BDTIME,
			case when MAX(RDTIME)<MAX(BDTIME) then null else MAX(RDTIME) end RDTIME 
            from BORROWS
			group by docid,copyno, libid)  b
on  r.docid=b.docid
and r.copyno=b.copyno
and r.libid=b.libid
where re.readerid=r.readerid

order by r.resumber desc
;

/*Print the document id and document titles of documents published by a publisher*/
select docid, title, pubname from document d, publisher p
where d.publisherid=p.publisherid
order by d.docid
;


