from django.core.management.base import BaseCommand
from django.db import transaction
import random
from menu.models import Restaurant, Menu


class Command(BaseCommand):
    help = 'Generates 20 restaurants with 10 menus each'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating restaurants and menus...')

        # Helper functions
        def random_price(min_price, max_price):
            return round(random.randint(min_price, max_price) / 500) * 500

        def generate_menu_name(category):
            prefixes = {
                'indonesian': ['Nasi', 'Mie', 'Soto', 'Gado-gado', 'Rendang', 'Satay', 'Bakso', 'Sambal'],
                'western': ['Burger', 'Steak', 'Pasta', 'Pizza', 'Sandwich', 'Salad', 'Wrap', 'Fries'],
                'chinese': ['Dimsum', 'Noodles', 'Fried Rice', 'Wonton', 'Mapo Tofu', 'Kung Pao', 'Sweet and Sour'],
                'japanese': ['Sushi', 'Ramen', 'Udon', 'Tempura', 'Donburi', 'Yakitori', 'Miso'],
                'korean': ['Bibimbap', 'Kimchi', 'Bulgogi', 'Tteokbokki', 'Samgyeopsal', 'Japchae', 'Gimbap'],
                'indian': ['Curry', 'Biryani', 'Tandoori', 'Naan', 'Tikka Masala', 'Samosa', 'Vindaloo']
            }
            suffixes = ['Special', 'Deluxe', 'Supreme', 'Classic', 'Spicy', 'Combo', 'Set']
            return f"{random.choice(prefixes[category])} {random.choice(suffixes)}"

        # Restaurant data
        categories = ['indonesian', 'western', 'chinese', 'japanese', 'korean', 'indian']
        restaurant_names = {
            'indonesian': ['Warung Nusantara', 'Padang Sedap', 'Java Delight', 'Bali Breeze', 'Sumatera Rasa'],
            'western': ['American Grill', 'Euro Bistro', 'The Steakhouse', 'Burger Joint', 'Pizza Palace'],
            'chinese': ['Golden Dragon', 'Peking Duck House', 'Sichuan Spice', 'Dim Sum Paradise', 'Wok & Roll'],
            'japanese': ['Sakura Sushi', 'Tokyo Ramen', 'Osaka Kitchen', 'Tempura House', 'Zen Garden'],
            'korean': ['Seoul Kitchen', 'K-BBQ Express', 'Kimchi House', 'Gangnam Style', 'Hallyu Flavors'],
            'indian': ['Taj Mahal', 'Curry House', 'Spice Route', 'Bombay Dreams', 'Delhi Delights']
        }

        # Generate restaurants and menus
        with transaction.atomic():
            for _ in range(20):
                category = random.choice(categories)
                price_range = random.choice(['cheap', 'medium', 'expensive'])

                restaurant = Restaurant.objects.create(
                    restaurant_name=f"{random.choice(restaurant_names[category])} {random.randint(1, 99)}",
                    category=category,
                    distance=random.randint(100, 5000),
                    rating=round(random.uniform(3.0, 5.0), 1),
                    # avatar field is left empty for now
                )

                for _ in range(10):
                    if price_range == 'cheap':
                        price = random_price(10000, 25000)
                    elif price_range == 'medium':
                        price = random_price(25500, 60000)
                    else:
                        price = random_price(60500, 150000)

                    Menu.objects.create(
                        menu_name=generate_menu_name(category),
                        restaurant=restaurant,
                        price=price,
                        description=f"Delicious {category.capitalize()} dish",
                        buy_count=random.randint(0, 1000)
                    )

        self.stdout.write(self.style.SUCCESS('Successfully generated 20 restaurants with 10 menus each.'))