from django.shortcuts import render

# Create your views here.
import os
import PyPDF2
import tempfile
from urllib.parse import urljoin
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.http import FileResponse

# labels_filename = 'FlipkartLabels.pdf'
# invoices_filename = 'FlipkartInvoices.pdf'
def mergeAndCrop(uploaded_files):
    outputForLabels = PyPDF2.PdfWriter()
    outputForInvoices = PyPDF2.PdfWriter()

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

            temp_filepath = temp_file.name

        with open(temp_filepath, 'rb') as pdf_file:
            pdf = PyPDF2.PdfReader(pdf_file)

            for page in pdf.pages:
                current_page = page
                currentPage = current_page
                currentPageForInvoice = current_page

                # Process for labels
                currentPage.trimbox.lower_left = (150, 450)
                currentPage.trimbox.upper_right = (425, 820)
                currentPage.cropbox.lower_left = (150, 450)
                currentPage.cropbox.upper_right = (425, 820)
                outputForLabels.add_page(currentPage)

                # Process for invoices
                currentPageForInvoice.trimbox.lower_left = (0, 470)
                currentPageForInvoice.trimbox.upper_right = (600, 120)
                currentPageForInvoice.cropbox.lower_left = (0, 470)
                currentPageForInvoice.cropbox.upper_right = (600, 120)
                outputForInvoices.add_page(currentPageForInvoice)

        os.remove(temp_filepath)

    labels_filename = 'FlipkartLabels.pdf'
    invoices_filename = 'FlipkartInvoices.pdf'

    labels_filepath = os.path.join(settings.MEDIA_ROOT, labels_filename)
    invoices_filepath = os.path.join(settings.MEDIA_ROOT, invoices_filename)

    with open(labels_filepath, 'wb') as labels_file:
        outputForLabels.write(labels_file)

    with open(invoices_filepath, 'wb') as invoices_file:
        outputForInvoices.write(invoices_file)

    return labels_filename, invoices_filename

def upload_pdf(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('pdf_files')

        if uploaded_files:
            # Process the uploaded PDFs
            labels_filename, invoices_filename = mergeAndCrop(uploaded_files)

            return render(request, 'upload.html', {
                'output_for_labels': urljoin(settings.MEDIA_URL, labels_filename),
                'output_for_invoices': urljoin(settings.MEDIA_URL, invoices_filename),
            })

    return render(request, 'upload.html')

def download_files(request):
    labels_filepath = request.GET.get('labels_path')
    invoices_filepath = request.GET.get('invoices_path')

    if labels_filepath and invoices_filepath:
        with open(labels_filepath, 'rb') as labels_file:
            response = FileResponse(labels_file)
            response['Content-Disposition'] = 'attachment; filename=Labels.pdf'
            return response

    return HttpResponse("Invalid file paths provided.")




























































































# def mergeAndCrop(uploaded_files):
#     outputForLabels = PyPDF2.PdfWriter()
#     outputForInvoices = PyPDF2.PdfWriter()

#     for uploaded_file in uploaded_files:
#         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#             for chunk in uploaded_file.chunks():
#                 temp_file.write(chunk)

#             temp_filepath = temp_file.name

#         with open(temp_filepath, 'rb') as pdf_file:
#             pdf = PyPDF2.PdfReader(pdf_file)

#             for page in pdf.pages:
#                 current_page = page
#                 currentPage = current_page
#                 currentPageForInvoice = current_page

#                 # Process for labels
#                 currentPage.trimbox.lower_left = (150, 450)
#                 currentPage.trimbox.upper_right = (425, 820)
#                 currentPage.cropbox.lower_left = (150, 450)
#                 currentPage.cropbox.upper_right = (425, 820)
#                 outputForLabels.add_page(currentPage)

#                 # Process for invoices
#                 currentPageForInvoice.trimbox.lower_left = (0, 470)
#                 currentPageForInvoice.trimbox.upper_right = (600, 120)
#                 currentPageForInvoice.cropbox.lower_left = (0, 470)
#                 currentPageForInvoice.cropbox.upper_right = (600, 120)
#                 outputForInvoices.add_page(currentPageForInvoice)

#         os.remove(temp_filepath)

#     labels_filename = 'FlipkartLabels.pdf'
#     invoices_filename = 'FlipkartInvoices.pdf'

#     labels_filepath = os.path.join(settings.MEDIA_ROOT, labels_filename)
#     invoices_filepath = os.path.join(settings.MEDIA_ROOT, invoices_filename)

#     with open(labels_filepath, 'wb') as labels_file:
#         outputForLabels.write(labels_file)

#     with open(invoices_filepath, 'wb') as invoices_file:
#         outputForInvoices.write(invoices_file)

#     return labels_filepath, invoices_filepath

# def upload_pdf(request):
#     if request.method == 'POST':
#         uploaded_files = request.FILES.getlist('pdf_files')

#         if uploaded_files:
#             # Process the uploaded PDFs
#             labels_filepath, invoices_filepath = mergeAndCrop(uploaded_files)

#             return render(request, 'upload.html', {
#                 'output_for_labels': labels_filepath,
#                 'output_for_invoices': invoices_filepath,
#             })

#     return render(request, 'upload.html')



# def download_files(request):
#     labels_filename = 'FlipkartLabels.pdf'
#     invoices_filename = 'FlipkartInvoices.pdf'

#     labels_filepath = os.path.join(settings.MEDIA_ROOT, labels_filename)
#     invoices_filepath = os.path.join(settings.MEDIA_ROOT, invoices_filename)

#     if os.path.exists(labels_filepath) and os.path.exists(invoices_filepath):
#         with open(labels_filepath, 'rb') as labels_file:
#             labels_response = FileResponse(labels_file)
#             labels_response['Content-Disposition'] = f'attachment; filename={labels_filename}'
        
#         with open(invoices_filepath, 'rb') as invoices_file:
#             invoices_response = FileResponse(invoices_file)
#             invoices_response['Content-Disposition'] = f'attachment; filename={invoices_filename}'

#         return [labels_response, invoices_response]
#     else:
#         return HttpResponse("Files not found.")
