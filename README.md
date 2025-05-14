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
- [ ] 해당 영역 기반 이후 프레임 순차적으로 크롭
- [ ] 페이지 레이아웃 지정 (1줄, 2줄, 4줄 등)
- [ ] 중복 프레임 필터링
- [ ] PDF 병합 및 경로 지정하여 다운로드
