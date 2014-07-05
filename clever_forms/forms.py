import csv

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from django.utils.translation import ugettext_lazy as _, ungettext_lazy


class CsvFormsetField(forms.FileField):
    """
    Processes a csv field input and validate each of its rows like a
    separate form.
    """
    form_class = None
    has_header_row = True
    field_names = []
    forms = []
    default_error_messages = {
        'invalid_csv': _("Upload a valid csv. The file you uploaded was either not a csv or a corrupted csv."),
        'row_error': _("Error in row %(line_number)s"),
    }

    def __init__(self, form_class, form_kwargs={}, *args, **kwargs):
        self.form_class = form_class
        self.form_kwargs = form_kwargs
        return super(CsvFormsetField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        cleaned_data = super(CsvFormsetField, self).clean(data, initial)
        row_forms = self.build_row_forms(cleaned_data)
        self.forms = [row_form['form'] for row_form in row_forms]
        self.validate_row_forms(row_forms)
        return self.forms

    def build_row_forms(self, csv_formset_file):
        """
        Build the row forms for each row of the csv (a dict of form and line number)
        """
        row_forms = []
        self.reader = csv.reader(csv_formset_file)
        self.form_class = self.get_form_class()
        self.field_names = self.get_field_names()
        for row in self.reader:
            row_form = {
                'form': self.build_form_from_csv_row(row),
                'line_number': self.reader.line_num
            }
            row_forms.append(row_form)
        return row_forms

    def get_form_class(self):
        return self.form_class

    def get_field_names(self):
        if self.get_has_header_row():
            return self.get_field_names_from_header_row()
        else:
            return self.get_field_names_from_form_class()

    def get_has_header_row(self):
        return self.has_header_row

    def get_field_names_from_header_row(self):
        field_names = []
        column_headings = self.reader.next()
        if len(column_headings) < 1:
            raise forms.ValidationError(self.error_messages['invalid_csv'], code='invalid_csv')
        # Convert csv header names into lowercase, underscore-separated field names
        for column_heading in column_headings:
            field_names.append(column_heading.lower().strip().replace(" ", "_"))
        return field_names

    def get_field_names_from_form_class(self):
        if form_class is None:
            return self.field_names
        return self.form_class.base_fields.keys()

    def build_form_from_csv_row(self, row):
        "Builds form for row using self.form_class "
        form_data = self.get_form_data_from_row(row)
        return self.form_class(form_data, **self.form_kwargs)

    def get_form_data_from_row(self, row):
        form_data = {}
        for field_name, value in zip(self.field_names, row):
            form_data[field_name] = value
        return form_data

    def validate_row_forms(self, row_forms):
        errors = []
        for row_form in row_forms:
            try:
                self.validate_row_form(row_form)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors, code='csv_error')

    def validate_row_form(self, row_form):
        if not row_form['form'].is_valid():
            raise ValidationError(
                self.error_messages['row_error'],
                code='row_error',
                params={'line_number': row_form['line_number']}
            )

