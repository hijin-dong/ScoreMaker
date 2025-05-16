## 🎼 영상 채보 유틸 (제작중)
### 🧰 스택 (업데이트 예정)
- React (Next.js)
- TypeScript
- react-image-crop
- FastAPI
- Python 3.11
- ffmpeg
- Pillow

### 📂 현재 파일 구조 (업데이트 예정)
```
project-root/
├── frontend/
│   ├── pages/
│   │   └── index.tsx         
│   ├── components/
│   │   ├── YouTubeInput.tsx  
│   │   ├── VideoCropper.tsx 
│   │   └── PdfDownloadButton.tsx
│   └── utils/
│       └── cropImage.ts
├── backend/
│   ├── main.py                    
│   └── utils/
│       ├── youtube_download.py  
│       ├── frame_extractor.py  
│       └── pdf_maker.py   
└── README.md
```

### ⚙️ 설치 및 실행
🔧 사전 준비
- Python 3.11 이상
- Node.js (v18 이상 권장)
- FFmpeg 설치 필요

```
cd backend
python -m venv venv
source venv/bin/activate
uvicorn main:app --reload
```

```
cd frontend
npm install
npm run dev
```
<br>

### ✅ 기능
- [x] 유튜브 링크 + 시작 시점 입력
- [x] 해당 시점에서 첫 프레임 추출 (서버 → 프론트 전송)
- [x] 사용자가 프레임에서 크롭할 영역 선택
- [x] 해당 영역 기반 이후 프레임 순차적으로 크롭
- [x] 중복 프레임 필터링
- [x] PDF 병합 및 경로 지정하여 다운로드
- [ ] 다양한 상황에 대응하기 위한 방법 기획 및 구현
  - 악보가 종료된 이후의 영상이 긴 경우: 종료점도 입력받기
  - [악보 진행 상황을 표시하는 경우](https://www.youtube.com/watch?v=X5ZcATGYoyo): threshold값 조정하거나 유사도 측정 방식 변경
  - ...
- [ ] 기타 편의 기능 기획 및 구현
  - 악보 제목 입력
  - 저장 경로 변경
  - 레이아웃 변경
  - ...
