from django import forms
from app.models import Usuario
from .models import Produto, Categoria
from django.contrib.auth.models import User


class formUsuario(forms.ModelForm):
    senha2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a senha'}),
        label="Confirme a senha"
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    class Meta:
        model = Usuario
        fields = (
            'nome', 'email', 'senha', 'senha2', 'cep', 'logradouro', 'bairro',
            'localidade', 'uf', 'numero_residencia'
        )
        widgets = {
            'nome': forms.TextInput(attrs={'type': 'text'}),
            'email': forms.TextInput(attrs={'type': 'email'}),
            'senha': forms.PasswordInput(),
            'cep': forms.TextInput(attrs={'onblur': 'buscarCEP(this.value)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha2 = cleaned_data.get("senha2")

        if senha and senha2 and senha != senha2:
            self.add_error("senha2", "As senhas não coincidem.")


class formLogin(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type':'email'}))
    senha = forms.CharField(widget=forms.PasswordInput())


class ProdutoForm(forms.ModelForm):
    foto = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'foto', 'categoria']
        widgets = {
            'categoria': forms.Select(attrs={
                'placeholder': 'Selecione uma categoria'
            }),
        }


class CadastroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
