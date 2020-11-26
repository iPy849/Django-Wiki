#Built-in imports
import re
import random

#Third party imports
from django.shortcuts import render, redirect, HttpResponse
from markdown2 import markdown

#My imports
from . import util
from . import forms

#index view
def index(request):
    context = {'searched': False}

    #If GET then check q arg and classify it in a list or a str
    #I don't know if it is right to execute this conditional everytime index function is called.
    #   I hope there is a better way.
    if request.method == 'GET':
        question = request.GET.get('q')
        results = doSearch(question) #None and '' checks and returns the list or a string

        #results check, add the context the render needs to display the template
        if results is not None:
            if type(results) == list:
                context['entries'] = doSearch(question)
                context['searched'] = True
                return render(request, 'encyclopedia/index.html', context)
            else:
                return redirect(f'wiki/{results}')

    #If not passed the search arg validation the retrieve all entry names and display it
    if not context['searched']:
        context['entries'] = util.list_entries()
        context['entries'].sort()
    return render(request, 'encyclopedia/index.html', context)

#entry view
def entry(request, entry_name):
    entry_text = util.get_entry(entry_name)
    context = {}

    if entry_text:
        context['title'] = entry_name
        context['content'] = markdown(entry_text)
        context['editable'] = True
    else:
        context['title'] = 'ERROR'
        context['content'] = f'<h1 style="text-align:center">The "{entry_name}" entry does not exists</h1>'
    
    return render(request, 'encyclopedia/entry.html', context)

#Writing and editing an entry
def newEntry(request, entry_name=None):

    #If it was accessed with an argument, add the needed context for the template
    if entry_name:
        context = {
            'form': forms.EntryForm(initial={
                'text': util.get_entry(entry_name),
                'title': entry_name
                }
            ),
            'edit': True,
            'title': entry_name
        }
        request.session['edit'] = True
    else:
        context = {
            'form': forms.EntryForm(),
        }

    if request.method == 'POST':
        form = forms.EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            #If it is in edit mode it doesn't matter checking for duplicate entries
            if type(doSearch(title)) is str and not request.session['edit']:
                context['title'] = title
                context['exists'] = True
                context['form'] = form
            else:
                request.session['edit'] = False
                util.save_entry(title, text)
                return redirect('index', permanent=True)

    return render(request, 'encyclopedia/new.html', context)

def randomPage(request):
    entries = util.list_entries()
    choice = random.choice(entries)
    return redirect('entry', choice)

def average(request):
    respuestas = None
    if request.method == 'POST':
        form = forms.AverageForm(request.POST)
        if form.is_valid():
            parcial_1 = form.cleaned_data['parcial1']
            parcial_2 = form.cleaned_data['parcial2']
            parcial_3 = form.cleaned_data['parcial3']
            parcial_4 = form.cleaned_data['parcial4']

            promedio = parcial_1 + parcial_2 + parcial_3 + parcial_4
            promedio /= 4
            promedio6 = promedio * 0.6
            promedio4 = 6 - promedio6

            if promedio4 > 0:
                promedio4 /= 0.4
                respuestas = promedio4

            elif promedio4 <= 0:
                respuestas.append('Estas bien')
    
    return render(request, 'encyclopedia/promedio.html', {
        'respuestas': respuestas,
        'form': forms.AverageForm()
    })


#Helper Functions
def doSearch(arg):
    '''
    Creates a list of names that contains the argument. If
    a word match the arg, that word will be returned 
    '''
    if arg == '' or arg == None:
        return None
    
    arg = arg.lower()
    result_list = []
    entries = util.list_entries()
        
    for entry in entries:
        entry = entry.lower()
        if re.search(arg, entry):
            result_list.append(entry)
            if arg == entry:
                return arg

    result_list.sort()
    return result_list