from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BlogPost, BlogCategory


class BlogListView(View):
    template_name = 'blog/list.html'

    def get(self, request):
        posts = BlogPost.objects.filter(status='published').select_related('author', 'category')
        category_slug = request.GET.get('category')
        if category_slug:
            posts = posts.filter(category__slug=category_slug)
        categories = BlogCategory.objects.all()
        return render(request, self.template_name, {'posts': posts, 'categories': categories})


class BlogDetailView(View):
    template_name = 'blog/detail.html'

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        post.views += 1
        post.save(update_fields=['views'])
        related = BlogPost.objects.filter(
            status='published', category=post.category
        ).exclude(pk=post.pk)[:3]
        return render(request, self.template_name, {'post': post, 'related': related})


@method_decorator(login_required, name='dispatch')
class GenerateBlogPostView(View):
    template_name = 'blog/generate.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        topic = request.POST.get('topic', '')
        if topic:
            from apps.ai_coach.services import chat_with_ai
            prompt = f"Write a detailed fitness blog post about: {topic}. Include introduction, main points, tips, and conclusion. Format with markdown."
            result = chat_with_ai(request.user, prompt)
            content = result.get('response', '')
            from django.utils.text import slugify
            from django.utils import timezone
            post = BlogPost.objects.create(
                title=topic,
                slug=slugify(topic) + f"-{int(timezone.now().timestamp())}",
                author=request.user,
                content=content,
                status='published',
                is_ai_generated=True,
                published_at=timezone.now(),
            )
            return render(request, self.template_name, {'post': post, 'generated': True})
        return render(request, self.template_name)
