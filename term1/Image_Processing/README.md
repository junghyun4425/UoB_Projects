# Image Processing and Computer Vision

## 프로젝트 설명
### Subtask1
Viola-Jones 알고리즘을 통해 얼굴인식률을 테스트하는 수행과제.  
AdaBoost를 사용하여 미리 얼굴식별의 훈련된 xml파일을 사용.  
정확도를 F1-score방식으로 계산하여 통계낸뒤 결론을 도출.  

### Subtask2
OpenCV에서 제공하는 Haar-like features 방법을 통해 물체(다트판)를 식별하는 수행과제.  
Haar-like features만으로는 훌륭한 성과가 나오기 힘들기에, F1-score값이 낮은것을 확인가능.  

### Subtask3
Subtask2에서의 성능을 끌어올리기 위해 이미지 프로세싱 알고리즘을 도입.
직접 구현한 Sobel Filter로 이미지의 경계를 추출.
직접 구현한 1차 2차 Hough Transform으로 이미지 원형을 형성한 부분을 Hough Field에서 확인.
Hough Transform 과 Sobel Filter 둘을 동시에 적용하여 다트판을 예측.
F1-score 가 Subtask2에 비해 향상됨.

### Subtask4
배우지 않은 방법들을 적용 및 개선하여 정확도를 더 끌어올릴 수 있도록 수행.

## 주요 업무
이번 프로젝트에서 주요 업무로,  
 * 1차, 2차 Hough Transform 구현.
 * Haar-like features에서 최고의 feature 를 찾기위해 AdaBoost 알고리즘 활용.
 * Feature기반의 알맞은 window를 찾기위해 Cascade 알고리즘 활용.
 
## 사용 기술
기본 라이브러리와 머신러닝 알고리즘 사용을위한 OpenCV  
Hough Transform, Sobel Filter 등의 구현을 위한 C++
