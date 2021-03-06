# Notícias sobre desinformação - NetLab
#### Autora: [Danielle de Pinho Mello](https://www.linkedin.com/in/danielledepinho/)
<br/>

A proposta deste projeto é coletar pelo menos 50 notícias sobre desinformação no Portal G1 e indexá-las na base Elasticsearch.

## Sumário

- [Sobre](#sobre)
- [Desenvolvimento](#desenvolvimento)
- [Implantação](#implantação)

## Sobre

Este projeto tem o objetivo de coletar e indexar notícias do Portal G1 sobre desinformação. O projeto consiste em um script python que utiliza a biblioteca requests para acessar e coletar as notícias, e utiliza a biblioteca BeautifulSoup para extrair do HTML os dados de título, data e corpo de cada notícia. 
Após a coleta, os dados são inseridos em uma base Elasticsearch e podem ser visualizados e manipulados através da UI Kibana.

O script python foi desenvolvido seguindo o paradigma de Programacão Orientada a Objetos (OOP).


## Desenvolvimento

Para a execução do script em ambiente local de desenvolvimento, é utilizada a ferramenta docker-compose através do seguinte comando:
```bash
$ docker-compose up
```

Após a execução do script, os dados estarão indexados no Elasticsearch e poderão ser visualizados e manipulados através da UI Kibana. O Kibana pode ser acessado através da url [http://localhost:5601](http://localhost:5601)

<img width="1436" alt="Screenshot 2022-07-12 at 23 38 04" src="https://user-images.githubusercontent.com/95288275/178600805-40526503-bd8b-40c9-a1b8-cc20b9b9a1aa.png">


#### Troubleshooting
Se o container principal da aplicação está retornando erros de timeout, pois a instância Elasticsearch está demorando mais do que o tempo que o container espera, recomenda-se executar os containers separadamente, como no exemplo abaixo:
```bash
$ docker-compose up elasticsearch kibana
```
Após a conclusão da inicialização do Elasticsearch e do Kibana, execute o script abaixo em outra sessão do terminal:
```bash
$ docker-compose run app
```

## Implantação

Neste momento, este projeto não contempla a implementação de um processo automatizado de implantação. No entanto, a arquitetura e os procedimentos necessários para implantação do projeto na plataforma GCP estão descritos em um [documento markdown em separado.](./docs/deployment.md)
<br/>

