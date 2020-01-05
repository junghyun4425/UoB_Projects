# Computational Neuroscience

## 프로젝트 설명

### Subtask1
HopField Network를 활용해 Seven-segment에 패턴을 적용하는 프로젝트  


자세한 프로젝트 내용  
 * 11-components vector을 7-digit number 에 호환되게끔 패턴을 설정.
 * 양극화 연산이 적용된 패턴이므로, 바로 Wegith matrix 생성후 저장.
 * 입력 1, 3, 6 에 대한 패턴을 저장 후, McCulloch-Pitts 공식에 따라 계산 및 threshold에 따른 결과값 생성.
 * Hopfield Energy값이 안정화 될때까지 동작.
 
### Subtask2
Spike train 을 포아송 통계모델을 사용하여 spike train을 생성해보고, 실제 데이터와 분석하는 프로젝트.  

자세한 프로젝트 내용  
 * 실제 Spike train은 포아송 분포 모델을 완전히 따르지 않지만, interval값을 설정하여 직접 생성 후, fano factor값 계산.
 * 실제 파리의 H1 Neuron에서 추출한 spike train의 fano factor값과 편차값 계산.  
 * Interval 값을 수정하면서 spike변화를 관찰.

각 뉴런들이 not necessarily adjacent case 와 아닐때의 관계에서 interval이 스파이크에 어떤 영향을 미치는지 확인할 수 있습니다.  

### Subtask3
뉴런이 여럿있을때, 서로 신호를 주고받는다는 가정하에 spike train이 어떤 영향을 받는지 구현 및 결과 분석.

자세한 프로젝트 내용  
 * Neural System을 분석하기에 적합한 Integrate and Fire 모델을 직접 구현 (spike train 생성 가능).  
 * 두개의 뉴런이 서로 synaptic connection 되어있다고 가정하여 두 뉴런의 spike train을 출력하여 분석.  
 * Integrate and Fire 모델이 어떻게 동작하는지 수치를 변경해보면서 분석. 실제 뉴런과 동작이 비슷한지 비교.
 
직접 뉴런의 spike train생성하는 모델을 구현해서 서로영향을 받는 뉴런의 경우를 실제 결과를 도출합니다.


## 주요 업무
이번 프로젝트에서 주요 업무로,  
 * Hopfield network 구현 및 seven-segment로 실습
 * 포아송 모델과 실제 파리의 뉴런데이터로 비교분석
 * Integrate and Fire 모델 직접 구현

 
## 사용 기술
다양한 뉴런모델을 구현하기 위한 Python  
