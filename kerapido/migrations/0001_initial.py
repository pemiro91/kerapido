# Generated by Django 3.0.8 on 2020-09-06 16:58

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefono', models.CharField(blank=True, max_length=255, null=True)),
                ('is_cliente', models.BooleanField(default=False)),
                ('is_afiliado', models.BooleanField(default=False)),
                ('is_persona_encargada', models.BooleanField(default=False)),
                ('is_administrador', models.BooleanField(default=False)),
                ('fecha_alta', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria_Negocio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria_Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Frecuencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Macro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Negocio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('portada', stdimage.models.StdImageField(blank=True, null=True, upload_to='portada/')),
                ('eslogan', models.CharField(blank=True, max_length=255, null=True)),
                ('horario', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono1', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono2', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('categorias', models.ManyToManyField(to='kerapido.Categoria_Negocio')),
                ('frecuencia', models.ManyToManyField(to='kerapido.Frecuencia')),
                ('macro', models.ManyToManyField(to='kerapido.Macro')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='imagen_plato/')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('precio', models.FloatField(max_length=255)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias_ordered', to='kerapido.Categoria_Producto')),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Negocio')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('color', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa_Entrega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar_destino', models.CharField(max_length=255)),
                ('precio', models.FloatField(max_length=55)),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Negocio')),
            ],
        ),
        migrations.CreateModel(
            name='Reservacion_Simple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto', models.IntegerField()),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Reservacion_Generada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_pagar', models.FloatField(max_length=255)),
                ('fecha_reservacion', models.DateField(default=datetime.date.today)),
                ('cliente_entrega', models.CharField(max_length=255)),
                ('telefono_entrega', models.CharField(max_length=255)),
                ('direccion_entrega', models.CharField(max_length=255)),
                ('estado', models.CharField(default='Pendiente', max_length=50)),
                ('fecha_estado', models.DateField(default=datetime.date.today)),
                ('cliente_auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reservaciones', models.ManyToManyField(to='kerapido.Reservacion_Simple')),
            ],
        ),
        migrations.CreateModel(
            name='Oferta_Laboral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Negocio')),
            ],
        ),
        migrations.AddField(
            model_name='negocio',
            name='servicios',
            field=models.ManyToManyField(to='kerapido.Servicio'),
        ),
        migrations.AddField(
            model_name='negocio',
            name='usuario_negocio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.FloatField(max_length=255)),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Negocio')),
            ],
        ),
        migrations.CreateModel(
            name='ComentarioEvaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('comentario', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_comentario', models.DateField(default=datetime.date.today)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kerapido.Negocio')),
            ],
        ),
        migrations.AddField(
            model_name='categoria_producto',
            name='negocio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Negocio'),
        ),
        migrations.AddField(
            model_name='categoria_negocio',
            name='macro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kerapido.Macro'),
        ),
    ]
