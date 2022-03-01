''' 
Author: Nguyen Phuc Minh
Lastest update: 1/3/2022
'''

SYMPTOM_CATEGORY = {
    "Ho" : {
        "symptom_period" : {
            "question" : "Bạn bị bao lâu rồi ?",
            "choices": {
                "< 1 day" : "Ho nhẹ",
                "1 tuần" : "Ho thường xuyên",
                "1 tháng": "Ho kéo dài",
                "> 1 tháng": []
            }
        },
        "related_symptoms" : ["Ho mãn tính","Ho có đờm","Ho ra máu","Ho khan"],
    },
    "Sốt" : {
        "symptom_period" : {
            "question" : "Bạn bị bao lâu rồi ?" ,
            "choices": {
                "< 1 day" : "Sốt",
                "1 tuần" : "Sốt kéo dài",
                "1 tháng": "Sốt kéo dài",
                "> 1 tháng": "Sốt kéo dài",
            }
        },
        "severity_question": {
            "question" : "Hãy đánh giá mức độ sốt của bạn",
            "choices" : {
                "37.5 - 38 độ" : "Sốt nhẹ",
                "> 38 độ C" : "Sốt cao",
            }
        },
        "related_symptoms" : ["Sốt tăng dần","Sốt mạn tính"]  
    }
}