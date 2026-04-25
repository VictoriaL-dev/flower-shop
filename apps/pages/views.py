from django.shortcuts import render, redirect, get_object_or_404

from apps.bouquets.models import Bouquet, Quiz, QuizQuestion, QuizAnswer


def index(request):
    recommended_bouquets = Bouquet.objects.filter(is_available=True)[:3]
    return render(request, "index.html", {"bouquets": recommended_bouquets})


def quiz_step(request, step=1):
    """
    Показывает вопрос квиза на указанном шаге.
    Если шаг > количества вопросов - перенаправляет на результаты.
    """
    quiz = get_object_or_404(Quiz, is_active=True)
    total_steps = quiz.questions.count()

    if total_steps > 0:
        progress_percent = int(((step - 1) / total_steps) * 100)
    else:
        progress_percent = 0

    if step == 1:
        request.session["quiz_tags"] = []

    try:
        question = quiz.questions.get(step_number=step)
    except QuizQuestion.DoesNotExist:
        return redirect("pages:quiz_result")
    
    if request.method == "POST":
        answer_id = request.POST.get("answer")
        if answer_id:
            answer = get_object_or_404(QuizAnswer, id=answer_id)

            current_tags = request.session.get("quiz_tags", [])

            new_tags = list(answer.tags.values_list("id", flat=True))
            current_tags.extend(new_tags)

            request.session["quiz_tags"] = list(set(current_tags))
            request.session.modified = True

        return redirect("pages:quiz_step", step=step + 1)

    context = {
        "question": question,
        "step": step,
        "total_steps": total_steps,
        "progress_percent": progress_percent,
    }
    return render(request, "quiz.html", context)


def quiz_result(request):
    """Показывает букеты, подходящие под собранные теги."""
    tag_ids = request.session.get("quiz_tags", [])

    if tag_ids:
        bouquets = Bouquet.objects.all()
        for tag_id in tag_ids:
            bouquets = bouquets.filter(tags__id=tag_id)
        bouquets = bouquets.distinct()
    else:
        bouquets = Bouquet.objects.none()

    context = {"bouquets": bouquets}

    return render(request, "quiz_result.html", context)
