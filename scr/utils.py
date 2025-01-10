from dataclasses import dataclass, field
from typing import Dict, Optional
import json
from difflib import SequenceMatcher
from app_logging import error_logger, state_logger

# Đường dẫn đến file dữ liệu
data_path = 'data/dakwaco_device_list.json'


@dataclass
class FunctionCall:
    name: str
    args: Dict[str, str] = field(default_factory=dict)


def parse_function_code(response_message: str) -> Optional[FunctionCall]:
    """
    Phân giải đoạn mã thành tên hàm và struct chứa danh sách tham số và giá trị.

    Args:
        response_message (str): Chuỗi chứa mã cần phân giải.

    Returns:
        FunctionCall: Một đối tượng chứa tên hàm và các tham số.
    """
    # Loại bỏ dấu ngoặc vuông ở hai đầu
    parsed_code = response_message.strip("[]")

    try:
        # Tách tên hàm và tham số
        function_name, args = parsed_code.split("(", 1)

        # Loại bỏ dấu ngoặc cuối cùng từ args nếu có
        args = args.rstrip(")")

        # Tách các tham số và loại bỏ khoảng trắng
        args_list = [arg.strip() for arg in args.split(",")]

        # Xử lý từng tham số và lưu vào dictionary
        args_dict = {}
        for arg in args_list:
            if "=" in arg:
                key, value = arg.split("=", 1)
                args_dict[key.strip()] = value.strip().strip("'")

        # Tạo đối tượng FunctionCall
        function_call = FunctionCall(name=function_name.strip(), args=args_dict)

        print(f"Function name: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        return function_call
    except Exception as e:
        error_logger.error(f"Error during parse function\nError: {str(e)}")
        print(f"Error while parsing: {e}")
        return None

def parse_and_validate_function(response):
    response_pre = response.strip()
    if (response_pre[0] == "'" and response_pre[-1] == "'") or (response_pre[0] == '"' and response_pre[-1] == '"'):
        response_pre = response_pre[1:-1]
    if not response_pre[0] == '[' or not response_pre[-1] == ']':
        error_logger.error(f"Can't parse function\nThe response format is incorrect for the function call tool.\nResponse: {response}\n")
        return None, None, "Error", "Can't parse function"

    parsed_function = parse_function_code(response_pre)
    if not parsed_function or not parsed_function.name:
        return None, None, "Error", "Can't parse function"

    return parsed_function.name, parsed_function.args, None, None

# Hàm đọc dữ liệu từ file JSON
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def normalize_text(text):
    """Chuyển đổi chuỗi về dạng chuẩn hóa (chữ thường và loại bỏ khoảng trắng dư thừa)"""
    return ' '.join(text.lower().strip().split())

def similar(a, b):
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()

def search_data(query, arg_name, max_results=5):
    try:
        # Tải dữ liệu từ file
        data = load_data(data_path)
    except Exception as e:
        error_logger.error(f"Error loading data: {e}")
        return json.dumps({"error": "Failed to load data"}, ensure_ascii=False)

    results = []
    high_score_found = False
    
    # Ánh xạ arg_name
    arg_name_mapping = {
        'dev_id': 'devID',
        'dev_name': 'Name'
    }

    # Thay thế arg_name nếu có trong ánh xạ
    mapped_arg_name = arg_name_mapping.get(arg_name, arg_name)
    try:
        print(f"Query: {query}")
        print(f"arg_name: {arg_name}")
        
        # Tìm kiếm trong dữ liệu theo Name
        query_normalized = normalize_text(query)  # Chuẩn hóa query
        score_value = 0.5 if mapped_arg_name == "Name" else 0.7

        for key, entry in data.items():
            score = similar(query_normalized, entry[mapped_arg_name])
            if score > score_value:
                results.append(entry[mapped_arg_name])
                print(f"{entry[mapped_arg_name]} | score: {score}")
                if score > 0.9:
                    high_score_found = True

        # Nếu có score > 0.9, giới hạn kết quả chỉ 1
        if high_score_found:
            max_results = 1

        # Sắp xếp kết quả theo độ tương đồng (score) từ cao đến thấp
        results.sort(key=lambda x: similar(x, query), reverse=True)

        # Lấy top `max_results` kết quả
        top_results = results[:max(1, min(max_results, len(results)))]
        
        return json.dumps(top_results, indent=4, ensure_ascii=False)
    
    except Exception as e:
        error_logger.error(f"Error during search: {e}")
        return json.dumps({"error": "Error during search"}, ensure_ascii=False)
    
# # Hàm tìm kiếm gần đúng và trả về kết quả dưới dạng chuỗi
# def search_data(query, arg_name, max_results=5):
#     # Tải dữ liệu từ file
#     data = load_data(data_path)
    
#     results = []
#         # Ánh xạ arg_name
#     arg_name_mapping = {
#         'dev_id': 'devID',
#         'dev_name': 'Name'
#     }

#     # Thay thế arg_name nếu có trong ánh xạ
#     mapped_arg_name = arg_name_mapping.get(arg_name, arg_name)
#     print(f"Query: {query}")
#     print(f"arg_name: {arg_name}")
#     # Tìm kiếm trong dữ liệu theo Name
#     query_normalized = normalize_text(query)  # Chuẩn hóa query
#     score_value = 0.5 if mapped_arg_name == "Name" else 0.7
#     for key, entry in data.items():
#         score = similar(query_normalized, entry[mapped_arg_name])
#         if score > score_value:  # Chỉ thêm vào kết quả nếu độ tương đồng cao hơn 0.1 (hoặc thay đổi ngưỡng này)
#             results.append(
#                 entry[mapped_arg_name]
#             )
#             print(f"{entry[mapped_arg_name]} | score: {score}")
#     # Sắp xếp kết quả theo độ tương đồng (score) từ cao đến thấp
#     results.sort(key=lambda x: similar(x, query), reverse=True)

#     # Lấy top `max_results` kết quả
#     top_results = results[:max(1, min(max_results, len(results)))]
    
#     # Trả về kết quả dưới dạng chuỗi
#     return json.dumps(top_results, indent=4, ensure_ascii=False)

def remove_quotes(response):
    if (response.startswith("'") and response.endswith("'")) or (response.startswith('"') and response.endswith('"')):
        return response[1:-1]
    return response
