from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import datamhs

class FormMhs(ModelForm):
    class Meta:
        model = datamhs
        fields = ('nim','nama', 'ipk', 'penghasilan', 'sertifikat', 'tanggungan', 'semester')
        labels = {
            'nim': _('NIM'),
            'nama': _('Nama'),
            'ipk':_('IPK'),
            'penghasilan': _('Penghasilan'),
            'sertifikat': _('Sertifikat'),
            'tanggungan': _('Tanggungan'),
            'semester': _('Semester'),
        }
        error_messages = {
            'nim': {
                'required': _("NIM harus diisi"),
            },
            'nama': {
                'required': _("Nama harus diisi"),
            },
            'ipk': {
                'required': _("IPK harus diisi"),
            },
            'penghasilan': {
                'required': _("Penghasilan harus diisi"),
            },
            'sertifikat': {
                'required': _("Sertifikat harus diisi"),
            },
            'tanggungan': {
                'required': _("Tanggungan harus diisi"),
            },
            'semester': {
                'required': _("Semester harus diisi"),
            },
        }

