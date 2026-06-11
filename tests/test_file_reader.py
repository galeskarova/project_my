from unittest.mock import MagicMock, mock_open, patch
from src.file_reader import read_csv_transactions, read_excel_transactions

# Тесты для CSV


def test_read_csv_transactions_success() -> None:
    """Успешное чтение CSV-файла."""
    csv_content = "id,amount,currency\n1,100,USD\n2,200,EUR"
    with patch("builtins.open", mock_open(read_data=csv_content)):
        result = read_csv_transactions("fake.csv")
        assert len(result) == 2
        assert result[0]["amount"] == "100"
        assert result[1]["currency"] == "EUR"


def test_read_csv_transactions_file_not_found() -> None:
    """Файл не найден -> пустой список."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_csv_transactions("nonexistent.csv")
        assert result == []


def test_read_csv_transactions_read_error() -> None:
    """Ошибка при чтении файла -> пустой список."""
    with patch("builtins.open", side_effect=PermissionError("Denied")):
        result = read_csv_transactions("fake.csv")
        assert result == []


# Тесты для Excel


def test_read_excel_transactions_success() -> None:
    """Успешное чтение Excel-файла (мокаем pandas)."""
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{"id": "1", "amount": "100"}, {"id": "2", "amount": "200"}]
    mock_df.fillna.return_value = mock_df

    with patch("src.file_reader.pd") as mock_pd:
        mock_pd.read_excel.return_value = mock_df
        result = read_excel_transactions("fake.xlsx")
        assert len(result) == 2
        assert result[0]["amount"] == "100"
        mock_pd.read_excel.assert_called_once_with("fake.xlsx", dtype=str, keep_default_na=False)


def test_read_excel_transactions_file_not_found() -> None:
    """Excel файл не найден -> пустой список."""
    with patch("src.file_reader.pd") as mock_pd:
        mock_pd.read_excel.side_effect = FileNotFoundError
        result = read_excel_transactions("nonexistent.xlsx")
        assert result == []


def test_read_excel_transactions_pandas_not_installed() -> None:
    """Если pandas не установлен, возвращаем пустой список."""
    with patch("src.file_reader.pd", None):
        result = read_excel_transactions("fake.xlsx")
        assert result == []


def test_read_excel_transactions_read_error() -> None:
    """Ошибка при чтении Excel -> пустой список."""
    with patch("src.file_reader.pd") as mock_pd:
        mock_pd.read_excel.side_effect = Exception("Read error")
        result = read_excel_transactions("fake.xlsx")
        assert result == []
