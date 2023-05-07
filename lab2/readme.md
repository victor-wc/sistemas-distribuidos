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
#### 3. 