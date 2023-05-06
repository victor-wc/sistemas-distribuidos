#servidor de echo: lado cliente
import socket

HOST = 'localhost' # maquina onde esta o servidor
PORT = 10006      # porta que o servidor esta escutando

class Interface:

  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.sock = None
    self.iniciaCliente()

  def iniciaCliente(self):
    #Cria um socket de cliente e conecta-se ao servidor.
    #Saida: socket criado
    #cria socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet (IPv4 + TCP) 

    # conecta-se com o servidor
    self.sock.connect((self.ip, self.port)) 


  def fazRequisicoes(self):
    '''Faz requisicoes ao servidor e exibe o resultado.
    Entrada: socket conectado ao servidor'''
    # le as mensagens do usuario ate ele digitar 'fim'

    msg = input("Digite uma mensagem ('fim' para terminar):")
    if msg == 'fim':
     self.encerraConexao()
    else:
     # envia a mensagem do usuario para o servidor
     self.sock.send(msg.encode('utf-8'))

     #espera a resposta do servidor
     msg = self.sock.recv(1024) 

     # imprime a mensagem recebida
     print(str(msg, encoding='utf-8'))

  def encerraConexao(self):
    self.sock.close()
    exit()

  

def main():
 '''Funcao principal do cliente'''
 #inicia o a interface
 cliente = Interface('localhost', 10004)

 print('Bem vindo ao Dicionário Remoto!') 
 print('O formato da mensagem deve ser: HEADER CHAVE VALOR')

 while True:
  cliente.fazRequisicoes()


main()