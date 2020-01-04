# Cloud Computing

## 프로젝트 설명
Cloud 기반의 비디오 및 스트림 Sync를 같은 room에 존재하는 유저들 모두에게 맞춰주는 웹어플리케이션입니다.  
간단한 사용법으로,  


 * 유저가 room을 만들고 Guests를 초대  
 * Master 권한을 가진 유저가 영상업로드 혹은 youtube link로 비디오 재생  
 * 같은 room에 있는 유저들 모두 비디오의 재생시간 혹은 일시정지상태 등 sync가 이루어짐  

Docker와 Kubernetes(k8s)를 오라클 클라우드 기반으로 하여 자동배포 및 스케일링 등에 강점을 얻었습니다.  
실로, 클라우드와 k8s 를 통해 얼마나 서버가 버틸수 있는지 서버단에서 테스트도 이루어졌습니다.  


k8s의 강점인 스케일링을 사용하지 않은 서버에선 34000명의 클라이언트 접속시 서버가 동작오류를 일으켰습니다.  
하지만 스케일링을 적용시 동시접속 60000명이 넘어도 latency가 조금은 증가할지라도 문제없이 동작하는것을 확인했습니다.  


## 주요 업무
이번 프로젝트에서 주요 업무로,  
 * 서버 클라이언트 API, 동작도 설계
 * Sync 알고리즘 리서치 및 실제 구현
 * Front-end 개발
 
## 사용 기술
Sync 알고리즘을 구현하기 위한 Javascript  
Front-end 개발을 위한 Bootstrap / Javascript  
자동배포와 컨테이너를 위한 Docker / Kubernetes  
클라우드 베이스 Oracle Cloud

## 오픈소스 링크
https://github.com/UoB-Cloud-Computing-2018-KLS/vchamber
