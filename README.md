# Gerenciador de Tarefas em Python (Tkinter)

Este é um aplicativo simples para **gerenciar suas tarefas diárias** feito com Python e a biblioteca Tkinter para interfaces gráficas. Ele ajuda você a organizar suas tarefas, definindo título, descrição, data de conclusão e prioridade.

---

## Funcionalidades do aplicativo

- **Adicionar tarefas** com:
  - Título (nome da tarefa)
  - Descrição detalhada
  - Data para conclusão (prazo)
  - Prioridade (Alta, Média ou Baixa)
- **Visualizar lista de tarefas** mostrando o status (concluído ou pendente)
- **Marcar tarefas como concluídas** com um clique
- **Excluir tarefas** que não são mais necessárias
- **Ver detalhes** completos de cada tarefa
- Campos com **placeholders inteligentes** que somem quando você começa a digitar

---

## Interface amigável

- Layout moderno, com campos organizados lado a lado para facilitar o uso
- Botões com cantos arredondados e cores suaves para melhor experiência
- Fonte padrão **Segoe UI** que deixa o texto claro e legível
- Design clean e intuitivo para facilitar seu aprendizado e uso

---

## Requisitos para executar o programa

- Você precisa ter o **Python 3.7 ou superior** instalado no seu computador.  
  [Baixe o Python aqui](https://www.python.org/downloads/)

---

## Passo a passo para rodar o programa

### 1. Baixar os arquivos

Você pode clonar este repositório usando o Git, ou baixar o código diretamente: 

- Para clonar com Git (se você já tem o Git instalado):

```bash
git clone https://github.com/zamyro/gerenciador-de-tarefas.git
cd gerenciador-de-tarefas
```

- Ou baixe o ZIP clicando em **Code > Download ZIP** no GitHub e extraia em uma pasta

### 2. Instalar o PyIntaller (opcional)

Se quiser transformar o programa em um arquivo executável (.exe) para rodar sem abir o terminal, instale o PyInstaller:

``` bash
pip install pyinstaller
```

### 3. Executar o programa

Para rodar o programa direto pelo Pyhon, abra o terminal ou prompt de comando na pasta onde está o arquivo **gerenciador-de-tarefas-py** e execute:

``` bash
python gerenciador-de-tarefas.py
```

O aplicativo abrirá uma janela para você começar a adicionar e gerenciar suas tarefas.

---

## Dicas para quem está aprendendo

- O código usa a biblioteca Tkinter, que é a forma mais simples de criar interfaces gráficas em Python.
- As tarefas são salvas localmente em um banco de dados SQLite, que é um arquivo simples no seu computador, sem precisar de conexão com internet.
- Você pode estudar o código para aprender como:
  - Criar e organizar janelas e botões
  - Trabalhar com eventos e interações do usuário
  - Conectar e manipular um banco de dados simples
- Se quiser personalizar, experimente mudar cores, fontes e layouts para praticar, mas tenha uma cópia do arquivo para caso houver algum erro tenha como retornar

---

## Suporte e contribuições

Se encontrar problemas ou quiser melhorias, sinta-se à vontade para abrir uma issue, enviar um pull request no GitHub, ou simplesmente entrar em contato através de uma das minhas redes sociais disponíveis aqui no GitHub!
