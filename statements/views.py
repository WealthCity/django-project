__author__ = 'leeward'
from django.views.generic import DetailView
from django.http import HttpResponse
from main.views.base import ClientView
from statements.models import StatementOfAdvice, RecordOfAdvice

__all__ = ["StatementView", "RecordView"]


class PDFView(DetailView, ClientView):
    def get_queryset(self):
        return self.model.objects.filter(
            account__primary_owner=self.request.user.client)

    def get(self, request, pk, ext=None):
        obj = self.get_object()
        if(ext.lower() == '.pdf'):
            response = HttpResponse(obj.render_pdf(self.template_name),
                                    content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="statement_%s.pdf"'%obj.date
        else:
            response = HttpResponse(obj.render_template(self.template_name))
        return response



class StatementView(PDFView):
    template_name = StatementOfAdvice.default_template
    model = StatementOfAdvice
class RecordView(PDFView):
    template_name = RecordOfAdvice.default_template
    model = RecordOfAdvice
