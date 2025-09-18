class Product:
    # product_count = 0  # счетчик продуктов

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        # Product.product_count += 1  # увеличиваем счетчик продуктов

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с валидацией"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        """Класс-метод для создания продукта из словаря с проверкой дубликатов"""
        # Извлекаем параметры из словаря
        name = product_data.get('name')
        description = product_data.get('description')
        price = product_data.get('price')
        quantity = product_data.get('quantity')
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
        self.__products  = products if products is not None else []
        Category.category_count += 1  # увеличиваем счетчик категорий
        Category.product_count += len(self.__products)  # Увеличиваем счетчик продуктов

    def add_product(self, product: Product):
        """Добавляет товар в категорию с проверкой дубликатов"""
        # Используем класс-метод для проверки дубликатов
        existing_product = Product.new_product(
            {
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity
            },
            self.__products
        )

        # Если вернулся существующий товар (был дубликат)
        if existing_product in self.__products:
            # Товар уже обновлен в списке, ничего не делаем
            pass
        else:
            # Новый товар - добавляем в список
            self.__products.append(existing_product)
            Category.product_count += 1  # увеличиваем общий счетчик продуктов

    @property
    def products(self):
        """Геттер для получения строкового представления всех продуктов"""
        products_list = []
        for product in self.__products:
            product_info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            products_list.append(product_info)
        return "\n".join(products_list)

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.products)
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 5})
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)
