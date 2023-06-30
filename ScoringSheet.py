import pandas as pd
import numpy as np
import re
import requests
from time import time 
from bs4 import BeautifulSoup

start_time = time()
#https://www.baseball-reference.com/boxes/CHN/CHN202206050.shtml#
df=pd.read_csv(r'C:\Users\papai\OneDrive\Documents\Scoring Sheet\Python\PHI202206050.csv').fillna("")

#Cosmetic pieces
l1="___1______2______3______4______5______6______7______8______9______"
l2=l5=l8=l11=l14=l17=l20=l23=l26=l30=l33=l36=l39=l42=l45=l48=l51=l54=["xx|"]
l3=l6=l9=l12=l15=l18=l21=l24=l27=l31=l34=l37=l40=l43=l46=l49=l52=l55=["  |"]
l4=l7=l10=l13=l16=l19=l22=l25=l28=l32=l35=l38=l41=l44=l47=l50=l53=l56=["__|"]
top=[l2,l5,l8,l11,l14,l17,l20,l23,l26,l30,l33,l36,l39,l42,l45,l48,l51,l54]
mid=[l3,l6,l9,l12,l15,l18,l21,l24,l27,l31,l34,l37,l40,l43,l46,l49,l52,l55]
bot=[l4,l7,l10,l13,l16,l19,l22,l25,l28,l32,l35,l38,l41,l44,l47,l50,l53,l56]
l29="=================================================================="
data=[" "," "," "," "," "," "]
data1=["_","_","_","_","_","_"]

#delcaring empty variables
i=0
j=0
k=0
l=0
m=0
awayOrder=0
homeOrder=0
outs=0
atBat=False
onBase=[None,None,None,None]
batters=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
awayTeam=None
homeTeam=None

while awayTeam == None or homeTeam == None:#Store team names for main while loop
        if df.iat[i,0].startswith("Top"):
                i+=1
                awayTeam=df.iat[i,6]
        if df.iat[i,0].startswith("Bottom"):
                i+=1
                homeTeam=df.iat[i,6]
        i+=1

i=0
while j<9:#Create empty score card
        while i<len(top):
                top[i]=top[i]+data+["|"]
                mid[i]=mid[i]+data+["|"]
                bot[i]=bot[i]+data1+["|"]
                i+=1
        i=0
        j+=1

inning=0
i=0
j=0
out=False
while True:
        #print(l)
        m=inning*7#This is used to position with column the program should edit

        if df.iat[i,9].startswith("Top of the "):#Skip these lines
                i+=1
        elif df.iat[i,9].startswith("Bottom of the "):
                i+=1
                
        if df.iat[i-1,7]==df.iat[i,7]:#if duplicate, skip
                j=j-1

        if len(df)!=i+1 and df.iat[i+1,11].__contains__(" running "):#Ghost runner
                onBase[1]=df.iat[i+1,11].split(" ")[df.iat[i+1,11].split(" ").index("running")-1]
                top[batters.index(onBase[1])][3+m]='\\'
                top[batters.index(onBase[1])][4+m]='G'
                mid[batters.index(onBase[1])][3+m]='/'
                mid[batters.index(onBase[1])][4+m]='R'
                j=j-1

        if "xx|" in top[j][0] and not df.iat[i-1,7]==df.iat[i,7]:#Cosmetic, batter initials 
                top[j][0]=df.iat[i,7].split()[0][0]+df.iat[i,7].split()[1][0]+"|"
                batters[j]=df.iat[i,7].split(" ")[1]
        elif df.iat[i,9].__contains__("pinch hits"):
                foo=df.iat[i,11].split(" ")[6]
                bot[batters.index(foo)][5+m]=df.iat[i,9].split()[0][0]
                bot[batters.index(foo)][6+m]=df.iat[i,9].split()[1][0]
                batters[batters.index(foo)]=df.iat[i,9].split(" ")[1]
                j=j-1
                
        if df.iat[i,9].__contains__(" replaces ") and not df.iat[i,9].__contains__(" running "):
                foo=df.iat[i,9].split(" ")
                if df.iat[i,9].split(" ")[df.iat[i,9].split(" ").index("replaces")+3].startswith("pitching"):
                        foo.pop(df.iat[i,9].split(" ").index("replaces"))
                if foo.__contains__("replaces"):
                        batters[batters.index(foo[foo.index("replaces")+2])]=foo[foo.index("replaces")-1]
                i+=1
        elif df.iat[i,9].__contains__(" moves "):
                if df.iat[i,9].__contains__(" running "):
                        j+=1
                i+=1
    
        if df.iat[i-1,6]==awayTeam or df.iat[i,6]==awayTeam:#pointer for at bat order, storing order for previous team in order to switch between the two  
                l=awayOrder=j+1
        elif df.iat[i-1,6]==homeTeam or df.iat[i,6]==homeTeam:
                l=homeOrder=j-8

        while k<len(re.split(r';|:|/',df.iat[i,11])):#Base running forceouts
                if re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                        if re.split(r';|:|/',df.iat[i,11])[k].__contains__(" at 2B"):
                                top[batters.index(onBase[0])][3+m]='X'
                                top[batters.index(onBase[0])][4+m]=l                               
                        elif re.split(r';|:|/',df.iat[i,11])[k].__contains__(" at 3B"):
                                top[batters.index(onBase[1])][2+m]='X'
                                top[batters.index(onBase[1])][1+m]=l
                        elif re.split(r';|:|/',df.iat[i,11])[k].__contains__(" at Hm"):
                                mid[batters.index(onBase[2])][2+m]='X'
                                mid[batters.index(onBase[2])][1+m]=l       
                k+=1
        k=0

        while k<len(re.split(r';|:|/',df.iat[i,11])):#Base running
                if re.split(r';|:|/',df.iat[i,11])[k].__contains__("Scores"):
                        onBase[3]=re.split(r';|:|/',df.iat[i,11])[k].replace(" Scores", "").split(" ")[1]
                        foo=batters.index(onBase[3])
                        top[foo][3+m]='\\'
                        mid[foo][3+m]='/'
                        mid[foo][2+m]='\\'
                        top[foo][2+m]='/'
                        mid[foo][1+m]=l
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("to 3B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Single"):
                        onBase[2]=re.split(r';|:|/',df.iat[i,11])[k].replace(" to 3B", "").split(" ")[1]
                        foo=batters.index(onBase[2])
                        top[foo][3+m]='\\'
                        mid[foo][3+m]='/'
                        top[foo][2+m]='/'
                        top[foo][1+m]=l
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("to 2B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Single"):
                        onBase[1]=re.split(r';|:|/',df.iat[i,11])[k].replace(" to 2B", "").split(" ")[1].replace(" ","")
                        foo=batters.index(onBase[1])
                        top[foo][3+m]='\\'
                        mid[foo][3+m]='/'
                        top[foo][4+m]=l
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("to 1B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Single"):
                        onBase[0]=re.split(r';|:|/',df.iat[i,11])[k].replace(" to 1B", "").split("/")[0].replace(" ","")
                        foo=batters.index(onBase[0])
                        mid[foo][3+m]='/'
                        mid[foo][4+m]=l
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("Steals 3B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Single"):#Stolen Bases
                        onBase[2]=re.split(r';|:|/',df.iat[i,11])[k].replace(" Steals 3B", "").split(" ")[0].replace(" ","")
                        foo=batters.index(onBase[2])
                        top[foo][3+m]='\\'
                        mid[foo][3+m]='/'
                        top[foo][2+m]='/'
                        top[foo][1+m]='s'
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("Steals 2B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Single"):
                        onBase[1]=re.split(r';|:|/',df.iat[i,11])[k].replace(" Steals 2B", "").split(" ")[0].replace(" ","")
                        foo=batters.index(onBase[1])
                        top[foo][3+m]='\\'
                        mid[foo][3+m]='/'
                        top[foo][4+m]='s'
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("Steals 1B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Single"):
                        onBase[0]=re.split(r';|:|/',df.iat[i,11])[k].replace(" Steals 1B", "").split("/")[0].replace(" ","")
                        foo=batters.index(onBase[0])
                        mid[foo][3+m]='/'
                        mid[foo][4+m]='s'
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("out at"):#Base running outs
                        out=True
                        if re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__("1B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[1])
                                mid[foo][3+m]='X'
                                mid[foo][4+m]=l
                        elif re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__("2B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[1])
                                top[foo][3+m]='X'
                                top[foo][4+m]=l
                        elif re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__("3B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[1])
                                top[foo][2+m]='X'
                                top[foo][1+m]=l
                        elif re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__(" Hm"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[1])
                                top[foo][3+m]='\\'
                                top[foo][2+m]='/'
                                mid[foo][2+m]='X'
                                mid[foo][1+m]=l
                elif re.split(r';|:|/',df.iat[i,11])[k].__contains__("Caught"):#Caught Stealing
                        out=True
                        if re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__("1B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[0])
                                mid[foo][3+m]='X'
                                mid[foo][4+m]='C'
                        elif re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__("2B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[0])
                                top[foo][3+m]='X'
                                top[foo][4+m]='C'
                        elif re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__("3B") and not re.split(r';|:|/',df.iat[i,11])[k].__contains__("Forceout"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[0])
                                top[foo][2+m]='X'
                                top[foo][1+m]='C'
                        elif re.split(r';|:|/',df.iat[i,11])[k].split("/")[0].__contains__(" Hm"):
                                foo=batters.index(re.split(r';|:|/',df.iat[i,11])[k].split("/ | ;")[0].split(" ")[0])
                                top[foo][3+m]='\\'
                                top[foo][2+m]='/'
                                mid[foo][2+m]='X'
                                mid[foo][1+m]='C'
                k+=1
        k=0

        if df.iat[i,11].__contains__("Walk"):#At bat outcomes 
                onBase[0]=df.iat[i,7].split()[1]
                mid[j][3+m]='/'
                if df.iat[i,11].startswith("Intentional"):
                        mid[j][4+m]='I'
                else:
                        mid[j][4+m]='B'
                mid[j][5+m]='B'
        elif df.iat[i,11].__contains__("Single"):                
                onBase[0]=df.iat[i,7].split()[1]
                mid[j][3+m]='/'
                mid[j][4+m]='S'
        elif df.iat[i,11].__contains__("Double") and not df.iat[i,11].__contains__("Double Play"):                
                onBase[1]=df.iat[i,7].split()[1]
                top[j][3+m]='\\'
                mid[j][3+m]='/'
                top[j][4+m]='D'
                if df.iat[i,11].startswith("Ground-rule"):
                        mid[j][4+m]='R'
        elif df.iat[i,11].__contains__("Triple") and not df.iat[i,11].__contains__("Triple Play"):
                onBase[2]=df.iat[i,7]
                top[j][2+m]='/'
                top[j][3+m]='\\'
                mid[j][3+m]='/'
                top[j][1+m]='T'
        elif df.iat[i,11].__contains__("Home Run"):
                onBase[2]=df.iat[i,7]
                top[j][2+m]='/'
                mid[j][2+m]='\\'
                top[j][3+m]='\\'
                mid[j][3+m]='/'
                top[j][1+m]='H'
                mid[j][1+m]='R'
        elif df.iat[i,11].__contains__("Groundout"):
                mid[j][2+m]='G'
                mid[j][3+m]='O'
                print("True ",i,"+",j)
                out=True
        elif df.iat[i,11].__contains__("Lineout"):
                mid[j][2+m]='L'
                mid[j][3+m]='O'
                out=True
        elif df.iat[i,11].__contains__("Popfly"):
                mid[j][2+m]='P'
                mid[j][3+m]='F'
                out=True
        elif df.iat[i,11].__contains__("Flyball"):
                mid[j][2+m]='F'
                mid[j][3+m]='B'
                out=True
        elif df.iat[i,11].__contains__("Strikeout"):
                mid[j][2+m]='K'
                out=True
                
        if df.iat[i,11].__contains__("Double Play"):
                mid[j][5+m]='D'
                mid[j][6+m]='P'
                outs+=1
                out=True
                
        if df.iat[i,11].startswith("Triple Play"):
                mid[j][5+m]='T'
                mid[j][6+m]='P'
                outs+=2
                out=True
        
        while df.iat[i,11].__contains__("Scores"):#RBIs
                if df.iat[i,5].count('R')>=1:
                        top[j][6+m]='R'
                if df.iat[i,5].count('R')>=2:
                        top[j][5+m]='R'
                if df.iat[i,5].count('R')>=3:
                        mid[j][6+m]='R'
                if df.iat[i,5].count('R')==4:
                        mid[j][5+m]='R'
                        break
                else:
                        break
                
        if out==True:#Storing number of outs
                outs+=1
                out=False

        i+=1
        j+=1
        if outs>=1:#Number of outs (Cosmetic)
                bot[j-1][1+m]='o'
        if outs>=2:
                bot[j-1][2+m]='o'
        if outs==3:
                bot[j-1][3+m]='o'
                if df.iat[i-1,6]==awayTeam:
                        awayOrder=j
                        j=homeOrder+9
                        f=0
                        atBat=True
                elif df.iat[i-1,6]==homeTeam:
                        homeOrder=j-9
                        j=awayOrder
                        inning+=1
                        atBat=False
                i+=1
                outs=0
                onBase=[None,None,None,None]
                


        if j==9 and atBat==0:#Pointer going back to top of the order
                j=0
        elif j==18 and atBat==1:
                j=9
        if len(df)==i:#Break at end of data frame
                break
        k=0
        if df.iat[i,11].startswith("Top of the ") and inning>=9:#Extra innings
                l1=l1+str(inning+1)+"_____"
                l29=l29+"======="
                while k<len(top):
                        top[k]=top[k]+data+["|"]
                        mid[k]=mid[k]+data+["|"]
                        bot[k]=bot[k]+data1+["|"]
                        k+=1

end_time = time()
print(f'Time to compute: {end_time - start_time}')
#DEUBG
start_time = time()

#Print scorecard
print(l1)
i=0
while len(top)!=i:
        if i==9:
                print(l29)
        print("".join(str(x) for x in top[i]))#Thank you MidZik from the Python Discord Server
        print("".join(str(x) for x in mid[i]))
        print("".join(str(x) for x in bot[i]))
        i+=1
end_time = time()
print(f'Time to print: {end_time - start_time}')
