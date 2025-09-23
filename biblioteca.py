import matplotlib.pyplot as plt #aqui importamos a biblioteca para mostrar os graficos

class Livro:  #fiz uma classe livro
  def __init__(self, titulo, autor, ano, quantidade, genero): #defini os atributos do livro
    self.titulo = titulo
    self.autor = autor
    self.ano = ano
    self.quantidade = quantidade
    self.genero = genero
  def __str__(self): #essa função retorna os atributos já formatados, em String
    return (
       f"Titulo: {self.titulo} == Autor: {self.autor} == Ano:{self.ano} =="
       f"Quantidade: {self.quantidade} == Genero: {self.genero}"
    )

lista_livros = [] #criei uma lista para armazenar os livros

def adicionar_livro(titulo,autor,ano,quantidade, genero): #defini uma funcao para adicionar os livros
  novo_livro = Livro(titulo,autor,ano,quantidade,genero) #aqui eu chamo os atributos da classe livro, e os guardo em "novo_livro"
  lista_livros.append(novo_livro) #adicionamos esse "novo_livro" na nossa lista
  print("Livro adiciondo com sucesso!")

def listar_livros():  #definimos a funcao para listar todos os livros
  print("Lista de livros: ")
  for livro in lista_livros:  #toda vez que o objeto livro passar na nossa lista
    print(livro)              #ele vai printar todos os objetos existentes na lista.

def buscar_livro(titulo): #colocamos um parametro titulo, para que possamos buscar 1 livro especifico
  for livro in lista_livros:                  #temos um laço que quando encontrar um livro
    if livro.titulo.lower() == titulo.lower():#com o parametro titulo, irá percorrer a nossa lista_livro
      return print(livro)                     #e se encontrar, vai retornar o objeto livro.
  print("Livro não encontrado")
  return None                           #caso não seja encontrado, vamos retornar nada,"livro nao encontrado"

adicionar_livro("Ecos do Amanha","Ana Luísa Fernandes", 1605,4,"Romance") #AQUI USAMOS ADICIONAMOS OS LIVROS COM NOSSA FUNÇÃO
adicionar_livro("O Silencio das Estrelas","Ricardo Monteiro", 1813,5,"Romance")
adicionar_livro("Fragmentos de Um Mundo Perdido","Camila Rocha", 1949,7,"Suspense")
adicionar_livro("Além do Horizonte de Vidro","Marcos Vinícius Duarte", 1967,2,"Suspense")
adicionar_livro("As Cores do Infinito","Helena Prado", 1951,3,"Romance")
print()
listar_livros()      #AQUI VERIFICAMOS A NOSSA LISTA DE LIVROS COM NOSSA FUNÇAO listar_livros
print()
buscar_livro("o silencio das estrelas") #BUSCAMOS UM LIVRO PELO TITULO.
print()

grafico_genero = [livro.genero for livro in lista_livros] #aqui percorremos nossa lista, pegando apenas o genero
grafico_quantidade = [livro.quantidade for livro in lista_livros] #aqui percorremos nossa lista, pegando apenas a quantidade
plt.bar(grafico_genero,grafico_quantidade) #construimos o grafico encima dos generos e quantidade(graficos de barra)
plt.xlabel("Gênero") #Nomeamos a linha x
plt.ylabel("Quantidade") #Nomeamos a linha y
plt.title("Quantidade de livros por gênero") #Demos titulo ao nosso grafico
plt.show() #exibimos nosso grafico