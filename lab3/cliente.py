# Cliente de dicionário usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# Classe da interface do cliente
class Interface:

  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.conn = None
    self.iniciaCliente()

  def iniciaCliente(self):
    #Cria um socket de cliente e conecta-se ao servidor.
    #Saida: socket criado

    #cria socket
    self.conn = rpyc.connect(self.ip, self.port)


  def fazRequisicoes(self):
    #Faz requisicoes ao servidor e exibe o resultado.
    #Entrada: socket conectado ao servidor

    # le as mensagens do usuario ate ele digitar 'fim'
    msg = input("\n Escolha uma opção abaixo: \n (1) Recuperar uma informação do dicionário (GET)\n (2) Inserir uma informação nova no dicionário (POST)\n (3) Encerrar conexão\n")
    if msg == '3':
      self.encerraConexao()
    elif msg == '1':
      msg = input("\n Digite a chave que quer recuperar: ")
      ret = self.conn.root.request("get "+ msg)
    elif msg == '2':
      msg = input("\n Digite a chave e a palavra que quer inserir na chave: ")
      ret = self.conn.root.request("post "+ msg)
    else:
      print("\n Opção inválida!")

    # imprime a mensagem recebida
    print(ret)

  # Descricao: encerra a conexao com o servidor
  def encerraConexao(self):
    self.conn.close()
    exit()

  

def main():
 #Funcao principal do cliente
 #inicia o a interface
 cliente = Interface('localhost', 10006)

 print('Bem vindo ao Dicionário Remoto!') 

 while True:
  cliente.fazRequisicoes()


main()