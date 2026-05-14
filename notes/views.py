from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Subject, Unit, Note, Course


@login_required
def home(request):
    subjects = Subject.objects.prefetch_related('units').all()
    return render(request, 'index.html', {'subjects': subjects})


@login_required
def subject_detail(request, subject_slug):
    subject = get_object_or_404(
        Subject.objects.prefetch_related('units__notes'),
        slug=subject_slug
    )

    units_qs = subject.units.all()
    # Agar Unit me 'order' field hai to use karo, warna simple all
    if units_qs.exists() and hasattr(units_qs.first(), 'order'):
        units = units_qs.order_by('order')
    else:
        units = units_qs

    context = {
        'subject': subject,
        'units': units,
    }
    return render(request, 'subject_detail.html', context)


@login_required
def units_and_notes(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)
    data = []
    for unit in subject.units.all():
        data.append({
            'id': unit.id,
            'title': unit.title,
            'notes': [
                {
                    'id': n.id,
                    'title': n.title,
                    'description': n.description,
                    'uploaded_at': n.uploaded_at,
                }
                for n in unit.notes.all()
            ]
        })
    return JsonResponse({'subject': subject.name, 'units': data}, safe=False)


@login_required
def view_note_pdf(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if not note.file:
        raise Http404("File not found")
    return FileResponse(note.file.open('rb'), content_type='application/pdf')

@login_required
def courses_list(request):
    """
    COURSES link se yaha aayega.
    Admin panel se jo bhi Course objects banoge,
    unki list yaha dikhegi.
    """
    courses = Course.objects.all().order_by("title")
    return render(request, "courses_list.html", {"courses": courses})


@login_required
def course_detail(request, slug):
    """
    Har course ka detail page:
    title, description, notes_url, video_url etc.
    """
    course = get_object_or_404(Course, slug=slug)
    return render(request, "course_detail.html", {"course": course})