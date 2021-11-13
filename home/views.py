from django.shortcuts import get_object_or_404, render
from posts.models import Post, Category

# Create your views here.


def index(request):
    categories = Category.objects.all()
    posts = Post.objects.select_related('category').all()
    context = {'categories': categories, 'posts': posts}
    return render(request, 'home/index.html', context)


def categoryView(request, slug):
    try:
        categories = Category.objects.all()
        obj = get_object_or_404(Category, slug=slug)
        posts = Post.objects.select_related('category').filter(category=obj)
    except Category.DoesNotExist:
        pass

    context = {'categories': categories, 'obj': obj, 'posts': posts}
    return render(request, 'home/index.html', context)
