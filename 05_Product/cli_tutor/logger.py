import logging
import os
import sys
from datetime import datetime

class CLILogger:
    @staticmethod
    def setup():
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"cli_tutor_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            encoding='utf-8'
        )

        # 외부 라이브러리(특히 마크다운 파서)의 과도한 DEBUG 로그 억제
        logging.getLogger("markdown_it").setLevel(logging.INFO)
        logging.getLogger("httpcore").setLevel(logging.INFO)
        logging.getLogger("httpx").setLevel(logging.INFO)
        
        # 기본 로그
        logging.info("=== CLI Tutor Logging Started ===")
        logging.info(f"OS: {os.name}, Platform: {sys.platform}")

    @staticmethod
    def debug(msg):
        logging.debug(msg)
        # 터미널에도 출력 (배후에서 보일 수 있도록)
        print(f"[DEBUG] {msg}")

    @staticmethod
    def info(msg):
        logging.info(msg)
        print(f"[INFO] {msg}")

    @staticmethod
    def error(msg):
        logging.error(msg)
        print(f"[ERROR] {msg}")
