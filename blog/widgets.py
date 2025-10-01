from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CustomCKEditorWidget(CKEditorUploadingWidget):
    """Custom CKEditor widget with simplified image handling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override to ensure drag-drop works
        self.config['filebrowserUploadUrl'] = '/ckeditor/upload/'
        self.config['uploadUrl'] = '/ckeditor/upload/'
