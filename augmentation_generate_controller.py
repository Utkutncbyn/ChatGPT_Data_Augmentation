from typing import List, Optional, Union
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile, File


augmentation_generate_router = APIRouter(tags=["AugmentationController"])

@cbv(augmentation_generate_router)
class AugmentationGenerateController:

    def __init__(self, jwt_data = Depends(JWTBearer())):
        self.augmentation_generate_service = AugmentationGenerateService()
        self.jwt_user = jwt_data[2]

    @augmentation_generate_router.post("/generate")
    def generate(self, payload: AugmentationGenerateDTO, permission=Depends(Permission(["augmentation:generate"])) ):
        business_response = self.augmentation_generate_service.generate(payload)
        return business_response