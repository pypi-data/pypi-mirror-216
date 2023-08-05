import json
import re
from os import environ

import requests
from pathlib3x import Path

# def qualquer(valor: str) -> str:
#     if valor == 'a':
#         dado = 'VOCE PASSOU A'
#     else:
#         dado = 'VOCE PASSOU OUTRA COISA'
#     return dado


def get_secret(
    app: str,
    env: str,
    proj: str,
    conf: str,
    token: str,
    vault_url: str
) -> dict:
    headers = {'X-Vault-Token': token}
    try:
        response = requests.request(
            'GET', url=vault_url + f'/v1/{env}-{proj}/data/{app}/{conf}', headers=headers
        )
    except Exception as e:
        return {'Status': e}
    
    if response.status_code == 200:
        if conf == 'env':
            ret = response.json()['data']['data']
        else:
            ret = response.json()['data']['data']['content']
    else:
        ret = {'Status': 'Erro'}
    return ret

def get_metadata(
    app: str,
    env: str,
    proj: str,
    token: str,
    vault_url: str,
) -> list:
    headers = {'X-Vault-Token': token}
    try:
        response = requests.request(
            'LIST', url=vault_url + f'/v1/{env}-{proj}/metadata/{app}', headers=headers
        )
    except Exception as e:
        return [f'Erro {e}']

    if response.status_code == 200:
        ret = response.json()['data']['keys']
    else:
        ret = [f'Erro', response.text]
    return ret

def convert_to_json(
    file: str,
) -> dict:
    with open(file, 'r') as f:
        content = f.readlines()

    contentList = [x.strip().split('#')[0].split('=', 1) for x in content if '=' in x.split('#')[0]]
    contentDict = dict(contentList)
    for k, v in contentList:
        for i, x in enumerate(v.split('$')[1:]):
            key = re.findall(r'\w+', x)[0]
            v = v.replace('$' + key, contentDict[key])
        contentDict[k] = v.strip()

    return json.dumps(contentDict)

def update_secret(
    app: str,
    env: str,
    proj: str,
    secret: str,
    token: str,
    vault_url: str,
    file: dict,
) -> dict:
    headers = {'X-Vault-Token': token}
    match secret:
        case 'env':
            json_file = Path('json_file.json')
            json_file.touch()
            json_file.write_text('{"data":'+file+'}')
            payload = open('json_file.json', 'rb').read()
            try:
                ret = requests.request(
                    'POST', url=vault_url + f'/v1/{env}-{proj}/data/{app}/{secret}', headers=headers, data=payload
                )
            except Exception as e:
                return {'Status': e}
            json_file.unlink()
        case _:            
            with open(file, 'r') as f:
                content = f.readlines()
            converted = ''
            # contentList = [x.strip().split('#')[0].split('=', 1) for x in content if '=' in x.split('#')[0]]
            for line in content:
                if converted == '':
                    converted = f'{line}'.strip()+'\\n'
                else:
                    converted = f'{converted}{line}'.strip()+'\\n'

            json_file = Path('json_file.json')
            json_file.touch()
            json_file.write_text('{"data": {"content": "'+converted+'"} }')

            payload = open('json_file.json', 'rb').read()
            try:
                ret = requests.request(
                    'POST', url=vault_url + f'/v1/{env}-{proj}/data/{app}/{secret}', headers=headers, data=payload
                )
            except Exception as e:
                return {'Status': e}
            json_file.unlink()

    if ret.status_code == 200:
        return {'Status': 'Success'}
    else:
        return {'Status': (ret.text)}

def make_conf() -> dict:
    home_dir = environ['HOME']
    try:
        path = Path(home_dir) / 'abin'
        path.mkdir()
        arq_conf = open(f'{path}/settings.toml', 'w')
    except Exception as e:
        erro = f'Arquivo de configuração já criado ou pasta já existe em {home_dir}.\n Comando retornorou {e}'
        retorno = {'Message': erro, 'Status': False}
    else:
        arq_conf.write('name = "ABIN"\n\n[params]\nvault_token = "ALTERAR"\nvault_url = "https://aspirina.simtech.solutions"\npath = "./"\n\n[console]\ntable_width = 40')
        arq_conf.close()
        retorno = {'Message': f'Arquivo de configuração criado em {path}', 'Status': False}
    return retorno

