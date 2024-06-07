
import json
from django.shortcuts import render, redirect
from .models import Cadastro, Avaliacao3
from .models import Cliente
from .models import Favorite
from django.contrib.auth import authenticate,login
from django.http.response import HttpResponse
from django.contrib.auth import login as logind
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import TagCafeteria2

def home(request):
    return render(request, 'index.html')  # Supondo que você tenha um template chamado index.html

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastroloja.html')
    elif request.method == "POST":
        email = request.POST.get('inputEmail4')
        senha = request.POST.get('inputPassword4')
        nome_loja = request.POST.get('inputStoreName')
        endereco = request.POST.get('inputAddress')
        complemento = request.POST.get('inputAddress2')
        cidade = request.POST.get('inputCity')
        bairro = request.POST.get('inputNeighborhood')
        estado = request.POST.get('inputState')
        cep = request.POST.get('inputZip')
        concordo_termos = request.POST.get('gridCheck')

        # Crie uma instância do modelo Cadastro com os dados do formulário
        cadastro = Cadastro(
            email=email,
            senha=senha,
            nome_loja=nome_loja,
            endereco=endereco,
            complemento=complemento,
            cidade=cidade,
            bairro=bairro,
            estado=estado,
            cep=cep,
            concordo_termos=concordo_termos
        )
        # Salve os dados no banco de dados
        cadastro.save()

        return redirect('home')  # Atualize isso com a URL desejada após o cadastro
    
'''def cadastro_cliente(request):
    if request.method == "GET":
        return render(request, 'cadastro_cliente.html')
    elif request.method == "POST":
        email = request.POST.get('inputEmail4')
        senha = request.POST.get('inputPassword4')
        nome_completo = request.POST.get('inputFullName')
        endereco = request.POST.get('inputAddress')
        complemento = request.POST.get('inputAddress2')
        cidade = request.POST.get('inputCity')
        bairro = request.POST.get('inputNeighborhood')
        estado = request.POST.get('inputState')
        cep = request.POST.get('inputZip')
        concordo_termos = request.POST.get('gridCheck')

        cliente = Cliente(
            email=email,
            senha=senha,
            nome_completo=nome_completo,
            endereco=endereco,
            complemento=complemento,
            cidade=cidade,
            bairro=bairro,
            estado=estado,
            cep=cep,
            concordo_termos=concordo_termos
        )
        cliente.save()

        return redirect('login')'''
    
def cadastro_cliente(request):
    if request.method == "GET":
        return render(request,'cadastro_cliente.html')
    elif request.method == "POST":
        nome = request.POST.get('inputFullName')
        email = request.POST.get('inputEmail4')
        senha = request.POST.get('inputPassword4')
        
        user = User.objects.filter(email=email).first()
        
        if user:
            return HttpResponse("essse email e esse nome já estão cadastrados")
        
        user = User.objects.create_user(username=nome,email=email,password=senha)
        user.save()

        return redirect('login')

    
@login_required
def perfil(request, nome_cafeteria):
    if request.method == 'POST':
        # Se for uma solicitação POST, processar a avaliação
        avaliador = request.user.username
        avaliado = nome_cafeteria
        nota = int(request.POST.get('rate'))  # Supondo que 'rate' seja o nome do campo do formulário para a avaliação
        Avaliacao3.objects.create(avaliador=avaliador, avaliado=avaliado, nota=nota, user=request.user)
        # Redirecionar de volta para o perfil da cafeteria após processar a avaliação
        return JsonResponse({'status': 'success'})
    else:
        # Se for uma solicitação GET, apenas renderizar o perfil da cafeteria
        cafeteria = Cadastro.objects.get(nome_loja=nome_cafeteria)
        return render(request, 'visperfil.html', {'cafeteria': cafeteria})


def menu(request):

    cafeterias = []


    for cafeterias_info in Cadastro.objects.all():

        cafeterias_data = {
            'nome_loja': cafeterias_info.nome_loja,
            'bairro': cafeterias_info.bairro,
            'endereco': cafeterias_info.endereco,
            'complemento': cafeterias_info.complemento
        }

        cafeterias.append(cafeterias_data)

    context = {
        'cafeterias': cafeterias
    }

    return render(request, 'menu.html', context)


def favorited_coffeeshop(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        
        favorited = {}
        
        try:
            favorited = Favorite.objects.get(user_id=user.id) 
            Favorite.delete(favorited)
        except:
            Favorite.objects.create(user_id=user)
    
    
    return redirect('perfil')


def login(request):
    if request.method=="GET":
        return render(request, 'login.html')
    else:
        name=request.POST.get('inputEmail4')
        senha=request.POST.get('inputPassword4')
        vali=authenticate(username=name,password=senha)
        if vali:
            logind(request,vali)
            return redirect('menu')
        else:
           return HttpResponse('Você precisa estar logado')

def AdicionandoTag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tag_name = data.get('tag')

        # Aqui você pode personalizar o salvamento para associar ao usuário logado
        # e a cafeteria específica, se necessário
        user = request.user
        tag_name = TagCafeteria2.objects.create(user_id=user, tag_name=tag_name)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})