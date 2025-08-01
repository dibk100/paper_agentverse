# paper_agentverse
update.2025/08/01   
```
paper_agentverse/experiments/agentverse$ agentverse-tasksolving --task tasksolving/myExperiments_test01 --tasks_dir ./tasks
```
yaml파일 수정이 필요함 : agent_type별 모델 설정과 프롬프트를 설정해야함.

## 📁 Folder Structure
```
paper_agentverse/
├── experiments/                        # official에서 복제
│   ├── agentverse/
│   │    └── tasks/
│   │        └── myExperiments_test01/
│   └── .../               
└── README.md
```

## ⚙️ agent_type
- solver : 작업을 수행하는 주체, 분류기 같은 역할
- role_assigner : 역할을 지정하는 에이전트
- critic : 평가나 피드백 담당
- executor : 실행 담당
- evaluator : 평가 담당 (정확도 평가 등)
- manager : 관리, 조율 역할