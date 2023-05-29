# Servidor de dicionário usando RPC 
import sys
import rpyc # modulo que oferece suporte a abstracao de RPC

#servidor que dispara uma nova thread a cada conexao

from rpyc.utils.server import ThreadedServer

#servidor de echo: lado servidor
# com multiplexacao e finalizacao do lado do servidor
import threading

# cria um lock para ser usado na escrita do arquivo
lock = threading.Lock()

# Classe do banco de dados
class BancoDados():
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
    return 'A chave '+key+' possui o(s) valor(es): '+ self.data[key] + '- Success 200'

  # Descricao: adiciona um novo valor a uma chave ou cria uma nova chave
  # Entrada: chave e valor
  # Saida: mensagem de sucesso ou erro
  def post(self, key, value):
    lock.acquire()
    if key not in self.data:
      self.data[key] = value
      msg = 'Adicionado novo valor ' + value + ' na nova chave ' + key + '- Success 200'
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
class Servidor(rpyc.Service):

  def __init__(self, dicionario):
    self.dados = dicionario
    self.conexoes = []

 
  # Descricao: aceita o pedido de conexao de um cliente
	# executa quando uma conexao eh criada
  def on_connect(self, conn):
    print("Conexao iniciada: ", conn.root)
    self.conexoes.append(conn)


  # Descricao: encerra a conexao com o cliente
  def on_disconnect(self, conn):
    print("Conexão finalizada: ", conn.root)
    self.conexoes.remove(conn)

  def encerraConexao(self):
    if len(self.conexoes) != 0:
      print("Você ainda possui conexões pendentes")
    else:
      print("Encerrando servidor...")
      return True
      

  # Descricao: Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
  # Entrada: socket da conexao e endereco do cliente

  def exposed_request(self, msg):

    while True:

      # divide a requisicao do cliente entre header, chave e valor
      print(msg)
      msg = msg.split(' ')

      # verifica se a requisicao possui chave e valor ou apenas chave
      if len(msg) == 3:
        header, chave, valor = msg
      else:
        header, chave = msg
 
      if header == 'get': # cliente requisita dados
        msg = self.dados.get(chave)
        return msg
    
      if header == 'post': # cliente envia dados
        self.dados.post(chave,valor)
        return msg


  
def main():
 #Inicializa e implementa o loop principal (infinito) do servidor
 dicionario = BancoDados()

 print("Inicializando servidor...")
 servidor = ThreadedServer(Servidor(dicionario), port = 10006)
 print("Pronto para receber conexoes...")
 servidor.start()

 while True:
    cmd = input("Digite 'fim' para encerrar o servidor ou 'delete' para deletar uma chave")
    if cmd == 'fim': #solicitacao de finalizacao do servidor
      if servidor.encerraConexao: #somente termina quando nao houver clientes ativos
        servidor.close()
        servidor.dados.gravaMemoria()
        sys.exit()
    elif cmd == 'delete': #Deletar uma chave ou um valor específico de uma chave
      print('Digite a chave que deseja deletar: ')
      chave = input()
      servidor.dados.delete(chave)
      print('Chave deletada com sucesso!')
    else:
      print("Comando inválido, tente novamente")

if(__name__ == '__main__'):
    main()