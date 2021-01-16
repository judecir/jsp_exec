import numpy as np
import os

# Checar se a matriz de tempo e ordem esta com as dimensoes corretas
def jsp_checar_tempo_ordem(_tempo, _ordem):
    tempo_n_linha, tempo_n_coluna = len(_tempo), len(_tempo[0])
    ordem_n_linha, ordem_n_coluna = len(_ordem), len(_ordem[0])
    
    if tempo_n_linha!=ordem_n_coluna or tempo_n_coluna!=ordem_n_linha:
        print("Erro: \n \t Tempo: ", (tempo_n_linha, tempo_n_coluna)
                    ,"\n \t Ordem: ", (ordem_n_linha, ordem_n_coluna))
        return False
    return True

def read_instance_from_taillard(nome_arquivo):
        
    instancias = []
    i = 0
    n=0
    m=0
    tempo=[]
    ordem=[]
    
    fl_tempo = False
    fl_ordem = False
    fl_instancia = False
    fl_inicio = True
    
    f = open("INSTANCES/"+nome_arquivo, "r")
    
    for l in f:
        termos = l.split()
        #print(termos)
        if fl_inicio:
            n=int(termos[0])
            m=int(termos[1])
            fl_inicio=False
        
        if fl_ordem and len(termos) > 1:
            ordem.append([int(t) for t in termos])
        if fl_tempo and len(termos) > 1:
            tempo.append([int(t) for t in termos])

        if str(termos[0])=="Times":
            fl_tempo = True
            fl_ordem = False
        elif str(termos[0])=="Machines":
            fl_tempo = False
            fl_ordem = True

    tempo = np.array(tempo)
    ordem = np.array(ordem)-1
    tempo_formatado = np.zeros((m,n))-np.inf
    for i in range(m):
        for j in range(n):
            maq = ordem[j,i]
            tempo_formatado[maq, j] = int(tempo[j, i])
            #print(j,i, maq)
            
            

    instancias = {"id":nome_arquivo.replace('.txt', '')
                    ,"n":n
                    ,"m":m
                    ,"tempo":tempo_formatado
                    ,"ordem":ordem
                    ,"lista_ub":[0]}

    f.close()

    
    return instancias

def read_instance_others(nome_arquivo):
    n=0
    m=0
    fl_inicial = True
    
    tempo = []
    ordem = []
    
    f = open("INSTANCES/"+nome_arquivo, "r")
    
    
    for l in f:
        termos = l.split()
        #print(termos)
        if fl_inicial:
            n = int(termos[0])
            m = int(termos[1])
            fl_inicial = False
        else:
            ordem.append([int(termos[t]) for t in range(len(termos)) if t%2==0])
            tempo.append([int(termos[t]) for t in range(len(termos)) if t%2==1])
            
    tempo = np.array(tempo) 
    ordem = np.array(ordem) 
    
    tempo_formatado = np.zeros((m,n))-np.inf
    for i in range(m):
        for j in range(n):
            maq = ordem[j,i]
            tempo_formatado[maq, j] = int(tempo[j, i])
            #print(j,i, maq)
    
    instancias = {"id":nome_arquivo.replace('.txt', '')
                    ,"n":n
                    ,"m":m
                    ,"tempo":tempo_formatado
                    ,"ordem":ordem
                    ,"lista_ub":[0]}

    f.close()
    
    return instancias

def criar_instancias():
    instancias = []

    # n=4, m=3
    tempo = np.array([[1, 5, 5, 10],
                      [3, 8, 8, 6],
                      [2, 10, 4, 4]])
    ordem = np.array([[0, 1, 2], 
                      [1, 0, 2],
                      [0, 2, 1],
                      [2, 0, 1]])
    if jsp_checar_tempo_ordem(tempo, ordem):
        instancias.append({"id":'mini1', "tempo": tempo, "ordem": ordem, "lista_ub":[0]})
    
    #n=5, m=3
    tempo = np.array([[1, 5, 5, 10, 7],
            		  [3, 8, 8, 6, 8], 
            		  [2, 10, 4, 4, 3]])
    ordem = np.array([[0, 1, 2],
            		  [1, 0, 2],
            		  [0, 2, 1],
            		  [2, 0, 1], 
            		  [1, 2, 0]])    
    if jsp_checar_tempo_ordem(tempo, ordem):
        instancias.append({"id":'mini2', "tempo": tempo, "ordem": ordem, "lista_ub":[0]})
        
    arquivos = os.listdir('INSTANCES')
    arquivos = [i for i in arquivos if '.txt' in i and 'desktop' not in i and 'PACKED' not in i]
    arquivos = [i for i in arquivos if 'yn' not in i]

    for arq in arquivos:
        #print(arq)
        if 'ta' in arq:
            instancias.append(read_instance_from_taillard(arq))
        else:
            instancias.append(read_instance_others(arq))
            
    return instancias
