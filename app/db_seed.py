from sqlalchemy.orm import Session
from app.models.models import NetworkParameter


def seed_network_parameters(db: Session):
    # Начальные значения из ТЗ
    initial_params = [
        {"key": "U", "value": 1000.0, "description": "Максимальная пропускная способность канала"},
        {"key": "c_km", "value": 100.0, "description": "Фиксированная стоимость за 1 км канала"},
        {"key": "c_u", "value": 10.0, "description": "Фиксированная стоимость за единицу пропускной способности"},
    ]

    for param_data in initial_params:
        # Проверяем, существует ли уже такой ключ
        exists = db.query(NetworkParameter).filter_by(key=param_data["key"]).first()
        if not exists:
            new_param = NetworkParameter(**param_data)
            db.add(new_param)
            print(f"SEED: Параметр {param_data['key']} успешно добавлен.")

    db.commit()