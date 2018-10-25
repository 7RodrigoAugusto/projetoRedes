#	----	Projeto Final Redes	----
#	 Rodrigo Augusto Vasconcelos Sarmento - 11218021
#	 Yuri Oliveira
#	----						----	

#	----	Bibliotecas

# Para realizar a escolha aleatória de uma aresta

import random
import sys 

# Threads
import time
from threading import Thread

#	----	Classe vértice
class vertice:
	def __init__(self, caminho, nome, energia):         
         self.caminho = caminho
         self.nome = nome
         self.energia = energia

#	----	Classe aresta
class aresta:
     def __init__(self, u, v):
     	# Vértices
         self.u = u	
         self.v = v
    
       
#	-----	Conjunto que contém todas as arestas	-----        
conj_arestas = []

#	-----	Conjunto inicial de vértices	-----
conj_vertices = []

#	-----	Conjunto que contém os vértices já visitados	-----
vertices_aux = []


#	---------- Variáveis aux.	----------
dic_rota = {}		# A chave é o vértice, a informação é uma lista com a rota até ele
visitados = set()	# Variável que funciona para marcar os vértices já visitados
fila_espera = []	# Fila de espera dos vértices que foram encontrados mas ainda não deram broadcast
arestas_a_serem_removidas = set() # Arestas a serem removidas, pois já foram visitadas
fim = 0

#	-----	Função para abrir arquivos e criar o conjunto de arestas	-----
def abreArquivo():
	txt = open('nos.txt','r').readlines()
	array = []
	i = 0
	for item in txt:
		if i == 0:
			vetor_aux = item.strip('\n').split(' ')
			qtd_vertices, qtd_arestas= int(vetor_aux[2]),int(vetor_aux[3])
			i = i + 1
			pass
		else:
			vetor_aux = item.strip('\n').split(' ') 
			print('Inicio',vetor_aux[1],vetor_aux[2])
			conj_arestas.append(aresta(vetor_aux[1],vetor_aux[2]))
			array.append(vetor_aux)	#Removo o \n de cada elemento do array
	
	return array, qtd_vertices, qtd_arestas
	
#	----------	FUNÇÕES QUE MANIPULAM AS LISTAS CLASSE DE VÉRTICES	----------
#	-----	Cria conjunto de todos os vértices, com informação de cabeçalho
def cria_vertice(caminho, nome):
	print('Caminho e nome:',caminho, nome)
	vertices_aux.append(vertice(caminho,nome))
	return

def cria_vertices():
	set_nos = set()
	for item in conj_arestas:
		set_nos.add(item.u)
		set_nos.add(item.v)
	
	for item in set_nos:
		conj_vertices.append(vertice([],item, 100))
		
	print_vertices(conj_vertices)
	return	
	
def print_vertices(vertices):
	print(" ------------------------------ \n")
	print("Quantidade de vertices:",len(vertices_aux))
	print("Vertices existentes: \n")
	for obj in vertices:
		print(obj.caminho,obj.nome,obj.energia)
	
	print(" ------------------------------ \n")
	return		
	
	
			
#	----------	FUNÇÕES QUE MANIPULAM A CLASSE ARESTA	----------
#	-----	Função para printar as arestas durante os testes
def print_arestas():
	print(" ------------------------------ \n")
	print("Quantidade de arestas:",len(conj_arestas))
	print("Arestas existentes: \n")
	for obj in conj_arestas:
		print(obj.u,obj.v)
	
	print(" ------------------------------ \n")
	return	
		

# - Função que cria as arestas para devolver a informação 
def alert(aux):
	print("Destino encontrado com caminho:",aux)
	fim = 1
	print_vertices()
	sys.exit()
		
#	----------	************************************	----------

def descobre_vizinhos(fnt_momento,dest):
	# A disposição dos nós foi implementada na forma de arestas de ligação
	# Visito as arestas que estão conectadas com meu nó atual
	
	# Se a aresta destino for a mesma, fim!
	if fnt_momento == dest:
			aux = []
			aux.append(dic_rota[fnt_momento])
			alert(aux)
	else:
		# Busca arestas vizinhas
		for i in conj_arestas:
			print('Nós visitados:',visitados)
			# Se o nó já foi visitado, ignora, pois ele já tá na fila de inundação
			if (i.v or i.u) in visitados:
				pass
			else:
				# Se for o nó do momento e o destino, destino encontrado
				if fnt_momento == i.v and dest == i.u:		
					# - Encadeia rota
					aux = []
					for item in dic_rota[fnt_momento]:
						aux.append(item)
					aux.append(i.u)	
					
					# - Cria elemento da classe vértice, com informação do encadeamento
					cria_vertice(aux,i.u)
					alert(aux)
					
				# Se for nó do momento e o destino, destino encontrado	
				if fnt_momento== i.u and dest == i.v:				
					# - Encadeia rota
					aux = []
					for item in dic_rota[fnt_momento]:
						aux.append(item)
					aux.append(i.v)
					
					# - Cria elemento da classe vértice, com informação do encadeamento
					cria_vertice(aux,i.v)
					alert(aux)
					
				# Se for o nó atual, descobre os vizinhos, e encadeia cabeçalho	
				if fnt_momento == i.u:
					print("Estamos em:",fnt_momento,'Destino em:',dest)
					print('Testando aresta:',i.u,i.v)
					
					# - Encadeia rota
					aux = []
					for item in dic_rota[fnt_momento]:
						aux.append(item)
					aux.append(i.v)
					dic_rota[i.v] = aux
					atual = i.v
					
					# - Cria elemento da classe vértice, com informação do encadeamento
					cria_vertice(aux,atual)
					
					# - Adiciona a aresta, no conjunto de arestas a serem removidas
					arestas_a_serem_removidas.add(i)
					
					# - Adiciona o atual na fila de espera para visita
					fila_espera.append(atual)
					
				# Se for o nó atual, descobre os vizinhos, e encadeia cabeçalho		
				if fnt_momento == i.v:
					print("Estamos em:",fnt_momento,'Destino em:',dest)
					print('Testando aresta:',i.u,i.v)
					
					# - Encadeia rota
					aux = []
					for item in dic_rota[fnt_momento]:
						aux.append(item)
					aux.append(i.u)
					dic_rota[i.u] = aux	
					atual = i.u
					
					# - Cria elemento da classe vértice, com informação do encadeamento
					cria_vertice(aux,atual)
					
					# - Adiciona a aresta, no conjunto de arestas a serem removidas
					arestas_a_serem_removidas.add(i)
					
					# - Adiciona o atual na fila de espera para visita
					fila_espera.append(atual)
		
		
	# Remove arestas já visitadas	
	try:
		for k in arestas_a_serem_removidas:
			conj_arestas.remove(k)
		arestas_a_serem_removidas.clear()
	except:
		pass
		
	print('Dicionario:',dic_rota)
	
	# Adiciona o nó atual aos visitados
	visitados.add(fnt_momento)
	
	# Remove nó atual da fila de espera
	try:
		print('Removendo:'+"'"+fnt_momento+"'")
		del fila_espera[0]
	except:
		pass
	
	return 

def dsr(fnt,dest):
	# Verifico todos os vizinhos do meu nó fonte e dissemino informação
	print("Fonte:",fnt)
	print("Destino:",dest)
	dic_rota[fnt] = fnt
	
	# Descobre os vizinhos de um nó e encadeia caminho até ele!
	descobre_vizinhos(fnt,dest)
	
	# Print dos nós à serem visitados
	print(fila_espera)
	
	# Enquanto a fila de espera existir, e o nó destino não for encontrado
	while fila_espera != []:
		print("Ainda falta:",fila_espera)
		descobre_vizinhos(fila_espera[0],dest) 
	
	return

		
#	----------	main
def main():

	# - Abre o arquivo e cria os elementos da classe aresta
	elementos, qtd_vertices, qtd_arestas = abreArquivo()
	
	# - Cria todos os vértices
	cria_vertices()
	
	#	----------	 INFORMAÇÕES	--------------
	print("	----- INFORMAÇÕES ----- \n")
	print("Quantidade inicial de vértices(nós): \n",qtd_vertices)
	print("Inicialmente temos:",len(conj_arestas),"arestas\n")
	
	# - Apresenta o conjunto de arestas atual
	print_arestas()	
	#	----------	FIM INFORMAÇÕES	--------------
	
	fonte = '1'
	destino = '7'
	#	----------	 DSR	-------------- 
	dsr(fonte,destino)
	print_vertices(vertices_aux)
	
	return
	
	
main()
