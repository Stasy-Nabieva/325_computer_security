import hashlib
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat, PrivateFormat, NoEncryption
)
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

@dataclass
class TxOutput:
    """Выход транзакции (адрес получателя и сумма)"""
    address: str    # Публичный ключ получателя
    amount: float   # Сумма перевода


@dataclass
class TxInput:
    """Вход транзакции (ссылка на выход предыдущей транзакции)"""
    tx_id: str      # ID предыдущей транзакции
    vout: int       # Индекс выхода в предыдущей транзакции
    signature: Optional[bytes] = None  # Цифровая подпись
    public_key: Optional[bytes] = None # Публичный ключ владельца


class Transaction:
    def __init__(self, tx_inputs: List[TxInput] = None, tx_outputs: List[TxOutput] = None):
        self.tx_inputs = tx_inputs if tx_inputs is not None else []
        self.tx_outputs = tx_outputs if tx_outputs is not None else []
        self.id = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Вычисляет хеш транзакции (SHA-256)"""
        tx_data = {
            "inputs": [
                {"tx_id": inp.tx_id, "vout": inp.vout, "public_key": inp.public_key.hex() 
                 if inp.public_key else None}
                for inp in self.tx_inputs
            ],
            "outputs": [asdict(tx_out) for tx_out in self.tx_outputs]
        }
        tx_json = json.dumps(tx_data, sort_keys=True).encode()
        return hashlib.sha256(tx_json).hexdigest()

    async def sign_input(self, input_index: int, private_key: ec.EllipticCurvePrivateKey):
        """Асинхронно подписывает указанный вход транзакции"""
        if input_index >= len(self.tx_inputs):
            raise IndexError("Input index out of range")
        
        # Получаем публичный ключ из приватного
        public_key = private_key.public_key()
        self.tx_inputs[input_index].public_key = public_key.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        )
        
        # Подписываем хеш транзакции
        signature = private_key.sign(
            self.id.encode(),
            ec.ECDSA(hashes.SHA256()))
        
        self.tx_inputs[input_index].signature = signature
        self.id = self.calculate_hash()  # Обновляем хеш после подписи

    def verify_signature(self, input_index: int) -> bool:
        """Проверяет подпись указанного входа"""
        if input_index >= len(self.tx_inputs):
            raise IndexError("Input index out of range")
        
        inp = self.tx_inputs[input_index]
        if not inp.signature or not inp.public_key:
            return False
        
        try:
            # Загружаем публичный ключ
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256K1(),
                inp.public_key
            )
            
            # Проверяем подпись
            public_key.verify(
                inp.signature,
                self.id.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except (InvalidSignature, ValueError):
            return False

    def is_valid(self) -> bool:
        """Проверяет валидность всей транзакции"""
        # Coinbase транзакция (без входов)
        if not self.tx_inputs:
            return len(self.tx_outputs) == 1 and self.tx_outputs[0].amount > 0
        
        # Проверяем все подписи
        if not all(self.verify_signature(i) for i in range(len(self.tx_inputs))):
            return False
            
        # TODO: Добавить проверку баланса (сумма входов >= суммы выходов)
        return True

    def add_input(self, tx_input: TxInput):
        self.tx_inputs.append(tx_input)
        self.id = self.calculate_hash()

    def add_output(self, tx_output: TxOutput):
        self.tx_outputs.append(tx_output)
        self.id = self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "inputs": [
                {
                    "tx_id": inp.tx_id,
                    "vout": inp.vout,
                    "signature": inp.signature.hex() if inp.signature else None,
                    "public_key": inp.public_key.hex() if inp.public_key else None
                }
                for inp in self.tx_inputs
            ],
            "outputs": [asdict(tx_out) for tx_out in self.tx_outputs]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        tx = cls()
        tx.tx_inputs = [
            TxInput(
                tx_id=inp["tx_id"],
                vout=inp["vout"],
                signature=bytes.fromhex(inp["signature"]) if inp["signature"] else None,
                public_key=bytes.fromhex(inp["public_key"]) if inp["public_key"] else None
            )
            for inp in data["inputs"]
        ]
        tx.tx_outputs = [TxOutput(**out) for out in data["outputs"]]
        tx.id = data["id"]
        return tx


async def generate_key_pair() -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Генерирует пару ECDSA ключей (secp256k1)"""
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    return private_key, private_key.public_key()


async def create_and_test_transaction():
    """Создаёт и тестирует транзакцию с ECDSA подписями"""
    # 1. Генерируем ключи для Alice
    alice_private, alice_public = await generate_key_pair()
    
    # 2. Создаём coinbase транзакцию (награда Alice)
    coinbase_tx = Transaction()
    coinbase_tx.add_output(TxOutput(
        address=alice_public.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        ).hex(),
        amount=50.0
    ))
    
    print("Coinbase transaction created:", coinbase_tx.id)
    print("Is valid:", coinbase_tx.is_valid(), "\n")
    
    # 3. Создаём обычную транзакцию (Alice отправляет 30 BTC на Bob)
    
    # Генерируем ключи для Bob
    bob_private, bob_public = await generate_key_pair()
    
    # Создаём вход, ссылающийся на coinbase транзакцию
    tx_input = TxInput(
        tx_id=coinbase_tx.id,
        vout=0,
        public_key=alice_public.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        )
    )
    
    # Создаём саму транзакцию
    tx = Transaction()
    tx.add_input(tx_input)
    tx.add_output(TxOutput(
        address=bob_public.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        ).hex(),
        amount=30.0
    ))
    tx.add_output(TxOutput(
        address=alice_public.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        ).hex(),
        amount=19.9  # Сдача (50 - 30 - 0.1 комиссия)
    ))
    
    # Подписываем вход
    await tx.sign_input(0, alice_private)
    
    print("Normal transaction created:", tx.id)
    print("Is valid:", tx.is_valid())
    
    # Проверяем подпись
    print("Signature verification:", tx.verify_signature(0))
    
    # Тестируем сериализацию
    tx_dict = tx.to_dict()
    restored_tx = Transaction.from_dict(tx_dict)
    print("Restored transaction valid:", restored_tx.is_valid())


# Запускаем тест
import asyncio
asyncio.run(create_and_test_transaction())
