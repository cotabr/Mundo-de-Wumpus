# **ETAPA 1 - Concluída**

<figure>
<center>
<img src='https://drive.google.com/uc?export=view&id=1lkwk72OaNdnkYdiHDC1K3PTNcsktZ-GC' width="600" />
</center>
</figure>

## **Primeiro ambiente gerado**

<p ALIGN=justify >O sistema gerado inicialmente é um ambiente composto por uma matriz de três por três, contendo dois espaços vazios, um wumpus e um tesouro. Esses objetos são distribuídos de forma aleatória pelo ambiente e somente um espaço fica livre constantemente, que será onde o agente irá começar o jogo. Embora tenha funcionado bem como protótipo, é importante salientar que sua capacidade ainda é limitada. Com isso em mente, procurou-se criar um ambiente capaz de se adaptar a diferentes tamanhos.</p>

## **Ambiente para qualquer tamanho**

<p ALIGN=justify >O ambiente agora permite que os usuários definam a quantidade de buracos, wumpus e tesouros, assim como o tamanho da matriz. Assim como no protótipo, os objetos são distribuídos aleatoriamente pelo ambiente e apenas um espaço permanece constantemente livre, onde o agente iniciará o jogo. Nesta versão, o ambiente pode ser configurado em qualquer tamanho e a quantidade de objetos pode ser personalizada de acordo com as preferências do usuário.</p>

<p ALIGN=justify >Além disso, cada objeto retornar para o agente uma percepção diferente, dentre elas temos: fedor (retornado pelo Wumpus), brisa (retornado pelo buraco) e brilho (retornado pelo ouro).</p>

[`Código de Implementação`](https://github.com/cotabr/Mundo-de-Wumpus/blob/main/Etapa%201/functions.py)
