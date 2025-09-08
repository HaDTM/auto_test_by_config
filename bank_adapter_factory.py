# 📂 bank_adapter_factory.py

from adapters.hdbank_adapter import HDBankAdapter
from adapters.acb_adapter import ACBBankAdapter
from adapters.lpbank_adapter import LPBankAdapter
from adapters.ncb_adapter import NCBAdapter
from adapters.shb_adapter import SHBAdapter
from adapters.tpbank_biz_adapter import TPBankBIZAdapter
from adapters.vib_adapter import VIBAdapter
from adapters.ssi_adapter import SSIAdapter
from adapters.vtb_adapter import VTBAdapter
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
        elif bank_name == "shbank":
            return SHBAdapter(config)
        elif bank_name == "vibank":
            return VIBAdapter(config)
        elif bank_name == "tpbankbiz":
            return TPBankBIZAdapter(config)
        elif bank_name == "ssi":
            return SSIAdapter(config)
        elif bank_name == "vtb":
            return VTBAdapter(config)
        elif bank_name == "ncbbank":
            return NCBAdapter(config)
        else:
            raise ValueError(f"[ERROR] Adapter chưa hỗ trợ cho bank: {bank_name}")
