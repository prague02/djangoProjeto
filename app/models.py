from django.utils import timezone

from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # <<< aqui, unicidade garantida no DB
    senha = models.CharField(max_length=16)

    cep = models.CharField(max_length=9, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    localidade = models.CharField(max_length=100, blank=True)  # cidade
    uf = models.CharField(max_length=2, blank=True)
    numero_residencia = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.email})"

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='imagens/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data = models.DateTimeField(default=timezone.now)
    confirmado = models.BooleanField(default=True)  # sempre true no seu caso

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} para {self.usuario.nome}"    