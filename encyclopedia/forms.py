from django import forms

class EntryForm(forms.Form):
    title = forms.CharField( 
        max_length=300,
        widget=forms.TextInput(attrs={'placeholder':'Entry title', 'class':'input-style'})
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Insert your entry text here (Markdown format)', 'class':'input-style'})
    )           
