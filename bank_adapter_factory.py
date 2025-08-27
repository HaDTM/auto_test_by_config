# 📂 bank_adapter_factory.py

from adapters.hdbank_adapter import HDBankAdapter
from adapters.acb_adapter import ACBBankAdapter
from adapters.lpbank_adapter import LPBankAdapter
# from adapters.tpbank_adapter import TPBankAdapter  # nếu sau này có thêm

class BankAdapterFactory:
    @staticmethod
    def create_adapter(bank_name, config):
        bank_name = bank_name.lower()

        if bank_name == "hdbank":
            return HDBankAdapter(config)
        elif bank_name == "acb":
            return ACBBankAdapter(config)
        elif bank_name == "lpbank":
            return LPBankAdapter(config)
        else:
            raise ValueError(f"[ERROR] Adapter chưa hỗ trợ cho bank: {bank_name}")
