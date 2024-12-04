from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Note
from .serializers import NoteSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Note
from .serializers import NoteSerializer
from django.shortcuts import render
from django.db.models import Q


class NoteListView(APIView):
    """
    API для отображения списка заметок, создания новой заметки,
    фильтрации, поиска и упорядочивания.
    """
    def get(self, request):
        # Получение параметров запроса
        search_query = request.GET.get('search', None)
        category = request.GET.get('category', None)
        ordering = request.GET.get('ordering', '-created_at')  # По умолчанию: новые заметки первыми

        notes = Note.objects.all()

        # Фильтрация по категории
        if category:
            notes = notes.filter(category=category)

        # Поиск по названию и содержимому
        if search_query:
            notes = notes.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        # Упорядочивание
        notes = notes.order_by(ordering)

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(APIView):
    """
    API для редактирования и удаления заметки.
    """
    def get_object(self, pk):
        return get_object_or_404(Note, pk=pk)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


def notes_list(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    ordering = request.GET.get('ordering', '-created_at')

    notes = Note.objects.all()

    if category:
        notes = notes.filter(category=category)

    if search_query:
        notes = notes.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    notes = notes.order_by(ordering)

    return render(request, 'notes_list.html', {
        'notes': notes,
        'search_query': search_query,
        'category': category,
        'ordering': ordering
    })


def delete_note(request, note_id):
    """
    Удаление заметки через HTML.
    """
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return HttpResponseRedirect('/notes/')
