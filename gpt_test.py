import openai

# Thay thế bằng API key của bạn từ OpenAI
openai.api_key = 'sk-proj-asBHiKgflgSSqjxi8TdxT3BlbkFJaeu3NLJXGrQgWqv6mYe9'

def analyze_command(command):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"Phân tích câu lệnh: '{command}' và chuyển đổi thành hành động cụ thể trong ứng dụng đọc sách. Các hành động có thể bao gồm: điều chỉnh tốc độ đọc, điều chỉnh âm lượng, điều chỉnh ngữ điệu giọng đọc, ra lệnh đọc sách, tua nhanh, tua chậm, chuyển trang, tìm kiếm theo tên tác giả, thể loại, tên sách, đánh dấu trang, ghi chú, thêm, sửa, xóa sách khỏi thư viện, sắp xếp theo tên sách, tên tác giả, thể loại, tra cứu thông tin, tóm tắt nội dung sách, gợi ý sách đọc.",
      max_tokens=150
    )

    action = response.choices[0].text.strip()
    return action

# Ví dụ sử dụng
command = "Tìm kiếm sách của tác giả Nguyễn Nhật Ánh"
action = analyze_command(command)
print(action)
