import cv2
from pyzbar.pyzbar import decode
import webbrowser

def detect_and_decode_codes(image):
    # Chuyển đổi hình ảnh sang định dạng grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Phát hiện và giải mã các mã QR code và barcode
    decoded_objects = decode(gray)
    code_scanned = False

    
    # Kiểm tra xem có mã QR được nhận diện hay không
    if decoded_objects:
        # Lặp qua tất cả các đối tượng được giải mã
        for obj in decoded_objects:
            # Trích xuất loại và dữ liệu của mã
            code_type = obj.type
            code_data = obj.data.decode("utf-8")

            # Kiểm tra xem dữ liệu có phải là URL hay không
            if code_data.startswith('http'):
                # Mở trình duyệt web và truy cập vào URL từ mã QR
                webbrowser.open(code_data)
                print("Đã truy cập vào trang web:", code_data)
            
            # Lấy tọa độ của các đỉnh của hình vuông chứa mã
            (x, y, w, h) = obj.rect
            
            # Vẽ khung xung quanh mã trên hình ảnh gốc
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Hiển thị loại và dữ liệu của mã
            cv2.putText(image, f"{code_type}: {code_data}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # In loại và dữ liệu của mã ra console
            print(f"{code_type}: {code_data}")
            code_scanned = True
            break
       
    return image, code_scanned


def main():
    # Mở camera
    cap = cv2.VideoCapture(0)
    code_scanned = False

    # Vòng lặp chạy cho đến khi nhấn 'q' để thoát
    while not code_scanned:
        # Đọc khung hình từ camera
        ret, frame = cap.read()   #ret là True/False frame là truy xuất vào khung hình
        
        # Kiểm tra xem việc đọc hình ảnh có thành công hay không
        if not ret:
            print("Không thể đọc hình ảnh từ camera.")
            break
        
        # Phát hiện và giải mã các mã QR code và barcode
        frame, code_scanned = detect_and_decode_codes(frame)
        
        
        # Hiển thị khung hình có mã QR code và barcode trên cửa sổ
        cv2.imshow('Code Scanner', frame)
        
        # Đợi 1ms và kiểm tra phím nhấn
        key = cv2.waitKey(1)
        
        # Nếu phím 'q' được nhấn, thoát khỏi vòng lặp
        if key == ord('q'):
            break
    
    # Giải phóng camera và đóng cửa sổ hiển thị
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
