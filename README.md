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

Para executar, basta rodar o comando do Python 3 equivalente para o sistema (confirme se o comando realmente está executando o Python 3, ou vão ocorrer problemas) seguido pelo nome do arquivo da tarefa.

```
python3 sample.py
```

Fique observando as saídas do terminal para possíveis problemas na execução. Perceba que a ordem de execução correta é: código da tarefa em python seguido pela execução do código RSI no Kuka.

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

### Coleta de dados

É possível armazenar os dados que estão sendo enviados pelo Kuka em arquivos como .txt ou .csv. Para isso, basta utilizar as funções **start_collect** e **stop_collect**. Os dados são escritos linha a linha, separados por vírgula e seguindo a seguinte ordem:

```
time,x,y,z,rotx,roty,rotz,fx,fy,fz,mx,my,mz,
```

Os tempos sempre começam em zero e são incrementados em 12 ms (tempo de ciclo do robô). Abaixo temos exemplos de coleta de dados durante uma movimentação do robô:

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
# os dados serão salvos a partir deste momento no arquivo "dados_de_movimentacao.csv" na pasta "data/"
kr16.start_collect("data/dados_de_movimentacao.csv")
kr16.sleep(0.1)
kr16.move(x=200, y=350, x=-20)
kr16.sleep(0.1)
# encerra a coleta dos dados e salva no arquivo
# é preciso especificar o nome do arquivo da coleta que está encerrando pois mais de uma coleta podem estar ocorrendo ao mesmo tempo
kr16.stop_collect("data/dados_de_movimentacao.csv")
kr16.sleep(0.1)
kr16.stop_communication()

```

### Uso da garra pneumática

As funções **open_grip** e **close_grip** podem ser utilizadas para abrir e fechar a garra pneumática respectivamente. Por exemplo:

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
# abre a garra
kr16.open_grip()
kr16.move(x=100)
kr16.sleep(0.1)
# fecha a garra
kr16.close_grip()
kr16.sleep(0.1)
kr16.stop_communication()

```

### Acesso direto aos dados do robô

Os dados do robô são armazenados em uma pilha, sendo o primeiro dado sempre o mais recente.	Uma instância da classe Data() (veja a descrição da classe e seus atributos no arquivo [models.py](models.py)) pode ser obtida pela função **read**. Essa função por padrão retorna o último conjunto de dados recebido, mas podem acessados valores mais antigos utilizando o parâmetro *index*.

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
kr16.move(x=100)
kr16.sleep(0.1)
# salva o último dado recebido no objeto 'data'
data = kr16.read()
# salva o antepenúltimo dado recebido no objeto 'old_data'
old_data = kr16.read(index=-2)
kr16.sleep(0.1)
kr16.stop_communication()

```

Também é possível salvar a posição atual do robô em uma instância da classe Coordinates (veja a descrição da classe e seus atributos no arquivo [models.py](models.py)) utilizando a função **get_current_position**. Da mesma forma, é possível salvar as forças atuais lidas pelo sensor de força utilizando a função **get_current_forces**.

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
kr16.move(x=100)
kr16.sleep(0.1)
# salva a última posição recebido no objeto 'pos'
pos = kr16.get_current_position()
# salva a última leitura de força/torque recebido no objeto 'ft'
ft = kr16.get_current_forces()
# imprime na tela o valor da posição x
print(pos.x)
# imprime o valor da força em z
print(ft.z)
# imprime o valor do torque em x
print(ft.c)
kr16.sleep(0.1)
kr16.stop_communication()

```

### Ativando o controle de impedância

Para ativar o controle de impedância durante a execução do robô utilize a função **activate_impedance_control** passando como parâmetros o M, B e K correspondentes, aĺém do algoritmo utilizado na implementação. Recomenda-se utilizar sempre o modo *discretization* (mode='d'). No exemplo abaixo o controle de impedância e ativado enquanto o robô fica livre por 20 segundos. Perceba que o controle precisa ser ativado para cada eixo de movimentação separadamente. Ainda não foi implementado o controle para as rotações, apenas para translação. Para desativar o controle, basta chamar a função **deactivate_impedance_control**.

```
from robot_kuka import *
kr16 = RobotKuka()
kr16.start_communication("192.168.10.15", 6008)
kr16.wait_robot()
kr16.sleep(0.5)
# ativa o controle de impedancia em x
kr16.activate_impedance_control_x(m=20, b=200, k=2200, mode='d')
# ativa o controle de impedancia em y
kr16.activate_impedance_control_y(m=20, b=200, k=2200, mode='d')
# ativa o controle de impedancia em z
kr16.activate_impedance_control_z(m=20, b=400, k=4400, mode='d')
# atua somente com o controle por 20s
kr16.sleep(20)
# desativa o controle de impedancia
kr16.deactivate_impedance_control()
kr16.sleep(0.1)
kr16.stop_communication()

```

### Exemplo mais complexo com todas as funções disponíveis

```
from robot_kuka import *
from models import Coordinates
import os
import logging as log

log.warning('Initiating threading task')

newpath = r'/home/user/uka_comunication/connection/robot/data'
if not os.path.exists(newpath):
    os.makedirs(newpath)

kr16 = RobotKuka()                                  # cria uma nova instancia do robo
kr16.start_communication('192.168.10.15', 6008)     # inicia a comunicaçao com o ip do pc e a porta desejada
kr16.wait_robot()                                   # espera pelo robo comunicar

log.warning('Doing initial approx moves')

kr16.open_grip()                                    # abre a garra
kr16.move(x=90, y=-291, li_speed=30)                # move o robo da posicao inicial ate ficar sobre o colar
kr16.sleep(0.5)                                     # pausa 0.5s para restaurar a fila

kr16.move(z=162, li_speed=30)                       # desce sobre o colar
kr16.sleep(0.5)                                     # espera 0.5s

pos = Coordinates(x=kr16.get_current_position().x, y=kr16.get_current_position().y, z=kr16.get_current_position().z)

# <------------------------------------------ INICIA O MOVIMENTO EM LOOP

log.warning('Entered on loops')

for i in range(1, 11):

    log.warning('Experiment: ' + str(i))

    mount = 0
    jammed = 0

    kr16.move(z=50, li_speed=10)               # desce sobre o colar
    kr16.sleep(1)                               # espera 1s

    kr16.close_grip()                           # fecha a garra
    kr16.sleep(0.5)                             # espera 0.5s

    kr16.move(z=-50, li_speed=30)              # sobe a garra com o colar
    kr16.sleep(0.5)                             # espera 0.5s

    error = 3
    kr16.move(x=-104+error, y=2, li_speed=10)         # aproxima o colar do parafuso no plano xy
    kr16.sleep(0.5)                             # espera 0.5s

    kr16.move(z=25, li_speed=10)                # aproxima o colar do parafuso em z (desce)
    kr16.sleep(2)                               # espera 2s

    log.warning('Experiment: ' + str(i) + ' | adjust')

    kr16.start_collect(''.join([newpath + '/data_adjust-', str(i), '.csv']))    # inicia a coleta dos dados
    kr16.activate_impedance_control_x(m=20, b=200, k=2200, mode='d')            # ativa o controle de impedancia em x
    kr16.activate_impedance_control_y(m=20, b=200, k=2200, mode='d')            # ativa o controle de impedancia em y
    kr16.activate_impedance_control_z(m=20, b=400, k=4400, mode='d')            # ativa o controle de impedancia em z
    kr16.sleep(20)                                                              # atua somente com o controle por 20s
    kr16.deactivate_impedance_control()                                         # desativa o controle de impedancia
    kr16.sleep(0.5)                                                             # espera 0.5s
    kr16.stop_collect(''.join([newpath + '/data_adjust-', str(i), '.csv']))     # para a coleta dos dados

    log.warning('Experiment: ' + str(i) + ' | threading')

    kr16.start_collect(''.join([newpath + '/data_threading-', str(i), '.csv']))  # inicia a coleta dos dados
    kr16.move(a=300, an_speed=10)                                                # gira 270° para rosquear
    kr16.stop_collect(''.join([newpath + '/data_threading-', str(i), '.csv']))   # inicia a coleta dos dados

    kr16.open_grip()                                                    # abre a garra e solta o colar
    kr16.sleep(1)                                                       # espera 1s

    # plot(i)

    kr16.move(z=-40, li_speed=30)                                       # move 100mm em z (sobe a garra)
    kr16.sleep(1)                                                       # espera 1s

    kr16.move(a=-300, an_speed=20)                                      # gira -270° para rosquear
    kr16.sleep(0.5)                                                     # espera 0.5s

    current_position = kr16.get_current_position()
    x = current_position.y-pos.y
    y = current_position.x-pos.x
    z = current_position.z-pos.z
    kr16.move(x=x, y=y, z=z, li_speed=10)                               # volta com a garra para pegar o colar
    kr16.sleep(0.5)                                                     # espera 0.5s

# <------------------------------------------ FIM DO MOVIMENTO EM LOOP

kr16.stop_communication()                                               # finaliza a comunicaçao com o robo
```












