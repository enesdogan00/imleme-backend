from typing import Literal


class Success:
    created = "Kayıt başarıyla oluşturuldu."
    updated = "Kayıt başarıyla güncellendi."
    deleted = "Kayıt başarıyla silindi."


class Error:
    no_record = "Kayıt bulunamadı."
    duplicate_record = "Kayıt zaten var."
    permission_denied = "Bu kaynağa erişiminiz bulunmamaktadır."


class Enum:
    levels = Literal["İlkokul", "Ortaokul", "Lise"]
    grades = {
        "İlkokul": ["1", "2", "3", "4"],
        "Ortaokul": ["5", "6", "7", "8"],
        "Lise": ["9", "10", "11", "12"],
    }
