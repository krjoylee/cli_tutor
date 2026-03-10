"""CLI Tutor — 패키지 엔트리포인트 (__main__)

프로그램의 시작점을 정의하며, 환경 정보 수집, 설정 확인, 
Setup 마법사 실행 또는 메인 TUI 앱 기동을 관리합니다.
"""

import sys
from rich.console import Console

from .env_info import EnvInfo
from .config_manager import ConfigManager
from .setup_wizard import SetupWizard
from .app import CLITutorApp


def main():
    """메인 실행 함수."""
    console = Console()
    
    # 1. 환경 정보 및 설정 로드
    try:
        env_info = EnvInfo()
        config = ConfigManager()
    except Exception as e:
        console.print(f"[red]❌ 초기화 중 치명적 오류 발생: {e}[/red]")
        sys.exit(1)

    # 2. 초기 설정 여부 확인
    if not config.is_configured():
        wizard = SetupWizard(console, env_info, config)
        try:
            success = wizard.run()
            if not success:
                console.print("[yellow]⚠️ 설정을 완료하지 못했습니다. 프로그램을 종료합니다.[/yellow]")
                sys.exit(0)
            
            # 설정 완료 후 즉시 앱 실행을 원할 경우 여기서 분기 가능
            # 현재는 재시작을 유도하는 방식 (안정성)
            sys.exit(0)
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 취소되었습니다.[/yellow]")
            sys.exit(0)

    # 3. 메인 TUI 앱 실행
    app = CLITutorApp(config, env_info)
    try:
        app.run()
    except Exception as e:
        console.print(f"[red]❌ 애플리케이션 실행 중 예외 발생: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
