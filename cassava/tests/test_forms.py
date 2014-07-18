import os

from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from cassava.fields import CsvFormsetField


class ShoppingListItemForm(forms.Form):
    item_code = forms.CharField(max_length=20)
    description = forms.CharField(max_length=255)
    quantity = forms.IntegerField()


class ShoppingListForm(forms.Form):
    title = forms.CharField(max_length=255)
    shopping_list_csv = CsvFormsetField(form_class=ShoppingListItemForm)


class CsvFormsetFieldTests(TestCase):
    """
    Test CsvFormsetField by mocking a ShoppingListCsv Form
    """
    def get_csv_file_data(self, filename):
        """
        Get csv file data from a filename relative this directory
        """
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, filename)
        csv_file = open(file_path, 'rb')
        return SimpleUploadedFile(csv_file.name, csv_file.read())

    def test_valid_formset_csv(self):
        """
        Test that a valid csv upload does not raise any errors
        """
        post_data = {
            'title': u'My Shopping List',
        }
        file_data = {
            'shopping_list_csv': self.get_csv_file_data('valid_formset_csv.csv')
        }
        form = ShoppingListForm(post_data, file_data)
        self.assertTrue(form.is_valid())

    def test_invalid_formset_csv_wrong_data_type(self):
        """
        Test that an invalid csv upload with a bad data type is invalid
        """
        post_data = {
            'title': u'My Shopping List',
        }
        file_data = {
            'shopping_list_csv': self.get_csv_file_data('invalid_formset_csv_wrong_data_type.csv')
        }
        form = ShoppingListForm(post_data, file_data)
        self.assertFalse(form.is_valid())
        self.assertIn(u"Error in row 3", form.errors['shopping_list_csv'])
        self.assertIn(u"quantity", form.fields['shopping_list_csv'].forms[1].errors)
        self.assertIn(u'Enter a whole number.', form.fields['shopping_list_csv'].forms[1].errors['quantity'])


