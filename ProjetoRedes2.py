#	----	Projeto Final Redes	----
#	 Rodrigo Augusto Vasconcelos Sarmento - 11218021
#	 Yuri Oliveira
#	----						----	

#	----	Bibliotecas
# Para realizar a escolha aleatória de uma aresta
import random
import sys


#	---------- CLASSES	---------- 
 
# Classe vértice
class vertice:
	def __init__(self, caminho, nome, energia, info_response, dado, alcanca):         
         self.caminho = caminho				# Caminho até si # Informação advinda de um route request
         self.nome = nome					# Nome do nó
         self.energia = energia				# Energia do nó
         self.info_response = info_response	# Informação advinda de um route request
         self.dado = dado					# Informação advinda de um envio de dados
         self.alcanca = alcanca
# Classe aresta
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

#	----------	*******	----------

#	----------	FUNÇÕES CLASSE DE VÉRTICES	----------

# Cria conjunto de todos os vértices, com informação de cabeçalho
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
		conj_vertices.append(vertice([],item, 100, [], [], set()))
		
	print_vertices(conj_vertices)
	return	

# Print da lista de elementos da classe vértice	
def print_vertices(vertices):
	print("\t-----\t \n")
	print("Quantidade de vertices:",len(vertices))
	print("Vertices existentes: \n")
	for obj in vertices:
		print('Nome do nó:',obj.nome,'\t Caminho:',obj.caminho,'\t Energia:',obj.energia,'\t Caminho response:',obj.info_response,'\t Informação:', obj.dado,'\t Alcança:', obj.alcanca)
	print("\t-----\t \n")
	return		

# Retorna pelo nome do nó, o seu elemento na classe vértice	
def retorna_vertice(no):
	for item in conj_vertices:
		if no == item.nome:
			return	item
		else:
			pass

# Função que mapeia cada elemento, funciona como o "sinal" que entra no range dos elementos.
def mapeia_vertices():
	for item in conj_arestas:
		print(item.u,item.v)
		# Pego elementos vértices para adicionar os alcançáveis de cada 
		i = retorna_vertice(item.u)
		j = retorna_vertice(item.v)
		
		if i.alcanca is None:
			conj_range = set()	
			conj_range.add(item.v)
			i.alcanca = conj_range
		else:
			conj_range = i.alcanca
			conj_range.add(item.v)
			i.alcanca = conj_range
			
		if j.alcanca is None:
			conj_range = set()	
			conj_range.add(item.u)
			j.alcanca = conj_range
		else:
			conj_range = j.alcanca
			conj_range.add(item.u)
			j.alcanca = conj_range	
	
	return
		
#	----------	*******	----------
	
		
#	----------	FUNÇÕES CLASSE ARESTA	----------

# Função para printar as arestas durante os testes
def cria_arestas(txt):
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

	return	array, qtd_vertices, qtd_arestas

def print_arestas():
	print(" ------------------------------ \n")
	print("Quantidade de arestas:",len(conj_arestas))
	print("Arestas existentes: \n")
	for obj in conj_arestas:
		print(obj.u,obj.v)
	
	print(" ------------------------------ \n")
	return	
	
#	----------	*******	----------


#	----------	FUNÇÕES	----------

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

# Limpa fila para inundação, pois o destino foi encontrado
def limpa_fila_espera():
	fila_espera.clear()
	return

# Energia é consumida em broadcast, route response e envio de dados
def remove_energia(atual):
	atual = retorna_vertice(atual)
	atual.energia = atual.energia - 10
	# Se energia chegou a zero, então removo nó do alcance de todos
	#if atual.energia == 0:
	#	for i in conj_vertices:
	return

#	----------	*******	----------


#	----------	DSR	----------

# Verifico todos os vizinhos do meu nó fonte e dissemino informação
def dsr(fnt,dest,info):
	elemento = retorna_vertice(fnt)		 # Pego o elemento da classe vertice que representa o nó, neste caso o nó fonte
	elemento_dest = retorna_vertice(dest)# Pego o elemento da classe vertice que representa o nó, neste caso o nó destino
	
	# Print informações iniciais da inundação
	print("Fonte:",elemento.caminho,elemento.nome,elemento.energia)
	print("Destino:",elemento_dest.caminho,elemento_dest.nome,elemento_dest.energia)
	
	# Crio dicionário do meu nó fonte
	dic_rota[elemento.nome] = elemento.nome
	# O caminho para a fonte é ele mesmo
	elemento.caminho =	list(elemento.nome)
	elemento.dado = info
	
	print("\tInicializando o Route Request")
	# ------	ROUTE REQUEST	------
	# Encadeia caminho até os vizinhos de um nó
	broadcast(elemento.nome,elemento_dest.nome)
	# Enquanto a fila de espera para BROADCAST
	while fila_espera != []:
		print("Fila de broadcast:",fila_espera) # FILA DE ESPERA PARA BROADCAST
		broadcast(fila_espera[0],dest)
	#	----------	*******	----------
	print("\tFim do Route Request\n")
	
	print("\tInformação antes do Route Response \n")
	print_vertices(conj_vertices)
	print("\tInicializando o Route Response \n")
	route_response(elemento_dest)
	print("\tFim do Route Response \n")
	
	print("\tInformação antes do Envio de dados \n")
	print_vertices(conj_vertices)
	print("\tInicializando o envio de dados \n")
	envia_dados(elemento,info)
	print("\tFim do envio de dados \n")
	
	return

# BROADCAST entre vizinhos, faz parte do contexto ROUTE REQUEST
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
		# Começa buscando vizinhos da fonte
		elemento_aux = retorna_vertice(no_atual) # Pego o elemento que corresponde ao vértice
		for i in elemento_aux.alcanca:
			# Se o nó já fez broadcast, ignora
			if	i  in broadcast_completo:
				pass
			else:
				# Se for o destino, então destino encontrado
				if dest == i:		
					encadeia(no_atual,i)
					elemento_final = retorna_vertice(i)
					alert(elemento_final)
					return
				if i in visitados:
					pass
					
				else:
					encadeia(no_atual,i)
					arestas_a_serem_removidas.add(i)	# - Adiciona a aresta, no conjunto de arestas a serem removidas
					visitados.add(i)					# - Adiciona o nó que eu encontro, do meu atual, aos visitados
					fila_espera.append(i)				# - Adiciona o visitado na fila de espera para BROADCAST
					
		# Diminui energia
		remove_energia(no_atual)		
		broadcast_completo.add(no_atual)
				
		print('Dicionario:',dic_rota)
		# O primeiro nó nunca esteve na fila de espera
		if no_atual in fila_espera:
			remove_no_espera(no_atual)	# - Remove nó atual da fila de espera
	
	return 

# ROUTE RESPONSE em conjunto com  ARESTA RESPONSE transmite a informação do "Caminho response"
def route_response(destino):
	caminho_resposta = destino.caminho
	for i in reversed(caminho_resposta[:-1]):
		# Diminui energia
		remove_energia(i)
		aresta_response(i,caminho_resposta) # Passo para o vértice o caminho até o destino
	return	
	
def aresta_response(dest, caminho):
	elemento = retorna_vertice(dest)
	elemento.info_response = caminho
	return	
	
# ENVIA DADOS, repassa a informação pelo "Caminho response" aprendido
def envia_dados(fonte,dados):
	caminho = fonte.info_response
	# Posso fazer pra ficar pegando o dado sempre do anterior, pra parecer mais 'real'
	for i in caminho:
		# Diminui energia
		remove_energia(i)
		elemento = retorna_vertice(i)	# Pego elemento
		elemento.dado = dados
	return
	
#	----------	*******	----------

#	----------	MAIN	----------
def main():
 
	txt = open('nos.txt','r').readlines()						# - Abre o arquivo
	elementos, qtd_vertices, qtd_arestas = cria_arestas(txt)	# - Cria os elementos da classe aresta, para que o mapeamento dos vizinhos seja feito
	dados = 'Hoje vai fazer sol'
	cria_vertices()												# - Cria todos os vértices
	print('\tMapeia vértices\n')
	mapeia_vertices()											# - Mapeia vizinhos
	
	print('\nVértices com sua informação inicial de quem percebe quem na rede:')
	print_vertices(conj_vertices)
	
	#	----------	 INFORMAÇÕES	--------------
	print("\tINFORMAÇÕES\t\n")
	print("Quantidade de vértices(nós): ",qtd_vertices)
	#	----------	FIM INFORMAÇÕES	--------------
	
	fonte = '1'
	destino = '7'
	#	----------	 DSR	--------------
	
	# PRECISO DECICDIR EM QUAL MOMENTO EU TESTO A ENERGIA, ACREDITO QUE SEMPRE
	
	print('\tDSR\n')
	dsr(fonte,destino,dados)
	print('\tFim DSR\n')
	
	print('\tResultado:\n')
	print_vertices(conj_vertices)
	
	return
	
	
main()
