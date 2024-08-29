import nn
import os
import pickle

angry=[]

for i in os.listdir('keypoints/angry'):
     with open(f'keypoints/angry/{i}','rb') as file:
         angry.append(pickle.load(file).xyn.flatten().tolist())
print(len(angry[0]),sep='\n')

happy=[]

for i in os.listdir('keypoints/happy'):
     with open(f'keypoints/happy/{i}','rb') as file:
         happy.append(pickle.load(file).xyn.flatten().tolist())
sad=[]

for i in os.listdir('keypoints/sad'):
     with open(f'keypoints/sad/{i}','rb') as file:
         sad.append(pickle.load(file).xyn.flatten().tolist())
fear=[]

for i in os.listdir('keypoints/fear'):
     with open(f'keypoints/fear/{i}','rb') as file:
         fear.append(pickle.load(file).xyn.flatten().tolist())
disquised=[]

for i in os.listdir('keypoints/disquised'):
     with open(f'keypoints/disquised/{i}','rb') as file:
         disquised.append(pickle.load(file).xyn.flatten().tolist())
neutral=[]

for i in os.listdir('keypoints/neutral'):
     with open(f'keypoints/neutral/{i}','rb') as file:
         neutral.append(pickle.load(file).xyn.flatten().tolist())
angry1=[]
happy1=[]
sad1=[]
fear1=[]
disquised1=[]
neutral1=[]
for i in angry:
    if len(i)==34:
        angry1.append(i)
for i in happy:
    if len(i)==34:
        happy1.append(i)
for i in fear:
    if len(i)==34:
        fear1.append(i)
for i in disquised:
    if len(i)==34:
        disquised1.append(i)
for i in sad:
    if len(i)==34:
        sad1.append(i)
for i in neutral:
    if len(i)==34:
        neutral1.append(i)
x=angry1+happy1+fear1+disquised1+sad1+neutral1
y=[]
for i in angry1:
    y.append([1,0,0,0,0,0])
for i in happy1:
    y.append([0,1,0,0,0,0])
for i in fear1:
    y.append([0,0,1,0,0,0])
for i in disquised1:
    y.append([0,0,0,1,0,0,])
for i in sad1:
    y.append([0,0,0,0,1,0])
for i in neutral1:
    y.append(([0,0,0,0,0,1]))
try:
    with open('pose-recognition/nn', 'rb') as file:
        network=pickle.load(file)
except:
    network=nn.NeuralNetwork([[34,nn.sigmoid],[200,nn.sigmoid],[150,nn.sigmoid],[100,nn.sigmoid],[6,nn.sigmoid]])
i=0
while True:
    i+=1
    network.train(x,y,0.00001,1,True)
    if i%100==0:
        with open('pose-recognition/nn', 'wb') as file:
            pickle.dump(network,file,0)
    print(i)