# kuka-python
Python library used to communicate and control Kuka manipulator (tested on KR16 model). Under continuous development.

## Versão: 1.0.0

### Novidades da nova versão

## Pré-requisitos
Python 3.x necessário.
Biblioteca testada nos seguintes plataformas:
* [Linux] Ubuntu 16.04
* [Linux] Ubuntu 14.04
* [Windows] Windows 7
* [Windows] Windows 10
Se você utilizou a bilbioteca em alguma outra plataforma e rodou tranquilamente ou obteve algum problema, por favor reporte aos desenvolvedores.

## Instalação da biblioteca
Faça o download do arquivo .zip do projeto ou clone via Git em diretório local. Se tiver baixado o .zip, faça a extração dos arquivos.
O Python 3.x deve estar instalado. Essa biblioteca não possui dependência de nenhuma outra biblioteca, portanto não exige nenhuma instalação adicional.

## Configurando o computador
A comunicação entre o computador e o robô Kuka é feita via Ethernet. Portanto, use um cabo de rede para conectar o controlador do Kuka diretamente ao seu pc (de preferência) ou conecte os dois numa mesma rede. O IP da sua máquina nessa rede deve ser modificado manualmente para "192.168.10.15" (padrão) com máscara de rede "255.255.255.0". Esse IP pode ser diferente, desde que seja passado corretamente na função que inicia a comunicação.
Para testar se a comunicação está funcionando corretamente utilize o comando ping para enviar pacotes de teste tanto para o IP da máquina
'''
ping 192.168.10.15
'''
quanto para o IP do robô
'''
ping 192.168.10.1
'''
Se tudo estiver certo os pacotes devem ser enviados e recebidos corretamente.

## Utilização da biblioteca









