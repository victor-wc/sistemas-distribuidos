import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5014        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

# aqui o ativo envia uma mensagem e espera a resposta do passivo
while True:
    texto = input("Mensagem do ativo: ") # leitura da mensagem do ativo
    if(texto == 'fim'): break # encerra a conexao
    sock.send(bytearray(texto, 'utf-8')) # envia a mensagem para o passivo
    print("teste")
    msg = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem
    print("Resposta do passivo: "+str(msg,  encoding='utf-8')) # mostra a resposta do passivo

sock.close() # encerra a conexao
