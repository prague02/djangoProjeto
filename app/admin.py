from django.contrib import admin
from .models import Produto, Usuario, Categoria

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome","email")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome","descricao", "preco","foto", "estoque","categoria")

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)  # <-- apenas 1 vez!
