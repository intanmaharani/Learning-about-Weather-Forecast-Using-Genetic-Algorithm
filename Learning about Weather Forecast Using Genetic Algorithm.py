# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:37:04 2019

@author: intan
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import csv
import random



# tentukan lokasi file, nama file, dan inisialisasi csv
#t = pd.read_csv('latih.csv')
#t.select_dtypes(include=[suhu])
#print(t.head(80))
#s = open('data_uji_opsi_1.csv', 'r')
#u = open('target_latih_opsi_1.csv','r')
#baca = csv.reader(s)
#membaca = csv.reader(u)
from numpy import array
from numpy import argmax
#from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import OneHotEncoder
from numpy import array
from numpy import argmax
#from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import OneHotEncoder
    
def readData():
    x = []
    with open('latih.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
           x.append(row)
    x.remove(x[0])
    return x
training = readData()

def encodeTrainingData(training): 
# data[0] = suhu, data[1] = waktu, data[2] = langit, data[3] = kelembapan, data[4] = terbang
    arr,dataTrain,tmp = [],[],[]
    x,q = [],[]
    
    for data in training: 
        suhu,waktu,langit,lembap,status = "","","","",""
        #arr = []
        if (data[0] == "rendah"):
            suhu = "001"
            arr.extend([0,0,1])
        elif (data[0] == "normal"): 
            suhu = "010" 
            arr.extend([0,1,0])
        elif (data[0] == "tinggi"): 
            suhu = "100"
            arr.extend([1,0,0])
        
        if (data[1] == "pagi"):
            waktu = "1000" 
            arr.extend([1,0,0,0])
        elif (data[1] == "siang"): 
            waktu = "0100" 
            arr.extend([0,1,0,0])
        elif (data[1] == "sore"): 
            waktu = "0010" 
            arr.extend([0,0,1,0])
        elif (data[1] == "malam"): 
            waktu = "0001"
            arr.extend([0,0,0,1])       
        
        if (data[2] == "berawan"):
            langit = "1000" 
            arr.extend([1,0,0,0])
        elif (data[2] == "cerah"): 
            langit = "0100" 
            arr.extend([0,1,0,0])
        elif (data[2] == "rintik"): 
            langit = "0010" 
            arr.extend([0,0,1,0])
        elif (data[2] == "hujan"): 
            langit = "0001"
            arr.extend([0,0,0,1])
        
        if (data[3] == "rendah"):
            lembap = "001" 
        elif (data[3] == "normal"): 
            lembap = "010" 
        elif (data[3] == "tinggi"): 
            lembap = "100"
            
        if data[4] == "Ya":
            terbang = "1"
        else:
            terbang = "0"
        
        genTraining = suhu+waktu+langit+lembap+terbang
        dataTrain.append(genTraining)
    for i in dataTrain:
        for z in range(len(i)):
            x.append(i[z])
        q.append(x)
        x = []
        
    return q
def encodeUji(ujidata): 
# data[0] = suhu, data[1] = waktu, data[2] = langit, data[3] = kelembapan, data[4] = terbang
    uji = []
    
    for data in ujidata: 
        suhu,waktu,langit,lembap,status = "","","","",""
        #arr = []
        if (data[0][:3] == ['0','0','1']):
            suhu = "rendah"
        elif (data[0][:3] == ['0','1','0']): 
            suhu = "normal" 
        elif (data[0][:3] == ['1','0','0']): 
            suhu = "tinggi" 
        
        if (data[0][3:7] ==['1','0','0','0']):
            waktu = "pagi" 
        elif (data[0][3:7] == ['0','1','0','0']): 
            waktu = "siang" 
        elif (data[0][3:7] == ['0','0','1','0']): 
            waktu = "sore" 
        elif (data[0][3:7] == ['0','0','0','1']): 
            waktu = "malam"     
        
        if (data[0][7:11] == ['1','0','0','0']):
            langit = "berawan" 
        elif (data[0][7:11] == ['0','1','0','0']): 
            langit = "cerah" 
        elif (data[0][7:11] == ['0','0','1','0']): 
            langit = "rintik" 
        elif (data[0][7:11] == ['0','0','0','1']): 
            langit = "hujan"
        
        if (data[0][11:14] == ['0','0','1']):
            lembap = "rendah" 
        elif (data[0][11:14] == ['0','1','0']): 
            lembap = "normal" 
        elif (data[0][11:14] == ['1','0','0']): 
            lembap = "tinggi"
            
        if data[0][14:15] == ['1']:
            terbang = "ya"
        else:
            terbang = "tidak"
        
        genUji = [suhu,waktu,langit,lembap,terbang]
        uji.append(genUji)
        

        
    return uji

#melakukan generate kromosom dengan maks 2 rule
def generatekromosom():
    arr = [15,30]
    q = ["0","1"]
    kromosom = [] 
    for i in range(random.choice(arr)):
        kromosom.append(random.choice(q))
    return kromosom
    #print (kromosom)

#melakukan generate populasi
def generatepopulation(p):
    populasi = []
    for i in range(p):
        individu = generatekromosom()
        populasi.append(individu)
    return populasi

def split(arr, size):
     arraySplit = []
     while len(arr) > size:
         slice = arr[:size]
         arraySplit.append(slice)
         arr   = arr[size:]
     arraySplit.append(arr)
     return arraySplit

def cariKesamaanAcie(suhu,waktu,langit,lembap,status,dataTrain):
    suhuTrain,waktuTrain,langitTrain,lembapTrain,statusTrain,data = [],[],[],[],[],[]
    cek = False
    cekSuhu,cekWaktu,cekLangit,cekLembap,cekStatus = False,False,False,False,False
    for k in range(0,3):
        suhuTrain.append(dataTrain[k])
    data.append(suhuTrain)
    for k in range(3,7):
        waktuTrain.append(dataTrain[k])
    data.append(waktuTrain)
    for k in range(7,11):
        langitTrain.append(dataTrain[k])
    data.append(langitTrain)
    for k in range(11,14):
        lembapTrain.append(dataTrain[k])
    data.append(lembapTrain)
    data.append([dataTrain[14]])
    #print(suhu,data[0])
    count = 0
    if(suhu == ["1","1","1"] and (data[0] == ["1","0","0"] or data[0] == ["0","1","0"] or data[0] == ["0","0","1"])):
        cekSuhu = True
    elif(suhu == ["1","1","0"] and (data[0] == ["1","0","0"] or data[0] == ["0","1","0"])):
        cekSuhu = True
    elif(suhu == ["1","0","1"] and (data[0] == ["1","0","0"] or data[0] == ["0","0","1"])):
        cekSuhu = True
    elif(suhu == ["0","1","1"] and (data[0] == ["0","1","0"] or data[0] == ["0","0","1"])):
        cekSuhu = True
    else:
        if(suhu == data[0]):
            cekSuhu = True
        elif(suhu != data[0]):
            cek = False
        
    if(waktu == ["1","1","1","1"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","1","0","0"] or data[1] == ["0","0","1","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True
    elif(waktu == ["1","1","1","0"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","1","0","0"] or data[1] == ["0","0","1","0"])):
        cekWaktu = True
    elif(waktu == ["1","1","0","1"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","1","0","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True 
    elif(waktu == ["1","0","1","1"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","0","1","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True 
    elif(waktu == ["0","1","1","1"] and (data[1] == ["0","1","0","0"] or data[1] == ["0","0","1","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True 
    elif(waktu == ["1","1","0","0"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","1","0","0"])):
        cekWaktu = True 
    elif(waktu == ["1","0","0","1"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True
    elif(waktu == ["0","0","1","1"] and (data[1] == ["0","0","1","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True 
    elif(waktu == ["1","0","1","0"] and (data[1] == ["1","0","0","0"] or data[1] == ["0","0","1","0"])):
        cekWaktu = True 
    elif(waktu == ["0","1","0","1"] and (data[1] == ["0","1","0","0"] or data[1] == ["0","0","0","1"])):
        cekWaktu = True
    elif(waktu == ["0","1","1","0"] and (data[1] == ["0","1","0","0"] or data[1] == ["0","0","1","0"])):
        cekWaktu = True
    else:
        if(waktu == data[1]):
            cekWaktu = True
        elif(waktu != data[1]):
            cek = False
    
    if(langit == ["1","1","1","1"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","1","0","0"] or data[2] == ["0","0","1","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True
    elif(langit == ["1","1","1","0"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","1","0","0"] or data[2] == ["0","0","1","0"])):
        cekLangit = True
    elif(langit == ["1","1","0","1"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","1","0","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True 
    elif(langit == ["1","0","1","1"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","0","1","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True 
    elif(langit == ["0","1","1","1"] and (data[2] == ["0","1","0","0"] or data[2] == ["0","0","1","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True 
    elif(langit == ["1","1","0","0"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","1","0","0"])):
        cekLangit = True 
    elif(langit == ["1","0","0","1"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True
    elif(langit == ["0","0","1","1"] and (data[2] == ["0","0","1","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True 
    elif(langit == ["1","0","1","0"] and (data[2] == ["1","0","0","0"] or data[2] == ["0","0","1","0"])):
        cekLangit = True 
    elif(langit == ["0","1","0","1"] and (data[2] == ["0","1","0","0"] or data[2] == ["0","0","0","1"])):
        cekLangit = True
    elif(langit == ["0","1","1","0"] and (data[2] == ["0","1","0","0"] or data[2] == ["0","0","1","0"])):
        cekLangit = True
    else:
        if(langit == data[2]):
            cekLangit = True
        elif(langit != data[2]):
            cek = False

    if(lembap == ["1","1","1"] and (data[3] == ["1","0","0"] or data[3] == ["0","1","0"] or data[3] == ["0","0","1"])):
        cekLembap = True
    elif(lembap == ["1","1","0"] and (data[3] == ["1","0","0"] or data[3] == ["0","1","0"])):
        cekLembap = True
    elif(lembap == ["1","0","1"] and (data[3] == ["1","0","0"] or data[3] == ["0","0","1"])):
        cekLembap = True
    elif(lembap == ["0","1","1"] and (data[3] == ["0","1","0"] or data[3] == ["0","0","1"])):
        cekLembap = True
    else:
        if(lembap == data[3]):
            cekLembap = True
        elif(lembap != data[3]):
            cek = False
            
    if status == data[4]:
        cekStatus = True
        
   
    if cekSuhu and cekStatus and cekWaktu and cekLangit and cekLembap:
        return True
    else:
        return False

#menghasilkan nilai fitness dalam bentuk proporsi 100% berdasarkan kecocokan antara kromosom dengan data train
def fungsi_fitness(fit):
    return (fit/80)
 
def hitungfitness(listRule):
    x = encodeTrainingData(training)
    q = 0
    nilai_fitness = []

    for rule in listRule:
        fit = 0
        for i in rule:
         #   print("rule",i)

            suhu,waktu,langit,lembap,status = [],[],[],[],[]
            for k in range(0,3):
                suhu.append(i[k])
            for k in range(3,7):
                waktu.append(i[k])
            for k in range(7,11):
                langit.append(i[k])
            for k in range(11,14):
                lembap.append(i[k])
            status.append(i[14])
            #dataRule = [suhu,waktu,langit,lembap,status]
            for data in x:
               q = cariKesamaanAcie(suhu,waktu,langit,lembap,status,data)
              # print(q)
               if q :
                   fit+=1
    #hasil fitness dari keseluruhan rule dalam kromosom
        fitness = fungsi_fitness(fit)
        nilai_fitness.append(fitness)
    return nilai_fitness
    #break
    #print(fit)
    #print("fitness =",nilai_fitness)
    #fitness = fungsi_fitness(fit)
    

#mendapatkan parent dari fitness terbaik untuk membangun generasi selanjutnya
def roulettewheelselection(populasi, fitness):
    total = np.sum(fitness)
    r = np.random.uniform()
    individu = 0
    while (r>0 and individu<9):
        r -= fitness[individu]/total
        individu += 1
        #if individu == len(populasi)-2:
            #break
            #pass
    return populasi[individu]

#crossover dimana parent1 dari angka random sesuai panjang rule, parent2 crossover disetiap titik potong pada setiap rulenya
def crossover(populasi, fitness):
    #mating = []
    LC = []
    x = []
    #TP = []
    #for i in range(len(fitness)//2):
    parent1 = roulettewheelselection(populasi, listFitness)
    parent2 = roulettewheelselection(populasi, listFitness)
    #print("panjang =",len(parent2))
    while (len(LC)==0):
        T1 = np.random.randint(len(parent1))
        T2 = np.random.randint(len(parent2))
        
        if T1 > T2:
            tmp = T1
            T1 = T2
            T2 = tmp
        else:
            tmp = T2
            T2 = T1
            T1 = tmp
        s1 = T1 % 15
        s2 = T2 % 15    
        banyakaturanperkromosom = len(parent2)//15
 #       print("Banyak aturan =",banyakaturanperkromosom)
        for i in range(banyakaturanperkromosom):
        #mendapatkan kemungkinan titik potong di setiap rulenya
            for j in range(i,banyakaturanperkromosom):
                f = i*15+s1
                g = j*15+s2
                if f > g:
                    break
                LC.append([f,g])
    
    idx = random.randint(0,len(LC)-1)
    x = LC[idx]
    child1 = (parent1[:T1]+parent2[x[0]:x[1]]+parent1[T2:])
    child2 = (parent2[:x[0]]+parent1[T1:T2]+parent2[x[1]:])
    child = [child1,child2]
    #print("kemungkinan =",child)
    return child
    #print("kemungkinan =",child)
   # print("anak1 =",child1)
  #  print("anak 2 =",child2)
    #print(arrCrossover)

def mutation(populasi):
    for i in range(len(populasi)):
        pilihmutasi = np.random.rand()
        if pilihmutasi < 0.01:
            kromosom = populasi[i]
            gen = np.random.randint(len(kromosom))
            if kromosom[gen] == 1: kromosom[gen] = 0
            elif kromosom[gen] == 0: kromosom[gen] = 1
            populasi[i] = kromosom
    return populasi

def generational_replacement(populasi):
    listpopulasi = []
    for i in populasi:
        listpopulasi.append(split(i,15))    
    nilai_fitness = hitungfitness(listpopulasi)
    idx = np.argmax(nilai_fitness)    
    populasibaru = [populasi[idx]]
    while len(populasibaru) < 10:
        offspring = crossover(populasi, nilai_fitness)
        populasibaru.extend(offspring)
     
    populasibaru = mutation(populasibaru)
    return populasibaru,nilai_fitness

def geneticalgorithm():
    anyar = []
    generasi = 0
    populasi = generatepopulation(10)
    while generasi<10:
        generasi += 1
        populasi,fit = generational_replacement(populasi)
        
        
        for i in populasi:
            #print(len(i))
            anyar.append(split(i,15))
  #          list_best.append(split(i,15)) 
        
        #print("Fitness dari Populasi Terbaik : ",fit)
 #       print(list_best)
        #print(anyar)
        nilai_fitness = hitungfitness(anyar)       
        idx = np.argmax(nilai_fitness)       
        best_kromosom = anyar[idx]
        
        
    print("Populasi Terbaik : ",anyar)
    print("nilai fitness dari populasi terbaik : ", nilai_fitness)
    print("index fitness terbaik : ",idx)
    print("kromosom terbaik : ",best_kromosom)
    return anyar
        
#cek = ['0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1']
populasi = generatepopulation(10)
listpopulasi = []
list_rule = []
for i in populasi :
    list_rule.append(split(i,15))

#print("list fitness =",listFitness)
listFitness = hitungfitness(list_rule)
listCrossover = crossover(populasi, listFitness)
listHasil = mutation(populasi)
listBaru = generational_replacement(populasi)
listGA = geneticalgorithm()
#print()
ujidataencode = encodeUji(listGA)
print("Hasil data uji: ",ujidataencode)
with open("Intan Maharani.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(ujidataencode)


#print("populasi dipertahankan =", listBaru)
#rint(listGA)
#print("hasil mutasi=",populasi)
#print("populasi dipertahankan =", populasibaru)
#parent1 = roulettewheelselection(populasi, listFitness)
#parent2 = roulettewheelselection(populasi, listFitness)
#print(parent1)
#print(parent2)

#nilai_fitness = hitungfitness(populasi)
#print(nilai_fitness)

#hasilfitness = hitungfitness(listRule)
#print(hasilfitness)

#print("---Encode---")
#x = encodeTrainingData(training)
#for i in x:
 #   print(i)
    
#print("---Split---")    
#print(split(populasi,15))
