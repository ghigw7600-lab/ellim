from PIL import Image
import numpy as np

# beom-logo1.png를 읽어서 텍스트 부분을 흰색으로 변경
input_path = r"C:\Users\기광우\makepage\tax-beom-website\assets\logo\beom-logo1.png"
output_path = r"C:\Users\기광우\makepage\tax-beom-website\assets\logo\beom-logo1-white.png"

print("Loading logo image...")
img = Image.open(input_path).convert("RGBA")
img_array = np.array(img)

width, height = img.size
print(f"Image size: {width} x {height}")

# 검은색/어두운 회색 텍스트를 흰색으로 변경
# RGB 값이 모두 100 이하인 픽셀 (어두운 색상) → 흰색으로
r = img_array[:, :, 0]
g = img_array[:, :, 1]
b = img_array[:, :, 2]
alpha = img_array[:, :, 3]

# 어두운 색상 (검은색/회색) 감지
is_dark = (r < 100) & (g < 100) & (b < 100) & (alpha > 0)

# 어두운 텍스트를 흰색으로 변경 (알파는 유지)
img_array[is_dark, 0] = 255  # R
img_array[is_dark, 1] = 255  # G
img_array[is_dark, 2] = 255  # B

# 결과 저장
result_img = Image.fromarray(img_array, mode='RGBA')
result_img.save(output_path, 'PNG')

print(f"[OK] White text logo saved to: {output_path}")
print(f"     Dark pixels converted: {np.sum(is_dark)}")
