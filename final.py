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
        if arqp.endswith(".txt"):
    	    nros_positivos +=1
    	    listaDePositivos.append(arqp)
 
    for arqn in os.listdir(path + '/negativo'):
        if arqn.endswith(".txt"):
    	    nros_negativos +=1
            listaDeNegativos.append(arqn)
            
    return [nros_positivos, nros_negativos, listaDePositivos, listaDeNegativos]

def get_test_files():

    listaDePositivos = []
    listaDeNegativos = []
    for arqp in os.listdir(path + '/positivoteste'):
        if arqp.endswith(".txt"):
    	    listaDePositivos.append(arqp)
 
    for arqn in os.listdir(path + '/negativoteste'):
        if arqn.endswith(".txt"):
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
        #result_temp += math.log(Decimal(calculate_word_prob_in_class(vocabulario_v, word, numeroPalavrasClasse)), 2)
	result_temp *= Decimal(calculate_word_prob_in_class(vocabulario_v, word, numeroPalavrasClasse))
	
    #result = Decimal(numeroArquivosClasse/numeroTotalArquivos) + Decimal(result_temp)
    result = Decimal(numeroArquivosClasse/numeroTotalArquivos) * Decimal(result_temp)

    return result

if __name__ == "__main__":

    
    
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
    
    for doc in documents[2]:
        listaDeAtributos = file_to_list(path + '/positivo/' + doc)
        with open('TextoP.txt', "a") as TextP:
            TextP.write("\n".join(listaDeAtributos))
            for atributo in listaDeAtributos:
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

    p = 0
    n = 0
    test = get_test_files()
    
    vocabularioCompleto = { k: vocabularioPositivo.get(k, 0) + vocabularioNegativo.get(k, 0) for k in set(vocabularioPositivo) | set(vocabularioNegativo) }

    # Para cada arquivo da pasta de teste, faz o calculo

    for d in test[1]:
	
	Doc = file_to_list(path + '/negativoteste/' + d)
        pos = calculate_vnb(Doc, vocabularioPositivo, numeroTotalDeArquivos, numeroArquivosPositivos, nroPalavrasEmPositivo)
        print pos
        neg = calculate_vnb(Doc, vocabularioNegativo, numeroTotalDeArquivos, numeroArquivosNegativos, nroPalavrasEmNegativo)
        print neg

        if pos > neg:
            print "POSITIVO"
            p += 1
        else:
            print "NEGATIVO"
            n += 1

    print 'positivos:' + str(p)
    print 'negativos:' + str(n)
