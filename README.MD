# Vietnamese Symptom Checker
This is a rule-based approach for Vietnamese Symptom Checker

<img src="asset/overview.png"/>

### Quick start
#### Installation
```
pip install -r requirements.txt
```
#### Example usage
1. Horizontal-based approach
```
python examples/consultation_horizontal_examples.py

From 30 symptoms, database has 223 disease
Reading weight from data/weight/disease_symptom_weight_random.csv
Xin hãy nhập triệu chứng nào bạn cảm thấy rõ nhất:ho
Bạn có bị Khó thở không ? (y/n/idk):y
Bạn có bị Đau đầu không ? (y/n/idk):n
Bạn có bị Mệt mỏi không ? (y/n/idk):y
Bạn có bị Sốt không ? (y/n/idk):y

Possible disease:
Nhiễm nấm Histoplasma (vi nấm histoplasma)
Covid
Ung thư phế quản phổi nguyên phát
Ung thư lá lách
Sốt siêu vi
{'symptom': ['Ho', 'Khó thở', 'Mệt mỏi', 'Sốt'], 'triage': 'Bạn cần phải đến phòng khám/bệnh viện sớm nhất có thể', 'possible_disease': [{'name': 'Nhiễm nấm Histoplasma (vi nấm histoplasma)', 'confidence': 16}, {'name': 'Covid', 'confidence': 16}, {'name': 'Ung thư phế quản phổi nguyên phát', 'confidence': 12}, {'name': 'Ung thư lá lách', 'confidence': 12}, {'name': 'Sốt siêu vi', 'confidence': 12}], 'asked_symptom': ['Ho', 'Khó thở', 'Đau đầu', 'Mệt mỏi', 'Sốt']}
```
2. Vertical-based approach
```
Xin hãy nhập triệu chứng nào bạn cảm thấy rõ nhất:sốt
=======================================================================
< 1 day - 0
1 tuần - 1
1 tháng - 2
> 1 tháng - 3
Bạn bị bao lâu rồi ? - (0-3):2
=======================================================================
37.5 - 38 độ - 0
> 38 độ C - 1
Hãy đánh giá mức độ sốt của bạn - (0-1):1
=======================================================================
Bạn có bị Sốt tăng dần không ? (y/n/idk):n
Bạn có bị Sốt mạn tính không ? (y/n/idk):n
{'symptom': ['Sốt'], 'triage': 'Bạn có thể chăm sóc tốt tại nhà', 'possible_disease': [{'name': 'Tắc tuyến lệ', 'confidence': 1}, {'name': 'Sốt rét', 'confidence': 1}, {'name': 'Áp xe não', 'confidence': 1}, {'name': 'Viêm cầu thận', 'confidence': 1}, {'name': 'Áp xe thận', 'confidence': 1}], 'asked_symptom': ['Sốt', 'Sốt tăng dần', 'Sốt mạn tính'], 'asked category': [], 'disease_period': ''}
Bạn có bị Thị lực nhìn mờ không ? (y/n/idk):y
{'symptom': ['Sốt', 'Thị lực nhìn mờ'], 'triage': 'Bạn có thể chăm sóc tốt tại nhà', 'possible_disease': [{'name': 'Tắc tuyến lệ', 'confidence': 4}, {'name': 'Áp xe não do amip', 'confidence': 4}, {'name': 'Sốt rét', 'confidence': 2}, {'name': 'Áp xe não', 'confidence': 2}, {'name': 'Viêm cầu thận', 'confidence': 2}], 'asked_symptom': ['Sốt', 'Sốt tăng dần', 'Sốt mạn tính', 'Thị lực nhìn mờ'], 'asked category': [], 'disease_period': ''}
Bạn có bị Mắt bị đỏ không ? (y/n/idk):y
{'symptom': ['Sốt', 'Thị lực nhìn mờ', 'Mắt bị đỏ'], 'triage': 'Bạn có thể chăm sóc tốt tại nhà', 'possible_disease': [{'name': 'Tắc tuyến lệ', 'confidence': 9}, {'name': 'Áp xe não do amip', 'confidence': 6}, {'name': 'Sốt rét', 'confidence': 3}, {'name': 'Áp xe não', 'confidence': 3}, {'name': 'Viêm cầu thận', 'confidence': 3}], 'asked_symptom': ['Sốt', 'Sốt tăng dần', 'Sốt mạn tính', 'Thị lực nhìn mờ', 'Mắt bị đỏ'], 'asked category': [], 'disease_period': ''}
Bạn có bị Sưng mắt không ? (y/n/idk):y
{'symptom': ['Sốt', 'Thị lực nhìn mờ', 'Mắt bị đỏ', 'Sưng mắt'], 'triage': 'Bạn nên đến phòng khám gần nhất', 'possible_disease': [{'name': 'Tắc tuyến lệ', 'confidence': 16}, {'name': 'Áp xe não do amip', 'confidence': 8}, {'name': 'Sốt rét', 'confidence': 4}, {'name': 'Áp xe não', 'confidence': 4}, {'name': 'Viêm cầu thận', 'confidence': 4}], 'asked_symptom': ['Sốt', 'Sốt tăng dần', 'Sốt mạn tính', 'Thị lực nhìn mờ', 'Mắt bị đỏ', 'Sưng mắt'], 'asked category': [], 'disease_period': ''}
=================================================================
Tóm tắt:
Bạn nên đến phòng khám gần nhất
Các bệnh có khả năng:
Tắc tuyến lệ
Áp xe não do amip
Sốt rét
Áp xe não
Viêm cầu thận
```

### Data
Symptom-Disease weights are automated generated and saved in `data/weight/`

### Examples

We provide examples in `./examples`:
- [horizontal-based consultation](examples/consultation_horizontal_examples.py) (swallow symptoms based on severity and commonness)
- [vertical-based consultation](examples/vertical_horizontal_examples.py) (deeper question for each symptom categories)

### Todo
- Deeper question:
    + If disease has same category: --> ask question y = f(possible disease, category)
- Get next symptom based on more weight:
    + symptom-disease reputation: common/uncommon
- Suggested doctor

### NLP-Toolkit
This class supports compare-string techniques, if you want to use semantic-based in `compare_string()`, please download word2vec (PhoW2V_syllables_100dims or PhoW2V_syllables_300dims) in [https://github.com/datquocnguyen/PhoW2V](https://github.com/datquocnguyen/PhoW2V)
