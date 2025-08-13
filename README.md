# paper_agentverse
기존 코드가 openAPI기반이라 openSource 모델 활용해서 실험하려니 코드 수정할 것이 너무 많다.   
각 폴더별 py파일부터 util파일 안의 모든 것 까지.. 진짜 살려줘   
(2025-08-13) review = await agent.astep 이거 이슈 여전히 미해결(decision_maker/brainstorming.py) 여기임.

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
- agent/role_assigner.py (2025.08.13)(done)
   - full_prompt 변수로 prompt를 재설정함.
   - full_prompt=prepend_prompt+history+append_prompt 를 합쳤는데, 이거 각 각 뜯어봐야할 것 같음.
   - max_send_token은 이미 history 생성 시 고려됨.
- environments/tasksolving_env/rules/decision_maker/brainstorming.py (2025.08.13)
   - Agent astep() 방법으로 수정해야하는데 기존 코드 수정이 너무 많아질거 같아서 패스함
   - 그냥 갈아 엎었음 : 모든 agent가 kwargs 기반으로 안전하게 호출되도록 바꿈.

## ⚙️ agent_type
- solver : 작업을 수행하는 주체, 분류기 같은 역할
- role_assigner : 역할을 지정하는 에이전트
- critic : 평가나 피드백 담당
- executor : 실행 담당
- evaluator : 평가 담당 (정확도 평가 등)
- manager : 관리, 조율 역할