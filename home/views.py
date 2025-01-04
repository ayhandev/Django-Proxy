from django.shortcuts import render
import httpx
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import re

def home(request):
    return render(request, 'index.html')

logger = logging.getLogger(__name__)

@csrf_exempt
def proxy_view(request, target_url):
    if not target_url:
        return JsonResponse({"error": "Целевой URL не указан"}, status=400)

    # Обработка целевого URL
    target_url = f"https://{target_url}" if not target_url.startswith("http") else target_url
    logger.info(f"Запрос к целевому серверу: {target_url}")

    try:
        # Создаем клиент httpx и разрешаем редиректы
        with httpx.Client(follow_redirects=True, timeout=60.0) as client:
            response = client.get(target_url, headers={"User-Agent": "Mozilla/5.0"})

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "text/html")

                if "text/html" in content_type:
                    # Если это HTML-страница, подменим ссылки на CSS, JS и изображения
                    html_content = response.text
                    html_content = fix_resources(html_content, target_url)

                    return StreamingHttpResponse(
                        html_content,
                        content_type=content_type
                    )

                return StreamingHttpResponse(
                    response.iter_bytes(),
                    content_type=content_type
                )

            else:
                logger.warning(f"Целевой сервер вернул статус: {response.status_code}")
                return JsonResponse(
                    {"error": f"Целевой сервер вернул статус: {response.status_code}"},
                    status=response.status_code
                )

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return JsonResponse({"error": f"Ошибка: {str(e)}"}, status=500)


def fix_resources(html_content, target_url):
    """
    Функция для исправления путей к ресурсам в HTML-контенте (CSS, JS, изображения).
    """
    base_url = target_url.rstrip("/")

    # Исправляем ссылки на CSS
    html_content = re.sub(r'(<link[^>]*href=")(/[^"]+)', r'\1' + base_url + r'\2', html_content)

    # Исправляем ссылки на JS
    html_content = re.sub(r'(<script[^>]*src=")(/[^"]+)', r'\1' + base_url + r'\2', html_content)

    # Исправляем пути к изображениям
    html_content = re.sub(r'(<img[^>]*src=")(/[^"]+)', r'\1' + base_url + r'\2', html_content)

    # Исправляем все ссылки на другие страницы
    html_content = re.sub(r'href="(/[^"]+)', r'href="' + base_url + r'\1', html_content)

    # Исправляем пути для ресурсов, использующих `url()`
    html_content = re.sub(r'url\((\'|\"?)(/[^)]+)(\'|\"?)\)', r'url(\1' + base_url + r'\2\3)', html_content)

    return html_content