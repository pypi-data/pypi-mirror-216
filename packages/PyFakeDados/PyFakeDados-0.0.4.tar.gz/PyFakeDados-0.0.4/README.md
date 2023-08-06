# PyFakeDados

![PyFakeDados](https://github.com/juliansantosinfo/PyFakeDados/logo.png)

PyFakeDados é uma ferramenta em Python que auxilia desenvolvedores na geração de dados falsos (fake) aleatórios para bancos de dados de teste ou APIs. Com essa ferramenta, é possível gerar uma variedade de informações, como nomes, telefones, CPFs, e-mails, senhas e muito mais.

O PyFakeDados oferece uma ampla gama de recursos para gerar dados em diversos formatos, como nomes, endereços, números de telefone, documentos como CPFs e CNPJs, e-mails, senhas, entre outros. Além disso, a ferramenta permite criar identidades completas de pessoas e empresas, fornecendo informações consistentes e realistas.

A biblioteca é de fácil utilização e pode ser integrada facilmente a projetos em Python. Com uma simples chamada de função, você pode gerar quantidades massivas de dados falsos para preencher suas necessidades de teste. A diversidade dos dados gerados e a capacidade de personalização tornam o PyFakeDados uma ferramenta indispensável para qualquer desenvolvedor que precise de dados fictícios em seus projetos.

Este repositório também fornece documentação completa sobre como usar a biblioteca e exemplos práticos para ajudá-lo a aproveitar ao máximo todas as funcionalidades do PyFakeDados.

Experimente o PyFakeDados agora e torne o processo de geração de dados falsos mais eficiente e realista em seus projetos!

## Recursos

PyFakeDados é capaz de gerar os seguintes tipos de dados:

- Nome
- Sobrenome
- Nome completo
- Nome com filiação
- Telefone fixo
- Telefone celular
- CPF
- RG
- PIS
- CTPS
- CNPJ
- Inscrição estadual
- E-mail
- Site
- Senhas

Além disso, a ferramenta também é capaz de gerar agrupamentos de dados, formando identidades de pessoas e empresas.

## Instalação

Você pode instalar o PyFakeDados através do pip, executando o seguinte comando:

```shell
pip install PyFakeDados
```

## Uso

Para utilizar o PyFakeDados em seu projeto, importe o pacote e utilize as funções correspondentes aos tipos de dados que deseja gerar. Por exemplo, para gerar um nome completo, utilize a função `gerar_nome_completo()`.

```python
from pyfakedados import gerar_nome_completo

nome_completo = gerar_nome_completo()
print(nome_completo)
```

Para mais exemplos de uso, consulte a documentação disponível em [link_da_documentacao](https://github.com/seu-usuario/repositorio/documentacao.md).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request* com melhorias, correções de bugs ou novos recursos.

## Licença

Este projeto é licenciado sob a [GPL-3.0 License](https://raw.githubusercontent.com/juliansantosinfo/PyFakeDados/main/LICENSE.txt).
