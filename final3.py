#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division #para divisao correta (e.g. 1/2= 0.5 ao inves de 1/2= 0)
from decimal import Decimal
import os
import random
import re
import time
import math

path = os.getcwd()
subsets = [19, 2419, 4819, 7219, 9619, 12019, 14419, 16819, 19219, 21619, 24019]
delimiter = 0

def file_to_list(arq):

	with open(arq, "r") as f:
    		content = f.read()
	listaDeAtributos = re.split(r'[,;.:() ]+', content)
	f.close()
	
	return listaDeAtributos


def get_all_files():

    nros_positivos = 0
    nros_negativos = 0
    listaDePositivos = []
    listaDeNegativos = []
    for arqp in os.listdir(path + '/positivo'):
        fileNumber = int(arqp.split(".", 1)[0])
        if arqp.endswith(".txt") and (fileNumber <= subsets[delimiter] or fileNumber > subsets[delimiter+1]):
    	    nros_positivos +=1
    	    listaDePositivos.append(arqp)
    
    for arqn in os.listdir(path + '/negativo'):
        fileNumber = int(arqn.split(".", 1)[0])
        if arqn.endswith(".txt") and (fileNumber <= subsets[delimiter] or fileNumber > subsets[delimiter+1]):
            nros_negativos +=1
            listaDeNegativos.append(arqn)
    
    return [nros_positivos, nros_negativos, listaDePositivos, listaDeNegativos]

def get_test_files():
    y = 0
    listaDePositivos = []
    listaDeNegativos = []
    for arqp in os.listdir(path + '/positivo'):
        fileNumber = int(arqp.split(".", 1)[0])
        if arqp.endswith(".txt") and (fileNumber > subsets[delimiter] and fileNumber <= subsets[delimiter+1]):
            listaDePositivos.append(arqp)
    
    for arqn in os.listdir(path + '/negativo'):
        fileNumber = int(arqn.split(".", 1)[0])
        if arqn.endswith(".txt") and (fileNumber > subsets[delimiter] and fileNumber <= subsets[delimiter+1]):
            listaDeNegativos.append(arqn)
            
    return [listaDePositivos, listaDeNegativos]

    

def calculate_word_prob_in_class(vocabulario, palavra, nroPalavrasTotalClasse):

    vocabulario_tamanho = len(vocabulario) #nro de palavras distintas na classe

    if palavra in vocabulario:
        return ((vocabulario[palavra] + 1) / (nroPalavrasTotalClasse + vocabulario_tamanho))
    else:
        return ((0 + 1) / (nroPalavrasTotalClasse + vocabulario_tamanho))
    
        
def calculate_vnb(Doc, vocabulario_v, numeroTotalArquivos, numeroArquivosClasse, numeroPalavrasClasse):

    result_temp = 1
   
    for word in Doc:
        result_temp *= Decimal.from_float(calculate_word_prob_in_class(vocabulario_v, word, numeroPalavrasClasse))
    
    result = Decimal.from_float(numeroArquivosClasse/numeroTotalArquivos) * Decimal(result_temp)

    return result
    
def calculateClass(classNumber, classFolder):
    p = 0
    n = 0
    for d in test[classNumber]:
        fileNumber = int(d.split(".", 1)[0])
        if (fileNumber > subsets[delimiter] and fileNumber <= subsets[delimiter+1]):
            Doc = file_to_list(path + '/' + classFolder +'/' + d)
            pos = calculate_vnb(Doc, vocabularioPositivo, numeroTotalDeArquivos, numeroArquivosPositivos, nroPalavrasEmPositivo)
            neg = calculate_vnb(Doc, vocabularioNegativo, numeroTotalDeArquivos, numeroArquivosNegativos, nroPalavrasEmNegativo)

            if pos > neg:
                p += 1
            else:
                n += 1
    return p, n
    
def split_group():
    os.rename(source, destination)
    

if __name__ == "__main__":
    for i in range(len(subsets)-1):
        print()
        print('----- ' + str(subsets[i]+1) + ' - ' + str(subsets[i+1]) + ' ----')
        documents = get_all_files()
        
        numeroArquivosPositivos = documents[0]
        numeroArquivosNegativos = documents[1]
        
        numeroTotalDeArquivos = (numeroArquivosNegativos+numeroArquivosPositivos)
        
        prob_p = numeroArquivosPositivos/numeroTotalDeArquivos
        prob_n = 1 - prob_p
        
        #### Remove arquivo Texto se ja existe na pasta para criar um novo a seguir com todas as palavras
        try:
            os.remove('TextoP.txt')
            os.remove('TextoN.txt')
        except OSError:
            pass

        vocabularioPositivo = {}  #Vocabulario positivo representa a classe n1 e seus atributos
        vocabularioNegativo = {}  #Vocabulario negativo representa a classe n2 e seus atributos
        vocabularioCompleto = {}
        
        nroPalavrasEmPositivo = 0
        nroPalavrasEmNegativo = 0
        
        #### Adiciona todas as palavras dos textos das pastas "positivo" e "negativo" em 2 arquivos textos, 1 para cada pasta
        
        for doc in documents[2]: #documents[2] é a lista de positivos
            listaDeAtributos = file_to_list(path + '/positivo/' + doc)
            with open('TextoP.txt', "a") as TextP:
                TextP.write("\n".join(listaDeAtributos))
                for atributo in listaDeAtributos:
                    print(atributo)
                    nroPalavrasEmPositivo += 1
                    if atributo in vocabularioPositivo:
                        vocabularioPositivo[atributo] = vocabularioPositivo[atributo] + 1
                    else:
                        vocabularioPositivo[atributo] = 1
        TextP.close()
        
        for doc in documents[3]:
            listaDeAtributos = file_to_list(path + '/negativo/' + doc)
            with open('TextoN.txt', "a") as TextN:
                TextN.write("\n".join(listaDeAtributos))
                for atributo in listaDeAtributos:
                    nroPalavrasEmNegativo += 1
                    if atributo in vocabularioNegativo:
                        vocabularioNegativo[atributo] = vocabularioNegativo[atributo] + 1
                    else:
                        vocabularioNegativo[atributo] = 1

        TextN.close()

        fp = 0
        tn = 0
        tp = 0
        fn = 0
        test = get_test_files()
        
        vocabularioCompleto = { k: vocabularioPositivo.get(k, 0) + vocabularioNegativo.get(k, 0) for k in set(vocabularioPositivo) | set(vocabularioNegativo) }

        # Para cada arquivo da pasta de teste, faz o calculo

        tp, fn = calculateClass(0, 'positivo') #positivos
        fp, tn = calculateClass(1, 'negativo') #negativos

        print ('Falsos positivos:' + str(fp))
        print ('Falsos negativos:' + str(fn))
        print ('Verdadeiros positivos:' + str(tp))
        print ('Verdadeiros negativos:' + str(tn))
        delimiter = delimiter + 1
