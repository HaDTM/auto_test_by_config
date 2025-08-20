# 📂 bank_adapter_factory.py

from adapters.hdbank_adapter import HDBankAdapter
# from adapters.tpbank_adapter import TPBankAdapter  # nếu sau này có thêm

class BankAdapterFactory:
    @staticmethod
    def create_adapter(bank_name, config):
        bank_name = bank_name.lower()

        if bank_name == "hdbank":
            return HDBankAdapter(config)
        # elif bank_name == "tpbank":
        #     return TPBankAdapter(config)
        else:
            raise ValueError(f"[ERROR] Adapter chưa hỗ trợ cho bank: {bank_name}")
