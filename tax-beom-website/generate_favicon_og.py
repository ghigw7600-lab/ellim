# -*- coding: utf-8 -*-
"""
파비콘 및 OG 이미지 자동 생성 스크립트
세무회계 범 브랜드 아이덴티티 적용
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# UTF-8 출력 설정
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 브랜드 컬러
BRAND_GREEN = (74, 140, 59)  # #4a8c3b
WHITE = (255, 255, 255)
LIGHT_GREEN = (232, 245, 228)  # #e8f5e4
DARK_GRAY = (55, 65, 81)  # #374151

# 출력 디렉토리
FAVICON_DIR = "assets/favicon"
os.makedirs(FAVICON_DIR, exist_ok=True)

def create_favicon(size, filename):
    """
    파비콘 생성 - "범" 한 글자를 초록색 배경에 흰색으로
    """
    img = Image.new('RGB', (size, size), BRAND_GREEN)
    draw = ImageDraw.Draw(img)

    # 폰트 크기 계산 (이미지의 70%)
    font_size = int(size * 0.7)

    try:
        # Windows 기본 한글 폰트 사용
        font = ImageFont.truetype("malgun.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", font_size)
        except:
            print(f"[Warning] 한글 폰트를 찾을 수 없습니다. 기본 폰트 사용")
            font = ImageFont.load_default()

    # 텍스트 "범" 중앙 배치
    text = "범"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2 - (bbox[1])  # 상단 여백 보정

    draw.text((x, y), text, fill=WHITE, font=font)

    # PNG로 저장
    img.save(f"{FAVICON_DIR}/{filename}", "PNG")
    print(f"OK {filename} 생성 완료 ({size}x{size}px)")

def create_og_image():
    """
    OG 이미지 생성 - 1200x630px
    카카오톡, 페이스북 공유 시 썸네일
    """
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(img)

    # 배경 그라데이션 효과 (상단: 흰색 → 하단: 연한 초록)
    for y in range(height):
        ratio = y / height
        r = int(255 + (LIGHT_GREEN[0] - 255) * ratio)
        g = int(255 + (LIGHT_GREEN[1] - 255) * ratio)
        b = int(255 + (LIGHT_GREEN[2] - 255) * ratio)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))

    try:
        font_title = ImageFont.truetype("malgunbd.ttf", 90)  # 굵은 고딕
        font_subtitle = ImageFont.truetype("malgun.ttf", 50)
        font_desc = ImageFont.truetype("malgun.ttf", 38)
        font_url = ImageFont.truetype("malgun.ttf", 32)
    except:
        try:
            font_title = ImageFont.truetype("C:\\Windows\\Fonts\\malgunbd.ttf", 90)
            font_subtitle = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 50)
            font_desc = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 38)
            font_url = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 32)
        except:
            print("[Warning] 한글 폰트를 찾을 수 없습니다. 기본 폰트 사용")
            font_title = ImageFont.load_default()
            font_subtitle = font_title
            font_desc = font_title
            font_url = font_title

    # 로고 이미지 삽입 (있다면)
    try:
        logo = Image.open("assets/logo/beom-logo1.png")
        # 로고 크기 조정 (최대 높이 120px)
        logo_height = 120
        ratio = logo_height / logo.height
        logo_width = int(logo.width * ratio)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        # 로고 중앙 상단 배치 (y=80)
        logo_x = (width - logo_width) // 2
        img.paste(logo, (logo_x, 80), logo if logo.mode == 'RGBA' else None)
        y_offset = 230
    except Exception as e:
        print(f"[Warning] 로고 삽입 실패: {e}")
        y_offset = 150

    # 텍스트 배치
    texts = [
        ("세무회계 범", font_title, BRAND_GREEN, y_offset),
        ("전문 세무사 1:1 매칭 서비스", font_subtitle, DARK_GRAY, y_offset + 120),
        ("대표세무사가 직접 상담합니다", font_desc, DARK_GRAY, y_offset + 200),
    ]

    for text, font, color, y in texts:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), text, fill=color, font=font)

    # 체크 마크 + 서비스
    services_y = y_offset + 280
    services = "세무기장 / 법인세 / 절세 컨설팅"
    bbox = draw.textbbox((0, 0), services, font=font_desc)
    services_width = bbox[2] - bbox[0]
    x = (width - services_width) // 2
    draw.text((x, services_y), services, fill=BRAND_GREEN, font=font_desc)

    # URL
    url_text = "taxbeom.com"
    bbox = draw.textbbox((0, 0), url_text, font=font_url)
    url_width = bbox[2] - bbox[0]
    x = (width - url_width) // 2
    draw.text((x, height - 80), url_text, fill=DARK_GRAY, font=font_url)

    # 저장
    img.save("assets/og-image.png", "PNG")
    print(f"OK og-image.png 생성 완료 (1200x630px)")

if __name__ == "__main__":
    print("=" * 60)
    print("세무회계 범 - 파비콘 및 OG 이미지 생성")
    print("=" * 60)

    # 파비콘 생성
    create_favicon(16, "favicon-16x16.png")
    create_favicon(32, "favicon-32x32.png")
    create_favicon(180, "apple-touch-icon.png")
    create_favicon(512, "android-chrome-512x512.png")

    # OG 이미지 생성
    create_og_image()

    print("=" * 60)
    print("모든 이미지 생성 완료!")
    print(f"파비콘 위치: {FAVICON_DIR}/")
    print("OG 이미지 위치: assets/og-image.png")
    print("=" * 60)
