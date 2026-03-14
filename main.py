from src.widget import get_date, mask_account_card


def main():
    # Примеры использования функций
    try:
        print(mask_account_card("Visa Platinum 7000792289606361"))
        print(mask_account_card("Счет 73654108430135874305"))
        print(get_date("2024-03-11T02:26:18.671407"))
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
