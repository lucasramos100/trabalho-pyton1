# app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from ..models import UsuarioLogin, UsuarioCadastro
from ..auth import get_usuario, gerar_hash, autenticar_usuario, criar_token, get_usuario_atual
from ..database import usuarios
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from ..viacep import buscar_cep


router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/test")
def test():
    return {"mensagem": "OK, tudo certo!"}

@router.post("/registro")
def registrar(usuariox: UsuarioCadastro):
#def registrar(usuariox: UsuarioCadastro, usuario=Depends(get_usuario_atual)):
    userData = get_usuario(usuariox.username)
    if userData:
        raise HTTPException(status_code=400, detail='Usuário já existe')
    hash_senha = gerar_hash(usuariox.password)

    dadosCep = buscar_cep(usuariox.cep)
    # chamar o viacep
    # adicionar no insert_one os demais dados
    usuarios.insert_one({
        "username":usuariox.username, 
        "password": hash_senha,
        "cep": usuariox.cep,
        "numero": usuariox.numero,
        "complemento": usuariox.complemento,
        "logradouro": dadosCep["logradouro"],
        "bairro": dadosCep["bairro"],
        "localidade": dadosCep["localidade"],
        "uf": dadosCep["uf"],
        })

    return {"mensagem": "Usuário registrado com sucesso!"} 

@router.post("/login")
def logar(usuario: UsuarioLogin):
    autenticado = autenticar_usuario(usuario.username, usuario.password)

    if not autenticado:
        raise HTTPException(status_code=400, detail='Usuário ou Senha Inválidos')

    access_token = criar_token(
        data={"sub":autenticado["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"token": access_token, "expires": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}

@router.get("/listar_usuarios")
def listar_usuarios(usuario_atual=Depends(get_usuario_atual)):
    usuarios_lista = list(usuarios.find({}, {"password":0}))
    for usuario in usuarios_lista:
        usuario["_id"] = str(usuario["_id"])
    return usuarios_lista

@router.put("/alterar_usuario")
def atualizar_usuario(user_id: str, usuario_dados: UsuarioCadastro, usuario_atual=Depends(get_usuario_atual)):
    if usuario_dados.username != usuario_existente["username"]:
        raise HTTPException(status_code=400, detail="Não é permitido alterar o username")

    dadosCep = buscar_cep(usuario_dados.cep)
    dados_atualizacao = {
        "cep": usuario_dados.cep,
        "numero": usuario_dados.numero,
        "complemento": usuario_dados.complemento,
        "logradouro": dadosCep["logradouro"],
        "bairro": dadosCep["bairro"],
        "localidade": dadosCep["localidade"],
        "uf": dadosCep["uf"]
    }
    
    if usuario_dados.password:
        dados_atualizacao["password"] = gerar_hash(usuario_dados.password)
    usuarios.update_one(
        {"_id": user_obj_id},
        {"$set": dados_atualizacao}
    )
    return {"mensagem": "Usuário atualizado!"}

@router.delete("/deletar_usuario")
def deletar_usuario(user_id: str, usuario_atual=Depends(get_usuario_atual)):
    if not usuario_alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if usuario_alvo["username"] == usuario_atual["username"]:
        raise HTTPException(status_code=403, detail="Essa ação não é permitida")  
    usuarios.delete_one(
        {"_id": user_obj_id}
    )
    return {"mensagem": "Usuário deletado com sucesso"}


