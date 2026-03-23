from django.shortcuts import render, get_object_or_404
from .models import Produto

def index(request):
    produtos = Produto.objects.all()[:8]
    return render(request, 'produtos/index.html', {'produtos': produtos})

def todos_produtos(request):
    categoria = request.GET.get('categoria', '')
    if categoria:
        produtos = Produto.objects.filter(categoria=categoria)
    else:
        produtos = Produto.objects.all()
    return render(request, 'produtos/todos_produtos.html', {
        'produtos': produtos,
        'categoria_ativa': categoria,
    })

def detalhe(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produtos/detalhe.html', {'produto': produto})