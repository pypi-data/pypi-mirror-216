EasyDesktop
EasyDesktop là một thư viện Python đơn giản cho phép thao tác với cửa sổ desktop trên hệ điều hành Windows.

python
Copy code
desktop = EasyDesktop()
Sau đó, bạn có thể sử dụng các phương thức sau:

go_to_xy(idx, x, y)
Di chuyển một mục trong cửa sổ desktop đến vị trí được chỉ định bởi tọa độ (x, y). Các tham số bao gồm:

idx: Chỉ số của item.
x: Tọa độ x của vị trí đích.
y: Tọa độ y của vị trí đích.
desktop.go_to_xy(idx, x, y)
get_item_count()

Trả về số lượng mục hiện có trong cửa sổ desktop.
count = desktop.get_item_count()
