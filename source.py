import mysql.connector as mycon
con=mycon.connect(host='localhost',user='root',
passwd='Mysql@2005',database='library management system') #Connector object
#All Functions
#Function to calculate fine amount for a days
def fine_amt(a):
    '''Function to calculate fine amount for a days'''
    d={0:0,1:10,2:10,3:25,4:25,5:25,6:50,7:50,8:50,9:50,10:50}
    if a == 0:
        return 0
    elif 0<a<=2:
        return a*10
    elif 3<=a<=5:
        return 20+(a-2)*25
    elif 6<=a:
        return 20+75+(a-5)*50
#Function to Auto Update Fine Table
def auto_update_fine_table():
    '''Function to Auto Update Fine Table'''
    v=f'''select name,`Borrowed Till` from `Fine Table` where `Paid On` is null;'''
    cursor.execute(v)
    v=cursor.fetchall()
    for i in range(len(v)):
        f=f"select datediff(curdate(),'{str(v[i][1])}');"
        cursor.execute(f)
        f=cursor.fetchall()
        f=f[0][0]
        q=f"update `Fine Table` set `Days Delayed` = {f}, Amount = {fine_amt(f)} where name = '{str(v[i][0])}';"
        cursor.execute(q)
        con.commit()
#Function to authenticate a user trying to access the LMS'
def authentication():
    '''Function to authenticate a user trying to access the LMS'''
    a="select `ID No`, `Employee Password` from Staff;"
    cursor.execute(a)
    a=cursor.fetchall()
    auth={'123456':'123456','1234567':'1234567'}
    auth.update(a)
    usname=input("Please enter your ID No. to access the System:")
    if usname in '123456':
        print("Welcome Trial User (Librarian)") 
        return True,usname,'Librarian'
    elif usname == '1234567':
        print("Welcome Trial User (Manager)")
        return True,usname,'Manager'
    elif usname in auth.keys():
        q=f"select Name FROM staff where `ID No` = '{usname}';"
        z=f"select Position FROM staff where `ID No` = '{usname}';"
        cursor.execute(q)
        person=cursor.fetchall()
        cursor.execute(z)
        position=cursor.fetchall()
        print(f"User identified as {str(person[0][0])}, {str(position[0][0])}.")
        while True:
            passwrd=input(f"{str(person[0][0])} please enter your password:")
            if passwrd == auth.get(usname):
                if position[0][0] == 'Manager':
                    print("Full Access Granted!!")
                    return True,usname,'Manager'
                else:
                    print("Access Granted!!")
                    return True,usname,'Librarian'
            else:
                print("Invalid password!")
                continue
    else:
        return False,usname,'XYZ'
#Function to search a book by different ways
def booksearch():
    '''Function to search a book by different ways'''
    while True:
        hwb=input("How would you like to search a book (Name, ID, Writer, Category):")
        q="SELECT `Book Name`, `Book ID`, Writer, Category, Location FROM `Book Details`;"
        cursor.execute(q)
        abc=cursor.fetchall()
        if hwb.lower() == 'name':
            x=0    
            break
        elif hwb.lower() == 'id':
            x=1 
            break   
        elif hwb.lower() == 'writer':
            x=2 
            break 
        elif hwb.lower() == 'category':
            x=3
            break
        else:
            print("Invalid choice!!")
            continue
    book_name=str(input(f"Enter the {hwb} of book you want to search:"))
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*128}
|{"S No":^4s}|{"Books Available":^55s}|{"Book ID":^7s}|{"Writer":^25s}|{"Category":^15s}|{"Location":^15s}|
{"="*128}''')
    j=0
    for i in range(len(abc)):
        if (book_name.lower() in abc[i][x].lower()) or (book_name.lower() == abc[i][x].lower()):
            j+=1
            print(f"|{str(j):^4s}|{abc[i][0]:<55s}|{abc[i][1]:^7s}|{abc[i][2]:^25s}|{abc[i][3]:^15s}|{abc[i][4]:^15s}|",end=" ")  
            print()          
    print("="*128)
#Function to add or remove books rom the Book Details Table
def editbooks():
    '''Function to add or remove books rom the Book Details Table'''
    while True:
        hwb=input("What would you like to do with books (Add or Remove):")
        if hwb.lower() in 'add books':
            hmb=int(input("How many books would you like to enter:"))
            for i in range(hmb):
                q="select max(`S No.`) from `Book Details`;"
                cursor.execute(q)
                SNo=int(cursor.fetchall()[0][0])+1
                z='select `Book ID` from `Book Details`;'
                cursor.execute(z)
                idl=cursor.fetchall()
                L=[]
                for j in range(len(idl)):
                    L.append(idl[j][0])
                bkname=input(f"Enter the name of the book you want to enter:")
                while True:
                    bkID=input(f"Enter book ID for '{bkname}' book:")
                    if bkID in L:
                        print("Book ID already assigned to a book!!")
                        print("Please enter a new book ID")
                    else:
                        break
                writer=input(f"Enter writer/author of '{bkname}':")
                catag=input(f"Enter the category of '{bkname}':")
                location=input(f"Enter the location where '{bkname}' book is kept:")
                q=f'''insert into `Book Details`
                (`S No.`,`Book Name`, `Book ID`, Writer, Category, Location) values
                ({SNo},'{bkname}','{bkID}','{writer}','{catag}','{location}');'''
                cursor.execute(q)
                con.commit()
                print(f"Added Book {bkname} successfully!!")
                print(f"{bkname} is {SNo}th book.")
            break
        
        elif hwb.lower() in 'remove books':
            bkid=input("Enter the ID of book you want to remove:")
            z=f"select `Book Name` from `Book Details` where `Book ID`='{bkid}';"
            cursor.execute(z)
            z=cursor.fetchall()
            q=f"delete from `Book Details` where `Book ID`='{bkid}';"
            cursor.execute(q)
            con.commit()
            print(f"Removed Book '{z[0][0]}' with ID '{bkid}' successfully!!!")
            z=f"select `Book Name` from `Book Details`;"
            cursor.execute(z)
            z=cursor.fetchall()
            for i in range(len(z)):
                s=F'''\
                    UPDATE `book details` 
                    SET `S No.` = {i+1}
                    WHERE `Book Name` = '{z[i][0]}';'''
                cursor.execute(s)
                con.commit()
            break
        else:
            print("Invalid choice!!")
            continue
#Function for accessing the amount earned from memberships 
def amtmembers():
    '''Function for accessing the amount earned for memberships'''
    Q1="select *from `Amount for Membership`;"
    cursor.execute(Q1)
    Q1=cursor.fetchall()
    print(f'''
{"="*19}
|{'Tenure':^8s}|{'Amount':^8s}|
{"="*19}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^8s}|{Q1[i][1]:^8}|",end=" ")
        print()
    print("="*19)
#Function for adding and removing members 
def add_remove_members():
    '''Function for adding and removing members'''
    ad_rmv=input('''What do you want to do (Add or Remove):''')
    if ad_rmv.lower() in 'add member':
        name=input("Enter the name of the new member:")
        regid=int(input("Enter the Reg ID of the new member:"))
        moblno=input("Enter the Mobile.No of the new member:")
        tnure=input("Enter the Tenure for the new member:")
        amt=int(input("Enter the amount:"))
        srtdt=input("Enter the start date:")
        eddt=input("Enter the end date:")
        Q2=f'''insert into Memberships(Name,`Reg ID`,`Mobile Number`,Tenure, Amount, `Start Date`,`End Date` ) values
                ('{name}',{regid},'{moblno}','{tnure}',{amt},'{srtdt}','{eddt}');'''
        cursor.execute(Q2)
        con.commit()
        print(f"Added Member {regid} successfully!!!")
        Q3="select * from Memberships;"
        cursor.execute(Q3)
        Q3=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*89}
| {'Name':^16} | {'Reg ID':^6} | {"Mobile Number":^13} | {"Tenure":^6} | {"Amount":^6} | {"Start Date":^10} | {"End Date":^10} |
{"="*89}''')
        for i in range(len(Q3)):
            print(f"|{Q3[i][0]:^18}|{Q3[i][1]:^8}|{Q3[i][2]:^15}|{Q3[i][3]:^8}|{Q3[i][4]:^8}|{str(Q3[i][5]):^12}|{str(Q3[i][6]):^12}|",end=" ")
            print()
        print("="*89)
    elif ad_rmv.lower() in 'remove member':
        regid=int(input("Enter the Reg ID of the Member to remove:"))
        Q4=f"delete from Memberships where `Reg ID`={regid} "
        cursor.execute(Q4)
        con.commit()
        print(f"Removed Member {regid} successfully!!!")
        Q3="select *from Memberships;"
        cursor.execute(Q3)
        Q3=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*89}
| {'Name':^16} | {'Reg ID':^6} | {"Mobile Number":^13} | {"Tenure":^6} | {"Amount":^6} | {"Start Date":^10} | {"End Date":^10} |
{"="*89}''')
        for i in range(len(Q3)):
            print(f"|{Q3[i][0]:^18}|{Q3[i][1]:^8}|{Q3[i][2]:^15}|{Q3[i][3]:^8}|{Q3[i][4]:^8}|{str(Q3[i][5]):^12}|{str(Q3[i][6]):^12}|",end=" ")
            print()
        print("="*89)
#Function to edit the details of staffs
def edit_staff():
    '''To edit the details of staffs'''
    while True:
        name=input("What is the full name of whose profile you want to edit:")
        q1='''select name from Staff;'''
        cursor.execute(q1)
        q1=cursor.fetchall()
        t=False
        for i in q1:
            if name.lower() != i[0].lower():
                t=False
                continue
            else:
                t=True
                break
        if t:
            break
        else:
            print(f"No employee with name {name}.")
            continue

    chng_plc = input("What do you want the change(Mobile Number,ID no,Position,Salary,Employee password):")
    chng = input(f"To what do you want to change {chng_plc} to:")
    Q5=f"update Staff set `{chng_plc.title()}`='{chng}' where Name='{name.title()}'; "
    cursor.execute(Q5)
    con.commit()
    print("Updated Staff Successfully!!!")
    Q3="select * from Staff;"
    cursor.execute(Q3)
    Q3=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*109}
|{'S No.':^5}|{'Name':^18}|{"Date of Birth":^15}|{"Mobile Number":^16}|{"ID No":^9}|{"Position":^11}|{"Salary":^7}|{"Employee password":^19}|
{"="*109}''')
    for i in range(len(Q3)):
        pls=Q3[i][7]
        if Q3[i][7]==None:
            pls="Null"
        print(f"|{Q3[i][0]:^5}|{Q3[i][1]:^18}|{str(Q3[i][2]):^15}|{Q3[i][3]:^16}|{Q3[i][4]:^9}|{Q3[i][5]:^11}|{Q3[i][6]:^7}|{pls:^19}|",end=" ")
        print()
    print("="*109)
#Function to check the lending details
def lend_details():
    '''Function to check the lending details'''
    catergory = input("How would you like to access, (using Name or Reg ID):")
    if catergory.lower() in 'name' or catergory.lower() in 'reg id':
        name=input(f"Enter the {catergory.lower()} of the person:")
    else:
        pass
    name=name.title()
    Q="select * from Lendings;"
    cursor.execute(Q)
    Q=cursor.fetchall()
    l=[]
    for j in range(len(Q)):
        l.append(Q[j][0])
        l.append(str(Q[j][1]))
    if name in l:
        if catergory.lower() in "name":
            Q=f"select * from Lendings natural join Memberships where Name='{name}';"
        elif catergory.lower() in "reg id":
            Q=f"select * from Lendings natural join Memberships where `Reg ID`={int(name)};"
        cursor.execute(Q)
        Q=cursor.fetchall()
        bokid=Q[0][2]
        Q1=f"select `book name`, category, Writer from `Book details` where `Book ID`='{bokid}';"
        cursor.execute(Q1)
        Q1=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*74}
|{' Name':<16}:{Q[0][0]:<55}|
|{' Reg ID':<16}:{Q[0][1]:<55}|
|{" Book ID":<16}:{Q[0][2]:<55}|
|{" Borrowed Date":<16}:{f'{Q[0][3]}':<55}|
|{" Borrowed Till":<16}:{f'{Q[0][4]}':<55}|
|{" Mobile number":<16}:{Q[0][5]:<55}|
|{" Tenure":<16}:{Q[0][6]:<55}|
|{" Books Available":<16}:{Q1[0][0]:<55}|
|{" Category":<16}:{Q1[0][1]:<55}|
|{" Writer":<16}:{Q1[0][2].title():<55}|
{"="*74}''')
    else:
        print(f"{name} has not taken any book for lend")
#Function to display the available books in library which can be borrowed 
def disp_avai_books():
    '''Function to display the available books in library which can be borrowed'''
    q='''select `Book ID` from `Book Details`;'''
    cursor.execute(q)
    l1=list(cursor.fetchall()) #Book IDs from book details
    z='''select `Book ID` from lendings;'''
    cursor.execute(z)
    l2=list(cursor.fetchall())
    for i in range(len(l2)):
        if l2[i] in l1:
            l1.remove(l2[i])
    hwl=input("What would you like to view (All details, search the book):")
    if hwl.lower() in 'search the book':
        hwb=input("How would you like to search a book (Name, ID, Writer, Category):")
        q="SELECT `Book Name`, `Book ID`, Writer, Category, Location FROM `Book Details`;"
        cursor.execute(q)
        abc=cursor.fetchall()
        if hwb.lower() == 'name':
            x=0    
        elif hwb.lower() == 'id':
            x=1    
        elif hwb.lower() == 'writer':
            x=2  
        elif hwb.lower() == 'category':
            x=3
        else:
            pass
        book_name=str(input(f"Enter the {hwb} of book you want to search:"))
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*128}
|{"S No":^4s}|{"Books Available":^55s}|{"Book ID":^7s}|{"Writer":^25s}|{"Category":^15s}|{"Location":^15s}|
{"="*128}''')
        j=0
        for i in range(len(abc)):
            for k in range(len(l1)):
                if (abc[i][1] == l1[k][0]) and ((book_name.lower() in abc[i][x].lower()) or (book_name.lower() == abc[i][x].lower())):
                    j+=1
                    print(f"|{str(j):^4s}|{abc[i][0]:^55s}|{abc[i][1]:^7s}|{abc[i][2]:^25s}|{abc[i][3]:^15s}|{abc[i][4]:^15s}|",end=" ")  
                    print()        
        print("="*128)
    elif hwl.lower() in 'all details':
        q="SELECT `Book Name`, `Book ID`, Writer, Category, Location FROM `Book Details`;"
        cursor.execute(q)
        abc=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*128}
|{"S No":^4s}|{"Books Available":^55s}|{"Book ID":^7s}|{"Writer":^25s}|{"Category":^15s}|{"Location":^15s}|
{"="*128}''')
        j=0
        for i in range(len(abc)):
            for k in range(len(l1)):
                if (abc[i][1] == l1[k][0]):
                    j+=1
                    print(f"|{str(j):^4s}|{abc[i][0]:^55s}|{abc[i][1]:^7s}|{abc[i][2]:^25s}|{abc[i][3]:^15s}|{abc[i][4]:^15s}|",end=" ")  
                    print()
                else:
                    pass      
        print("="*128)
#Function to display details of all the borrowed books
def disp_borr_books():
    '''Function to display details of all the borrowed books'''
    q='''select `Book ID`, Name, `Borrowed Till` from Lendings;'''
    cursor.execute(q)
    l1=cursor.fetchall()
 
    q="SELECT `Book Name`, `Book ID`, Writer, Category, Location FROM `Book Details`;"
    cursor.execute(q)
    abc=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*144}
|{"S No":^4s}|{"Books Borrowed":^55s}|{"Book ID":^7s}|{"Writer":^25s}|{"Category":^15s}|{"Location":^15s}|{"Borrowed By":^15s}|
{"="*144}''')
    j=0
    for i in range(len(abc)):
        for k in range(len(l1)):
            if (abc[i][1] == l1[k][0]):
                j+=1
                print(f"|{str(j):^4s}|{abc[i][0]:^55s}|{abc[i][1]:^7s}|{abc[i][2]:^25s}|{abc[i][3]:^15s}|{abc[i][4]:^15s}|{l1[k][1]:^15s}|",end=" ")  
                print()
            else:
                pass      
    print("="*144) 
#Function to display the details of members 
def disp_mem_details():
    '''Function to display the details of members'''
    hwl=input("How would you like to see the details of the members (search or all):")
    if hwl.lower() in 'search':
        id=int(input("Enter ID of the member:"))
        q="SELECT * FROM Memberships;"
        cursor.execute(q)
        q=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*92}
|{'Name':^18s}|{'Reg ID':^8s}|{"Mobile Number":^14s}|{"Tenure":^9s}|{"Amount":^15s}|{"Start Date":^10s}|{"End Date":^10s}|
{"="*92}''')
        for i in range(len(q)):
            if id == q[i][1]:
                print(f"|{q[i][0]:^18s}|{q[i][1]:^8}|{q[i][2]:^14s}|{q[i][3]:^9s}|{q[i][4]:^15}|{str(q[i][5]):^10s}|{str(q[i][6]):^10s}|",end="\n")
        print("="*92)
    elif hwl.lower() in 'all':
        q="SELECT * FROM Memberships;"
        cursor.execute(q)
        q=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*92}
|{'Name':^18s}|{'Reg ID':^8s}|{"Mobile Number":^14s}|{"Tenure":^9s}|{"Amount":^15s}|{"Start Date":^10s}|{"End Date":^10s}|
{"="*92}''')
        for i in range(len(q)):
            print(f"|{q[i][0]:^18s}|{q[i][1]:^8}|{q[i][2]:^14s}|{q[i][3]:^9s}|{q[i][4]:^15}|{str(q[i][5]):^10s}|{str(q[i][6]):^10s}|", end=" ")
            print()
        print("="*92)
#Function to extend the borrowed till date
def extd_borrowed_till():
    '''Function to extend the borrowed till date'''
    regid=input("Enter the Reg ID of the person:")
    Q=f"select datediff(`Borrowed Till`,`Borrowed Date`) from lendings where `Reg ID`={regid};"
    cursor.execute(Q)
    Q=cursor.fetchall()
    extd=input(f'''
Currently you have borrowed a book for {int(Q[0][0])} days, you are allowed to extend till maximum 30 days
Enter the no.of days to extend:''')
    Q=f'''select datediff(DATE_ADD(`Borrowed Till`, INTERVAL {extd} DAY),`Borrowed Date`) from lendings where `Reg ID`={regid};'''
    cursor.execute(Q)
    Q=cursor.fetchall()
            
    if int(Q[0][0])<=30:
        Q1=f"update Lendings set `Borrowed Till`=DATE_ADD(`Borrowed Till`, INTERVAL {extd} DAY) where `Reg ID`='{regid}';"
        cursor.execute(Q1)
        con.commit()
        Q1="select *from Lendings;"
        cursor.execute(Q1)
        Q1=cursor.fetchall()
        print(f"Borrowed Till extended by {extd} days successfully!!!")
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*71}
|{'Name':^18}|{'Reg ID':^8}|{"Book ID":^9}|{"Borrowed Date":^15}|{"Borrowed Till":^15}|
{"="*71}''')
        for i in range(len(Q1)):
            print(f"|{Q1[i][0]:^18}|{Q1[i][1]:^8}|{Q1[i][2]:^9}|{str(Q1[i][3]):^15}|{str(Q1[i][4]):^15}|",end=" ")
            print()
        print("="*71)
    else:
        print(f"Cannot extend till {extd} because lending time is greater than 30 days.")
#Function to renew membership of a person
def renew_mem():
    '''Function to renew membership of a person'''
    id=input("Enter the Reg ID of the member:")
    q=f"select Name, `Start Date`, `End Date` from Memberships where `Reg ID` = {id};"
    cursor.execute(q)
    q=cursor.fetchall()
    L=[]
    A=[]
    for i in range(len(q)):
        L.append(q[i][1])
        z=f"select datediff(curdate(),'{q[i][1]}');"
        cursor.execute(z)
        z=cursor.fetchall()
        A.append(z[0][0])
        index=A.index(min(A))
    y=f"select `End Date` from Memberships where `Start Date`='{L[index]}';"
    cursor.execute(y)
    y=cursor.fetchall()
    print(f"{q[0][0]}'s current membership started from {L[index]} and end's/ended on {y[0][0]}")
    z=f"select datediff(curdate(),'{y[0][0]}');"
    cursor.execute(z)
    z=cursor.fetchall()
    if z[0][0] < 0:
        wlr=input(f"{-z[0][0]} days are left for your membership, would you like to renew it now (Yes/No):")
        if wlr.lower() in 'yes':
            ten1=int(input("For how much time would you like to renew your membership (years):"))
            ten=f'{ten1} year'
            q1="SELECT * FROM `Amount for Membership`;"
            cursor.execute(q1)
            q1=cursor.fetchall()
            for i in range(len(q1)):
                if ten == q1[i][0]:
                    amt=q1[i][1]
            if ten1 == 1:
                print(f"Please pay AED {amt} for renewing membership for {ten1} year.")
            else:
                print(f"Please pay AED {amt} for renewing membership for {ten1} years.")
            q2=f"SELECT * FROM Memberships where `Reg ID` = {id};"
            cursor.execute(q2)
            q2=cursor.fetchall()
 
            if ten1 == 1:
                q3=f'''INSERT INTO Memberships 
    (Name,`Reg ID`,`Mobile Number`,Tenure, Amount, `Start Date`,`End Date`) values
    ('{q2[0][0]}',{q2[0][1]},'{q2[0][2]}','{ten1} year',{q2[0][4]},'{q2[0][6]}',DATE_ADD('{q2[0][6]}' , INTERVAL 1 YEAR));'''
                cursor.execute(q3)
                con.commit()
                print(f"Renewed {q[0][0]}'s membership for {ten1} year successfully!!")
            else:
                q3=f'''INSERT INTO Memberships 
    (Name,`Reg ID`,`Mobile Number`,Tenure, Amount, `Start Date`,`End Date`) values
    ('{q2[0][0]}',{q2[0][1]},'{q2[0][2]}','{ten1} years',{q2[0][4]},'{q2[0][6]}',DATE_ADD('{q2[0][6]}' , INTERVAL 2 YEAR));'''
                cursor.execute(q3)
                con.commit()
                print(f"Renewed {q[0][0]}'s membership for {ten1} years successfully!!")
            Q3="select * from Memberships;"
            cursor.execute(Q3)
            Q3=cursor.fetchall()
            print()
            print("Retrieving Data...")
            print()
            print(f'''\
 
{"="*89}
| {'Name':^16} | {'Reg ID':^6} | {"Mobile Number":^13} | {"Tenure":^6} | {"Amount":^6} | {"Start Date":^10} | {"End Date":^10} |
{"="*89}''')
            for i in range(len(Q3)):
                print(f"|{Q3[i][0]:^18}|{Q3[i][1]:^8}|{Q3[i][2]:^15}|{Q3[i][3]:^8}|{Q3[i][4]:^8}|{str(Q3[i][5]):^12}|{str(Q3[i][6]):^12}|",end=" ")
                print()
            print("="*89)
        elif wlr.lower() in 'no':
            print(f"Your current membership expires in {-z[0][0]} days!!")
    elif z[0][0]>0:
        wlr=input(f"{z[0][0]} days are over since your membership expired, would you like to renew it now:")
        if wlr.lower() in 'yes':
            ten1=int(input("For how much time would you like to renew your membership (years):"))
            ten=f'{ten1} year'
            q1="SELECT * FROM `Amount for Membership`;"
            cursor.execute(q1)
            q1=cursor.fetchall()
            for i in range(len(q1)):
                if ten == q1[i][0]:
                    amt=q1[i][1]
            if ten1 == 1:
                print(f"Please pay AED {amt} for renewing membership for {ten1} year.")
            else:
                print(f"Please pay AED {amt} for renewing membership for {ten1} years.")
            q2=f"SELECT * FROM Memberships where `Reg ID` = {id};"
            cursor.execute(q2)
            q2=cursor.fetchall()
 
            if ten1 == 1:
                q3=f'''INSERT INTO Memberships 
    (Name,`Reg ID`,`Mobile Number`,Tenure, Amount, `Start Date`,`End Date`) values
    ('{q2[0][0]}',{q2[0][1]},'{q2[0][2]}','{ten1} year',{q2[0][4]},curdate(),DATE_ADD(curdate() , INTERVAL 2 YEAR));'''
                cursor.execute(q3)
                con.commit()
                print(f"Renewed {q[0][0]}'s membership for {ten1} year successfully!!")
            else:
                q3=f'''INSERT INTO Memberships 
    (Name,`Reg ID`,`Mobile Number`,Tenure, Amount, `Start Date`,`End Date`) values
    ('{q2[0][0]}',{q2[0][1]},'{q2[0][2]}','{ten1} years',{q2[0][4]},curdate(),DATE_ADD(curdate() , INTERVAL 2 YEAR));'''
                cursor.execute(q3)
                con.commit()
                print(f"Renewed {q[0][0]}'s membership for {ten1} years successfully!!")
            Q3="select * from Memberships;"
            cursor.execute(Q3)
            Q3=cursor.fetchall()
            print()
            print("Retrieving Data...")
            print()
            print(f'''\
 
{"="*89}
| {'Name':^16} | {'Reg ID':^6} | {"Mobile Number":^13} | {"Tenure":^6} | {"Amount":^6} | {"Start Date":^10} | {"End Date":^10} |
{"="*89}''')
            for i in range(len(Q3)):
                print(f"|{Q3[i][0]:^18}|{Q3[i][1]:^8}|{Q3[i][2]:^15}|{Q3[i][3]:^8}|{Q3[i][4]:^8}|{str(Q3[i][5]):^12}|{str(Q3[i][6]):^12}|",end=" ")
                print()
            print("="*89)
        elif wlr.lower() in 'no':
            pass
#Function for adding and removing staff
def add_rem_staff():
    '''Function for adding and removing staff'''
    add_rem=input("What would you like to do (Add or Remove) Staff:")
    if add_rem.lower() in 'add':
        name=input("Enter name of new staff member:")
        dob=input(f"Enter date of birth of {name} (yyyy-mm-dd):")
        mob=input(f"Enter mobile number of {name}:")
        salary=input(f"Enter salary for {name}:")
        d={'manager':'LIB20XX', 'librarian':'LIB10XX', 'guard':'LIB30XX', 'janitor': 'LIB00XX'}
        b=True
        while b:
            position=input(f"Enter position on which {name} is assigned:")
            if position.lower() == 'manager' or position.lower() == 'librarian':
                passwrd=input(f"Enter a password for {name}:")
            else:
                passwrd='NULL'
            for i in d.keys():
                if position.lower() == i:
                    while True:
                        print(f"ID should be of the form '{d.get(i)}'")
                        id=input(f"Enter an appropriate id for {name}:")
                        if d.get(i)[0:5] in id:
                            break
                        else:
                            print("ID not according to the required format!!!")
                            continue
                    if type(id) is not None:
                        b=False
                else:
                    pass
            if position.lower() not in list(d.keys()):
                ask=input(f"Is {position} a new position (yes/no):")
                if ask.lower() in 'yes':
                    while True:
                        print("ID should be of the form LIBXXXX")
                        id=input(f"Enter an appropriate id for {name}:")
                        if 'LIB' in id:
                            break
                        else:
                            print("ID not according the the required format!!!")
                            continue
                    sq=input("Is password required for this position (yes/no):")
                    if sq.lower() in 'yes':
                        passwrd=input(f"Enter a password for {name}:")
                    else:
                        pass
                    if type(id) is not None:
                        b=False
                else:
                    print("Please enter correct information!!")
                    break
 
        q1="select `S No.` from staff;"
        cursor.execute(q1)
        q1=cursor.fetchall()
        L=[]
        for i in range(len(q1)):
            L.append(q1[i][0])
        q=f'''\
INSERT INTO Staff
(`S No.`,Name,`Date of Birth`,`Mobile Number`,`ID No`,Position,Salary,`Employee Password`) VALUES
({max(L)+1}, '{name.capitalize()}', '{dob}', '{mob}', '{id}', '{position}', {salary}, '{passwrd}');'''
        cursor.execute(q)
        con.commit()
        print(f"New staff member {name} successfully added!!")
        Q3="select *from Staff;"
        cursor.execute(Q3)
        Q3=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*109}
|{'S No.':^5}|{'Name':^18}|{"Date of Birth":^15}|{"Mobile Number":^16}|{"ID No":^9}|{"Position":^11}|{"Salary":^7}|{"Employee password":^19}|
{"="*109}''')
        for i in range(len(Q3)):
            pls=Q3[i][7]
            if Q3[i][7]==None:
                pls="Null"
            print(f"|{Q3[i][0]:^5}|{Q3[i][1]:^18}|{str(Q3[i][2]):^15}|{Q3[i][3]:^16}|{Q3[i][4]:^9}|{Q3[i][5]:^11}|{Q3[i][6]:^7}|{pls:^19}|",end=" ")
            print()
        print("="*109)
    elif add_rem.lower() in 'remove':
        id=input("Enter the id of person who you would like to remove:")
        q1=f'''select * from Staff where `ID No` = '{id}';'''
        cursor.execute(q1)
        q1=cursor.fetchall()
        q=f'''delete from Staff where `ID No` = '{id}';'''
        cursor.execute(q)
        con.commit()
        print(f"Removed {q1[0][5]} ({q1[0][1]}) with id {id} successfully!!")
        Q3="select *from Staff;"
        cursor.execute(Q3)
        Q3=cursor.fetchall()
        print()
        print("Retrieving Data...")
        print()
        print(f'''
{"="*109}
|{'S No.':^5}|{'Name':^18}|{"Date of Birth":^15}|{"Mobile Number":^16}|{"ID No":^9}|{"Position":^11}|{"Salary":^7}|{"Employee password":^19}|
{"="*109}''')
        for i in range(len(Q3)):
            pls=Q3[i][7]
            if Q3[i][7]==None:
                pls="Null"
            print(f"|{Q3[i][0]:^5}|{Q3[i][1]:^18}|{str(Q3[i][2]):^15}|{Q3[i][3]:^16}|{Q3[i][4]:^9}|{Q3[i][5]:^11}|{Q3[i][6]:^7}|{pls:^19}|",end=" ")
            print()
        print("="*109)
#Function to Access the spendings
def access_spendings():
    '''Function to Access the spendings'''
    q="select distinct `spend on` from `Library Spending`;"
    cursor.execute(q)
    q=cursor.fetchall()
    Q=[]
    for i in range(len(q)):
        Q.append(q[i][0])
    item=input(f"Enter the item to display the details of{Q}:")
    Q=f"select *from `Library Spending` where `Spend On`='{item.title()}'; "
    cursor.execute(Q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*52}
|{'S No.':^5}|{'Amount':^8}|{"Spend On":^11}|{"Quantity":^10}|{"Bought on":^12}|
{"="*52}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^5}|{Q1[i][1]:^8}|{Q1[i][2]:^11}|{Q1[i][3]:^10}|{str(Q1[i][4]):^12}|",end=" ")
        print()
    print("="*52)
#Function to add in spendings
def add_spending():
    '''Function to add in spendings'''
    item=input("Enter the name of the item you want to add:")
    amt=input(f"Enter the amount spent on {item.title()}:")
    quantity=input(f"Enter the quantity of the {item.title()}:")
    date=input(f"Enter the date when {item.title()} was bought:")
    Q="select count(`S No.`) from `Library Spending`;"
    cursor.execute(Q)
    Q=cursor.fetchall()
    S_No=int(Q[0][0])+1
    Q=f"insert into `Library Spending` (`S No.`,Amount,`Spend On`,Quantity,Date) values ({S_No},'{amt}','{item.title()}','{quantity}','{date}');"
    cursor.execute(Q)
    con.commit()
    Q="select *from `Library Spending`;"
    cursor.execute(Q)
    Q1=cursor.fetchall()
    print("Successfully added item!!!")
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*52}
|{'S No.':^5}|{'Amount':^8}|{"Spend On":^11}|{"Quantity":^10}|{"Bought On":^12}|
{"="*52}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^5}|{Q1[i][1]:^8}|{Q1[i][2]:^11}|{Q1[i][3]:^10}|{str(Q1[i][4]):^12}|",end=" ")
        print()
    print("="*52)
#Function to add lendings
def add_lendings():
    '''Function to add lendings'''
    q='''select `Book ID` from `Book Details`;'''
    cursor.execute(q)
    l1=list(cursor.fetchall()) #Book IDs from book details
    z='''select `Book ID` from lendings;'''
    cursor.execute(z)
    l2=list(cursor.fetchall())
    for i in range(len(l2)):
        if l2[i] in l1:
            l1.remove(l2[i])
    q="SELECT `Book Name`, `Book ID`, Writer, Category, Location FROM `Book Details`;"
    cursor.execute(q)
    abc=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*138}
|{"S No":^4s}| {"Books Available":^55s} | {"Book ID":^7s} | {"Writer":^25s} | {"Category":^15s} | {"Location":^15s} |
{"="*138}''')
    j=0
    for i in range(len(abc)):
        for k in range(len(l1)):
            if (abc[i][1] == l1[k][0]):
                j+=1
                print(f"|{str(j):^4s}| {abc[i][0]:^55s} | {abc[i][1]:^7s} | {abc[i][2]:^25s} | {abc[i][3]:^15s} | {abc[i][4]:^15s} |",end=" ")  
                print()
                break    
    print("="*138)    
    Q="select `Reg ID` from Memberships;"
    cursor.execute(Q)
    Qa1=list(cursor.fetchall())
    Q="select `Book ID` from Lendings;"
    cursor.execute(Q)
    Qa2=list(cursor.fetchall())
    Q="select `Book ID` from `Book Details`;"
    cursor.execute(Q)
    Qa3=list(cursor.fetchall())
    nd=int(input("Enter the Reg ID of member who want's to borrow:"))
    if (nd,) in Qa1:
        name=input("Enter the name of member who want's to borrow:")
        bokid=input("Enter the book ID of the book to be borrowed:")
        if (bokid,) not in Qa2 and (bokid,) in Qa3:
            dateof=input("Enter the date of borrowing:")
            datetil=input("Enter the date till the book is borrowed:")
            Q=f"insert into Lendings (Name,`Reg ID`,`Book ID`,`Borrowed date`,`Borrowed Till` ) values ('{name.title()}',{nd},'{bokid}','{dateof}','{datetil}');"
            cursor.execute(Q)
            con.commit()
            Q1="select *from Lendings;"
            cursor.execute(Q1)
            Q1=cursor.fetchall()
            print("New lending added Successfully!!!")
            print()
            print("Retrieving Data...")
            print()
            print(f'''
{"="*71}
|{'Name':^18}|{'Reg ID':^8}|{"Book ID":^9}|{"Borrowed Date":^15}|{"Borrowed Till":^15}|
{"="*71}''')
            for i in range(len(Q1)):
                print(f"|{Q1[i][0]:^18}|{Q1[i][1]:^8}|{Q1[i][2]:^9}|{str(Q1[i][3]):^15}|{str(Q1[i][4]):^15}|",end=" ")
                print()
            print("="*71)
        elif (bokid,) in Qa2:
            print(f"{bokid},this book is already borrowed!")
        else:
            print(f"{bokid},this book is not there in the library")
    else:
        print(f"{nd} is not a member!")
#Function to calculate total spending for a certain time period
def tspending():
    '''Function to calculate total spending for a certain time period'''
    Q=f"select *from `Library Spending`; "
    cursor.execute(Q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*52}
|{'S No.':^5}|{'Amount':^8}|{"Spend On":^11}|{"Quantity":^10}|{"Bought on":^12}|
{"="*52}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^5}|{Q1[i][1]:^8}|{Q1[i][2]:^11}|{Q1[i][3]:^10}|{str(Q1[i][4]):^12}|",end=" ")
        print()
    print("="*52)
    a=input('Enter the starting date: ')
    b=input('Enter the ending date: ')
    q=f"select sum(amount) from `library spending` where date<='{b}' and date>='{a}';"
    cursor.execute(q)
    a=cursor.fetchall()
    print(a[0][0])
#Function to calculate the total spending and get details for a specific item for a certain time period.
def tspending_details():
    '''Function to calculate total spending for a certain time period'''
    h=f"select * from `library spending`"
    cursor.execute(h)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*52}
|{'S No.':^5}|{'Amount':^8}|{"Spend On":^11}|{"Quantity":^10}|{"Bought on":^12}|
{"="*52}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^5}|{Q1[i][1]:^8}|{Q1[i][2]:^11}|{Q1[i][3]:^10}|{str(Q1[i][4]):^12}|",end=" ")
        print()
    print("="*52)
    a=input('Enter the item: ')
    c=input('Enter the starting date: ')
    b=input('Enter the ending date: ')
    q=f"select * from `library spending` where `Spend On`='{a}' and date<='{b}' and date>='{c}';"
    p=f"select sum(amount) from `library spending` where `Spend On`='{a}' and date<='{b}' and date>='{c}';"
    cursor.execute(q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*52}
|{'S No.':^5}|{'Amount':^8}|{"Spend On":^11}|{"Quantity":^10}|{"Bought on":^12}|
{"="*52}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^5}|{Q1[i][1]:^8}|{Q1[i][2]:^11}|{Q1[i][3]:^10}|{str(Q1[i][4]):^12}|",end=" ")
        print()
    print("="*52)
    cursor.execute(p)
    x=cursor.fetchall()
    print(f"The total spending on {a} is: ",x[0][0])
#Function to access and update the details of a person with fine.
def editfine():
    '''To edit the details of a person with fine'''
    q=f'select * from `Fine table`;'
    cursor.execute(q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*93}
|{'S no':^4}|{'Name':^13}|{'REG ID':^8}|{"Book ID":^9}|{"Days Delayed":^16}|{"Amount":^8}|{"Borrowed Till":^15s}|{"Paid on":^11}|
{"="*93}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^4}|{Q1[i][1]:^13}|{Q1[i][2]:^8}|{Q1[i][3]:^9}|{Q1[i][4]:^16}|{Q1[i][5]:^8}|{str(Q1[i][6]):^15}|{str(Q1[i][7]):^11}|",end=" ")
        print()
    print('='*93)
    name=input('Enter name of the person whose details you want to edit: ')
    change=input('What do what to change (Days delayed,Amount,Borrowed Till Date,Paid_on): ')
    change2=input(f"To what do you want to change {change} to:")
    abc=f"update `Fine table` set `{change.title()}`='{change2}' where Name='{name}';"
    cursor.execute(abc)
    con.commit()
    q=f'select * from `Fine table`;'
    cursor.execute(q)
    Q2=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*93}
|{'S no':^4}|{'Name':^13}|{'REG ID':^8}|{"Book ID":^9}|{"Days Delayed":^16}|{"Amount":^8}|{"Borrowed Till":^15s}|{"Paid on":^11}|
{"="*93}''')
    for i in range(len(Q2)):
        print(f"|{Q2[i][0]:^4}|{Q2[i][1]:^13}|{Q2[i][2]:^8}|{Q2[i][3]:^9}|{Q2[i][4]:^16}|{Q2[i][5]:^8}|{str(Q2[i][6]):^15}|{str(Q2[i][7]):^11}|",end=" ")
        print()
    print('='*93)
#Function for adding a person with fine
def add_fine_members():
    '''Function for adding a person with fine'''
    Q3="select * from `Fine Table`;"    
    cursor.execute(Q3)
    Q3=cursor.fetchall()  
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*93}
|{'S no':^4}|{'Name':^13}|{'REG ID':^8}|{"Book ID":^9}|{"Days Delayed":^16}|{"Amount":^8}|{"Borrowed Till":^15s}|{"Paid on":^11}|
{"="*93}''')
    for i in range(len(Q3)):
        print(f"|{Q3[i][0]:^4}|{Q3[i][1]:^13}|{Q3[i][2]:^8}|{Q3[i][3]:^9}|{Q3[i][4]:^16}|{Q3[i][5]:^8}|{str(Q3[i][6]):^15}|{str(Q3[i][7]):^11}|",end=" ")
        print()
    print('='*93)
    name=input("Enter the name of the person:")
    regid=int(input("Enter the Reg ID of the person:"))
    bookid=input("Enter the Book Id of the book borrowed:")
    daysdelayed=int(input("Enter how many days late the book was returned:"))
    borrowed_till=input("Till which date was the book borrowed:")
    amt=int(input("Enter the amount:"))
    paidon=input("Enter the date on which fine was paid:")
    Q3="select * from `Fine Table`;"
    cursor.execute(Q3)
    Q3=cursor.fetchall()
    Q2=f"insert into `Fine Table`(`S no.`,Name,`REG ID`,`Book ID`,`Days Delayed`,Amount,`Borrowed Till`,`Paid On`) values ({len(Q3)+1},'{name}','{regid}','{bookid}',{daysdelayed},{amt},'{borrowed_till}','{paidon}');"
    cursor.execute(Q2)
    con.commit()
    Q3="select * from `Fine Table`;"    
    cursor.execute(Q3)
    Q3=cursor.fetchall()
    print(f"Added the member successfully!!!")
    print()
    print("Retrieving Data...")
    print()  
    print(f'''
{"="*93}
|{'S no':^4}|{'Name':^13}|{'REG ID':^8}|{"Book ID":^9}|{"Days Delayed":^16}|{"Amount":^8}|{"Borrowed Till":^15s}|{"Paid on":^11}|
{"="*93}''')
    for i in range(len(Q3)):
        print(f"|{Q3[i][0]:^4}|{Q3[i][1]:^13}|{Q3[i][2]:^8}|{Q3[i][3]:^9}|{Q3[i][4]:^16}|{Q3[i][5]:^8}|{str(Q3[i][6]):^15}|{str(Q3[i][7]):^11}|",end=" ")
        print()
    print('='*93)
#Function for calculating the total earnings from fine
def t_earningfine():
    '''Function to calculate the total earnings from fine'''
    Q=f'select * from `Fine Table`;'
    cursor.execute(Q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*77}
|{'S no':^4}|{'Name':^13}|{'REG ID':^8}|{"Book ID":^9}|{"Days Delayed":^16}|{"Amount":^8}|{"Paid on":^11}|
{"="*77}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^4}|{Q1[i][1]:^13}|{Q1[i][2]:^8}|{Q1[i][3]:^9}|{Q1[i][4]:^16}|{Q1[i][5]:^8}|{str(Q1[i][6]):^11}|",end=" ")
        print()
    print('='*77)
    q=f'select sum(Amount) from `Fine Table`'
    cursor.execute(q)
    a=cursor.fetchall()
    print('The total earnings from fine is: ',a[0][0])
#Function for calculating the total earnings from memberships
def t_earningmemberships():
    '''Function to calculate the total earnings from memberships'''
    Q=f'select * from Memberships;'
    cursor.execute(Q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*95}
|{'Name':^16}|{'`Reg ID`':^10}|{'`Mobile number`':^15}|{"Tenure":^10}|{"Amount":^6}|{"`Start date`":^15}|{'`End date`':^15}|
{"="*95}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^16}|{Q1[i][1]:^10}|{Q1[i][2]:^15}|{Q1[i][3]:^10}|{Q1[i][4]:^6}|{str(Q1[i][5]):^15}|{str(Q1[i][6]):^15}|",end=" ")
        print()
    print("="*95)
    q=f'select sum(Amount) from Memberships'
    cursor.execute(q)
    a=cursor.fetchall()
    print('The total earnings from memberships is: ',a[0][0])
#Function to review total earnings
def t_earning():
    '''Function to review the total earnings'''
    q=f'select sum(Amount) from `Fine Table`'
    p=f'select sum(Amount) from Memberships'
    cursor.execute(p)
    a=cursor.fetchall()
    cursor.execute(q)
    b=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print('The total earnings  is: ',a[0][0]+b[0][0])
#Function to update the amount for membership table
def upd_amtmembership():
    '''Function to update the amount for membership table'''
    q=f'select * from `Amount for Membership`;'
    cursor.execute(q)
    Q1=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*17}
|{'Tenure':^8}|{'Amount':^6}
{"="*17}''')
    for i in range(len(Q1)):
        print(f"|{Q1[i][0]:^8}|{Q1[i][1]:^6}|",end=" ")
        print()
    print("="*17)
    tenure=input('Enter the tenure whos amount is to be updated: ')
    n_amount=int(input('Enter the new amount: '))
    Q1=f"update `Amount for Membership` set Amount={n_amount} where Tenure='{tenure}';"
    cursor.execute(Q1)
    con.commit()
    q=f'select * from `Amount for Membership`;'
    cursor.execute(q)
    Q2=cursor.fetchall()
    print()
    print("Retrieving Data...")
    print()
    print(f'''
{"="*17}
|{'Tenure':^8}|{'Amount':^6}
{"="*17}''')
    for i in range(len(Q2)):
        print(f"|{Q2[i][0]:^8}|{Q2[i][1]:^6}|",end=" ")
        print()
    print("="*17)

if con.is_connected:
    #print(f'''{"Please use 'COURIER NEW' font with 'SIZE:9' for best results!!!":^100s}''')
    cursor=con.cursor()
    Menu1=f'''
{'MENU':^31s} 
1. Book Details
2. Membership Details 
3. Fine
4. Lendings
5. Library Spendings 
6. Earnings of the library
7. Change amount for Membership
8. Staff 
9. Exit \n'''
    Menu2=f'''
{'MENU':^21s}
1. Book Details
2. Membership Details 
3. Fine
4. Lendings
5. Library Spendings 
6. Earnings of the library
7. Exit \n'''   
    M_1=f'''
{'Book Detail Menu':^26s}

1. Search for a book 
2. Add or remove a book
3. Display available books  
4. Display borrowed books \n'''  
    M_2=f'''
{'Membership Menu':^34s}

1. Display the details of a member
2. Add or remove a member 
3. Renew a membership 
4. Amount for memberships \n''' 
    M_3=f'''
{'Fine Menu':^34s}

1. Access and edit fine details of a person 
2. Add fine \n'''
    M_4=f'''
{'Lending Menu':^22s}

1. Details of a person 
2. Extending lend date 
3. Add a new lending \n'''
    M_6=f'''
{'Staff Menu':^22s}

1. Add or Remove staff
2. Edit Staff Details \n''' 
    M_7=f'''
{'Library Spending Menu':^46s}

1. Accessing the details of an item  
2. Add a purchased item 
3. Total spending in a time period  
4. Total spendings of an item in a time period \n'''
    M_8=f'''
{"Library Earning's Menu":^33s}

1. Total earnings from fine 
2. Total earnings from membership
3. Review total earnings \n'''
    def common_choice():
        global choice 
        choice=input("Enter your choice:")
        if choice=="1":
            print(f"{M_1:^100}")
            ch=input("Enter you choice:")
            if ch=="1":
                booksearch()
            elif ch=="2":
                editbooks()
            elif ch=="3":
                disp_avai_books()
            elif ch=="4":
                disp_borr_books()
        elif choice=="2":
            print(f"{M_2:^100}")
            ch=input("Enter you choice:")
            if ch=="1":
                disp_mem_details()
            elif ch=="2":
                add_remove_members()
            elif ch=="3":
                renew_mem()
            elif ch=="4":
                print()
                print("Retrieving Data...")
                print()
                amtmembers()
        elif choice=="3":
            print(f"{M_3:^100}")
            ch=input("Enter you choice:")
            if ch=="1":
                editfine()
            elif ch=="2":
                add_fine_members()
        elif choice=="4":
            print(f"{M_4:^100}")
            ch=input("Enter you choice:")
            if ch=="1":
                lend_details()
            elif ch=="2":
                extd_borrowed_till()
            elif ch=="3":
                add_lendings()   
        elif choice=="5":
            print(f"{M_7:^100}")
            ch=input("Enter you choice:")
            if ch=="1":
                access_spendings()
            elif ch=="2":
                add_spending()
            elif ch=="3":
                tspending()               
            elif ch=="4":
                tspending_details()
        elif choice=="6":
            print(f"{M_8:^100}")
            ch=input("Enter you choice:")
            if ch=="1":
                t_earningfine()
            elif ch=="2":
                t_earningmemberships()
            elif ch=="3":
                t_earning()         
        else:
            False
    print(f"{'WELCOME TO LMS!':^144s}")
    auth,usname,position=authentication()           
    while True:
        if auth:
            auto_update_fine_table()
            if  usname=='1234567' or position=='Manager':
                print(f'{Menu1:^50s}')
                if common_choice():
                    pass
                elif choice=="7": 
                    upd_amtmembership()
                elif choice=="8":
                    print(f"{M_6:^100}")
                    ch=input("Enter you choice:")
                    if ch=="1":
                        add_rem_staff()
                    elif ch=="2":
                        edit_staff()               
                elif choice=="9":
                    print("Thank you for using LMS!!")
                    break 
            else:
                print(f'{Menu2:^100}')
                if common_choice():
                    continue
                elif choice == '7':
                    print("Thank you for using LMS!!")
                    break      
        else:
            print("Unidentified User!!")
            break
else:
    print("Error! Not connected to MySQL")
