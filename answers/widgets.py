# coding: utf-8
__author__ = 'petrmatuhov'


from  django.forms.widgets import Input, FileInput

class TagsInput(Input):
    """
    widget for js-based tag field
    """
    input_type = None  # Subclasses must define this.
    template_name = 'answers/widgets/tags_input.html'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super(Input, self).__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super(Input, self).get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context


class ImageInput(FileInput):
    input_type = 'file'
    needs_multipart_form = True
    template_name = 'answers/widgets/image_input.html'
