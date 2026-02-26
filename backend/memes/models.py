from django.db import models


class MemeTemplate(models.Model):
    """A base meme template image that users can add text to."""
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='templates/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GeneratedMeme(models.Model):
    """A meme created by overlaying text on a template."""
    template = models.ForeignKey(
        MemeTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_memes',
    )
    top_text = models.CharField(max_length=300, blank=True)
    bottom_text = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='generated/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Meme ({self.top_text[:30]})"
