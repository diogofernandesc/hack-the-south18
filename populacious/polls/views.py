from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from datetime import timedelta

from .models import Vote, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'polls_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #return Poll.objects.order_by('-start_time')[:5]
        return Poll.objects.all()


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Poll, pk=question_id)
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
	
def done(request):
	Poll(vote_area=request.POST['area'],
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(days=7),
        poll_type=request.POST['type'],
        title=request.POST['title'],
        question=request.POST['question'],
        values=request.POST['values']).save()
	return render(request, 'polls/done.html')