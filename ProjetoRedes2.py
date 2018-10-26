#	----	Projeto Final Redes	----
#	 Rodrigo Augusto Vasconcelos Sarmento - 11218021
#	 Yuri Oliveira
#	----						----	

#	----	Bibliotecas
# Para realizar a escolha aleatória de uma aresta
import random
import sys


#	---------- CLASSES	----------  
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
         
#	---------- FIM CLASSES	----------       


#	---------- Variáveis aux.	----------    
conj_arestas = []	#	-----	Conjunto que contém todas as arestas	-----    
conj_vertices = []	#	-----	Conjunto inicial de vértices	-----
vertices_aux = []	#	-----	Conjunto que contém os vértices já visitados	-----

dic_rota = {}		# A chave é o vértice, a informação é uma lista com a rota até ele
visitados = set()	# Variável que funciona para marcar os vértices já visitados
fila_espera = []	# Fila de espera dos vértices que foram encontrados mas ainda não deram broadcast
arestas_a_serem_removidas = set() # Arestas a serem removidas, pois já foram visitadas
fim = 0
#	---------- FIM AUX	----------


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
	

#	----------	FUNÇÕES CLASSE DE VÉRTICES	----------

#	-----	Cria conjunto de todos os vértices, com informação de cabeçalho
def cria_vertice(caminho, nome):
	print('Caminho e nome:',caminho, nome)
	vertices_aux.append(vertice(caminho,nome))
	return

# Cria cada elemento da classe vértice
def cria_vertices():
	set_nos = set()
	for item in conj_arestas:
		set_nos.add(item.u)
		set_nos.add(item.v)
	
	for item in set_nos:
		conj_vertices.append(vertice([],item, 100))
		
	print_vertices(conj_vertices)
	return	

# Print da lista de elementos da classe vértice	
def print_vertices(vertices):
	print(" ------------------------------ \n")
	print("Quantidade de vertices:",len(vertices_aux))
	print("Vertices existentes: \n")
	for obj in vertices:
		print(obj.caminho,obj.nome,obj.energia)
	
	print(" ------------------------------ \n")
	return		

# Retorna pelo nome do nó, o seu elemento na classe vértice	
def retorna_vertice(no):
	for item in conj_vertices:
		if no == item.nome:
			return	item
		else:
			pass

#	----------	FIM VÉRTICES	----------	
	

			
#	----------	FUNÇÕES CLASSE ARESTA	----------
#	-----	Função para printar as arestas durante os testes
def print_arestas():
	print(" ------------------------------ \n")
	print("Quantidade de arestas:",len(conj_arestas))
	print("Arestas existentes: \n")
	for obj in conj_arestas:
		print(obj.u,obj.v)
	
	print(" ------------------------------ \n")
	return	

def remove_arestas_visitadas():
	# Remove arestas já visitadas	
	try:
		for k in arestas_a_serem_removidas:
			conj_arestas.remove(k)
		arestas_a_serem_removidas.clear()
	except:
		pass
	return		
#	----------	FIM ARESTAS	----------



#	----------	FUNÇÕES	----------
# - Função que cria as arestas para devolver a informação 
def alert(aux):
	print("Destino encontrado com caminho:",aux.caminho)
	fim = 1
	print_vertices(vertices_aux)
	sys.exit()

def encadeia(atual,vizinho):
	print(atual,vizinho)
	aux = []	# Lista auxiliar para conter os dados do caminho até o nó atual
	# Encontro o vizinho
	for item in dic_rota[atual]:
		aux.append(item)
	# Crio o caminho para o meu vizinho de acordo com o caminho para o atual + vizinho
	aux.append(vizinho)	
	
	# Retorno o elemento que representa o meu vizinho
	elemento_vizinho = retorna_vertice(vizinho)
	
	# Atualiza informação do vértice vizinho, com a lista de dados encadeados
	elemento_vizinho.caminho = aux
	
	try:
		dic_rota[vizinho] = aux
	except:
		pass
	
	return

def remove_no_espera(atual):
	# Remove nó atual da fila de espera
	try:
		print('Removendo:'+"'"+atual+"'")
		del fila_espera[0]
	except:
		pass
	return			

#	----------	************************************	----------

def broadcast(fnt_momento,dest):

	# A disposição dos nós foi implementada na forma de arestas de ligação
	# Visito as arestas que estão conectadas com meu nó atual
	print('Nós visitados:',visitados)
	# Se a aresta destino for a mesma, fim!
	if fnt_momento == dest:
			aux = []
			aux.append(dic_rota[fnt_momento])
			alert(aux)
	else:
		# Busca arestas vizinhas
		for i in conj_arestas:
			# Se o nó já foi visitado, ignora, pois ele já tá na fila de inundação
			if (i.v or i.u) in visitados:
				pass
			else:
				# Se for o nó do momento e o destino, destino encontrado
				if fnt_momento == i.v and dest == i.u:		
					encadeia(fnt_momento,i.u)
					elemento_final = retorna_vertice(i.u)
					alert(elemento_final)
					
				# Se for nó do momento e o destino, destino encontrado	
				if fnt_momento== i.u and dest == i.v:				
					encadeia(fnt_momento,i.v)
					elemento_final = retorna_vertice(i.v)
					alert(elemento_final)
					
				# Se for o nó atual, descobre os vizinhos, e encadeia cabeçalho	
				if fnt_momento == i.u:
					encadeia(fnt_momento,i.v)
					arestas_a_serem_removidas.add(i)	# - Adiciona a aresta, no conjunto de arestas a serem removidas
					fila_espera.append(i.v)				# - Adiciona o atual na fila de espera para visita
					
				# Se for o nó atual, descobre os vizinhos, e encadeia cabeçalho		
				if fnt_momento == i.v:
					encadeia(fnt_momento,i.u)
					arestas_a_serem_removidas.add(i)	# - Adiciona a aresta, no conjunto de arestas a serem removidas
					fila_espera.append(i.u)			# - Adiciona o atual na fila de espera para visita
		
	remove_arestas_visitadas()	# - Remove arestas já visitadas	
		
	print('Dicionario:',dic_rota)
	
	# Adiciona o nó atual aos visitados
	visitados.add(fnt_momento)
	
	remove_no_espera(fnt_momento)	# - Remove nó atual da fila de espera
	
	return 

def dsr(fnt,dest):
	# Verifico todos os vizinhos do meu nó fonte e dissemino informação
	elemento = retorna_vertice(fnt)		# Pego o elemento da classe vertice que representa o nó, neste caso o nó fonte
	elemento_dest = retorna_vertice(dest)# Pego o elemento da classe vertice que representa o nó, neste caso o nó destino
	
	# Print informações iniciais da inundação
	print("Fonte:",elemento.caminho,elemento.nome,elemento.energia)
	print("Destino:",elemento_dest.caminho,elemento_dest.nome,elemento_dest.energia)
	
	# Crio dicionário do meu nó fonte
	dic_rota[elemento.nome] = elemento.nome
	
	# Descobre os vizinhos de um nó e encadeia caminho até ele!
	broadcast(elemento.nome,elemento_dest.nome)
	
	# Print dos nós à serem visitados
	print(fila_espera)
	
	# Enquanto a fila de espera existir, e o nó destino não for encontrado
	while fila_espera != []:
		print("Ainda falta:",fila_espera)
		broadcast(fila_espera[0],dest) 
	
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
