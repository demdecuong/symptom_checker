

class InferenceEngine:
    def __init__(self):
        pass

    def get_personal_info(self):
        pass

    def greeting(self):
        print("Chào bạn, chức năng này không thể thay thế bác sĩ chẩn đoán.") 
        print("Bạn có muốn tiếp tục (y/n)")
        if input() == "y":
            self.get_personal_info()
        else:
            print("Chúc bạn 1 ngày vui")

    def update_current_response(self, symptom):
        self.current_response['symptom'].append(symptom)

    def query(self,symptom):
        '''
        Args:
            - symptom (list)
        Return:
        '''
        pass