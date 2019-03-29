from django.shortcuts import render

# Create your views here.

#League of Legends 전적검색
def score_view(request):
    return render(request, 'score/score_view.html')

