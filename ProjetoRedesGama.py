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
	def __init__(self, caminho, nome, energia, cache, dado, alcanca, num_sequencia):         
         self.caminho = caminho				# Caminho até si # Informação advinda de um route request
         self.nome = nome					# Nome do nó
         self.energia = energia				# Energia do nó
         self.cache = cache	# Informação advinda de um route request
         self.dado = dado					# Informação advinda de um envio de dados
         self.alcanca = alcanca
         self.num_sequencia = num_sequencia
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

fila_espera = []	# Fila de espera dos vértices que foram encontrados mas ainda não deram broadcast
fim = 0				# Variável que determina fim do broadcast (route request)

def limpa_tudo():
	dic_rota = {}		# A chave é o vértice, a informação é uma lista com a rota até ele
	visitados = set()	# Variável que funciona para marcar os vértices já visitados
	fila_espera = []	# Fila de espera dos vértices que foram encontrados mas ainda não deram broadcast
	fim = 0				# Variável que determina fim do broadcast (route request)
	return

#procura se o destino esta na cache do nó fonte
def ProcuraNaCache(fonte, destino): 
	fonte = retorna_vertice(fonte)
	destino = retorna_vertice(destino)
	for lista in fonte.cache:
		for no in lista: 
			#se o destino estiver na cache, retorna o caminho
			if destino.nome == no:
				print(destino.nome)
				aux = fonte.cache
				aux.append(lista)
				fonte.cache = aux
				return lista
	return False
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
	
	for item in set_nos:		#caminho, nome, energia, cache, dado, alcanca, nm_sequencia
		conj_vertices.append(vertice([],item, 100, [[]], [], set(),0))
		
	print_vertices(conj_vertices)
	return	

# Print da lista de elementos da classe vértice	
def print_vertices(vertices):
	print("\t-----\t \n")
	print("Quantidade de vertices:",len(vertices))
	print("Vertices existentes: \n")
	for obj in vertices:
		print('Nome do nó:',obj.nome,'\tNúmero de sequência',obj.num_sequencia,'\t Caminho:',obj.caminho,'\t Energia:',obj.energia,'\t Caminho response:',obj.cache,'\t Informação:', obj.dado,'\t Alcança:', obj.alcanca)
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
	# break e chama DSR(fonte,dst) novamente
	return

#	----------	*******	----------


#	----------	DSR	----------

# Verifico todos os vizinhos do meu nó fonte e dissemino informação
def dsr(fnt,dest,info,n_seq):
	elemento = retorna_vertice(fnt)		 # Pego o elemento da classe vertice que representa o nó, neste caso o nó fonte
	elemento_dest = retorna_vertice(dest)# Pego o elemento da classe vertice que representa o nó, neste caso o nó destino
	
	# Print informações iniciais da inundação
	print("Fonte:",elemento.nome,elemento.energia)
	print("Destino:",elemento_dest.nome,elemento_dest.energia)
	print("Número de sequência do broadcast:",n_seq)
	
	# Crio dicionário do meu nó fonte
	dic_rota[elemento.nome] = elemento.nome
	# O caminho para a fonte é ele mesmo
	elemento.caminho =	list(elemento.nome)
	elemento.dado = info
	elemento.num_sequencia = n_seq
	
	print("\tInicializando o Route Request")
	# ------	ROUTE REQUEST	------
	# Encadeia caminho até os vizinhos de um nó
	broadcast(elemento.nome,elemento_dest.nome)
	# Enquanto a fila de espera para BROADCAST
	while fila_espera != []:
		print("Fila de broadcast:",fila_espera) # FILA DE ESPERA PARA BROADCAST
		aux = fila_espera[0] 
		# Adiciona num. de sequência antes de fazer broadcast
		aux = retorna_vertice(aux)
		aux.num_sequencia = n_seq
		broadcast(fila_espera[0],dest)
	
	#	----------	*******	----------
	print("\tFim do Route Request\n")
	
	print("\tInformação antes do Route Response \n")
	print_vertices(conj_vertices)
	print("\tInicializando o Route Response \n")
	route_response(elemento_dest,fnt)
	print("\tFim do Route Response \n")
	
	
	# O destino não necessariamente vai ser o final da cache, pode ser outra coisa
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
	
	# Se o nó atual for igual ao destino, fim
	if no_atual == dest:
			aux = []
			aux.append(dic_rota[no_atual])
			alert(aux)
	else:
		# Começa buscando vizinhos da fonte
		elemento_aux = retorna_vertice(no_atual) # Pego o elemento que corresponde ao vértice
		for i in elemento_aux.alcanca:
			i_aux = retorna_vertice(i)
			# Se o nó já fez broadcast, ignora. Para isso testo o número de sequência do broadcast
			if	i_aux.num_sequencia  == elemento_aux.num_sequencia:
				print('Já foi visitado:',i_aux.nome,i_aux.num_sequencia)
				pass
			else:
				# Se for o destino, então destino encontrado
				if dest == i:		
					encadeia(no_atual,i)
					elemento_final = retorna_vertice(i)
					elemento_final.num_sequencia = elemento_aux.num_sequencia
					alert(elemento_final)
					return
				if i in visitados:
					pass
				else:
					encadeia(no_atual,i)
					visitados.add(i)					# - Adiciona o nó que eu encontro, do meu atual, aos visitados
					fila_espera.append(i)				# - Adiciona o visitado na fila de espera para BROADCAST
					
		# Diminui energia
		remove_energia(no_atual)
				
		print('Dicionario:',dic_rota)
		
		# O primeiro nó nunca esteve na fila de espera
		if no_atual in fila_espera:
			remove_no_espera(no_atual)	# - Remove nó atual da fila de espera
	
	return 

# ROUTE RESPONSE em conjunto com  ARESTA RESPONSE transmite a informação do "Caminho response"
def route_response(destino,fonte):
	caminho_resposta = destino.caminho
	#no_atual = destino
	# Faço um for de todos os meus nós vizinhos
	# Para cada um deles faço uma função que testa se aquela informação é realmente pra ele
	# Se não for não atualiza informação
	# Se for atualiza informação
	'''
	while no_atual != fonte:
		print('No atual momento:',no_atual.nome)
		near = no_atual.alcanca				# Vizinhos do meu nó atual
		for item in near:					# Checo vizinhos ao meu nó atual
			item = retorna_vertice(item)	# Pego o elemento do meu vizinho
			print('Testando nó:',item.nome)
			if item.nome in caminho_resposta:
				print('Sou parte do caminho:', item.nome)
				remove_energia(no_atual.nome)
				aresta_response(no_atual.nome,caminho_resposta)
				no_atual = item
				print('Novo nó atual:',no_atual.nome)
				break
			else:
				print(item.nome)
				print('Não faço parte do caminho')
	'''	
	for i in reversed(caminho_resposta[:-1]):
		# Diminui energia
		remove_energia(i)
		aresta_response(i,caminho_resposta) # Passo para o vértice o caminho até o destino
	return	
	
def aresta_response(dest, caminho):
	elemento = retorna_vertice(dest)
	aux = elemento.cache
	aux.append(caminho)
	elemento.cache = aux
	return	
	
# ENVIA DADOS, repassa a informação pelo "Caminho response" aprendido
def envia_dados(fonte,dados):
	print('Fonte:',fonte.nome)
	caminho = fonte.cache[-1]	# Pego a última informação que foi adicionada ao meu cache
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
	num_sequencia = 'T1'
	# procura_na_cache()
	#	----------	 DSR	--------------
	
	# PRECISO DECICDIR EM QUAL MOMENTO EU TESTO A ENERGIA, ACREDITO QUE SEMPRE
	
	print('\tDSR\n')
	dsr(fonte,destino,dados,num_sequencia)
	print('\tFim DSR\n')
	
	print('\tResultado:\n')
	print_vertices(conj_vertices)
	
	limpa_tudo()
	# Limpo número de sequência também
	
	dados = "Deu certo"
	fonte = '1'
	destino = '6'
	num_sequencia ='T2'
	
	teste = ProcuraNaCache(fonte,destino)
	if teste == False:
		dsr(fonte,destino,dados,num_sequencia)
	else:
		fonte = retorna_vertice(fonte)
		envia_dados(fonte,dados)
	
	print_vertices(conj_vertices)

	dados = "Deu certo 2"
	fonte = '2'
	destino = '9'
	num_sequencia ='T3'
	
	teste = ProcuraNaCache(fonte,destino)
	if teste == False:
		dsr(fonte,destino,dados,num_sequencia)
	else:
		fonte = retorna_vertice(fonte)
		envia_dados(fonte,dados)
	
	print_vertices(conj_vertices)
	
	
	return
	

# Número de sequência diferente para cada tipo(route request, response, enviar dados)
	
main()
