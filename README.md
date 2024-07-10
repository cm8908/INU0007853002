## ⚡프로젝트 개요
- 인천대학교 컴퓨터공학부 빅데이터입문 기말 프로젝트
- League of Legends 게임 내의 복합적인 요소들에 의해 팀의 승패과 좌우됨
- **프로젝트 목표: 게임 매치 데이터를 이용해 승패에 가장 결정적인 영향을 주는 요인을 분석**
    - 세부 목표: 게임 내 포지션 중 하나인 **“Top Laner”에 대한 승률 분석**
    - 게임플레이에서의 행동 선택에 도움 될만한 Insight 제공을 기대
- 게임 데이터에 대해 다양한 분석 기법을 활용해보는 데 의의를 둠

## 💻 구현한 내용

### 데이터 수집

- Riot 공식 API 사용하여 데이터 수집하는 툴 사용 ([`LolCrawler`](https://github.com/cm8908/LolCrawler)
- MongoDB에 저장 (약 19만개의 게임 매치 기록 수집)

### 데이터 전처리

- 경기 시간에 있어서 이상치 제거 (Quantile 0.90)
- “Top Laner” 아닌 게임 플레이 제거
- 특징 생성 (분당 creep score, K/D/A평점)

### 데이터 분석

- 게임 진행 시간, 캐릭터 분류에 따라 승패 시각화
- Kruskal-Wallis H-test를 통해 각 특징의 승패에의 영향 분석
- `XGBoost`, `LightGBM`을 이용해 승패 분류기 학습 및 feature importance 분석
