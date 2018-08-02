# Import forms class for handling frontend forms
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

# Form class pulling data manually
class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(help_text="Enter a date between nw and 4 weeks (default 3).")

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		# Check date is not in past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - renewal in past'))

		# Check date is in range librarian allowed to change (+4 weeks).
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead.'))

		# Remember to always return the cleaned data
		return data


# Same as above class, just using ModelForm instead of Form, this way you pass a model to it: works really well for longer forms.
from django.forms import ModelForm
from django.contrib.auth.models import User

class EditUserModelForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'