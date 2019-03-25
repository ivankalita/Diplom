from django import forms
from SH.banner.models import Document


class UserForm(forms.Form):
  # search = forms.CharField()
    CHOICES_for_webserver = [(1, "Nginx"), (2, "Apache"), (3, "Lighttpd"),
                            (4, "Hiawatha"), (5, "Cherokee"), (6, "Monkey "),
                            (7, "Apache Tomcat")]
    webserver = forms.ChoiceField(choices=CHOICES_for_webserver)
  #  counrty = forms.widgets.CheckboxSelectMultiple()
    CHOICES_for_country = [('US', 'us'),
                            ('RU', 'ru')]
    counrty = forms.ChoiceField(choices=CHOICES_for_country, widget=forms.RadioSelect)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )