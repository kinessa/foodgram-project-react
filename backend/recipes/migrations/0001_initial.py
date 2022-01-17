import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(
                    max_length=150,
                    verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(
                    max_length=25, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(
                    null=True, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингредиент рецепта',
                'verbose_name_plural': 'Ингредиенты рецептов',
                'ordering': ['recipe'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/',
                                            verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(
                    verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50,
                                          verbose_name='Название тэга')),
                ('color', models.CharField(max_length=8,
                                           verbose_name='Цвет тэга')),
                ('slug', models.SlugField(verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='shopping_cart', to='recipes.Recipe',
                    verbose_name='Покупка')),
            ],
            options={
                'verbose_name': 'Список для покупок',
                'verbose_name_plural': 'Списки для покупок',
                'ordering': ['-id'],
            },
        ),
    ]
