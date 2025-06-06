from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Usuario
from app.forms import formUsuario, formLogin
from .models import Produto, Venda
from .forms import ProdutoForm
import requests
import matplotlib.pyplot as plt
import io, urllib, base64
from django.utils import timezone
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

# ================== SESSÃO & CONTEXTO ===================

def verificar_sessao(request):
    if not request.session.get('email'):
        return redirect('index')
    return None

def get_contexto_logado(request, extras=None):
    contexto = extras or {}
    if request.session.get('email'):
        contexto['logado'] = True
    return contexto


# ================== PÁGINAS PRINCIPAIS ===================

def index(request):
    context = get_contexto_logado(request)
    return render(request, "index.html", context)

def dashboard(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    context = get_contexto_logado(request, {"email": request.session.get("email")})
    return render(request, "dashboard.html", context)

from django.contrib.auth.hashers import check_password

def login(request):
    frmLogin = formLogin(request.POST or None)
    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email')
            _senha = frmLogin.cleaned_data.get('senha')
            try:
                userLogin = Usuario.objects.get(email=_email)
                if check_password(_senha, userLogin.senha):
                    request.session.set_expiry(timedelta(seconds=300))
                    request.session['email'] = _email
                    request.session['logado'] = True   # <<< ESSA LINHA AQUI
                    request.session['is_admin'] = (_email == 'laura.campos3@gmail.com')
                    return redirect("dashboard")
                else:
                    frmLogin.add_error('senha', 'Senha incorreta.')
            except Usuario.DoesNotExist:
                frmLogin.add_error('email', 'Usuário não encontrado.')
    return render(request, "login.html", {'form': frmLogin})


def logout_view(request):
    request.session.flush()
    return redirect('index')


def quem_somos(request):
    logado = request.session.get('logado', False)
    return render(request, "quem_somos.html", {'logado': logado})




# ================== USUÁRIOS ===================

from django.contrib import messages  # já deve estar importado

def exibirUsuarios(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    # Verifica se o usuário logado é o admin
    email_logado = request.session.get('email')
    if email_logado != 'laura.campos3@gmail.com':
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')  # Redireciona para o dashboard ou outra página segura

    # Se for admin, mostra a lista
    usuarios = Usuario.objects.all()
    context = get_contexto_logado(request, {'ListUsuarios': usuarios})
    return render(request, 'usuarios.html', context)



from django.contrib.auth.hashers import make_password  # Importa função de hash

def addUsuario(request):
    formUser = formUsuario(request.POST or None)
    
    if request.POST and formUser.is_valid():
        usuario = formUser.save(commit=False)  # Cria o objeto sem salvar ainda
        usuario.senha = make_password(usuario.senha)  # Criptografa a senha
        usuario.save()  # Salva com a senha já criptografada

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect("login")

    context = get_contexto_logado(request, {'form': formUser})
    return render(request, "add-usuario.html", context)



def editarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    formUser = formUsuario(request.POST or None, instance=usuario)
    if request.POST and formUser.is_valid():
        formUser.save()
        return redirect("exibirUsuarios")
    context = get_contexto_logado(request, {'form': formUser})
    return render(request, "editar-usuario.html", context)

def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")


# ================== PRODUTOS ===================

def listar_produtos(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    produtos_db = Produto.objects.all()
    try:
        produtos_api = requests.get("https://fakestoreapi.com/products").json()
    except:
        produtos_api = []
    context = get_contexto_logado(request, {
        'produtos_db': produtos_db,
        'produtos_api': produtos_api,
    })
    return render(request, 'produtos/listar.html', context)

def cadastrar_produto(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    form = ProdutoForm(request.POST or None, request.FILES or None)
    if request.POST and form.is_valid():
        form.save()
        return redirect('listar_produtos')
    context = get_contexto_logado(request, {'form': form, 'titulo': 'Cadastrar Produto'})
    return render(request, 'produtos/form.html', context)

def editar_produto(request, pk):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)
    if request.POST and form.is_valid():
        form.save()
        return redirect('listar_produtos')
    context = get_contexto_logado(request, {'form': form, 'titulo': 'Editar Produto'})
    return render(request, 'produtos/form.html', context)

def excluir_produto(request, pk):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    context = get_contexto_logado(request, {'produto': produto})
    return render(request, 'produtos/confirmar_exclusao.html', context)


# ================== CHECKOUT / VENDA ===================

def checkout(request, produto_id):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    produto = get_object_or_404(Produto, pk=produto_id)
    email = request.session.get('email')
    usuario = get_object_or_404(Usuario, email=email)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))

        if produto.estoque >= quantidade:
            Venda.objects.create(
                produto=produto,
                usuario=usuario,
                quantidade=quantidade,
                confirmado=True
            )
            produto.estoque -= quantidade
            produto.save()
            return render(request, 'produtos/checkout_sucesso.html', {'produto': produto})
        else:
            return render(request, 'produtos/checkout.html', {
                'produto': produto,
                'usuario': usuario,
                'erro': 'Estoque insuficiente'
            })

    context = {
        'usuario': usuario,
        'produto': produto
    }
    return render(request, 'produtos/checkout.html', context)


# ================== GRÁFICOS ===================

def grafico(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    produtos = Produto.objects.all()
    nome = [produto.nome for produto in produtos]
    estoque = [produto.estoque for produto in produtos]

    fig, ax = plt.subplots()
    ax.bar(nome, estoque)
    ax.set_xlabel("Produto")
    ax.set_ylabel("Estoque")
    ax.set_title("Produtos")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    context = get_contexto_logado(request, {'dados': uri})
    return render(request, 'grafico.html', context)

def grafico_vendas(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    vendas_por_data = (
        Venda.objects.filter(confirmado=True)
        .annotate(data_trunc=TruncDate('data'))
        .annotate(valor=F('quantidade') * F('produto__preco'))
        .values('data_trunc')
        .annotate(total=Sum('valor'))
        .order_by('data_trunc')
    )

    datas = [v['data_trunc'].strftime('%d/%m') for v in vendas_por_data]
    totais = [v['total'] for v in vendas_por_data]

    plt.figure(figsize=(8, 5))
    plt.plot(datas, totais, marker='o', color='blue')
    plt.title('Vendas por Data')
    plt.xlabel('Data')
    plt.ylabel('Total de Vendas (R$)')
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imagem = base64.b64encode(buf.read()).decode('utf-8')
    uri = f'data:image/png;base64,{imagem}'

    context = get_contexto_logado(request, {'grafico_vendas': uri})
    return render(request, 'grafico_vendas.html', context)

from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import CadastroForm  # Exemplo
from .models import Usuario

