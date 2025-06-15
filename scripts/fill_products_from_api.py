import os
import sys
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile
from requests.exceptions import RequestException
import cloudinary.uploader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models import Product, ProductCategory
from django.contrib.auth.models import User

API_URL = 'https://fakestoreapi.com/products'

seller = User.objects.first()
if not seller:
    print('Нет пользователей в базе. Создайте хотя бы одного пользователя!')
    exit(1)

print('Запрос к API...')
try:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    products_data = response.json()
    print('Ответ получен, начинаю импорт товаров...')
except RequestException as e:
    print(f'Ошибка запроса к API: {e}')
    exit(1)

for item in products_data:
    category, _ = ProductCategory.objects.get_or_create(name=item['category'])

    try:
        product = Product.objects.get(name=item['title'])
        created = False
        print(f'Товар уже существует: {product.name}')
    except Product.DoesNotExist:
        
        product = Product.objects.create(
            name=item['title'],
            description=item['description'],
            price=item['price'],
            category=category,
            seller=seller,
        )
        created = True
        print(f'Добавлен товар: {product.name}')

    if created:
        image_url = item.get('image')
        if image_url:
            try:
                img_response = requests.get(image_url, timeout=5)
                img_response.raise_for_status()
                    
                result = cloudinary.uploader.upload(
                    img_response.content,
                    folder='products',
                    resource_type='image',
                    transformation={
                        'width': 800,
                        'height': 600,
                        'crop': 'fill',
                        'quality': 'auto',
                        'format': 'auto',
                    }
                )
                
                product.image = result['public_id']
                product.save()
                print(f'  - Изображение для {product.name} загружено в Cloudinary.')
            except RequestException as e:
                print(f'  - Ошибка загрузки изображения для {product.name}: {e}')
            except Exception as e:
                print(f'  - Ошибка загрузки в Cloudinary для {product.name}: {e}')
        else:
            print(f'  - Изображение отсутствует в API для {product.name}.')

print('Готово!') 