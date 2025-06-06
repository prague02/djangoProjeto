from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import logout_view, quem_somos
urlpatterns = [
    # Página inicial
    path('', views.index, name="index"),

    # Usuários
    path('usuarios/', views.exibirUsuarios, name="exibirUsuarios"),
    path('add-usuario/', views.addUsuario, name="addUsuario"),
    path('excluir-usuario/<int:id_usuario>/', views.excluirUsuario, name="excluirUsuario"),
    path('editar-usuario/<int:id_usuario>/', views.editarUsuario, name="editarUsuario"),

    # Produtos
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/novo/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),

    # Sessão (Login e Logout)
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name="dashboard"),

    # Outros
    path('grafico/', views.grafico, name="grafico"),

    path('checkout/<int:produto_id>/', views.checkout, name='checkout'),

    path('grafico-vendas/', views.grafico_vendas, name='grafico_vendas'),

    path("quem-somos/", quem_somos, name="quem_somos"),
]

# Configuração para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
