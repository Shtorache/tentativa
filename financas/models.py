from django.db import models

class Perfil(models.Model):
    pessoa = models.CharField(
        max_length=10,
        choices=[
            ('IAN', 'Ian'),
            ('JULIA', 'Julia'),
            ('JUNTOS', 'Juntos'),
        ],
        unique=True
    )
    senha = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.pessoa


class Movimento(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    PESSOA_CHOICES = (
        ('IAN', 'Ian'),
        ('JULIA', 'Julia'),
        ('JUNTOS', 'Juntos'),
    )

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    pessoa = models.CharField(max_length=10, choices=PESSOA_CHOICES)
    origem = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.pessoa} - {self.origem}"
