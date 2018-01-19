from django.db import models
from django.conf import settings
from ..core.mail import send_mail_template
from django.utils import timezone
# Create your models here
from django.urls import reverse


class CourseManager(models.Manager):

    def get_queryset(self, query):
        return super().get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )


class Courses(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o curso', blank=True)
    start_date = models.DateField('Data de Inicio', null=True, blank=True)
    image = models.ImageField(upload_to='couses/images', verbose_name='Imagem', null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, null=True)

    objects = models.Manager()
    CM = CourseManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('courses:details', (), {'slug': self.slug})

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


class Lesson(models.Model):

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Numero (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    course = models.ForeignKey(Courses, verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updates_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, verbose_name='aula', related_name='materials', on_delete=models.CASCADE)

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Matérial'
        verbose_name_plural = 'Matériais'


class Enrollment(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuario',
        related_name='enrollments', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Courses, verbose_name='Curso',
        related_name='enrollments', on_delete=models.CASCADE
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updates_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approve(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscriçao'
        verbose_name_plural = 'Incrições'
        unique_together = (('user', 'course'),)


class Announcement(models.Model):
    course = models.ForeignKey(
        Courses, verbose_name='Curso', related_name='announcements', on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteudo')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updates_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio', related_name='comments', on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', on_delete=models.CASCADE)
    comment = models.TextField('Comentarios')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updates_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']


def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course, status=1
        )
        for enrollments in enrollments:
            recipient_list = [enrollments.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_migrate.connect(
    post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement'
)


