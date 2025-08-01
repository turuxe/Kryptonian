import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from tqdm import tqdm
from web3 import Web3

# --- Цветовые константы для стильного интерфейса сканера ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def initialize_node_link():
    """Инициализирует линк с нодой Ethereum через Infura."""
    load_dotenv()
    infura_project_id = os.getenv("INFURA_PROJECT_ID")
    if not infura_project_id or infura_project_id == "YOUR_INFURA_PROJECT_ID_HERE":
        print(f"{Colors.FAIL}Сбой связи: INFURA_PROJECT_ID не обнаружен.{Colors.ENDC}")
        print(f"Требуется калибровка. Создайте файл {Colors.BOLD}.env{Colors.ENDC} с вашим ключом доступа.")
        print("Формат: INFURA_PROJECT_ID=\"abcdef1234567890\"")
        return None
    
    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_project_id}'))
    
    if not w3.is_connected():
        print(f"{Colors.FAIL}Ошибка подключения к сети Ethereum.{Colors.ENDC}")
        return None
        
    print(f"{Colors.GREEN}Соединение с нейросетью Ethereum установлено.{Colors.ENDC}")
    return w3

def perform_xray_scan(w3, contract_address, num_blocks):
    """
    Выполняет X-Ray сканирование смарт-контракта на предмет новых "био-сигнатур".
    """
    try:
        target_address = w3.to_checksum_address(contract_address)
    except ValueError:
        print(f"{Colors.FAIL}Ошибка декодирования: неверный формат адреса объекта.{Colors.ENDC}")
        return

    latest_block_number = w3.eth.block_number
    start_block = latest_block_number - num_blocks + 1

    print(f"\n{Colors.HEADER}{Colors.BOLD}🔬 Активация Криптонианского X-Ray Сканера...{Colors.ENDC}")
    print(f"🎯 {Colors.CYAN}Целевой объект:{Colors.ENDC} {target_address}")
    print(f" SCANNING_DEPTH  SCANNING_DEPTH_IN_BLOCKS{Colors.CYAN}Глубина сканирования:{Colors.ENDC} {num_blocks} блоков (с {start_block} по {latest_block_number})")
    
    detected_signatures = set()
    total_interactions = 0

    pbar = tqdm(range(start_block, latest_block_number + 1), 
                desc=f"{Colors.BLUE}Сканирование секторов{Colors.ENDC}",
                ncols=100)

    for block_num in pbar:
        try:
            block = w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                if tx['to'] and w3.to_checksum_address(tx['to']) == target_address:
                    total_interactions += 1
                    # Каждая "био-сигнатура" - это уникальный адрес отправителя
                    signature = w3.to_checksum_address(tx['from'])
                    detected_signatures.add(signature)
        except Exception as e:
            tqdm.write(f"{Colors.WARNING}Аномалия в секторе {block_num}: {e}{Colors.ENDC}")
            continue

    # --- ВЫЧИСЛЕНИЕ МЕТРИК ---
    total_unique_signatures = len(detected_signatures)
    
    # Симуляция. "Новые" сигнатуры - это все, что мы обнаружили в этом скане.
    # В продвинутой версии мы бы сравнивали с базой данных известных сигнатур.
    known_signatures_db = set() 
    new_signatures = detected_signatures - known_signatures_db
    
    # Наша ключевая метрика!
    bio_signature_index = (len(new_signatures) / total_unique_signatures) * 100 if total_unique_signatures > 0 else 0

    # --- ВЫВОД РЕЗУЛЬТАТОВ ---
    print(f"\n{Colors.HEADER}{Colors.BOLD}🧬 Результаты сканирования Био-Сигнатур:{Colors.ENDC}")
    print("=" * 60)
    print(f"Всего взаимодействий с объектом: {Colors.BOLD}{Colors.GREEN}{total_interactions}{Colors.ENDC}")
    print(f"Обнаружено уникальных био-сигнатур: {Colors.BOLD}{Colors.GREEN}{total_unique_signatures}{Colors.ENDC}")
    
    print(f"\n{Colors.HEADER}{Colors.UNDERLINE}Ключевой показатель Kryptonian:{Colors.ENDC}")
    print(f"🔥 {Colors.WARNING}Индекс Био-Сигнатур (Bio-Signature Index):{Colors.ENDC} "
          f"{Colors.BOLD}{bio_signature_index:.2f}%{Colors.ENDC}")
    print(f"   {Colors.WARNING}(Процент новых, ранее не известных сигнатур в общем потоке){Colors.ENDC}")
    print("=" * 60)
    
    if bio_signature_index > 85:
         print(f"{Colors.GREEN}ВЕРДИКТ: Критическая масса! Обнаружен экспоненциальный приток новых био-сигнатур.{Colors.ENDC}")
    elif bio_signature_index > 50:
        print(f"{Colors.CYAN}ВЕРДИКТ: Обнаружен устойчивый сигнал. Проект привлекает новые формы жизни.{Colors.ENDC}")
    else:
        print(f"{Colors.BLUE}ВЕРДИКТ: Стабильная экосистема. Активность поддерживается ядром известных сигнатур.{Colors.ENDC}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Kryptonian - X-Ray сканер для обнаружения роста сообщества.")
    parser.add_argument("contract", help="Адрес целевого объекта (смарт-контракта) для сканирования.")
    parser.add_argument("-b", "--blocks", type=int, default=1000, help="Глубина сканирования в блоках (по умолчанию: 1000).")
    
    args = parser.parse_args()
    
    node_link = initialize_node_link()
    if node_link:
        perform_xray_scan(node_link, args.contract, args.blocks)
