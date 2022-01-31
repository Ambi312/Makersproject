from django.shortcuts import render


def post_list(request):
    return render(request, 'oursite/post_list.html', {})
