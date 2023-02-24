from mangum import Mangum
from vision_backend.controller.app import app

handler = Mangum(app)