
# Configuração do Projeto

## Pré-requisitos

Para executar o projeto você precisará de:

- Conta AWS
- AWS Lambda
- AWS Step Functions
- Amazon Bedrock
- Python 3.x
- AWS CLI

## 1. Criar a função Lambda

Crie uma função Lambda chamada:

`buscar-restaurantes`

Utilize Python 3.x como runtime.

Copie o conteúdo de:

`funcoes-lambda/buscar-restaurantes/lambda_function.py`

A função não utiliza dependências externas.

## 2. Permissões IAM

A função utilizada pelo Step Functions precisa ter permissão para executar a Lambda.

O Step Functions também precisa possuir permissão para invocar o modelo
selecionado no Amazon Bedrock.

Utilize o princípio do menor privilégio.

## 3. Amazon Bedrock

Habilite acesso ao modelo escolhido no Amazon Bedrock.

O projeto utiliza como exemplo:

`nvidia.nemotron-nano-12b-v2`

O formato exato da requisição pode variar de acordo com o modelo.

## 4. Criar o State Machine

Crie uma nova State Machine no AWS Step Functions.

Utilize:

`step-functions/assistente-delivery.asl.json`

como definição.

Atualize o ARN da Lambda conforme sua conta AWS.

## 5. Testar

Utilize:

`exemplos/entrada.json`

como entrada de teste.

Exemplo:

"Acabei de chegar na cidade e quero sugestões de restaurantes próximos."

## 6. Segurança

Nunca armazene credenciais AWS ou chaves de API no GitHub.

Utilize IAM Roles e variáveis de ambiente quando necessário.

Arquivos `.env` e credenciais estão incluídos no `.gitignore`.
