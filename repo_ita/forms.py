# -*- coding: utf-8 -*-
from django import forms
from repo_ita.models import Articulo


class ArticuloForm(forms.ModelForm):
    """Form definition for Articulo."""

    class Meta:
        """Meta definition for Articuloform."""

        model = Articulo
        fields = ('name', 'description', 'type_of_articule', 'file_path')
