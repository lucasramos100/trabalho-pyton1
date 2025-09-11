
## Instruções para Rodar a API

1. Instale as dependências:
pip install -r requirements.txt

2. Execute a API:
uvicorn app.main:app --reload


# Endpoints Criados
# 1. Listar Usuários
- **GET** `/usuarios/listar_usuarios`

# 2. Atualizar Usuário
- **PUT** `/usuarios/alterar_usuario?user_id={id}`

# 3. Deletar Usuário
- **DELETE** `/usuarios/deletar_usuario?user_id={id}`

# Erro ao Tentar Deletar o Usuário Logado

1. Faça login com um usuário para obter o token
2. Tente deletar o mesmo usuário que está logado usando o endpoint DELETE
3. Você receberá um erro 403 com a mensagem "Essa ação não é permitida"

