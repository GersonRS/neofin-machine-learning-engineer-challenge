# Card ML Deployment

## **Overview**

Este projeto demonstra o desenvolvimento completo de um modelo de **Machine Learning** para a classificação de **customers** (clientes dos nossos clientes) com base em seus padrões de pagamento. O objetivo é identificar categorias como **Bons Pagadores, Maus Pagadores, Pagadores Esquecidos, Pagadores Duvidosos e Novos Pagadores**, permitindo uma abordagem personalizada na cobrança e auxiliando na redução da inadimplência.

O modelo foi treinado utilizando o **Scikit-learn** e implementado dentro de um **pipeline de Machine Learning** que inclui pré-processamento, normalização e inferência. Para disponibilizar a classificação em produção, desenvolvemos uma **API robusta com FastAPI**, que recebe os dados brutos de um pagamento, processa-os dinamicamente e retorna a categoria prevista do customer.

Além disso, o projeto foi estruturado para facilitar a **implantação e escalabilidade**, permitindo sua execução em **contêineres Docker** e suportando testes de desempenho via ferramentas como **Locust**. Dessa forma, garantimos que a solução possa ser utilizada de forma eficiente e confiável no ambiente de produção da Neofin.

## Tabela de Conteúdo

- [Objetivo](#objetivo)
- [Fluxo de Versionamento](#fluxo-de-versionamento)
- [Ferramentas](#ferramentas)
- [Getting Started](#getting-started)
- [Requisitos](#requisitos)
- [Usage](#usage)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Troubleshooting](#troubleshooting)
- [Contributions](#contribuições)
- [License](#license)
- [Contato](#contato)
- [Acknowledgments](#acknowledgments)

## Objetivo

O objetivo deste projeto é criar uma pipeline de treinamento e implantação de um modelo de machine learning usando Scikit-learn, FastAPI e Docker. O modelo é treinado com base no conjunto de dados de Cards do Gods Unchained e é capaz de fazer classificação de cards `early` e `late` game com base nas características fornecidas e é implantado em um cluster kubernetes servindo uma api http que recebe o `id` de um card e retorna a classificação deste card.

## Fluxo de Versionamento

Este projeto segue um fluxo de versionamento baseado no Git. Cada grande alteração no projeto deve ser acompanhada por um novo commit com uma mensagem descritiva. Versões do modelo treinado e da API devem ser controladas com base em tags no Git.

## Ferramentas

- Scikit-learn: Biblioteca para machine learning em Python.
- FastAPI: Framework para criar APIs web rápidas com Python.
- Docker: Plataforma para criar, implantar e executar aplicativos em contêineres.
- Locust: Ferramenta para teste de carga.

## Getting Started

Siga estas instruções para configurar o ambiente de desenvolvimento e executar o projeto:

1. Clone o repositório:
```
git clone https://github.com/GersonRS/neofin-machine-learning-engineer-challenge.git
cd neofin-machine-learning-engineer-challenge
```


2. Instale as dependências:
```
poetry install
```


3. Treine o modelo:

Execute o pipeline no [notebook](notebooks/Test Case - ML Engineer.ipynb) de treinamento do modelo.


4. Inicie a API:
```
fastapi run
```

5. Acesse a documentação da API em seu navegador em http://localhost:8000/docs para fazer previsões.

## Requisitos

- Python 3.8+
- Scikit-learn
- FastAPI
- Docker (para implantação)
- Locust (opcional, para teste de carga)

## Usage

Após seguir as instruções em **[Getting Started](#getting-started)**, você pode acessar a documentação da API em http://localhost:8000/docs para fazer previsões sobre a espécie das flores de íris com base nas características fornecidas.

## Dockernization

Este projeto pode ser facilmente "dockernizado" para facilitar a implantação em contêineres Docker. A utilização de contêineres Docker ajuda a garantir a portabilidade e a independência das dependências do sistema, tornando a implantação mais fácil e consistente em diferentes ambientes.

Siga estas etapas para criar uma imagem Docker e executar a aplicação em um contêiner:

### 1. Construir uma imagem docker da aplicação

```
docker build -t customer-ml:latest .
```

### 2. Executar o container

```
docker run -d -p 8000:8000 --name customer-api customer-ml:latest
```
O comando acima executa um contêiner Docker a partir da imagem que você construiu. Ele mapeia a porta 8000 do contêiner para a porta 8000 do host local.

### 3. Va para o localhost
```
http://localhost:8000/docs
```
Agora, a aplicação estará em execução dentro do contêiner Docker. Você pode acessá-la em [http://localhost:8000/docs](http://localhost:8000/docs) para fazer previsões por meio da API.


### 4. Experimente o método post/predict
```
curl -X 'POST' \
  'http://localhost:8000/v1/customer/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_id": "83 0b f4 f3 45 67 54 39 74 c5 43 31 ae 73 a3 09 23 3e b4 47 5b 47 9d 11 e5 1d e8 c7 90 cb 92 fd",
  "company_name": "40 f9 0d a5 a9 d9 29 33 ac 84 f2 9b 3f 86 b0 05 69 48 dd 6d 83 52 0e d2 8a 80 de 20 8c 49 71 da",
  "company_document": "37 2a 52 fa 18 60 9c 5c 72 47 98 27 bd 58 45 83 11 25 69 3b a0 3f 45 3c d9 9a 60 67 49 bb c1 2e",
  "company_trade_name": "40 f9 0d a5 a9 d9 29 33 ac 84 f2 9b 3f 86 b0 05 69 48 dd 6d 83 52 0e d2 8a 80 de 20 8c 49 71 da",
  "customer_id": "02 60 80 35 3c d3 09 5f be 20 e5 8d ed 3d 2e fe bd f6 ce 88 18 80 6e 71 ef 32 6a 63 f0 22 18 bf",
  "customer_name": "c4 52 91 30 34 b0 96 83 05 98 61 da 5c 3b a1 12 6f 34 07 c0 50 af 1f 29 c0 17 bb 62 e3 bf 9b da",
  "customer_trade_name": "c4 52 91 30 34 b0 96 83 05 98 61 da 5c 3b a1 12 6f 34 07 c0 50 af 1f 29 c0 17 bb 62 e3 bf 9b da",
  "parent_type": "billing",
  "parent_id": "f02f0294-ce57-431c-b008-483d92dce72a",
  "payment_number": "e5 fa 90 b0 7e 55 6e 80 20 06 2b f0 f8 30 cc 55 84 fa eb e1 eb 48 20 76 4b 1a d6 bf ae ae 59 74",
  "issue_date_dte": "2024-12-30",
  "original_due_date_dte": "2025-01-10",
  "due_date_dte": "2025-01-10",
  "paid_at_dte": "2025-01-05",
  "issue_at_tsmp": "2024-12-30 03:04:27.000",
  "original_due_date_tsmp": "2025-01-10 23:59:59.000",
  "due_date_tsmp": "2025-01-10 23:59:59.000",
  "paid_at_tsmp": "2025-01-05 15:04:28.000",
  "payment_method": "generic",
  "payment_status": "paid",
  "paid_amount": 99.5,
  "billing_amount": 99.5,
  "payment_amount": 99.5,
  "installment": "1/1",
  "payment_provider": "",
  "discount_before_payment": 0.0,
  "discount_before_payment_due_date": 0,
  "description": "22 d0 50 cc 66 fb 05 10 a3 12 0e b8 9b a3 8c d2 9c 0b 29 cd 65 77 f0 74 f4 ea cd bb 35 73 12 74",
  "qrcode_number": "",
  "os_code": "e3 b0 c4 42 98 fc 1c 14 9a fb f4 c8 99 6f b9 24 27 ae 41 e4 64 9b 93 4c a4 95 99 1b 78 52 b8 55",
  "os_identifier": "e3 b0 c4 42 98 fc 1c 14 9a fb f4 c8 99 6f b9 24 27 ae 41 e4 64 9b 93 4c a4 95 99 1b 78 52 b8 55",
  "by_mail": true,
  "by_whatsapp": true,
  "fees": 0,
  "fine": 0,
  "paid_at": "2025-01-05 15:04:28.000",
  "paid_method": "generic",
  "manual": "",
  "billing_number": "44 b5 2b 63 14 51 4a 9e be e1 19 c0 39 ad af 26 6e a5 d2 c8 be 1e 70 1d 6f d9 37 9b a6 62 4a 13"
}'
```

> Lembre-se de que você pode personalizar as portas e os nomes dos contêineres conforme necessário. Certifique-se de ter o Docker instalado e em execução em seu sistema antes de prosseguir.

Ao implantar em um ambiente de produção, você pode usar orquestradores de contêineres, como Kubernetes ou Docker Compose, para gerenciar a implantação e escalabilidade de contêineres. Certifique-se de configurar e ajustar seu ambiente de acordo com suas necessidades específicas.

## Testes

Este projeto inclui a capacidade de realizar testes automatizados usando a biblioteca Locust. Os testes de carga fornecidos podem ser usados para avaliar o desempenho da API e medir a capacidade de resposta em diferentes cenários de carga.

Siga estas etapas para executar os testes de carga:

1. Execute os Testes de Carga:

Navegue até o diretório de testes:


```
cd tests
```

2. Execute o Locust com o arquivo de teste específico:


```
locust -f load_test.py
```
Isso iniciará o servidor de teste do Locust em [http://localhost:8089/](http://localhost:8089/). Você pode acessar o painel de controle do Locust em seu navegador.

3. Configure os Parâmetros de Teste:

* Acesse o painel de controle do Locust em [http://localhost:8089/](http://localhost:8089/).
* Defina o número de usuários virtuais (virtual users) que você deseja simular e a taxa de spawn (quantos usuários por segundo serão iniciados).
* Clique no botão `Start` para iniciar os testes.

4. Execute os Testes de Carga:

Os usuários virtuais gerados pelo Locust irão acessar a API automaticamente de acordo com a configuração que você definiu. Eles enviarão solicitações de previsão à API e coletarão métricas de desempenho.

5. Analise os Resultados:

* Você pode monitorar o progresso dos testes e visualizar métricas de desempenho em tempo real no painel de controle do Locust.
* Ao encerrar os testes, você poderá acessar relatórios detalhados e gráficos para avaliar o desempenho da API.

Lembre-se de que os testes de carga com o Locust são uma maneira eficaz de avaliar o desempenho da sua aplicação e identificar possíveis gargalos. Certifique-se de ajustar os parâmetros dos testes de acordo com as necessidades e requisitos da sua aplicação.

## Estrutura do Projeto

O projeto tem a seguinte estrutura de diretórios:

```
.
├── CHANGELOG.md
├── charts
│   └── customer-ml
│       ├── Chart.yaml
│       ├── templates
│       │   ├── card_clusterip.yaml
│       │   ├── card_deployment.yaml
│       │   ├── card_ingress.yaml
│       │   ├── _helpers.tpl
│       │   ├── hpa.yaml
│       │   └── service-accounts.yaml
│       └── values.yaml
├── CODEOWNERS
├── commitlint.config.js
├── csvjson.json
├── data
│   ├── company_profiling_mle.csv
│   └── payments_mle.csv
├── docker-compose.yml
├── Dockerfile
├── example.json
├── folders.txt
├── LICENSE
├── main.py
├── models
│   ├── customer_classification_pipeline.pkl
│   ├── ml
│   │   ├── classifier.py
│   │   └── __pycache__
│   │       └── classifier.cpython-310.pyc
│   ├── modelo_onehotenc.pkl
│   ├── schemas
│   │   ├── customer.py
│   │   └── __pycache__
│   │       ├── card.cpython-310.pyc
│   │       └── customer.cpython-310.pyc
│   └── target_encoder.pkl
├── mypy.ini
├── notebooks
│   └── Test Case - ML Engineer.ipynb
├── package.json
├── package-lock.json
├── poetry.lock
├── __pycache__
│   └── main.cpython-310.pyc
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── routes
│   ├── home.py
│   ├── __pycache__
│   │   └── home.cpython-310.pyc
│   └── v1
│       ├── customer_predict.py
│       └── __pycache__
│           ├── card_predict.cpython-310.pyc
│           └── customer_predict.cpython-310.pyc
├── tests
│   ├── __init__.py
│   ├── load_test_new.py
│   ├── load_test.py
│   ├── __pycache__
│   │   └── load_test.cpython-310.pyc
│   └── test_response.py
└── version.txt

17 directories, 49 files

```


## Troubleshooting

Se você encontrar problemas ou tiver dúvidas sobre o projeto, consulte a seção **[Contribuições](#contribuições)** para obter informações sobre como relatar problemas ou fazer perguntas.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para criar uma solicitação pull com melhorias, correções de bugs ou novos recursos. As contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será muito apreciada.

Para contribuir com o projeto, siga os passos abaixo:

1. Bifurque o projeto.
2. Crie um branch para sua contribuição (git checkout -b feature-mycontribution).
3. Faça as alterações desejadas no código.
4. Confirme suas alterações (git commit -m 'MyContribution: Adicionando novo recurso').
5. Envie o branch para seu repositório Fork (git push origin feature-mycontribution).
6. Abra uma solicitação pull no branch principal do projeto original. Descreva as alterações e aguarde a revisão e discussão da comunidade.

Valorizamos verdadeiramente o seu interesse em contribuir para o projeto. Juntos, podemos torná-lo ainda melhor!

## License

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para entrar em contato, envie um e-mail para [gersonrodriguessantos8@gmail.com](mailto:gersonrodriguessantos8@gmail.com).

<p align="center">

 <a href="https://twitter.com/gersonrs3" target="_blank" >
     <img alt="Twitter" src="https://img.shields.io/badge/-Twitter-9cf?logo=Twitter&logoColor=white"></a>

  <a href="https://instagram.com/gersonrsantos" target="_blank" >
    <img alt="Instagram" src="https://img.shields.io/badge/-Instagram-ff2b8e?logo=Instagram&logoColor=white"></a>

  <a href="https://www.linkedin.com/in/gersonrsantos/" target="_blank" >
    <img alt="Linkedin" src="https://img.shields.io/badge/-Linkedin-blue?logo=Linkedin&logoColor=white"></a>

  <a href="https://t.me/gersonrsantos" target="_blank" >
    <img alt="Telegram" src="https://img.shields.io/badge/-Telegram-blue?logo=Telegram&logoColor=white"></a>

  <a href="mailto:gersonrodriguessantos8@gmail.com" target="_blank" >
    <img alt="Email" src="https://img.shields.io/badge/-Email-c14438?logo=Gmail&logoColor=white"></a>

</p>

## Acknowledgments

Agradecimentos a todos os desenvolvedores e mantenedores das bibliotecas e ferramentas utilizadas neste projeto, bem como a toda a comunidade de código aberto que torna projetos como este possíveis.
