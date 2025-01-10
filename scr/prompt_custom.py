import sys
sys.path.append('scr')
from function_call import function_descriptions

def create_prompt(role, message="", end=False):
#     if role == "system":
        
#         return f"""<|begin_of_text|><|start_header_id|>{role}<|end_header_id|>
# {message}{"<|eot_id|>" if end else ""}"""
#     else:
    return f"""<|start_header_id|>{role}<|end_header_id|>
{message}{"<|eot_id|>" if end else ""}"""

def user_prompt(message):
    return create_prompt("user", message, end=True)

def system_prompt(prior_system_instruction="", custom_tool=""):
    return create_prompt("system", f"{prior_system_instruction}{custom_tool}" if prior_system_instruction else "",end=True)

def assistant_prompt(message="", end=False):
    return create_prompt("assistant", message, end)

def python_tag(response_message=""):
    return f"<|python_tag|>{response_message}"

def ipython(result=""):
    return create_prompt("ipython", result, end=True)

def end_prompt():
    return "<|eot_id|>"

def eom_prompt():
    return "<|eom_id|>"

# ------------------------------------PROMPT------------------------------------
prior_system_instruction = """\
Bạn là một chuyên gia trong việc xây dựng và gọi các hàm. Bạn được cung cấp một câu hỏi và một tập hợp các hàm/công cụ có thể sử dụng.  
Dựa trên câu hỏi, bạn cần quyết định xem có thực hiện gọi hàm/công cụ để đạt được mục đích hay chi cẩn trả lời bình thường.  
Nếu không có hàm nào có thể sử dụng được, hãy chỉ ra điều đó. Nếu câu hỏi không cung cấp đủ tham số cần thiết cho hàm, cũng hãy chỉ ra điều đó.  

Nếu bạn quyết định gọi bất kỳ hàm nào, BẮT BUỘC phải đặt trong định dạng:  
[func_name(params_name1=params_value1, params_name2=params_value2...)]  
func_name bắt buộc phải trùng với tên hàm trong danh sách công cụ.
Bạn KHÔNG được thêm bất kỳ văn bản nào khác vào phản hồi khi quyết định gọi hàm.  

Dưới đây là danh sách các hàm ở dạng JSON mà bạn có thể gọi.
"""

custom_tool = """\
[
    {
        "name": "get_weather",
        "description": "Lấy dữ liệu thời tiết cho một địa điểm cụ thể trong khoảng thời gian xác định.",
        "parameters": {
            "type": "object",
            "required": ["location", "start_time", "stop_time", "view_mode"],
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Tên địa điểm (vd: 'Hanoi', 'New York', 'Tokyo')."
                },
                "start_time": {
                    "type": "string",
                    "description": "Thời gian bắt đầu lấy dữ liệu (định dạng: YYYY-MM-DD HH:MM:SS)."
                },
                "stop_time": {
                    "type": "string",
                    "description": "Thời gian kết thúc lấy dữ liệu (định dạng: YYYY-MM-DD HH:MM:SS)."
                },
                "view_mode": {
                    "type": "string",
                    "description": "Chế độ xem dữ liệu, có thể là 'summary' hoặc 'detailed'."
                }
            }
        }
    },
    {
        "name": "setup_server",
        "description": "thiết lập một máy chủ.",
        "parameters": {
            "type": "object",
            "required": ["server_name", "ip_address", "port", "os_type", "cpu_cores", "memory_gb", "storage_gb"],
            "properties": {
                "server_name": {
                    "type": "string",
                    "description": "Tên của máy chủ."
                },
                "ip_address": {
                    "type": "string",
                    "description": "Địa chỉ IP của máy chủ."
                },
                "port": {
                    "type": "integer",
                    "description": "Số cổng cho máy chủ."
                },
                "os_type": {
                    "type": "string",
                    "description": "Loại hệ điều hành (vd: 'Linux', 'Windows')."
                },
                "cpu_cores": {
                    "type": "integer",
                    "description": "Số lõi CPU."
                },
                "memory_gb": {
                    "type": "integer",
                    "description": "Dung lượng bộ nhớ (GB)."
                },
                "storage_gb": {
                    "type": "integer",
                    "description": "Dung lượng lưu trữ (GB)."
                }
            }
        }
    },
    {
        "name": "search_device_by_id",
        "description": "Tìm kiếm thiết bị trong cơ sở dữ liệu JSON bằng ID.",
        "parameters": {
            "type": "object",
            "required": ["dev_id"],
            "properties": {
                "dev_id": {
                    "type": "string",
                    "description": "ID của thiết bị cần tìm kiếm."
                }
            }
        }
    },
    {
        "name": "search_device_by_name",
        "description": "Tìm kiếm thiết bị trong cơ sở dữ liệu JSON theo tên thiết bị.",
        "parameters": {
            "type": "object",
            "required": ["dev_name"],
            "properties": {
                "dev_name": {
                    "type": "string",
                    "description": "Tên thiết bị cần tìm kiếm."
                }
            }
        }
    },
    {
        "name": "config_sampling_rate",
        "description": "Cài đặt tần số lấy mẫu hay còn gọi là tốc độ lấy mẫu. Giá trị cài đặt cần chuyển đồi sang đơn vị giây.",
        "parameters": {
            "type": "object",
            "required": ["dev_id", "sampling_rate"],
            "properties": {
                "dev_id": {
                    "type": "string",
                    "description": "Tên của thiết bị."
                },
                "sampling_rate": {
                    "type": "string",
                    "description": "Tốc độ lấy mẫu cần cài đặt."
                }
            }
        }
    },
    {
        "name": "config_sending_rate",
        "description": "Cài đặt tần số gởi dữ liệu hay còn gọi là tốc độ gởi hay cập nhật dữ liệu.",
        "parameters": {
            "type": "object",
            "required": ["dev_id", "sending_rate"],
            "properties": {
                "dev_id": {
                    "type": "string",
                    "description": "Tên của thiết bị."
                },
                "sending_rate": {
                    "type": "string",
                    "description": "Tốc độ gởi dữ liệu cần cài đặt."
                }
            }
        }
    },
    {
        "name": "config_reset_device",
        "description": "Khởi động lại thiết bị.",
        "parameters": {
            "type": "object",
            "required": ["dev_id"],
            "properties": {
                "dev_id": {
                    "type": "string",
                    "description": "Tên của thiết bị."
                }
            }
        }
    },
    {            
        "name": "config_update_rtc",
        "description": "Cập nhật thời gian cho thiết bị.",
        "parameters": {
            "type": "object",
            "required": ["dev_id"],
            "properties": {
                "dev_id": {
                    "type": "string",
                    "description": "Tên của thiết bị."
                }
            }
        }
    },
    {
        "name": "config_update_new_firmware",
        "description": "Cài đặt phần mềm mới cho thiết bị.",
        "parameters": {
            "type": "object",
            "required": ["dev_id"],
            "properties": {
                "dev_id": {
                    "type": "string",
                    "description": "Tên của thiết bị."
                }
            }
        }
    },
]"""

system_ins2_pre = f"""\
Bạn là một trợ lý hợ trợ người dùng sử dụng công cụ gọi hàm.
Bạn được cung cấp một ánh xạ theo tên hàm.
Danh sách chức năng:
function_descriptions
{{{function_descriptions}}}
Hãy ánh xạ tên hàm từ công cụ với danh sách dưới đay để xác định chức năng của hàm.
Chỉ ghi một dòng theo cấu trúc 'Chức năng: {{chức năng của hàm (không phải tên hàm)}}'.
Sau đó tạo markdown table mô tả các thông số từ công cụ theo cấu trúc (Thông số - giá trị).

"""

system_ins2_2 = """\
Bạn là một trợ lý hợ trợ người dùng sử dụng công cụ gọi hàm.
Dựa trên yêu cầu người dùng, bạn hãy điều chỉnh lại các thông số .
Sau đó, bạn BẮT BUỘC phải mô tả lại các thông số sau khi cập nhật theo cấu trúc hàm như sau:
[func_name(params_name1=params_value1, params_name2=params_value2...)]  
Bạn KHÔNG được thêm bất kỳ văn bản nào khác vào phản hồi. 
Dưới đây là danh sách các hàm ở dạng JSON, hãy dựa vào đó để viết chính xác cấu trúc:

"""

system_ins3 = """\
Bạn là một chuyên gia trong việc cấu trúc định dạng hàm.
Dưa vào hội thoại hãy điều chỉnh thông số và định dạng thành hàm theo cấu trúc:
[func_name(params_name1=params_value1, params_name2=params_value2...)]  
Bạn KHÔNG được thêm bất kỳ văn bản nào khác vào phản hồi. 

Dưới đây là danh sách các hàm ở dạng JSON mà bạn có thể gọi.
"""
system_ins3_2_database = f"""\
Bạn là một chuyên gia trong việc ánh xạ.
Bắt buộc trả về một trong các chuỗi dưới đây dựa trên sự tương đồng với yêu cầu người dùng và không được thêm bất kỳ văn bản khác vào phản hồi.
Nếu không tìm được, chỉ trả về 'Không' và không kèm bất kỳ văn bản nào khác.

"""
system_ins4 = """\
Bạn là một chuyên gia trong việc báo cáo kết quả trả về từ một tool.
Hãy mô tả đầy đủ thông tin trả về từ tool, bao gồm trạng thái và các thông số.

"""

system_ins_fix = """\
Bạn là một trợ lý thông minh trong việc xác định kết quả.
Dựa trên kết quả trả về  bên dưới, hãy xác định xem là "Success" hay "Error".
Chỉ trả về theo Literal['Success', 'Error'], không được thêm bất kỳ văn bản nào khác vào phản hồi.

"""

system_ins_user_intent = """\
Bạn là một trợ lý thông minh trong việc xác định mong muốn của người dùng.
Dựa trên yêu cầu được cung cấp bên dưới, hãy xác định xem mong muốn của người dùng là "Điều chỉnh", "Bỏ qua" hay "Thực hiện".
Chỉ trả về theo Literal['Điều chỉnh', 'Bỏ qua', 'Thực hiện'], không được thêm bất kỳ văn bản nào khác vào phản hồi.

"""
# chưa xong-----------------------------------------------------
system_ins_plot = """\
Bạn là một chuyên gia trong việc tạo và hiển thị plot.
Dựa vào đoạn hội thoại, hãy viết thành code python để tạo plot từ dữ liệu.
Ví dụ:

'''
import matplotlib.pyplot as plt
import numpy as np

def generate_plot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    return fig

'''
Bạn chỉ tạo code python để tạo plot. Tất cả phải nằm trong hàm generate_plot(). 
Bạn chỉ cần tạo hàm và return fig, không cần gọi plt.show() hay gọi hàm generate_plot().
Bạn KHÔNG được thêm bất kỳ văn bản nào khác vào phản hồi. 

"""