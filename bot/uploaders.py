from vkbottle import PhotoMessageUploader


photo_uploader = None
def init_uploader(api):
    global photo_uploader
    photo_uploader = PhotoMessageUploader(api)