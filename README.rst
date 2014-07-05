Django Clever Forms
===================
Django Clever Forms is a library of useful form fields and features.  For the moment this only includes the CsvFormsetField.

CsvFormsetField
---------------
The CsvFormsetField processes a csv field input and validate each of its rows like a separate form.

To use it, you just need to add a CsvFormsetField to your form (the one to render on the webpage), specifying a form class to handle each of the rows of your csv file. The file will be handled by looking for a header row with each of the field names.

The example below illustrates how this could be used to implement a simple shopping list as a csv upload::


    from clever_forms.forms import CsvFormsetField


    class ShoppingListItemForm(forms.Form):
        # This form handles each row of the csv
        item_code = forms.CharField(max_length=20)
        description = forms.CharField(max_length=255)
        quantity = forms.IntegerField()


    class ShoppingListForm(forms.Form):
        # This is the form to render to the webpage
        title = forms.CharField(max_length=255)
        shopping_list_csv = CsvFormsetField(form_class=ShoppingListItemForm)
