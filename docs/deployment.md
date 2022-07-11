## Cloud Deployment através do GCP

### Arquitetura

O script python irá ser executado usando um container docker pelo serviço Cloud Run do GCP.
O script é responsável pela coleta dos dados e pela sua inserção na base Elasticsearch.

A base Elasticsearch, assim como a UI Kibana, são disponibilizadas pelo serviço Elastic Cloud, do GCP.

### Implantação

O primeiro passo é criar um novo projeto dentro da plataforma do Google Cloud, de modo a isolar os serviços utilizados por esta solução.
Para criar é necessário definir um nome, qual conta de cobrança e a organização, quando aplicável.
Dentro do projeto, os serviços Elastic Cloud e Cloud Run devem ser habilitados.

#### Elastic Cloud
O Elastic Cloud pode ser encontrado dentro do Marketplace do GCP. Para utilizá-lo, primeiramente, deve ser assinado, onde é necessário definir o período de assinatura e a taxa de uso.

Ao ser habilitado, o serviço deve ser gerenciado através da plataforma da Elastic Cloud que pode ser acessada pela área API & Services no GCP.
Para acessar a plataforma da Elastic Cloud é necessário criar uma conta e realizar login.

Na plataforma, é possível visualizar a conexão com a assinatura realizada no GCP na área de Account.
Na área de Deployment, crie um novo deployment do tipo Elastic Stack (este tipo de deployment irá criar uma instância da base Elasticsearch e da UI Kibana). Durante a criação, deverá ser definida a região, a versão do Elasticsearch, o provedor Cloud, e definir configurações de infraestrutura para cada serviço que será criado.

Após a criação, a plataforma irá disponibilizar apenas uma vez as credenciais de acesso aos serviços criados.
Em alguns minutos, os serviços estarão disponíveis para acesso.

A Cloud ID pode ser acessada logo na página principal do deployment. As credenciais e a Cloud ID deverão ser utilizadas pelo script python para se conectar a instância Elasticsearch criada neste deployment.

O script python atual será atualizado para se conectar a instância Elasticsearch de produção conforme o exemplo abaixo:

```python
from elasticsearch import Elasticsearch

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = "<password>"

# Found in the 'Manage Deployment' page
CLOUD_ID = "deployment-name:dXMtZWFzdDQuZ2Nw..."

# Create the client instance
client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

```

#### Google Cloud Build



#### Google Cloud Run



O Dockerfile será atualizado, como mostrado abaixo, para ser executável no ambiente Cloud Run.

```docker
FROM python:3.10-bullseye

WORKDIR /app

#install the requirements
COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
RUN rm -f /temp/requirements.txt

COPY . .
CMD ["python3", "code/news_collector.py"]
```