# paper_agentverse
yaml파일 수정이 필요함 : agent_type별 모델 설정과 프롬프트를 설정해야함.

## 📁 Folder Structure
```
paper_agentverse/
├── experiments/                      # 공식 repo에서 복제한 실험 환경
│   ├── agentverse/
│   │    └── tasks/
│   │         └── myExperiments/
│   │              └── config.yaml           # Task 및 에이전트 설정 파일
│   ├── data/
│   │    └── Myexperiments/
│   │         ├── waam_cls.json              # WAAM 결함 분류 데이터
│   │         ├── waam_heat_opt.json         # 열 최적화 데이터
│   │         ├── waam_energy_efficiency.json# 에너지 효율 데이터
│   │         └── ...                        
│   └── ...                             # 기타 공식 repo 파일들
└── README.md

```
## 📌 Notes.
- requirements.txt 업데이트(2025.08.06)
- waam dataset(ignore)


## ⚙️ agent_type
- solver : 작업을 수행하는 주체, 분류기 같은 역할
- role_assigner : 역할을 지정하는 에이전트
- critic : 평가나 피드백 담당
- executor : 실행 담당
- evaluator : 평가 담당 (정확도 평가 등)
- manager : 관리, 조율 역할