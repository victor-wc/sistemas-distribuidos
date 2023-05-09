#servidor de echo: lado servidor
# com multiplexacao e finalizacao do lado do servidor
import socket
import select
import sys
import threading
from time import sleep

# cria um lock para ser usado na escrita do arquivo
lock = threading.Lock()

# Classe do banco de dados
class BancoDados:
  def __init__(self):
    self.data = {}
    self.inicializaMemoria()

  # Descricao: inicializa o banco de dados com os dados do arquivo memory.txt
  def inicializaMemoria(self):
   with open('memory.txt', 'r') as file:
    for line in file:
      key, value = line.split()
      self.data[key] = value

  # Descricao: grava o banco de dados no arquivo memory.txt
  def gravaMemoria(self):
    with open('memory.txt', 'w') as file:
      for key, value in self.data.items():
        file.write(key + ' ' + value + '\n') 

  # Descricao: retorna o valor da chave passada como parametro
  # Entrada: chave
  # Saida: valor da chave junto com mensagem de sucesso ou erro
  def get(self, key):
    if key not in self.data:
      return 'Chave não encontrada - Erro 500'
    return 'A chave '+key+' possui o(s) valor(es): '+ self.data[key] + '- Sucess 200'

  # Descricao: adiciona um novo valor a uma chave ou cria uma nova chave
  # Entrada: chave e valor
  # Saida: mensagem de sucesso ou erro
  def post(self, key, value):
    lock.acquire()
    if key not in self.data:
      self.data[key] = value
      msg = 'Adicionado novo valor ' + value + ' na nova chave ' + key + '- Sucess 200'
    else:
      self.data[key] = self.data[key] + ',' + value
      msg = 'Adicionado novo valor '+value+' na chave já existente '+key+'- Success 200'
    lock.release()
    return msg

  # Descricao: deleta uma chave
  # Entrada: chave
  # Saida: mensagem de sucesso ou erro
  def delete(self, key):
    if key not in self.data:
      return 'Chave não encontrada - Erro 500'
    lock.acquire()
    del self.data[key]
    lock.release()
    return 'Chave deletada - Sucess 200'

# Classe da interface do servidor e dos comandos
class Servidor:

  def __init__(self, ip, port, dicionario):
    self.ip = ip
    self.port = port
    self.sock = None
    self.conexoes = {}
    self.dados = dicionario
    # define a lista de I/O de interesse (não sei o que fazer com isso)
    self.entradas = [sys.stdin]
    self.iniciaServidor()

 
  # Descricao: inicia o servidor
  def iniciaServidor(self):

    # cria o socket 
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

    # vincula a localizacao do servidor
    self.sock.bind((self.ip, self.port))

    # coloca-se em modo de espera por conexoes
    self.sock.listen(5)

    # configura o socket para o modo nao-bloqueante
    self.sock.setblocking(False)

    # inclui o socket principal na lista de entradas de interesse
    self.entradas.append(self.sock) 



  # Descricao: aceita o pedido de conexao de um cliente
  # Entrada: o socket do servidor
  # Saida: o novo socket da conexao e o endereco do cliente

  def aceitaConexao(self):

    # estabelece conexao com o proximo cliente
    clisock, endr = self.sock.accept()

    # registra a nova conexao
    lock.acquire()
    self.conexoes[clisock] = endr
    lock.release()

    return clisock, endr
  
  # Descricao: encerra a conexao com o cliente
  def encerraConexaoCliente(self, clisock, endr):
    print(str(endr) + '-> encerrou a conexão.')

    # remove o cliente da lista de conexoes ativas
    lock.acquire()
    del self.conexoes[clisock]
    lock.release()

    # encerra a conexao com o cliente
    clisock.close()

  # Descricao: Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
  # Entrada: socket da conexao e endereco do cliente
  def atendeRequisicoes(self, clisock, endr):

    while True:

      #recebe dados do cliente
      data = str(clisock.recv(1024), encoding='utf-8')

      if not data: # dados vazios: cliente encerrou
        self.encerraConexaoCliente(clisock, endr)
        break

      # divide a requisicao do cliente entre header, chave e valor
      print("Mensagem enviada pelo Cliente de conexão "+ str(endr) + ": " + data)
      data = data.split(' ')

      # verifica se a requisicao possui chave e valor ou apenas chave
      if len(data) == 3:
        header, chave, valor = data
      else:
        header, chave = data
 
      if header == 'get': # cliente requisita dados
        clisock.send(self.dados.get(chave).encode('utf-8'))
    
      if header == 'post': # cliente envia dados
        clisock.send(self.dados.post(chave,valor).encode('utf-8'))


  
def main():
 #Inicializa e implementa o loop principal (infinito) do servidor
 dicionario = BancoDados()

 print("Inicializando servidor...")
 # Frufru para simular inicializacao de um servidor
 sleep(2)
 servidor = Servidor('', 10005, dicionario)
 print("Pronto para receber conexoes...")

 while True:

  # espera por qualquer entrada de interesse

  leitura, escrita, excecao = select.select(servidor.entradas, [], [])

  #tratar todas as entradas prontas

  for pronto in leitura:
    if pronto == servidor.sock:  #pedido novo de conexao
      clisock, endr = servidor.aceitaConexao()
      print ('Conectado com: ', endr)
      cliente = threading.Thread(target=servidor.atendeRequisicoes, args=(clisock, endr))
      cliente.start()
    elif pronto == sys.stdin: #entrada padrao
      cmd = input()
      if cmd == 'fim': #solicitacao de finalizacao do servidor
        if not servidor.conexoes: #somente termina quando nao houver clientes ativos
          servidor.dados.gravaMemoria()
          servidor.sock.close()
          sys.exit()
        else: print("O servidor ainda possui conexoes ativas com clientes")
      elif cmd == 'delete': #Deletar uma chave
        print('Digite a chave que deseja deletar: ')
        chave = input()
        servidor.dados.delete(chave)
        print('Chave deletada com sucesso!')

main()
