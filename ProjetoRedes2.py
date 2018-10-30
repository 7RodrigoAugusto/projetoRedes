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


dic_rota = {}		# A chave é o vértice, a informação é uma lista com a rota até ele

visitados = set()	# Variável que funciona para marcar os vértices já visitados
broadcast_completo = set()	# Conjunto de nós que já fizeram broadcast

fila_espera = []	# Fila de espera dos vértices que foram encontrados mas ainda não deram broadcast
arestas_a_serem_removidas = set() # Arestas a serem removidas, pois já foram visitadas
fim = 0				# Variável que determina fim do broadcast (route request)


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
	print("Quantidade de vertices:",len(vertices))
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


# Limpa fila para inundação, pois o destino foi encontrado
def limpa_fila_espera():
	fila_espera.clear()
	return

#	----------	FUNÇÕES	----------
# - Função que cria as arestas para devolver a informação 
def alert(aux):
	print("Destino encontrado com caminho:",aux.caminho)
	fim = 1
	print_vertices(conj_vertices)
	limpa_fila_espera()
	return

def encadeia(atual,vizinho):
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
#nós já são visitados de cara, broadcast é outra coisa

def broadcast(no_atual,dest):
	# A disposição dos nós foi implementada na forma de arestas de ligação
	# Visito as arestas que estão conectadas com meu nó atual
	print('Nós visitados:', visitados)
	print("Nós com broadcast completo:", broadcast_completo)
	
	# Se a aresta destino for a mesma, fim!
	if no_atual == dest:
			aux = []
			aux.append(dic_rota[no_atual])
			alert(aux)
	else:
		# Busca arestas vizinhas
		for i in conj_arestas:
			# Se o nó já fez broadcast, ignora
			print(i.u,i.v)
			print("Nós com broadcast completo:", broadcast_completo)
			if	i.u  in broadcast_completo:
				print('O nó',i.u,'já fez broadcast')
				pass
			elif i.v in broadcast_completo:
				print('O nó',i.v,' já fez broadcast')
				pass
			else:
				# Se for o nó do momento e o destino, destino encontrado
				if no_atual == i.v and dest == i.u:		
					encadeia(no_atual,i.u)
					elemento_final = retorna_vertice(i.u)
					alert(elemento_final)
					return
					
				# Se for nó do momento e o destino, destino encontrado	
				if no_atual== i.u and dest == i.v:				
					encadeia(no_atual,i.v)
					elemento_final = retorna_vertice(i.v)
					alert(elemento_final)
					return
					
				# Se for o nó atual, descobre os vizinhos, e encadeia cabeçalho	
				if no_atual == i.u:
					if i.v in visitados:
						pass
					else:
						encadeia(no_atual,i.v)
						arestas_a_serem_removidas.add(i)	# - Adiciona a aresta, no conjunto de arestas a serem removidas
						visitados.add(i.v)					# - Adiciona o nó que eu encontro, do meu atual, aos visitados
						fila_espera.append(i.v)				# - Adiciona o visitado na fila de espera para BROADCAST
					
				# Se for o nó atual, descobre os vizinhos, e encadeia cabeçalho		
				if no_atual == i.v:
					if i.u in visitados:
						pass
					else:	
						encadeia(no_atual,i.u)
						arestas_a_serem_removidas.add(i)	# - Adiciona a aresta, no conjunto de arestas a serem removidas
						visitados.add(i.u)					# - Adiciona o nó que eu encontro, do meu atual, aos visitados
						fila_espera.append(i.u)				# - Adiciona o visitado na fila de espera para BROADCAST
				
		broadcast_completo.add(no_atual)
		
		print('Fila de espera:',fila_espera)
				
		remove_arestas_visitadas()	# - Remove arestas já visitadas	
		
		print('Dicionario:',dic_rota)
		# O primeiro nó nunca esteve na fila de espera
		if no_atual in fila_espera:
			remove_no_espera(no_atual)	# - Remove nó atual da fila de espera
	
	return 
	
def route_response():

	return	

def dsr(fnt,dest):
	# Verifico todos os vizinhos do meu nó fonte e dissemino informação
	elemento = retorna_vertice(fnt)		 # Pego o elemento da classe vertice que representa o nó, neste caso o nó fonte
	elemento_dest = retorna_vertice(dest)# Pego o elemento da classe vertice que representa o nó, neste caso o nó destino
	
	# Print informações iniciais da inundação
	print("Fonte:",elemento.caminho,elemento.nome,elemento.energia)
	print("Destino:",elemento_dest.caminho,elemento_dest.nome,elemento_dest.energia)
	
	# Crio dicionário do meu nó fonte
	dic_rota[elemento.nome] = elemento.nome
	# O caminho para a fonte é ele mesmo
	elemento.caminho =	list(elemento.nome)
	
	# Descobre os vizinhos de um nó e encadeia caminho até ele!
	broadcast(elemento.nome,elemento_dest.nome)
	
	# Enquanto a fila de espera para BROADCAST
	while fila_espera != []:
		print("Ainda falta:",fila_espera) # FILA DE ESPERA PARA BROADCAST
		if fim != 0:
			print('Destino:',elemento_dest.caminho,elemento_dest.nome,elemento_dest.energia)
			#route_response()
			sys.exit()
		else:
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
	print_vertices(conj_vertices)
	
	return
	
	
main()
