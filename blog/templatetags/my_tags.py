from django import template

register = template.Library()


@register.filter(name="mediapath")
def get_image_path(image_path):
    return f"/media/{image_path}"


@register.simple_tag(name="mediapath")
def get_image_path(image_path):
    return f"/media/{image_path}"
