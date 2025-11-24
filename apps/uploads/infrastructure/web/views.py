# apps/uploads/views.py

import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser


class PatentesUploadView(APIView):
    """
    POST /api/upload/patentes
    Recibe un archivo en multipart/form-data con los campos:
    - file: archivo a subir
    - folder: subcarpeta (opcional, por defecto 'patentes')
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        folder = request.data.get('folder', 'patentes')

        if not file_obj:
            return Response(
                {"success": False, "message": "No se adjuntó ningún archivo en el campo 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ruta física: MEDIA_ROOT/folder/filename
        dest_dir = os.path.join(settings.MEDIA_ROOT, folder)
        os.makedirs(dest_dir, exist_ok=True)

        # En este ejemplo guardamos con el nombre original
        file_path = os.path.join(dest_dir, file_obj.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Nombre que regresamos al frontend para guardar en 'archivo' en el registro
        filename = file_obj.name

        return Response(
            {
                "success": True,
                "filename": filename,
                "message": "Archivo subido correctamente."
            },
            status=status.HTTP_201_CREATED
        )


class PatentesFileDetailView(APIView):
    """
    GET    /api/upload/patentes/<filename>   -> descarga/visualización
    DELETE /api/upload/patentes/<filename>   -> borrado
    """
    permission_classes = [AllowAny]

    def get_file_path(self, filename: str, folder: str = 'patentes') -> str:
        file_path = os.path.join(settings.MEDIA_ROOT, folder, filename)
        if not os.path.exists(file_path):
            raise Http404("Archivo no encontrado.")
        return file_path

    def get(self, request, filename: str, *args, **kwargs):
        file_path = self.get_file_path(filename)
        return FileResponse(open(file_path, 'rb'), as_attachment=True)

    def delete(self, request, filename: str, *args, **kwargs):
        try:
            file_path = self.get_file_path(filename)
        except Http404:
            return Response(
                {"success": False, "message": "Archivo no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        os.remove(file_path)
        return Response(
            {"success": True, "message": "Archivo eliminado correctamente."},
            status=status.HTTP_200_OK
        )
