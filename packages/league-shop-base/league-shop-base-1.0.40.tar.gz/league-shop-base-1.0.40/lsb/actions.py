from django.contrib import messages
from form_action import form_action

from lsb.forms import ProductStatusRemarksForm


def mark_as_handleveled(modeladmin, request, queryset):
    updated = queryset.update(is_handleveled=True)
    messages.info(request, f'{updated} product(s) marked as handleveled.')


def clear_handleveled(modeladmin, request, queryset):
    updated = queryset.update(is_handleveled=False)
    messages.info(request, f'Cleared handleveled from {updated} product(s).')


@form_action(ProductStatusRemarksForm, description='Mark as Disabled')
def mark_as_disabled_with_status(modeladmin, request, queryset, form):
    status = form.cleaned_data['status']
    remarks = form.cleaned_data['remarks']

    to_update = {
        'is_disabled': True,
    }

    if status != 'unchanged':
        to_update['status'] = None if status == '' else status
    if remarks != 'unchanged':
        to_update['remarks'] = None if remarks == '' else remarks

    updated = queryset.update(**to_update)
    messages.info(
        request, f'{updated} product(s) marked as disabled with status {status} and remarks {remarks}.')


@form_action(ProductStatusRemarksForm, description='Clear Disabled')
def clear_disabled_with_status(modeladmin, request, queryset, form):
    status = form.cleaned_data['status']
    remarks = form.cleaned_data['remarks']

    to_update = {
        'is_disabled': False,
    }

    if status != 'unchanged':
        to_update['status'] = None if status == '' else status
    if remarks != 'unchanged':
        to_update['remarks'] = None if remarks == '' else remarks

    updated = queryset.update(**to_update)
    messages.info(
        request, f'Cleared disabled from {updated} product(s) marked with status {status} and remarks {remarks}.')
