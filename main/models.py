from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FoundationInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название фонда")
    description = models.TextField(verbose_name="Описание фонда")
    mission = models.TextField(verbose_name="Миссия фонда")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес")
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    bank_account = models.CharField(max_length=20, verbose_name="Расчетный счет")
    bank_name = models.CharField(max_length=255, verbose_name="Название банка")
    bik = models.CharField(max_length=9, verbose_name="БИК")
    corr_account = models.CharField(max_length=20, verbose_name="Корреспондентский счет")

    logo = models.ImageField(upload_to='foundation/', verbose_name="Логотип")
    qr_code = models.ImageField(upload_to='foundation/', verbose_name="QR код для оплаты")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Информация о фонде"
        verbose_name_plural = "Информация о фонде"

    def __str__(self):
        return self.name


class News(models.Model):
    """Новости фонда"""
    title = models.CharField(max_length=255, verbose_name="Заголовок новости")
    content = models.TextField(verbose_name="Содержание новости")
    image = models.ImageField(upload_to='news/', verbose_name="Изображение", blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class FundraisingGoal(models.Model):
    """Цели сбора средств"""
    GOAL_STATUS = [
        ('active', 'Активный сбор'),
        ('completed', 'Сбор завершен'),
        ('suspended', 'Сбор приостановлен'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название цели")
    description = models.TextField(verbose_name="Описание цели")
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Целевая сумма")
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Собранная сумма")
    image = models.ImageField(upload_to='goals/', verbose_name="Изображение", blank=True, null=True)
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='active', verbose_name="Статус")
    deadline = models.DateField(verbose_name="Срок сбора", blank=True, null=True)
    priority = models.PositiveIntegerField(default=1, verbose_name="Приоритет отображения")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Цель сбора"
        verbose_name_plural = "Цели сбора"
        ordering = ['priority', '-created_at']

    def __str__(self):
        return self.title

    def progress_percentage(self):
        """Процент выполнения цели"""
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

    def days_left(self):
        """Оставшееся количество дней"""
        if self.deadline:
            today = timezone.now().date()
            days = (self.deadline - today).days
            return max(0, days)
        return None


class Donation(models.Model):
    """Пожертвования"""
    PAYMENT_METHODS = [
        ('bank_transfer', 'Банковский перевод'),
        ('qr_code', 'QR код'),
        ('card', 'Карта'),
        ('cash', 'Наличные'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Ожидает подтверждения'),
        ('completed', 'Завершено'),
        ('failed', 'Не удалось'),
        ('refunded', 'Возвращено'),
    ]

    donor_name = models.CharField(max_length=255, verbose_name="Имя жертвователя", blank=True)
    donor_email = models.EmailField(verbose_name="Email жертвователя", blank=True)
    donor_phone = models.CharField(max_length=20, verbose_name="Телефон жертвователя", blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма пожертвования")
    goal = models.ForeignKey(FundraisingGoal, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="Цель сбора")
    message = models.TextField(verbose_name="Сообщение от жертвователя", blank=True)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending',
                                      verbose_name="Статус платежа")

    is_anonymous = models.BooleanField(default=False, verbose_name="Анонимное пожертвование")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пожертвование"
        verbose_name_plural = "Пожертвования"
        ordering = ['-created_at']

    def __str__(self):
        return f"Пожертвование {self.amount} руб. от {self.donor_name or 'Аноним'}"


class ExpenseReport(models.Model):
    """Отчеты о расходах"""
    REPORT_TYPES = [
        ('purchase', 'Закупка товаров'),
        ('logistics', 'Логистика'),
        ('humanitarian', 'Гуманитарная помощь'),
        ('other', 'Прочие расходы'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название отчета")
    description = models.TextField(verbose_name="Описание расходов")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, verbose_name="Тип отчета")
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Потраченная сумма")
    goal = models.ForeignKey(FundraisingGoal, on_delete=models.CASCADE, verbose_name="Цель сбора")

    # Документы и фото
    document = models.FileField(upload_to='expense_docs/', verbose_name="Документ", blank=True, null=True)
    photos = models.ManyToManyField('ExpensePhoto', blank=True, verbose_name="Фотографии")

    report_date = models.DateField(default=timezone.now, verbose_name="Дата отчета")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отчет о расходах"
        verbose_name_plural = "Отчеты о расходах"
        ordering = ['-report_date']

    def __str__(self):
        return self.title


class ExpensePhoto(models.Model):
    """Фотографии для отчетов о расходах"""
    title = models.CharField(max_length=255, verbose_name="Название фото")
    image = models.ImageField(upload_to='expense_photos/', verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото расхода"
        verbose_name_plural = "Фото расходов"

    def __str__(self):
        return self.title