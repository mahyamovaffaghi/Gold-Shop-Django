from django  import  forms

class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)


class replyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea())
