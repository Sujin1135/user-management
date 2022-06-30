class SnsSender:
    @staticmethod
    def send_message(phone_number: str, message: str) -> True:
        """실제 외부 서비스와 연동하여 발송하지 않으므로 발송 성공 처리"""
        print(f"send a message to this phone number({phone_number})")
        print(message)
        return True
