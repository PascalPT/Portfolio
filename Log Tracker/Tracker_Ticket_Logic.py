#Pascal Pelletier-Thériault
import os
from csv import writer
import ntplib
import datetime
from pandas import read_csv, DataFrame
from time import strptime
from tkinter import filedialog, Tk

########
########
########
######## fonction call
########
def Verify_CSV(Name):
    Config()
    #Creating it if none
    
    k=1
    if Name.find("#/",0,2) == 0:
        Path_directory = os.path.join(Ticket_Directory_Location,"Search")
        Name = Name[2:]
        Path = os.path.join(Path_directory,Name)
    elif Name == "Search.conf":
        Directory = ""
        Path_directory = os.path.join(Ticket_Directory_Location)
    elif Name.find("/#/",0,3)== 0:
        Path_directory = Name[3:Name.rfind("/")]
        Name = Name[Name.rfind("/")+1:]
        Path = os.path.join(Path_directory,Name)
        k=0
    else:
        Path_directory = os.path.join(Ticket_Directory_Location)
    Path = os.path.join(Path_directory,Name)
   
    if not os.path.exists(Path):
        try:
            os.makedirs(Path_directory)
        except:
            None
        os.chdir(Path_directory)

        CSV_File = writer(open(Name,"w",newline = "\n"))
        if Name == "Members.csv":
            CSV_File.writerow(["Username","Roles_Level","Hash_Password"])
        elif Name == "Search.conf":
            CSV_File.writerow(["Id_ticket","Title","Assigned_To","Issue","Creator","Tags","Progress",
                             "Creation_Date","Last_Edit_Date","Last_Modify_by","Date_Range"])
        else:
            CSV_File.writerow(["Id_ticket","Title","Assigned_To","Issue","Creator","Tags","Progress",
                             "Creation_Date","Last_Edit_Date","Last_Modify_by"])
    else:

        CSV_File = read_csv(Path,skip_blank_lines=True)
        #Checking if columns are right (not ordered)
        if Name == "Members.csv":
            Columns_Name = ["Username","Roles_Level","Hash_Password"]
        elif Name == "Search.conf":
            Columns_Name = ["Id_ticket","Title","Assigned_To","Issue","Creator","Tags","Progress",
                             "Creation_Date","Last_Edit_Date","Last_Modify_by","Date_Range"]
        else:
            Columns_Name = ["Id_ticket","Title","Assigned_To","Issue","Creator","Tags",
                                                       "Progress","Creation_Date","Last_Edit_Date","Last_Modify_by"]
        if (sorted(list(CSV_File.columns))== sorted(Columns_Name)
        and list(CSV_File.columns)!=(Columns_Name)):
            CSV_File = CSV_File[Columns_Name]
            CSV_File.to_csv(path_or_buf = Path)
        #If wrong columns delete and start again
        elif ((sorted(list(CSV_File.columns))!= sorted(Columns_Name))) and (k==1):
            os.chdir(Path_directory)
            os.remove(Name)
            Verify_CSV(Name)
        elif ((sorted(list(CSV_File.columns))== sorted(Columns_Name))):
              k = 0
        else:
            k = 1
        return(k)

def Verify_User(User):
    Config()
    Verify_CSV("Members.csv")
    Path = os.path.join(Ticket_Directory_Location,"Members.csv")
    Members = read_csv(Path,skip_blank_lines=True)
    u = False
    for i in range(0,len(Members["Username"])):
        if User == Members["Username"][i]:
            if Members["Roles_Level"][i] == "Admin":
                u = True
    return(u)


def Create_Ticket(Title,Assigned_To,Issue,User,Tags):
    Config()
    Verify_CSV("Members.csv")
    Verify_CSV("Ticket_All.csv")
    Verify_CSV("Awaiting_Ticket.csv")

    Creator = User
    Last_Edit_Date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    Creation_Date = Last_Edit_Date
    Progress = "In Progress"
    if Verify_User(User) == True:
        CSV_File = "Ticket_All.csv"
    else:
        CSV_File = "Awaiting_Ticket.csv"


    Path = os.path.join(Ticket_Directory_Location, CSV_File)
    Ticket_All = read_csv(Path,skip_blank_lines=True)
    try:
        Id_ticket = max(list(Ticket_All["Id_ticket"])) + 1
    except:
        Id_ticket = 1
    Ticket = DataFrame([[Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,
                         Creation_Date,Last_Edit_Date,User]],
                          columns = list(["Id_ticket","Title","Assigned_To","Issue","Creator","Tags","Progress",
                                          "Creation_Date","Last_Edit_Date","Last_Modify_by"]))
    Ticket_All.append(Ticket,sort=False).to_csv(path_or_buf = Path, index=False)
    return("Done")

def Modify_Ticket(Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,User):
    Config()
    Verify_CSV("Ticket_All.csv")

    Path = os.path.join(Ticket_Directory_Location,"Ticket_All.csv")
    Path_Original = os.path.join(Ticket_Directory_Location,"Original_Ticket.csv")
    Path_Awaiting = os.path.join(Ticket_Directory_Location,"Awaiting_Ticket.csv")

    Ticket_All = read_csv(Path,skip_blank_lines=True)
    Creation_Date = Ticket_All.iloc[Id_ticket-1,:][7]
    Last_Edit_Date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    if (User == Creator):
        Ticket_All.iloc[Id_ticket-1,:] = list([Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,
                                           Creation_Date,Last_Edit_Date,User])
        Ticket_All.to_csv(path_or_buf = Path,index=False)
    elif Verify_User(User) == True:
        Verify_CSV("Original_Ticket.csv")
        Original_Ticket_CSV = read_csv(Path_Original,skip_blank_lines=True)
        Original_Ticket = Ticket_All.iloc[Id_ticket-1,:]
        Original_Ticket_CSV.append(Original_Ticket,sort=False).to_csv(path_or_buf = Path_Original, index = False)


        Ticket_All.iloc[Id_ticket-1,:] = list([Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,
                                           Creation_Date,Last_Edit_Date,User])
        Ticket_All.to_csv(path_or_buf = Path, index=False)
    else:
        Verify_CSV("Awaiting_Ticket.csv")

        Awaiting_Ticket = read_csv(Path_Awaiting,skip_blank_lines=True)

        Ticket = DataFrame([[Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,
                         Creation_Date,Last_Edit_Date,User]],
                          columns = list(["Id_ticket","Title","Assigned_To","Issue","Creator","Tags","Progress",
                                          "Creation_Date","Last_Edit_Date","Last_Modify_by"]))
        Awaiting_Ticket.append(Ticket,sort=False).to_csv(path_or_buf = Path_Awaiting, index = False)
    return("Done")

def Awaiting_Create_Ticket(Last_Edit_Date,User,Operation):
    Config()
    Verify_CSV("Awaiting_Ticket.csv")
    Verify_CSV("Ticket_All.csv")

    Path = os.path.join(Ticket_Directory_Location,"Ticket_All.csv")
    Path_Original = os.path.join(Ticket_Directory_Location,"Original_Ticket.csv")
    Path_Awaiting = os.path.join(Ticket_Directory_Location,"Awaiting_Ticket.csv")

    Awaiting_Ticket = read_csv(Path_Awaiting,skip_blank_lines=True)
    if (Verify_User(User) == True) or (User ==
                                       Awaiting_Ticket[Awaiting_Ticket["Last_Edit_Date"]=="2019-11-24 17:25:03.182871"].iloc[0][4]):
        if Operation == "Delete":
            Awaiting_Ticket[Awaiting_Ticket["Last_Edit_Date"]!=Last_Edit_Date].to_csv(path_or_buf = Path_Awaiting,index=False)
        elif Operation == "Accept":
            Ticket = list(Awaiting_Ticket[Awaiting_Ticket["Last_Edit_Date"]==Last_Edit_Date].iloc[0]) #:?
            Id_ticket = Ticket[0]
            Ticket_All = read_csv(Path, skip_blank_lines=True)

            Original_Ticket_CSV = read_csv(Path_Original,skip_blank_lines=True)
            Original_Ticket_CSV.append(Ticket_All.iloc[Id_ticket-1,:],sort=False).to_csv(path_or_buf = Path_Original, index = False)

            Ticket_All.iloc[Id_ticket-1,:] = list(Ticket)

            Ticket_All.to_csv(path_or_buf = Path, index=False)

            Awaiting_Ticket[Awaiting_Ticket["Last_Edit_Date"]!=Last_Edit_Date].to_csv(path_or_buf = Path_Awaiting, index=False)
    return("Done")

def Sort_By(Column,Name):
    #Title="dsa";Assigned_To="";Issue="";Creator="";Tags="";Progress="";Creation_Date="";Last_Edit_Date=""
    Config()

    if Name != "":
        Verify_CSV("#/" + Name)
        Path = os.path.join(Ticket_Directory_Location,"Search",Name)
    else:
        Verify_CSV(Name)
        Path = os.path.join(Ticket_Directory_Location,Name)

    Path_Key = os.path.join(Ticket_Directory_Location,"Sort_Key.csv")    

    n = 1
    try:
        if Column == read_csv(Path_Key,skip_blank_lines=True)["0"].iloc[0]:
            n = -1
            #if it exist erase it, then sort
            DataFrame([]).to_csv(path_or_buf = Path_Key,index=False)
        else:
            DataFrame([Column]).to_csv(path_or_buf = Path_Key,index=False)
    except:
        DataFrame([Column]).to_csv(path_or_buf = Path_Key,index=False)
    
    Ticket_Sorted = read_csv(Path,skip_blank_lines=True)
    Ticket_Sorted.iloc[Ticket_Sorted[Column].str.lower().argsort()][::n].to_csv(
        path_or_buf = Path,index=False)
    return("Done")


def Search_CSV(Title="",Assigned_To="",Issue="",Creator="",Tags="",Progress="",Creation_Date="",
           Last_Edit_Date="",Last_Modify_by="",Date_Range="",Name="Ticket_Active.csv"):
    #Title = ['titre1','titre2'...] <- Title = "asda;dsada;asd dsad"  # Date_Range="2018-09-09 02:21:12.123456,2019-01-01 12:00:00";....)
    #Name : custom name in the Search folder (to save it)
    Config()
    Verify_CSV("Ticket_All.csv")
    
    Path = os.path.join(Ticket_Directory_Location, "Ticket_All.csv")
    if Name == "Ticket_Active.csv":
        Path_Search = os.path.join(Ticket_Directory_Location, "Ticket_Active.csv")
    else:
        Path_Search = os.path.join(Ticket_Directory_Location, "Search",Name)

    Ticket_All = read_csv(Path,skip_blank_lines=True)
    y = []
    for f in range(0,len(Ticket_All["Id_ticket"])):
          y.append(True)

    #a = Title
    #b = "Title"
    def Col_Search(a,b,y):
        if a !="" and a == a:
            a = a.split(";")
            for i in range(0,len(a)):
                x=[]
                for j in range(0,len(Ticket_All["Id_ticket"])):
                    x.append(Ticket_All[b].iloc[j].find(a[i].strip())!=-1)
                for k in range(0,len(Ticket_All["Id_ticket"])):
                    y[k] = y[k] and x[k]

        return(y)


    Col_Search(Title,"Title",y)
    Col_Search(Assigned_To,"Assigned_To",y)
    Col_Search(Issue,"Issue",y)
    Col_Search(Creator,"Creator",y)
    Col_Search(Tags,"Tags",y)
    Col_Search(Progress,"Progress",y)
    Col_Search(Creation_Date,"Creation_Date",y)
    Col_Search(Last_Edit_Date,"Last_Edit_Date",y)
    Col_Search(Last_Modify_by,"Last_Modify_by",y)


    a = Date_Range
    b = "Creation_Date"
    if a !="" and a == a:
        a = a.split(";")
        for i in range(len(a)):
            x=[]
            a[i] = a[i].strip().split(",")

            if len(a[i][0]) == 10:
                a[i][0] = a[i][0] + " 00:00:00.000000"
            elif len(a[i][0]) == 19:
                a[i][0] = a[i][0] + ".000000"
            if len(a[i][0]) != 26:
                a[i][0] = "0001-01-01 00:00:00.000000"
            if len(a[i][1]) == 10:
                a[i][1] = a[i][1] + " 23:59:59.999999"
            elif len(a[i][1]) == 19:
                a[i][1] = a[i][1] + ".999999"
            if len(a[i][1]) != 26:
                a[i][1] = "0001-01-01 00:00:00.000000"


            for j in range(0,len(Ticket_All["Id_ticket"])):
                if len(Ticket_All[b].iloc[j].strip()) == 26:
                    h = strptime(Ticket_All[b].iloc[j].strip(),'%Y-%m-%d %H:%M:%S.%f')
                else:
                    h = strptime("0001-01-01 00:00:00.000000",'%Y-%m-%d %H:%M:%S.%f')
                x.append( h >= strptime(a[i][0],'%Y-%m-%d %H:%M:%S.%f')
                              and h <= strptime(a[i][1],'%Y-%m-%d %H:%M:%S.%f'))
            for k in range(0,len(Ticket_All["Id_ticket"])):
                y[k] = y[k] and x[k]

    Ticket_All[y].to_csv(path_or_buf = Path_Search, index=False)
    return("Done")

def Add_Quick_Search(Id_ticket,Title="",Assigned_To="",Issue="",Creator="",Tags="",Progress="",Creation_Date="",
                     Last_Edit_Date="",Last_Modify_by="",Date_Range=""):
    Config()
    Verify_CSV("Search.conf")

    Path = os.path.join(Ticket_Directory_Location, "Search.conf")

    Quick_Search_File = read_csv(Path, skip_blank_lines=True)

    if len(Quick_Search_File[Quick_Search_File["Id_ticket"]==Id_ticket]) > 0:
        Id_ticket = Id_ticket + " 2"
        Add_Quick_Search(Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,Creation_Date,
                     Last_Edit_Date,Last_Modify_by,Date_Range)
    else:
        Search = DataFrame([[Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,Creation_Date,Last_Edit_Date,Last_Modify_by,Date_Range]],
                       columns = ["Id_ticket","Title","Assigned_To","Issue","Creator","Tags","Progress","Creation_Date",
                       "Last_Edit_Date","Last_Modify_by","Date_Range"])
        Quick_Search_File.append(Search,sort=False).to_csv(path_or_buf = Path,index=False)
    return("Done")

def Button_Search():
    Config()
    Verify_CSV("Search.conf")

    Path = os.path.join(Ticket_Directory_Location, "Search.conf")
    Quick_Search_File = read_csv(Path, skip_blank_lines=True)
    Quick_Search_File.to_csv(path_or_buf = Path, index=False)
    return("Done")

def Edit_Search(Operation,Id_ticket,Title="",Assigned_To="",Issue="",Creator="",Tags="",Progress="",Creation_Date="",
                Last_Edit_Date="",Last_Modify_by="",Date_Range=""):
    Config()
    Verify_CSV("Search.conf")

    Path = os.path.join(Ticket_Directory_Location, "Search.conf")
    Quick_Search_File = read_csv(Path,skip_blank_lines=True)
    Quick_Search_File[Quick_Search_File["Id_ticket"]!=Id_ticket].to_csv(path_or_buf =Path, index=False)
    if Operation == "Modify":
        Add_Quick_Search(Id_ticket,Title,Assigned_To,Issue,Creator,Tags,Progress,Creation_Date,
                Last_Edit_Date,Last_Modify_by,Date_Range)
    return("Done")

def Create_Quick_Search():
    Config()
    Verify_CSV("Search.conf")

    Path = os.path.join(Ticket_Directory_Location, "Search.conf")
    Path_directory_Search =  os.path.join(Ticket_Directory_Location,"Search")

    Quick_Search_File = read_csv(Path, skip_blank_lines=True)
    n = len(Quick_Search_File["Id_ticket"]) #name -> 0 -> search(...,name,11)
    
    try:
        os.makedirs(Path_directory_Search)
    except:
        None
    
    for item in os.listdir(Path_directory_Search):
        if item.endswith(".csv"):        
            try:
                os.remove(os.path.join(Path_directory_Search,item))
            except:
                None
        
    if n > 0:  
        for i in range(n):
            Search = list(Quick_Search_File.iloc[i,:])
            Search_CSV(Search[1],Search[2],Search[3],Search[4],Search[5],Search[6],
               Search[7],Search[8],Search[9],Search[10],(Search[0]+".csv"))
    return("Done")

def Default_Config(User):
    Config()
    Path_directory = os.path.join(Ticket_Directory_Location)
    try:
        os.makedirs(Path_directory)
    except:
        None
    os.chdir(Path_directory)
    try:
        os.remove("Search.conf")
        os.remove("Config.conf")
    except:
        None
    Add_Quick_Search(Id_ticket,Title="",Assigned_To=User,Issue="",Creator="",Tags="",Progress="In_Progress",Creation_Date="",
                     Last_Edit_Date="",Last_Modify_by="",Date_Range="")

    return("Done")
    
def Import_CSV(Operation,User,file_path = ""): 
    Config()

    if Operation == "replace":
        if file_path == "":
            root = Tk()
            root.attributes("-topmost", True)
            root.withdraw()
            file_path = filedialog.askopenfilename(title = "Select files",
                                        filetypes=[("CSV files","*.csv")])
        if file_path == "":
            return ("Done")
        CSV_File = read_csv(file_path,skip_blank_lines=True)
        if Verify_CSV("/#/" + file_path)== 1:
            return("File does not match patern")
        else:
            if Verify_User(User)== False:
                return("insufficient administrative privilege") 
            else:
                Path = os.path.join(Ticket_Directory_Location,"Ticket_All.csv")       
                Path_Original = os.path.join(Ticket_Directory_Location,"Original_Ticket.csv")
                Path_Awaiting = os.path.join(Ticket_Directory_Location,"Awaiting_Ticket.csv")       

                Verify_CSV("Ticket_All.csv")
                Verify_CSV("Original_Ticket.csv")
                Ticket_All = read_csv(Path,skip_blank_lines=True)

                Ticket_Original = read_csv(Path_Original,skip_blank_lines=True)
                Ticket_Original.append(Ticket_All,sort=False, ignore_index=True).to_csv(
                    path_or_buf = Path_Original, index = False)

                #delete old awaiting
                Ticket_Awaiting = read_csv(Path_Awaiting,skip_blank_lines=True)
                Ticket_Awaiting.append([1,2,3]).to_csv(path_or_buf = Path_Awaiting, index = True)
                Verify_CSV("Awaiting_Ticket.csv")
                       
                for i in range(1, len(CSV_File["Id_ticket"])+1):
                    CSV_File.iat[i-1,0] = i
                CSV_File.to_csv(path_or_buf = Path, index = False)
     
                return("Done")
            
    elif Operation == "add":
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        files_path = filedialog.askopenfilenames(title = "Select files",
                                        filetypes=[("CSV files","*.csv")])
        if files_path == "":
            return("Done")
        for j in range(0,len(files_path)):
            if Verify_CSV("/#/" + files_path[j]) == 1:
                return("One or more files do not match patern")
            if Verify_User(User)== False:
                return("insufficient administrative privilege")
            
            Verify_CSV("Ticket_All.csv")    
            Path = os.path.join(Ticket_Directory_Location,"Ticket_All.csv")
            Ticket_All = read_csv(Path,skip_blank_lines=True)
            try:
                Id_ticket = max(list(Ticket_All["Id_ticket"])) + 1
            except:
                Id_ticket = 1
            for t in range(0,len(files_path)):
                New_Ticket = read_csv(files_path[t],skip_blank_lines=True)
                for h in range(0,len(New_Ticket["Id_ticket"])):
                    New_Ticket.iat[h,0] = Id_ticket
                    Id_ticket += 1
                
                Ticket_All=Ticket_All.append(New_Ticket,sort=False, ignore_index=True)
            
            Ticket_All.to_csv(path_or_buf = Path,index = False)
            return("Done")

def Export_CSV(Name):
    Name = Name.split(";")
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askdirectory(title = "Select folder")
    Config()
    
    for i in range(0,len(Name)):
        Verify_CSV("/#/" + directory_path + "/" + Name[i]+ ".csv")
        
        if Name[i] == ("Awaiting_Ticket") or (Name[i] =="Members") or (Name[i] =="Original_Ticket") or (Name[i]
                                    =="Search") or (Name[i] =="Ticket_Active") or (Name[i] =="Ticket_All") or (Name[i] =="Ticket_Active"):
            Verify_CSV(Name[i]+".csv")
            Path_CSV = os.path.join(Ticket_Directory_Location,Name[i]+".csv")
            read_csv(Path_CSV,skip_blank_lines=True).to_csv(path_or_buf = directory_path + "/" +Name[i] + ".csv",index = False)
        else:
            Verify_CSV("#/" + Name[i]+".csv")
            Path_CSV = os.path.join(Ticket_Directory_Location,"Search",Name[i]+".csv")
            read_csv(Path_CSV,skip_blank_lines=True).to_csv(path_or_buf = directory_path + "/" +Name[i] + ".csv",index = False)
            
                
    
def Clean_CSV(User,In_Progress=False,Close=True,Resolve=True):
    # remove the one who are true
    
    Config()
    
    if In_Progress == True:
        Progress = "In_Progress"
    else:
        Progress = "None"
    if Close == True:
        Progress = Progress + (";Close")
    if Resolve == True:
        Progress = Progress +(";Resolve")
        
    Search(Title="",Assigned_To="",Issue="",Creator="",Tags="",Progress= "",Creation_Date="",
           Last_Edit_Date="",Last_Modify_by="",Date_Range="",Name="Ticket_Active.csv")
    Export_CSV("Ticket_Active")

    if In_Progress == False:
        Progress = "In_Progress"
    else:
        Progress = "None"
    if Close == False:
        Progress = Progress + (";Close")
    if Resolve == False:
        Progress = Progress +(";Resolve")
        
    Search(Title="",Assigned_To="",Issue="",Creator="",Tags="",Progress= "",Creation_Date="",
           Last_Edit_Date="",Last_Modify_by="",Date_Range="",Name="Ticket_Active.csv")
    
    Path_Active = os.path.join(Ticket_Directory_Location,"Ticket_Active.csv")
    Import_CSV("replace",User,file_path = Path_Active)
    
    
    
    
"""Creation_Date = datetime.datetime.fromtimestamp(
        ntplib.NTPClient().request(Time_Server).tx_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    Last_Edit_Date = Abs_Creation_Date

https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://console.developers.google.com/apis/credentials?showWizardSurvey=true&project=ticket-all&folder&organizationId
https://drive.google.com/drive/my-drive
https://docs.google.com/spreadsheets/d/1CM-lnBjyvrGUhSk9K3GQxAzN74sITR_uFS9jeGZGEx0/edit?folder=15kyVk3nY3oqoIxc7SAq3j4Xp_tQhLlTf#gid=0

"""

def Config():
    global Ticket_Directory_Location, Directory_Type,  Time_Server
    current_directory = os.getcwd()
    ###
    ###
    ###Config 
    ###
    ###
    #Line_1 = "Ticket_Directory_Name : 'Ticket_Directory' #'Custom_Name'\n"
    Line_1 = "Ticket_Directory_Location : '" + os.path.join(current_directory,"Ticket_Directory")+ "' " + "#Custom_Path\n" 
    Line_2 = "Directory_Type : 'Locally' #'Locally', 'Url_Google_drive', 'Url_Github'\n"
    Line_3 = "Time_Server : 'ca.pool.ntp.org' #'Go on poo.ntp.org and choose a link/country'\n"
    #########
    #########
    #########
    ##########recreate
    #########                                                         
    if not os.path.exists(os.path.join(current_directory,r"config.conf")):
        config = open("config.conf", "w")
        config.write(Line_1)
        config.write(Line_2)
        config.write(Line_3)
        config.close()
    #########
    #########
    #########
    ##########recreate only 1 line
    #########                                                          
    def Re_Config(line):
        config = open("config.conf", "r")
        config_tmp = open("config_tmp.conf", "a")

        for i in range(1,line):
            config_tmp.write(config.readline())
            
        #if line == 1:
            #config_tmp.write(Line_1)
        if line == 1:
            config_tmp.write(Line_1)
        elif line == 2:
            config_tmp.write(Line_2)
        elif line == 3:
            config_tmp.write(Line_3)
        skipt=config.readline()
        
        for i in range(line+1,3):
            config_tmp.write(config.readline())
            
        config.close()
        config_tmp.close()
        
        os.remove("config.conf")
        os.rename(os.path.join(current_directory,r"config_tmp.conf"),os.path.join(current_directory,r"config.conf"))
    #########
    #########
    #########    
    #########Evaluating the first line
    #########
    config = open("config.conf","r")
    #Ticket_Directory_Name = config.readline()
    #x = -2
    #y = -2
    #if Ticket_Directory_Name.find("Ticket_Directory_Name : '") == 0:
    #    x = Ticket_Directory_Name.find("'")
    #    if Ticket_Directory_Name.find("'",x+1,len(Ticket_Directory_Name)) != -1 :
    #        y = Ticket_Directory_Name.find("'",x+1,len(Ticket_Directory_Name))
    #    else :
    #        config.close()
    #        Re_Config(1)
    #if (x or y) == (-2 or -1):
    #    config.close()
    #    Re_Config(1)
    #Ticket_Directory_Name = Ticket_Directory_Name[x+1:y]
    #########
    #########
    #########
    #########Evaluating the second line
    #########
    config = open("config.conf","r")
    for i in range (0,0):
        skipt=config.readline()
    Ticket_Directory_Location = config.readline()
    x = -2
    y = -2
    if Ticket_Directory_Location.find("Ticket_Directory_Location : '") == 0:
        x = Ticket_Directory_Location.find("'")
        if Ticket_Directory_Location.find("'",x+1,len(Ticket_Directory_Location)) != -1 :
            y = Ticket_Directory_Location.find("'",x+1,len(Ticket_Directory_Location))
        else :
            config.close()
            Re_Config(1)
    if (x or y) == (-2 or -1):
        config.close()
        Re_Config(1)
    Ticket_Directory_Location = Ticket_Directory_Location[x+1:y]
    #########
    #########
    #########
    #########Evaluating the third line
    #########
    config = open("config.conf","r")
    for i in range (0,1):
        skipt=config.readline()
    Directory_Type = config.readline()
    x = -2
    y = -2
    if Directory_Type.find("Directory_Type : '") == 0:
        x = Directory_Type.find("'")
        if Directory_Type.find("'",x+1,len(Directory_Type)) != -1 :
            y = Directory_Type.find("'",x+1,len(Directory_Type))
        else :
            config.close()
            Re_Config(2)
    if (x or y) == (-2 or -1):
        config.close()
        Re_Config(2)
    Directory_Type = Directory_Type[x+1:y]
    #########
    #########
    #########
    #########Evaluating the fourth line
    #########
    config = open("config.conf","r")
    for i in range (0,2):
        skipt=config.readline()
    Time_Server = config.readline()
    x = -2
    y = -2
    if Time_Server.find("Time_Server : '") == 0:
        x = Time_Server.find("'")
        if Time_Server.find("'",x+1,len(Time_Server)) != -1 :
            y = Time_Server.find("'",x+1,len(Time_Server))
        else :
            config.close()
            Re_Config(3)
    if (x or y) == (-2 or -1):
        config.close()
        Re_Config(3)
    Time_Server = Time_Server[x+1:y]
    #########
    #########
    #########
    #########Applying config
    #########
    #if Directory_Type == "Locally":
    #    if not os.path.exists(os.path.join(Ticket_Directory_Location,Ticket_Directory_Name)):
    #        os.makedirs(os.path.join(Ticket_Directory_Location,Ticket_Directory_Name))






            


