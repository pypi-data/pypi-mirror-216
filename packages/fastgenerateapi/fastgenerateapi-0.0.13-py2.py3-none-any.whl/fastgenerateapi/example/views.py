from fastgenerateapi import APIView, DeleteTreeView, GetTreeView
from modules.example.models import StaffInfo, CompanyInfo


class CompanyView(APIView, DeleteTreeView, GetTreeView):
    model_class = CompanyInfo


class StaffView(APIView):

    def __init__(self):
        self.model_class = StaffInfo
        self.order_by_fields = ["-created_at"]
        super().__init__()





