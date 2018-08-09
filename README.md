# kuka-python

Python library used to communicate and control Kuka manipulator (tested on KR16 model). Under continuous development.

### Versão: 1.0.0

## Pré-requisitos

Python 3.x necessário.

Biblioteca testada nas seguintes plataformas:

* [Linux] Ubuntu 16.04
* [Linux] Ubuntu 14.04
* [Windows] Windows 7
* [Windows] Windows 10

Se você utilizou a bilbioteca em alguma outra plataforma e rodou tranquilamente ou obteve algum problema, por favor reporte aos desenvolvedores.

## Instalação da biblioteca

Faça o download do arquivo .zip do projeto ou clone via Git em diretório local. Se tiver baixado o .zip, faça a extração dos arquivos.

O Python 3.x deve estar instalado. Essa biblioteca não possui dependência de nenhuma outra biblioteca, portanto não exige nenhuma instalação adicional.

## Configurando o computador

A comunicação entre o computador e o robô Kuka é feita via Ethernet. Portanto, use um cabo de rede para conectar o controlador do Kuka diretamente ao seu pc (de preferência) ou conecte os dois numa mesma rede. O IP da sua máquina nessa rede deve ser modificado manualmente para **192.168.10.15** (padrão) com máscara de rede **255.255.255.0**. Esse IP pode ser diferente, desde que seja passado corretamente na função que inicia a comunicação.

Para testar se a comunicação está funcionando corretamente utilize o comando **ping** para enviar pacotes de teste tanto para o IP da máquina

``` 
ping 192.168.10.15
```

quanto para o IP do robô

```
ping 192.168.10.1
```

Se tudo estiver certo os pacotes devem ser enviados e recebidos corretamente.

## Utilização da biblioteca

Para utilizar a biblioteca em um nova tarefa, basta criar um script do Python .py no diretório principal do projeto (veja o exemplo [sample.py](sample.py)). A base para estabelecer uma comunicação com o robô está no exemplo a seguir:

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
# your code goes here
kr16.stop_communication()

```

Este código importa a bilbioteca **robot_kuka** e cria uma instância da classe RobotKuka. Todas as funções utilizadas são métodos dessa classe. A função **start_communication** recebe como argumentos o IP da sua máquina e a porta definida para a comunicação e cria uma conexão com o controlador do robô. A função **wait_robot** é necessária para travar o código até que o robô seja acionado (código RSI executado). Sem ela, é possível que o computador comece a enviar dados para o robô sem ele estar em execução.

Tudo que vier em seguida está relacionado às necessidades da tarefa específica. Funções de movimentação, coleta de dados e controle de impedância serão detalhadas a seguir. O script deve ser finalizado pela função **stop_communication**, que encerra a conexão com o robô de forma segura.

## Ferramentas disponíveis

Todas as funções citadas nesse tópico estão implementadas e podem ser consultadas ou alteradas no arquivo [robot_kuka.py](robot_kuka.py).

### Movimentação

A função **sleep** faz o robô parar e ficar inativo pelo tempo passado como argumento, em segundos. É altamente recomendado que entre movimentações consecutivas exista pelo menos um intervalo de 0.1 segundos, evitando possíveis conflitos na execução com sobreposição de movimentos.

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
# O robô inicia a comunicação, espera 5 segundos e finaliza a conexão
kr16.sleep(5)
kr16.stop_communication()

```

A função **move** pode ser utilizada para movimentação relativa do robô, tanto translação como rotação. Veja o exemplo abaixo:

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
# movimenta 100 mm ao longo do eixo x, com velocidade linear de 100 mm/s
kr16.move(x=100, y=0, z=0, a=0, b=0, c=0, li_speed=100, an_speed=6)
kr16.sleep(0.1)
# os valores nulos default de movimentação podem ser emitidos, assim como as velocidades lineares e angulares default (100 mm/s e 6 deg/s)
kr16.move(x=100)
kr16.sleep(0.1)
# pode-se alterar os valores das velocidades
kr16.move(x=100, z=60, li_speed=300)
kr16.sleep(0.1)
kr16.stop_communication()

```

As movimentações de orientação são feitas utilizando ângulos de Euler (z-y'-x''). Por esse motivo, se quiser movimentar o robô para uma nova orientação, os movimentos devem ser separados e em ordem específica:

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
# movimenta 20 graus em torno do eixo z com 6 graus/s
kr16.move(a=20)
kr16.sleep(0.1)
# movimenta -60 graus em torno do eixo y com 10 graus/s
kr16.move(b=60, an_speed=10)
kr16.sleep(0.1)
# movimenta 60 graus em torno do eixo x com 6 graus/s
kr16.move(c=60)
kr16.sleep(0.1)
kr16.stop_communication()

```




testesGuilhermeRSI.xml




