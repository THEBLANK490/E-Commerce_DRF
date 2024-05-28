from django.urls import path

from payment.views import (  # Khalti_Transaction_List,; Khalti_status,; Khalti_Retrieve_Payment,
    Khalti_Data,
    Khalti_data_save,
    Khalti_Verification,
)

urlpatterns = [
    path("khalti-data-save/", Khalti_data_save.as_view()),
    path("khalti-verification/", Khalti_Verification.as_view()),
    # path('khalti-transaction-list/',Khalti_Transaction_List.as_view()),
    # path('khalti-retrieve-payment/',Khalti_Retrieve_Payment.as_view()),
    # path('khalti-status/',Khalti_status.as_view()),
    path("khalti-data/", Khalti_Data.as_view()),
]
