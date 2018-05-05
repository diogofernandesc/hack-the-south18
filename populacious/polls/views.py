from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from datetime import timedelta

from .models import Vote, Poll


def index(request, name="jack"):
	if request.method == "POST":
		request.session["button"] = request.POST
		name = request.POST.get("button")
	return render(request, 'polls/index.html', {"name": name})

def vote(request, name):
    question = get_object_or_404(Poll, name=name)
    try:
        selected_choice = question.vote_set.get(pk=request.POST['choice'])
    except (KeyError, Vote.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
		
def submit(request):
    return render(request, 'polls/submit.html', {})