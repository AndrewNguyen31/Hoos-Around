from django import forms
from .models import Picture, Place


class PictureForm(forms.ModelForm):
    """
    Smaller form for creating a picture
    """
    class Meta:
        model = Picture
        fields = ["img", "description"]


PictureFormSet = forms.modelformset_factory(
    Picture, form=PictureForm, extra=1, can_delete=True
)


class PlaceForm(forms.ModelForm):
    """
    Form for creating a place
    """
    class Meta:
        model = Place
        fields = [
            "name",
            "description",
            "address1",
            "address2",
            "zip_code",
            "city",
            "country",
            "latitude",
            "longitude",
        ]
