class Product:
    product_count = 0
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        Product.product_count += 1

    def __str__(self):
        """Строковое представление продукта"""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Магический метод для сложения общей стоимости двух продуктов"""
        if isinstance(other, Product):
            return (self.price * self.quantity) + (other.price * other.quantity)
        return NotImplemented

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с валидацией и подтверждением понижения"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Если новая цена ниже текущей, запрашиваем подтверждение
        if new_price < self.__price:
            confirmation = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердите действие (y/n): ")
            if confirmation.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price
        print("Цена успешно обновлена")

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        """Класс-метод для создания продукта из словаря с проверкой дубликатов"""
        # Извлекаем параметры из словаря
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")
        # Если передан список существующих товаров, ищем дубликаты
        if existing_products:
            for existing_product in existing_products:
                if existing_product.name.lower() == name.lower():
                    # Найден дубликат - обновляем существующий товар
                    existing_product.quantity += quantity
                    # Выбираем максимальную цену
                    existing_product.price = max(existing_product.price, price)
                    # Обновляем описание, если новое не пустое
                    if description:
                        existing_product.description = description
                    return existing_product

        # Если дубликатов не найдено, создаем новый товар
        return cls(name, description, price, quantity)


class Category:
    category_count = 0  # общее количество категорий
    product_count = 0  # общее количество уникальных продуктов во всех категориях

    def __init__(self, name: str, description: str, products: list[Product] = None):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1  # увеличиваем счетчик категорий

        # Добавляем продукты через метод add_product для правильного подсчета
        if products is not None:
            for product in products:
                self.add_product(product)

    def __str__(self):
        """Строковое представление категории"""
        total_quantity = self.get_total_quantity()
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def get_total_quantity(self):
        """Подсчитывает общее количество всех продуктов в категории"""
        return sum(product.quantity for product in self.__products)

    def get_total_value(self):
        """Подсчитывает полную стоимость всех товаров в категории"""
        return sum(product.price * product.quantity for product in self.__products)

    # def __add__(self, other):
    #     """Магический метод для сложения общей стоимости двух категорий"""
    #     if isinstance(other, Category):
    #         return self.get_total_value() + other.get_total_value()
    #     return NotImplemented

    def add_product(self, product: Product):
        """Добавляет товар в категорию с проверкой дубликатов"""
        # Проверяем, есть ли уже такой товар в категории
        found_duplicate = False
        for existing_product in self.__products:
            if existing_product.name.lower() == product.name.lower():
                found_duplicate = True
                # Обновляем существующий товар
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                if product.description:
                    existing_product.description = product.description
                break

        # Если дубликат не найден, добавляем новый товар
        if not found_duplicate:
            self.__products.append(product)
            Category.product_count += 1  # увеличиваем общий счетчик продуктов

    @property
    def products(self):
        """Геттер для получения строкового представления всех продуктов"""
        return "\n".join(str(product) for product in self.__products)


# if __name__ == "__main__":
#     # Создаем продукты
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 10)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 10)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 10)
#     # Создаем категорию
#     category1 = Category("Смартфоны", "Смартфоны как средство", [product1, product2, product3])
#     print(f"===Список продуктов (всего {category1.product_count} шт. в категории 1):")
#     print(category1.products)
#     print("===Тестируем строковое представление категории:")
#     print(category1)  # Выведет: "Смартфоны, общее количество продуктов: 27 шт."
#     print(f"===Проверяем добавление нового продукта в категорию 1")
#     product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
#     category1.add_product(product4)
#     print(category1.products)
#     print(f"===Теперь всего товаров {category1.product_count} шт.")
#     # Можно также отдельно получить общее количество
#     print(f"===Общее количество продуктов в категории: {category1.get_total_quantity()} шт.")
#     print("===Добавление продукта")
#     new_product = Product.new_product(
#         {
#             "name": "Samsung Galaxy S23 Ultra",
#             "description": "256GB, Серый цвет, 200MP камера",
#             "price": 180000.0,
#             "quantity": 5,
#         }
#     )
#     print(new_product.name)
#     print(new_product.description)
#     print(new_product.price)
#     print(new_product.quantity)
#     print("===Изменение цены продукта")
#     new_product.price = 800
#     print(new_product.price)
#     new_product.price = -100
#     print(new_product.price)
#     new_product.price = 0
#     print(new_product.price)
#     print(f"===Список продуктов (всего {category1.product_count} шт. в категории 1):")
#     print(category1.products)
