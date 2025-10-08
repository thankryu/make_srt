import os
import sys
import glob
import subprocess
import time

# -------------------------------------------------------------
# ✅ Windows 한글 경로 및 콘솔 인코딩 대응
# -------------------------------------------------------------
if sys.platform == 'win32':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

# -------------------------------------------------------------
# Faster-Whisper-XXL 실행 파일 및 모델 경로
# -------------------------------------------------------------
WHISPER_XXL_PATH = r"faster-whisper-xxl.exe 설치 경로"

# 모델 폴더의 상위 : faster-whisper-xxl 실행 시 모델이 설치 되는데 해당 경로 상위 폴더 
# ex) C:\Users\thank\AppData\Roaming\PotPlayerMini64\Model\faster-whisper-large-v3 일 경우  C:\Users\thank\AppData\Roaming\PotPlayerMini64\Model
MODEL_DIR = r"C:\Users\thank\AppData\Roaming\PotPlayerMini64\Model"  
MODEL_NAME = "large-v2"  # 모델 이름

# -------------------------------------------------------------
# 1️⃣ 자막 생성 (Faster-Whisper-XXL 호출)
# -------------------------------------------------------------
def generate_subtitles_with_xxl(video_file: str, output_dir: str):
    """
    Faster-Whisper-XXL.exe를 직접 호출하여 자막 생성
    팟플레이어와 동일한 엔진 및 모델 사용
    """
    
    if not os.path.exists(WHISPER_XXL_PATH):
        print(f"❌ Faster-Whisper-XXL을 찾을 수 없습니다: {WHISPER_XXL_PATH}")
        return False
    
    print(f"🎤 모델: {MODEL_NAME}")
    print(f"🎬 처리 중: {os.path.basename(video_file)}")
    
    # 예상되는 출력 파일 경로
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    expected_srt = os.path.join(output_dir, f"{base_name}.ja.srt")
    
    # Faster-Whisper-XXL 명령어 구성
    command = [
        WHISPER_XXL_PATH,
        video_file,
        "--language", "ja",              # 일본어
        "--model", MODEL_NAME,           # 모델 이름 (large-v2)
        "--model_dir", MODEL_DIR,        # 모델이 있는 상위 폴더
        "--output_dir", output_dir,      # 출력 폴더
        "--output_format", "srt",        # SRT 형식
        "--compute_type", "float16",     # 팟플레이어 기본값
        # GPU는 자동 감지됨
    ]
    
    try:
        # XXL 실행 (check=True 제거!)
        result = subprocess.run(
            command,
            capture_output=False,  # 진행 상황을 실시간으로 보기 위해
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 반환 코드 출력 (디버깅용)
        print(f"ℹ️ 프로세스 종료 코드: {result.returncode}")
        
        # 실제 자막 파일이 생성되었는지 확인
        if os.path.exists(expected_srt):
            print(f"✅ 자막 파일 생성 확인: {expected_srt}")
            return True
        else:
            print(f"❌ 자막 파일이 생성되지 않음: {expected_srt}")
            return False
        
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

# -------------------------------------------------------------
# 2️⃣ 메인 실행
# -------------------------------------------------------------
if __name__ == "__main__":
    print("="*60)
    print("🚀 Faster-Whisper-XXL 자막 생성기")
    print("="*60)
    print(f"📍 엔진: faster-whisper-xxl.exe")
    print(f"🧠 모델: large-v2 (팟플레이어 미니 내장)")
    print(f"⚙️ 하드웨어: Ryzen 9 9950X3D + RTX 5070 Ti 16GB")
    print("="*60)
    
    # 경로 검증
    if not os.path.exists(WHISPER_XXL_PATH):
        print(f"\n❌ 엔진을 찾을 수 없습니다:")
        print(f"   {WHISPER_XXL_PATH}")
        input("\n아무 키나 눌러 종료...")
        sys.exit(1)
    
    if not os.path.exists(MODEL_DIR):
        print(f"\n❌ 모델 폴더를 찾을 수 없습니다:")
        print(f"   {MODEL_DIR}")
        input("\n아무 키나 눌러 종료...")
        sys.exit(1)
    
    model_full_path = os.path.join(MODEL_DIR, f"faster-whisper-{MODEL_NAME}")
    if not os.path.exists(model_full_path):
        print(f"\n❌ 모델을 찾을 수 없습니다:")
        print(f"   {model_full_path}")
        input("\n아무 키나 눌러 종료...")
        sys.exit(1)
    
    print("\n✅ 엔진 및 모델 확인 완료")
    
    # 작업 경로 설정
    work_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    os.chdir(work_dir)
    print(f"\n📂 작업 경로: {work_dir}")
    
    print(f"📁 모델 디렉토리: {MODEL_DIR}")
    print(f"🎯 모델: faster-whisper-{MODEL_NAME}")
    print(f"   └── {model_full_path}")
    print(f"       ├── config.json")
    print(f"       ├── model.bin")
    print(f"       ├── tokenizer.json")
    print(f"       └── vocabulary.txt")
    
    # 영상 파일 검색
    video_exts = ["*.mp4", "*.mkv", "*.avi", "*.mov", "*.webm", "*.flv"]
    video_files = []
    for ext in video_exts:
        video_files.extend(glob.glob(ext))
    
    if not video_files:
        print("\n📭 처리할 영상 파일이 없습니다.")
        input("\n아무 키나 눌러 종료...")
        sys.exit(0)
    
    print(f"\n📹 발견된 영상: {len(video_files)}개")
    
    # 처리 시작
    start_time = time.time()
    success_count = 0
    skip_count = 0
    
    for idx, video_file in enumerate(video_files, 1):
        video_start = time.time()
        
        print(f"\n{'='*60}")
        print(f"🎬 [{idx}/{len(video_files)}] {video_file}")
        print(f"{'='*60}")
        
        # 파일 경로 처리
        video_dir = os.path.dirname(os.path.abspath(video_file))
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        expected_srt = os.path.join(video_dir, f"{base_name}.ja.srt")
        
        # 이미 자막이 있는지 확인
        if os.path.exists(expected_srt):
            print(f"⏭️ 이미 존재하는 자막: {expected_srt}")
            skip_count += 1
            continue
        
        try:
            # Faster-Whisper-XXL 호출
            success = generate_subtitles_with_xxl(video_file, video_dir)
            
            if success:
                video_elapsed = time.time() - video_start
                print(f"\n✅ 완료! 처리 시간: {video_elapsed/60:.1f}분")
                success_count += 1
                
                # 생성된 자막 파일 확인
                if os.path.exists(expected_srt):
                    print(f"📝 자막 저장: {expected_srt}")
                else:
                    print(f"⚠️ 자막 파일이 예상 위치에 없습니다.")
            else:
                print(f"❌ 자막 생성 실패")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ 사용자가 중단했습니다.")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
    
    # 최종 결과
    total_elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✅ 모든 작업 완료!")
    print(f"{'='*60}")
    print(f"📊 처리 결과:")
    print(f"   - 성공: {success_count}개")
    print(f"   - 스킵: {skip_count}개")
    print(f"   - 실패: {len(video_files) - success_count - skip_count}개")
    print(f"⏱️ 총 소요시간: {total_elapsed/60:.1f}분 ({total_elapsed/3600:.2f}시간)")
    print(f"{'='*60}")
    
    input("\n아무 키나 눌러 종료...")