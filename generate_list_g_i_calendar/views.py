import os
from django.http import FileResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.views import View
from urllib.parse import quote
from .models import EventLink


class EventLinkGenerator(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        if self.request.method == 'POST':
            title = self.request.POST.get('event-title')
            google_calendar_link = self.request.POST.get('google_calendar_link')
            icalendar_file = self.request.FILES.get("icalendar_file")

            if icalendar_file and google_calendar_link:
                timestamp = now().strftime('%Y%m%d%H%M%S')
                file_name, file_extension = os.path.splitext(icalendar_file.name)
                unique_file_name = f"{title}_{timestamp}{file_extension}"

                event_link = EventLink.objects.create(
                    title=title,
                    google_calendar_link=google_calendar_link,
                )

                event_link.icalendar.save(unique_file_name, icalendar_file)

                return JsonResponse({'message': 'Links saved successfully.', "id": event_link.pk})
            elif not google_calendar_link:
                return JsonResponse({'error': 'Google calendar link is missing.'}, status=400)
            elif not icalendar_file:
                return JsonResponse({'error': 'Iphone calendar link is missing.'}, status=400)
            else:
                return JsonResponse({'error': 'No file uploaded.'}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


def download_icalendar(request, event_id):
    event_link = get_object_or_404(EventLink, pk=event_id)

    file_path = event_link.icalendar.path
    file_name = os.path.basename(file_path)

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'

    return response
