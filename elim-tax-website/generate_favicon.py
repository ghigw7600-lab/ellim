"""
파비콘 생성 스크립트
elim-logo.png를 기반으로 4종 파비콘 생성
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PIL import Image
import os

# 경로 설정
base_dir = r"C:\Users\기광우\makepage\elim-tax-website"
logo_path = os.path.join(base_dir, "assets", "logo", "elim-logo.png")
favicon_dir = os.path.join(base_dir, "assets", "favicon")

# 파비콘 크기 정의
sizes = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "android-chrome-512x512.png": 512
}

def generate_favicons():
    # 원본 로고 열기
    logo = Image.open(logo_path)

    # RGBA 모드로 변환 (투명 배경 지원)
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')

    # 정사각형으로 크롭 (중앙 기준)
    width, height = logo.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    logo_cropped = logo.crop((left, top, right, bottom))

    # 각 크기별 파비콘 생성
    for filename, size in sizes.items():
        output_path = os.path.join(favicon_dir, filename)

        # 리사이즈 (고품질 리샘플링)
        resized = logo_cropped.resize((size, size), Image.Resampling.LANCZOS)

        # 저장
        resized.save(output_path, "PNG", optimize=True)
        print(f"✅ {filename} ({size}x{size}) 생성 완료")

    print(f"\n🎉 파비콘 4종 생성 완료!")
    print(f"📁 저장 위치: {favicon_dir}")

if __name__ == "__main__":
    generate_favicons()
