from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404


from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """Default home page for web_journal"""
    return render(request, "web_journals/index.html")


def home(request):
    """Personal home page for web_journal"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")

    context = {"topics": topics}
    return render(request, "web_journals/home.html", context)


@login_required
def topics(request):
    """Show subjects"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics, }
    return render(request, "web_journals/topics.html", context)


@login_required
def topic(request, topic_id):
    """Shows a single topic and all associated entries"""
    topic = Topic.objects.get(id=topic_id)
    # Make sure topic belongs to current user
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic,
               "entries": entries}
    return render(request, "web_journals/topic.html", context)


@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != "POST":
        # No data submitted, create a blank form
        form = TopicForm()
    else:
        # POST data submitted, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("web_journals:topics")

    # Display blank or invalid form
    context = {"form": form}
    return render(request, "web_journals/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a specific topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # No data submitted, create a blank form
        form = EntryForm()
    else:
        # POST data submitted, process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("web_journals:topic", topic_id=topic_id)

    # Display a blank or invalid form
    context = {
        "topic": topic,
        "form": form
    }
    return render(request, "web_journals/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # Initial request, pre-fill form with current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted, process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("web_journals:topic", topic_id=topic.id)

    context = {
        "entry": entry,
        "topic": topic,
        "form": form
    }
    return render(request, "web_journals/edit_entry.html", context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    entry.delete()

    context = {
        "entry": entry,
        "topic": topic,
    }
    return render(request, "web_journals/delete_entry.html", context)


@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    topic.delete()

    context = {"topic": topic}
    return render(request, "web_journals/delete_topic.html", context)


@login_required
def edit_topic(request, topic_id):
    """Edit an existing entry"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # Initial request, pre-fill form with current entry
        form = TopicForm(instance=topic)
    else:
        # POST data submitted, process data
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("web_journals:topic", topic_id=topic.id)

    context = {
        "topic": topic,
        "form": form,

    }
    return render(request, "web_journals/edit_topic.html", context)
