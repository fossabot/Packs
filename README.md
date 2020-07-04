<p align="center">
    <img src="https://github.com/Vupy/Packs/blob/master/Packs/logo/logo.png" width="256" height="256"/>
</p>

# Packs

Packs é um pacote que auxilia o Pip na instalação e gerenciamento de pacotes. Com o Pip é possível instalar varios pacotes para o Python, todavia no momento de gerar o arquivo requirements.txt sempre haverá alguns pacotes que não são necessários para o ambiente de produção. E nesse contexto o Packs pode lhe auxiliar com os pacotes de desenvolvimento e os de produção.

No momento de instalação de qualquer pacote é possível adicionar a flag --dev ou apenas -d desse modo é definido que este pacote será apenas para o ambiente de desenvolvimento e não de produção. Ao final de qualquer instalação ou remoção de pacotes o Packs automaticamente irá gerar dois arquivos: requirements.txt e requirements-dev.txt, a qual representam a lista de dependência de produção e desenvolvimento respectivamente.

## Instalação

pip install packs

## Uso 

Para instalar qualquer pacote você pode usar os seguintes comandos e flags:

```
packs install <Nome do pacote>
packs i <Nome do pacote>

-u para atualizar
--dev ou -d para pacotes de produção
-r <Arquivo> para instalar os pacotes atráves de uma arquivo
```

Para remover qualquer pacote use os comando a seguir e as flags:

```
packs remove <Nome do pacote>
packs uninstall <Nome do pacote>
packs rm <Nome do pacote>

--yes ou -y para aceitar tudo
-r <Arquivo> para remover os pacotes atráves de uma arquivo
```

Para listar os pacotes instalados use estes comandos e as flags:

```
packs ls
packs list

--freeze ou -f para listar no formato freeze
--color ou -c para remover as cores
```

<strong>
    <p align="center" style="text-align: center;">Vupy social networking© 2020</p>
</strong>