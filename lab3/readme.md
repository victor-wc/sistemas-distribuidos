# Laboratório 2: Dicionário Remoto

### Atividade 1
#### 1. O estilo arquitetural escolhido foi o de camadas. Ele servirá de base para para a minha aplicação
#### 2. A arquitetura será dividida em 3 camadas.
1.  A primeira será a interface que vai providenciar ao usuário comum da aplicação a posssibilidade de interagir e solicitar informações referentes a base de dados. Ele vai prover output ao usuário.
2. A segunda camada será o servidor da aplicação. Ele será responsável por gerenciar as conexões existentes, além de interagir tanto com o cliente quanto com o base de dados persistentes utilizada nessa atividade. Suas interações serão de adicionar informações, recuperar informações e deletar informações.
3. A última camada será a base de dados persistentes. Esta camada será responsável por gravar os dados da memória da aplicação na memória do disco bem como escrever os dados da memória de disco na da aplicação. Além disso, ela pode interagir com o servidor de forma que ela retorne os dados pedidos por ele, deletá-los ou adicioná-los.
4. O modo de conexão entre os componentes foi o TCP, que é o protocolo da camada de transporte orientado a conexão. Então, para que a troca de mensagens ocorra, é necessário que haja primeiro a conexão entre os sockets, para então começar a troca de mensagens.

### Atividade 2
#### 1. No lado do cliente, apenas os componentes de interação com o servidor serão incluídos, bem como mensagens da interface.
#### 2. No lado do servidor, tanto o banco de dados quanto o servidor em si ficarão nele. Os componentes de recuperar, adicionar, remover os dados, inicializar e gravar a memória serão funções nativas dele. Porém apenas o servidor será responsável por possuir funções e métodos que interajam com as funções nativas do banco de dados. Então é necessário essa camada intermediária entre o banco e o usuário para que as ações sejam registradas.
#### 3. A ordem das mensagens se dará da seguinte forma: A interface do cliente pedirá uma frase com formato de requisição (possui um método, uma chave e um valor). Essa mensagem será enviada para o servidor, que está constantemente esperando mensagens de clientes. Assim que ele receber essa mensagem, ele vai processar e verificar, através do método requisitado pelo cliente, como ele irá interagir com o banco de dados (a última camada). Identificado o método, o servidor fará um pedido ao banco de dados (de forma local visto que eles se encontram do mesmo lado da conexão) e receberá uma resposta, sendo ela um valor ou apenas uma mensagem. Após essa resposta, o servidor irá retransmitir essa mensagem de volta para o cliente (em sua interface), e a partir desse ponto, o cliente, que estava esperando a resposta do servidor, decidirá o que irá fazer com essa informação. Ele possui as escolhas tanto de pedir um informação, criar uma nova informação ou encerrar sua interação com o servidor.

### Atividade 3 (detalhes da implementação)
#### Lado do cliente: Decide criar uma classe para a interface, como forma de visualizar melhor os componentes da aplicação de forma mais isolada. Ele possui 3 métodos: Inicia, faz requisição e encerra a conexão. Criei uma main que vai ser responsável por inicialziar a interface e manter a conexão em  um loop até que o cliente queira que ela finalize.
##### Já do lado do servidor, criei duas classes. A primeira classe foi a "BancoDados" que vai ser responsável por armazenar as informações da memória volátil de forma persistente, além de inicializar as informações na memória volátil para que seja utilizada enquanto o servidor está ativo. Criei métodos nativos do banco de dados que serão usados pelo servidor par a conseguir interagir com ele. Decidi utilizar a convenção de nomes da arquitetura RestFUL, por se tratar de uma aplicação da arquitetura cliente-servidor e que faria sentido no caso da minha implementação. Além disso, utilizei a estrutura de dicionário em python, e cada chave pode possuir mais de um valor, porém este valor estará truncado em um string, onde as palavras serão separadas por ",". Apesar de não haver necessidade, criei códigos para simbolizar erros ou acertos das aplicações. Não decidi seguir com uma convenção específica, pois a ideia era manter a mensagem simples. Do lado do servidor, ele possui métodos similares aos do cliente, porém a implementação do atende requisições foi feita utilizando um While, pois ela se manterá ativa em todo o momento que o servidor estiver ligado. O usuário do servidor tem a possibilidade de apagar a entrada de uma chave do dicionário. Não decidi manter no mesmo padrão que as requisições feitas pelo cliente, pois se trata da interação com o servidor local.