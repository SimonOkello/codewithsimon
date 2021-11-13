from .forms import CreatePostForm
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from. models import Post, Category


def index(request):
    context = {}
    return render(request, 'posts/index.html', context)


def postDetail(request, post_id):
    categories = Category.objects.all()
    obj = get_object_or_404(Post, pk=post_id)
    context = {'categories': categories, 'obj': obj}
    return render(request, 'posts/post-detail.html', context)


def createPost(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'posts/new-post.html', {'form': form})


def editPost(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    form = CreatePostForm(instance=obj)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'posts/edit-post.html', {'form': form, 'obj': obj})


def deletePost(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('index')
    return render(request, 'posts/delete-confirmation.html', {'obj': obj})
