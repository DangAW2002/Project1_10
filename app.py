import gradio as gr
from scr.prompt_custom import *
from scr.function_call import *
from scr.app_logging import error_logger, state_logger, configure_logger  # Import error_logger and state_logger from logging.py
from scr.timeout_guard import timeout_guard  # Import timeout_guard from timeout_guard.py
from scr.state import state_1, state_2_pre, state_2, state_4, state_fix, state_plot, user_assistant_prompt, state_3_model, state_3_parse, state_3_result, state_3_searchdb  # Import state functions from state.py
import matplotlib.pyplot as plt
import numpy as np

LENGTH = 100
state = 1

current_tool = ""


def run_conversation(message):
    global state, current_tool
    response = ""
    # Quyết định xem có thực hiện gọi hàm(tool calling) hay không
    if state == 1:
        state_logger.info('\n' + '/'*LENGTH + '\n') 
        # if message == "vẽ":
        #     return state_plot(message)
        response = state_1(message)
        response_tool = response
        response_tool = response_tool.replace("\n", "")
        user_assistant_prompt[0] = user_assistant_prompt[0] + user_prompt(message) + assistant_prompt(response, end = True)

        # Kiểm tra xem response có theo cấu trúc hàm hay không
        if response_tool[0] == '[' and response_tool[-1] == ']':
            current_tool = response_tool
            state_logger.info(f"STATE 1 --> STATE 2\n")
            state = 2
            response = state_2_pre(response_tool)
            return 'Đang trong giai đoạn tùy chỉnh. Nhập "đúng" để  thực hiện công cụ hoặc "bỏ qua" để bỏ qua\n' + response
        else:
            state_logger.info('\n' + '\\'*LENGTH + '\n') 
            return response
    
    # Tùy chỉnh thông số theo yêu cầu người dùng
    if state == 2:
        if message == "đúng":
            state_logger.info(f"STATE 2 | user\n{message}\n")
            state_logger.info(f"STATE 2 --> STATE 3\n")
            state = 3
        elif message == "bỏ qua":
            state = 1
            current_tool = ""
            user_assistant_prompt[0] = user_assistant_prompt[0] + user_prompt(message) + assistant_prompt(end=True)
            state_logger.info(f"STATE | user\n {message}\n")
            state_logger.info(f"STATE 2 --> STATE 1\n")
            state_logger.info('\n' + '\\'*LENGTH + '\n') 
            return "Đã bỏ qua"
        else:
            response = state_2(message)
            current_tool = response
            user_assistant_prompt[0] = user_assistant_prompt[0] + user_prompt(message) + assistant_prompt() + response + end_prompt()
            response = state_2_pre(response)

            return 'Đang trong giai đoạn tùy chỉnh. Nhập "đúng" để  thực hiện công cụ hoặc "bỏ qua" để bỏ qua\n' + response
        
    if state == 3:
        for i in range (3):
            state_logger.info(f"STATE 3 & 4 | Lần: {i+1}\n")

            # Lần đầu tiên không cần chạy state_3_model
            if i:
                response = state_3_model(message)
                current_tool = response
            else:
                response = current_tool
            # Phân giải cấu trúc hàm lấy arg
            function_name, args = state_3_parse(response)

            # Nếu function_name thuộc search database thì thực hiện RAG
            args = state_3_searchdb(function_name, args)


            python_tag_str = function_name

            # Thực thi hàm công cụ và lấy kết quả JSON
            ipython_str  = state_3_result(function_name, args)
            # python_tag_str, ipython_str = state_3(message)
            if python_tag_str == "Error":
                continue

            print("---------------------------------------------------")
            print("STATE 4")
            print(f"Lần: {i+1}")
            state_logger.info(f"STATE 3 --> STATE FIX\n")

            # Kiểm tra status là Error hay Success
            check = state_fix(ipython_str)
            print("check RESPONSE")
            print(check)

            state_logger.info(f"STATE FIX --> STATE 4\n")
            response = state_4(python_tag_str, ipython_str)
            user_assistant_prompt[0] = user_assistant_prompt[0] + user_prompt(message) + assistant_prompt(python_tag(python_tag_str)) + eom_prompt() + ipython(ipython_str)
            user_assistant_prompt[0] = user_assistant_prompt[0] + user_prompt("Mô tả kết quả") + assistant_prompt(response, end = True)

            print("---------------------------------------------------")
            print("STATE 4")
            print(user_assistant_prompt[0])

            # Nếu lỗi thì thực hiện lại vòng lặp để tự sửa lỗi
            if check == "Error" or check == '"Error"':
                message = "Sửa lại lỗi và gọi lại công cụ. Không viết thêm văn bản."
                state_logger.info(f"STATE 4 --> STATE 3\n")
            else:
            # Nếu thành công thì hiển thị kết quả và kết thúc 
                state = 1
                current_tool = ""
                state_logger.info(f"STATE 4 --> STATE 1\n")
                state_logger.info('\n' + '\\'*LENGTH + '\n') 

                return response
            
        # Lỗi tại lúc chạy model và phân giải hàm
        if python_tag_str == "Error":
            state = 1
            current_tool = ""
            response = "Đã có lỗi xảy ra trong lúc dùng công cụ, quay về mặc định."
            user_assistant_prompt[0] = user_assistant_prompt[0] + user_prompt(message) + assistant_prompt(response, end=True) 
            state_logger.info(f"STATE 3 | ERROR\n Có lỗi tại state 3\n")
            state_logger.info(f"STATE 3 --> STATE 1\n")
            state_logger.info('\n' + '\\'*LENGTH + '\n') 
            return response
        # Lỗi tại lúc check == Error <==> Thường là sai format
        else:
            response = response + "\n\nQuay về mặc định."
            state = 1
            current_tool = ""
            state_logger.info(f"STATE 4 | ERROR \n Có lỗi tại state 4\n")
            state_logger.info(f"STATE 4 --> STATE 1\n")
            state_logger.info('\n' + '\\'*LENGTH + '\n') 
            return response
        
# Hàm gradio_interface với timeout
def gradio_interface(message, history):
    def process_message():  # Gói logic của bạn trong hàm này
        global state
        response = run_conversation(message)
        return response

    try:
        # Thêm cơ chế timeout vào hàm chính
        response = timeout_guard(process_message, timeout=120)  # Giới hạn thời gian 120 giây
    except Exception as e:
        response = 'Quá thời gian xử lý. Vui lòng nhấn "Reset Chat" để bắt đầu lại.'
        state_logger.info("Quá thời gian xử lý")
        state_logger.info(f"STATE {state} --> STATE 1\n")
        state_logger.info('\n' + '\\'*LENGTH + '\n') 
        error_logger.error(str(e) + '\n')
        reset_chat()  # Reset chat
    return response

# Define your custom button functionality (reset chat)
def reset_chat():
    global state, current_tool
    state = 1
    current_tool = ""
    user_assistant_prompt[0] = ""
    return []  # Return empty message and empty chat history to reset

# # Function to generate a demo plot
# def generate_demo_plot():
#     x = np.linspace(0, 10, 100)
#     y = np.sin(x)
#     fig, ax = plt.subplots()
#     ax.plot(x, y)
#     ax.set_title("Demo Plot")
#     ax.set_xlabel("X-axis")
#     ax.set_ylabel("Y-axis")
#     ax.grid(True)
#     return fig

# Create a Gradio Blocks interface
with gr.Blocks(fill_height=True) as demo:
    # Define the chat interface
    with gr.Column():
        iface = gr.ChatInterface(
            fn=gradio_interface,
            type="messages",
            title="Llama AI Assistant",
            description="Ask questions to the AI Assistant.",
            examples=[
            "Bạn là ai?",
            "tôi muốn biết thời tiết ở Hà Nội",
            "Thiết lập máy chủ tên 'Server1' với IP '192.168.1.1', cổng 8080, hệ điều hành 'Linux', 4 lõi CPU, 16GB RAM, 256GB lưu trữ",
            "thời tiết tại 'Hanoi' từ '2024-12-16 08:00:00' đến '2024-12-16 12:00:00'",
            "Cài đặt lại thiết bị zxc1",
            "Reset device2",
            "Cấu hình tốc độ lấy mẫu",
            "Cấu hình tốc độ gửi cho thiết bị system1",
            "Cập nhật thời gian",
            "Update phần mềm",
            "Lấy thông tin thiết bị f 16020",
            "Lấy thông tin thiết bị f-16020",
            "Lấy thông tin thiết bị F122334",
            "Lấy thông tin thiết bị F16021",
            "Lấy thông tin thiết bị f@16020",
            "Lấy thông tin thiết bị F-16020",
            "tìm thông tim thiết bị quang trung - xô viết",
            "lấy thông tin thiết bị đồng hồ nguyễn công trứ",
        ],
    )
    # Add a button to the layout
    button = gr.Button("Reset Chat", elem_id="reset_button")
    # Set up the click event for the button to reset the chat
    button.click(reset_chat, outputs=[iface.chatbot])

    # # Add a collapsible box in the bottom-right corner to display a plot
    # with gr.Accordion("Plot", open=False, elem_id="plot_box") as plot_box:
    #     plot = gr.Plot(label="Demo Plot", elem_id="plot")
    # def toggle_plot():
    #     if plot_box.open:
    #         plot_box.open = False
    #         return gr.Accordion(open=False), None
    #     else:
    #         # plot.value = generate_demo_plot()
    #         plot = gr.Plot(value= generate_demo_plot(),label="Demo Plot", elem_id="plot")
    #         plot_box.open = True    
    #     return gr.Accordion(open=True), plot

    # plot_button = gr.Button("Show Plot", elem_id="plot_button")
    # plot_button.click(toggle_plot, inputs=[], outputs=[plot_box, plot])
    
# # Add custom CSS to position the plot box in the bottom-right corner
# css = """
# #plot_box {
#     position: fixed;
#     bottom: 10px;
#     right: 10px;
#     width: 70%;
#     heifht: auto;
#     z-index: 1000;
#     background: white;
#     padding: 10px;
#     border: 1px solid #ccc;
#     box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
# }
# """

# demo.css = css

if __name__ == "__main__":
    configure_logger()  # Configure logger
    demo.launch(server_name="0.0.0.0", server_port=8080)