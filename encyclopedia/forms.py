from django import forms

class EntryForm(forms.Form):
    title = forms.CharField( 
        max_length=300,
        widget=forms.TextInput(attrs={'placeholder':'Entry title', 'class':'input-style'})
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Insert your entry text here (Markdown format)', 'class':'input-style'})
    )           

class AverageForm(forms.Form):
    parcial1 = forms.FloatField(min_value=0, max_value=10, label='Parcial 1')
    parcial2 = forms.FloatField(min_value=0, max_value=10, label='Parcial 2')
    parcial3 = forms.FloatField(min_value=0, max_value=10, label='Parcial 3')
    parcial4 = forms.FloatField(min_value=0, max_value=10, label='Parcial 4')