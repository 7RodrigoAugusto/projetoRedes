#	----	Projeto Final APA	----
#	Código Final APA - Rodrigo Augusto Vasconcelos Sarmento - 11218021
#	----						----	

#	----	Bibliotecas

# Para realizar a escolha aleatória de uma aresta
import random

# Threads
import time
from threading import Thread

#	----	Classe aresta
class aresta:
     def __init__(self, u, v):
     	# Vértices
         self.u = u	
         self.v = v
         
#	-----	Conjunto que contém todas as arestas         
conj_arestas = []

vertices_aux = []



#	-----	Função para abrir arquivos e criar o conjunto de arestas
def abreArquivo():
	#frb30-15-mis/frb30-15-1.mis
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
			conj_arestas.append(aresta(vetor_aux[1],vetor_aux[2]))
			array.append(vetor_aux)	#Removo o \n de cada elemento do array
	
	return array, qtd_vertices, qtd_arestas
	
#	----------	FUNÇÕES QUE MANIPULAM AS LISTAS E SETS DE VÉRTICES	----------
	
#	-----	Cria conjunto de todos os vértices para auxiliar na função limpa()
def cria_vertices():
	for item in conj_arestas:
		if item.u not in vertices_aux:
			vertices_aux.append(item.u)
		if item.v not in vertices_aux:
			vertices_aux.append(item.v)
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
		
#	-----	Remover arestas que contenham elementos dos vértices já escolhidos
def remove_arestas():
	for item in reversed(conj_arestas):
		#print(item.u,item.v)
		if item.u in conj_vertices:
			#print("Remove", item.u, item.v)
			conj_arestas.remove(item)
		elif item.v in conj_vertices:
			#print("Remove", item.u, item.v)
			conj_arestas.remove(item)
		else:
			#print("Fica", item.u, item.v)
			pass 
	return

# - Remove todas as arestas	
def remove_arestas_todas():
	for item in reversed(conj_arestas):	
		conj_arestas.remove(item)

#	-----	Cria o conjunto de arestas
def cria_arestas(objs):
	for item in objs:
		conj_arestas.append(aresta(item[1],item[2]))
	return
		
		
#	----------	************************************	----------

# Variáveis aux.
dic_rota = {}	# A chave é o vértice, a informação é uma lista com a rota até ele
visitados = set()
fila_espera = []
arestas_a_serem_removidas = set()
caminho = 0

def descobre_vizinhos(fnt_momento,dest):
	# A disposição dos meus nós foi implementada na forma de arestas de ligação
	for i in conj_arestas:
		# Não posso visitar quem já deve ser visitado
		if (i.v or i.u) in visitados:
			break
		if fnt_momento == i.v and dest == i.u:
			aux = []
			aux.append(dic_rota[fnt_momento])
			aux.append(i.u)
			print("Destino encontrado com caminho:",aux)
			caminho = aux
			return
		if fnt_momento== i.u and dest == i.v:
			aux = []
			aux.append(dic_rota[fnt_momento])
			aux.append(i.v)
			print("Destino encontrado com caminho:",aux)
			caminho = aux
			return
		if fnt_momento == i.u:
			print("Estamos em:",fnt_momento,'Destino em:',dest)
			print('Testando aresta:',i.u,i.v)
			aux = []
			aux.append(dic_rota[fnt_momento])
			aux.append(i.v)
			dic_rota[i.v] = aux
			atual = i.v
			#conj_arestas.remove(i)
			#descobre_vizinhos(atual,dest)
			arestas_a_serem_removidas.add(i)
			fila_espera.append(atual)
		if fnt_momento == i.v:
			print("Estamos em:",fnt_momento,'Destino em:',dest)
			print('Testando aresta:',i.u,i.v)
			aux = []
			aux.append(dic_rota[fnt_momento])
			aux.append(i.u)
			dic_rota[i.u] = aux	
			atual = i.u
			#conj_arestas.remove(i)
			#descobre_vizinhos(atual,dest)
			arestas_a_serem_removidas.add(i)
			fila_espera.append(atual)
		
	# Remove arestas ja utilizadas		
	for k in arestas_a_serem_removidas:
		conj_arestas.remove(k)
		
	arestas_a_serem_removidas.clear()	
	print(dic_rota)
	# Descobre vizinhos dos novos nos	
	copia = fila_espera
	#if copia == False:
	#	return
	print("Precisamos visitar:",fila_espera)
	for l in copia:
		fila_espera.remove(l)
		descobre_vizinhos(l,dest)
	
	return 

def dsr(fnt,dest):
	# Verifico todos os vizinhos do meu nó fonte e dissemino informação
	print("Fonte:",fnt)
	print("Destino:",dest)
	rota_final = []

	dic_rota[fnt] = fnt
	
	descobre_vizinhos(fnt,dest)
	if not fila_espera:
		print("Inundação completa")
		pass
	else
		descobre_vizinhos(fila_espera[0]) 
	
	return

		
#	-----	main
def main():

	# - Abre o arquivo e cria os elementos da classe aresta
	elementos, qtd_vertices, qtd_arestas = abreArquivo()
	
	#	----------	 INFORMAÇÕES	--------------
	print("	----- INFORMAÇÕES ----- \n")
	print("Quantidade inicial de vértices(nós): \n",qtd_vertices)
	print("Inicialmente temos:",len(conj_arestas),"arestas\n")
	
	# - Cria lista dos vértices para ajudar na função limpa()
	cria_vertices()
	print("Vertices_aux:",vertices_aux,"\n")
	
	# - Apresenta o conjunto de arestas atual
	print_arestas()	
	#	----------	FIM INFORMAÇÕES	--------------
	
	fonte = '1'
	destino = '7'
	#	----------	 DSR	-------------- 
	dsr(fonte,destino)
	print('Resultado:',caminho)
	
	return
	
	
main()
